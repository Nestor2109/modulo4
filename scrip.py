import requests
import time
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient, Point

token = 'nGf_e-6LihQR2AqEFbD5Bhc0iFlcAl8WeD6SlOgG883Fgmroau4fhBie5Ydzzij72UqtManqpm0MlxjZ2FMlXw=='
bucket = 'test'
client = InfluxDBClient('http://localhost:8086',token = token, org='test')

write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()


while True:
    city = "bogota"
    def return_weather(city):
      url = "https://es.wttr.in/{city}?format=j1"

      response = requests.get(url)
      weather_dic = response.json()

      temp_c = weather_dic["current_condition"][0]['temp_C']
      humedad= weather_dic["current_condition"][0]['humidity']
      return temp_c,humedad
        
    def main():
       temp_c,humedad = return_weather(city)
    
       if    temp_c !=0 and   humedad !=0:
           print(f"La temperatura actual de {city} es {temp_c} °C.")
           print(f"La humedad actual de {city} es {humedad} %. .")

           p = Point("Datos").field("temperatura", float(temp_c)).field('humedad', float(humedad))
           write_api.write(bucket=bucket, org='test', record=p)

    time.sleep(1)
 
    if __name__ == '__main__':
        main()