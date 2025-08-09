import os
import requests

from config import config
from weather_types import WeatherResponse

API_URL = config.get("API", "BaseUrl")
GEO_URL = config.get("API", "GeoUrl")
API_KEY = os.getenv("API_KEY")


def get_current_weather(lat_lon=(None, None), *, city=None):
    if city:
        lat_lon = get_city_coords(city)

    params = {
        "lat": lat_lon[0],
        "lon": lat_lon[1],
        "units": config.get("API", "units"),
        "exclude": ",".join(["minutely", "hourly", "daily", "alerts"]),
        "appid": API_KEY,
    }
    r = requests.get(API_URL, params=params)
    data: WeatherResponse = r.json()

    return data["current"]


def get_city_coords(city):
    params = {"q": city, "limit": 1, "appid": API_KEY}
    r = requests.get(GEO_URL, params)
    city = r.json()[0]

    return (city["lat"], city["lon"])
