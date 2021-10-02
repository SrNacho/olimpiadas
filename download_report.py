import requests
import time
# Reporte COVID-19
report_url = 'https://cdn.buenosaires.gob.ar/datosabiertos/datasets/salud/reporte-covid/dataset_reporte_covid_sitio_gobierno.xlsx'

print("DOWNLOADING...")
time.sleep(60)
r = requests.get(report_url)
with open('./covid_report.csv', 'wb') as f:
    f.write(r.content)