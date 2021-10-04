from django.http.response import JsonResponse
import pandas as pd
from datetime import datetime
import moment
from time import process_time
from pandas.core.frame import DataFrame
import requests

# Reporte COVID-19
report_url = 'https://cdn.buenosaires.gob.ar/datosabiertos/datasets/salud/reporte-covid/dataset_reporte_covid_sitio_gobierno.csv'

def get_new_report():
    print("DOWNLOADING...")
    r = requests.get(report_url)
    covid_report = r.content.decode()
    df = pd.DataFrame([x.split(',') for x in covid_report.split('\n')])
    df = df[(len(df.index)-5312):-1]
    df.columns = ['FECHA','TIPO_REPORTE','TIPO_DATO','SUBTIPO_DATO','VALOR','FECHA_PROCESO','ID_CARGA']
    df.index.name = None
    return df

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
    df = get_new_report()
    dates_from_df = df['FECHA'].to_frame()
    new_dates_from_df = date_formatter(dates_from_df)
    new_dates_from_df = pd.DataFrame(new_dates_from_df, columns=['FECHA'])
    df['FECHA'] = new_dates_from_df['FECHA'].values
    print(df)
    df = df.sort_values(by=["FECHA"], ascending=False)
    global dataFrame
    dataFrame = df

flag = 0

def index(request):
    global flag
    print(flag)
    t1_start = process_time() 
    if flag == 0:
        flag = 1
        df_state()
    t1_stop = process_time()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                         t1_stop-t1_start) 
    return JsonResponse(dataFrame.to_dict('records'), safe=False)
