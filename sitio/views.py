from django.http.response import JsonResponse
import pandas as pd
from datetime import datetime
import moment
from time import process_time

def custom_date_parser(date):
    t1_start = process_time()
    x = []
    for index, row in date.iterrows():
        newDate = moment.date(row['FECHA'][0:9]).date
        x.append(datetime.strftime(newDate, '%Y-%m-%d'))
    t1_stop = process_time()
    print("Con for: ", t1_stop-t1_start)
    return x


def date_formatter(date):
    return [datetime.strftime(moment.date(row['FECHA'][0:9]).date, '%Y-%m-%d') for index, row in date.iterrows()]


def df_state():
    line = 0
    chksz = 1000
    for chunk in pd.read_csv("covid_report.csv", chunksize=chksz, index_col=0):line += chunk.shape[0]
    df = pd.read_csv('covid_report.csv', skiprows=line-5311, names=[
                     'FECHA', 'TIPO_REPORTE', 'TIPO_DATO', 'SUBTIPO_DATO', 'VALOR', 'FECHA_PROCESO', 'ID_CARGA'])
    df.to_csv('./new_covid_report.csv', index=None)  # With less lines (5311)
    new_df = pd.read_csv('new_covid_report.csv')
    dates_from_df = new_df['FECHA'].to_frame()
    new_dates_from_df = date_formatter(dates_from_df)
    new_dates_from_df = pd.DataFrame(new_dates_from_df, columns=['FECHA'])
    df['FECHA'] = new_dates_from_df['FECHA']
    df = df.sort_values(by=["FECHA"], ascending=False)

    global dataFrame
    dataFrame = df

flag = 0

def index(request):
    global flag
    print(flag)
    if flag == 0:
        flag = 1
        df_state()
    return JsonResponse(dataFrame.to_dict('records'), safe=False)
