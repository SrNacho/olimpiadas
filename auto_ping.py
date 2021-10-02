import requests
import time

while True:
  url = 'https://covidolimpiada.herokuapp.com/'
  r = requests.get(url)
  time.sleep(3500)
