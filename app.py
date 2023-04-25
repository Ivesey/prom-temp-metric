from prometheus_client import Gauge, Summary, start_http_server
import random
import time
import os
import requests
import json

#TEMPERATURES = Summary('temperatures', 'City temperature')
FREQUENCY = int(os.getenv('FREQUENCY', '3600'))
VALUE = Gauge('temperatures', 'City temperatures', ['city'])
API_KEY = os.getenv('OWM_KEY')
API_FORMAT = "http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}&units=metric"

def get_cities_from_config():
    cities = {}
    pairs = os.getenv('CITY_CODES', 'London:2643743').split(',')
    for pair in pairs:
        values = pair.split(':')
        cities[values[0]] = values[1]
    return cities

CITIES=get_cities_from_config()

#@TEMPERATURES.collect()
def collect():
    for key in CITIES:
        # print(CITIES[key])
        url = API_FORMAT.format(city_id=CITIES[key], api_key=API_KEY)
        # print(url)
        response = requests.get(url)
        data = json.loads(response.text)
        # print(data)
        temperature = data['main']['temp']
        VALUE.labels(city=key).set(temperature)

    time.sleep(FREQUENCY)

if __name__ == '__main__':
    start_http_server(8000)
    while True:
        collect()