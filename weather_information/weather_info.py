import requests
from pprint import pprint
API_KEY='156a958b8ab43f9d7a2d725de7db79c0'
city = input("Enter your city")
base_url = "http://api.openweathermap.org/data/2.5/weather?appid="+API_KEY+"&q="+city
weather_data = requests.get(base_url).json()
pprint(weather_data)
