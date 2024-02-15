import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

# set the apikey
apikey = os.getenv("WEATHER_API")  # click to set to your apikey
lmt = 1

def _get_coordinates(city):
	r = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={lmt}&appid={apikey}")
	if r.status_code == 200:
		result_request = json.loads(r.content)
	else:
		result_request = None
	result_coordinates = result_request[0]["lat"], result_request[0]["lon"]

	return result_coordinates


def get_weather(city):
	lat, lon = _get_coordinates(city)

	r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&lang=pt_br&units=metric&appid={apikey}")

	if r.status_code == 200:
		result_weather = json.loads(r.content)
	else:
		result_weather = None

	return result_weather

if __name__ == "__main__":
	print(get_weather("Maceió"))
