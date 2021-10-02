import requests
import time
import pathlib
# Reporte COVID-19
report_url = 'https://cdn.buenosaires.gob.ar/datosabiertos/datasets/salud/reporte-covid/dataset_reporte_covid_sitio_gobierno.csv'

print("DOWNLOADING...")
r = requests.get(report_url)
dir = '{}/covid_report.csv'.format(pathlib.Path(__file__).parent.resolve())
with open(dir, 'wb') as f:
    f.write(r.content)
time.sleep(60)
