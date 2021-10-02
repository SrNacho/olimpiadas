from django.http.response import JsonResponse
import requests
import pandas as pd
from datetime import datetime
import moment
import tailer as tl
import io

#Reporte COVID-19
report_url = 'https://cdn.buenosaires.gob.ar/datosabiertos/datasets/salud/reporte-covid/dataset_reporte_covid_sitio_gobierno.xlsx'

def saveReport():
  r = requests.get(report_url)
  with open('./covid_report.xlsx', 'wb') as f:
    f.write(r.content)

def custom_date_parser(date):
  x = []
  for index,row in date.iterrows():
    print(index,row['FECHA'])
    print("-----")
    newDate = moment.date(row['FECHA'][0:9]).date
    print(newDate)
    x.append(datetime.strftime(newDate, '%Y-%m-%d'))
  return x
 


def dfState():
  line = 0
  chksz = 1000

  for chunk in pd.read_csv("covid_report.csv",chunksize = chksz,index_col=0):
      line += chunk.shape[0]

  df = pd.read_csv('covid_report.csv',skiprows=line-5311, names=['FECHA','TIPO_REPORTE','TIPO_DATO','SUBTIPO_DATO','VALOR','FECHA_PROCESO','ID_CARGA'])
  df.to_csv('./new_covid_report.csv', index=None) # With less lines (5311)
  new_df = pd.read_csv('new_covid_report.csv')
  dates_from_df = new_df['FECHA'].to_frame()
  new_dates_from_df = custom_date_parser(dates_from_df)
  new_dates_from_df = pd.DataFrame(new_dates_from_df, columns=['FECHA'])
  df['FECHA']=new_dates_from_df['FECHA']
  df = df.sort_values(by=["FECHA"], ascending=False)
  print(df)

  
  """"
  dates_from_df = new_df.index.to_frame(index=None)
  new_dates_from_df = custom_date_parser(dates_from_df)
  new_dates_from_df = pd.DataFrame(new_dates_from_df, columns=['FECHA'])
  df.index= new_dates_from_df['FECHA']
  df = df.sort_values(by=["FECHA"], ascending=False)
  print(df)"""
  global dataFrame
  dataFrame = df

flag = 0
def index(request):
  global flag
  print(flag)
  if flag == 0:
    flag = 1
    dfState()
  print(flag)
  return JsonResponse(dataFrame.to_dict('records'),safe=False)