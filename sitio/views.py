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
  for d in date:
    newDate = moment.date(d[0:10]).date
    x.append(datetime.strftime(newDate, '%Y-%m-%d'))
  return x
 


def dfState():
  line = 0
  chksz = 1000
  for chunk in pd.read_csv("covid_report.csv",chunksize = chksz,index_col=0):
      line += chunk.shape[0]
  print(line)
  #df = pd.read_csv ('covid_report.csv',skiprows=line-5311, names=['FECHA','TIPO_REPORTE','TIPO_DATO','SUBTIPO_DATO','VALOR','FECHA_PROCESO','ID_CARGA'], parse_dates=['FECHA'], date_parser=custom_date_parser)
  #dff = df.sort_values(by=["FECHA"], ascending=False)
  #global dataFrame
  #dataFrame = df

flag = 0
def index(request):
  global flag
  print(flag)
  if flag == 0:
    flag = 1
    dfState()
  print(flag)
  #df = pd.read_csv ('covid_report.csv', parse_dates=['FECHA'])
  #dff = df.sort_values(by=["FECHA"], ascending=False)
  """file = open('./covid_report.csv')
  lastLines = tl.tail(file,5311) #to read last 15 lines, change it  to any value.
  file.close()
  abc=pd.read_csv(io.StringIO('\n'.join(lastLines)))"""

  return JsonResponse({"de matos es gay":dataFrame.to_dict()})