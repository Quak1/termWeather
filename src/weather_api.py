import os
import requests
from typing import List

from config import config
from weather_types import WeatherResponse, City

API_URL = config.get("API", "BaseUrl")
GEO_URL = config.get("API", "GeoUrl")
API_KEY = os.getenv("API_KEY")


def get_current_weather(coords=(None, None), *, city=None):
    if city:
        city = get_cities(city)[0]
        coords = (city["lat"], city["lon"])

    params = {
        "lat": coords[0],
        "lon": coords[1],
        "units": config.get("API", "units"),
        "exclude": ",".join(["minutely", "hourly", "daily", "alerts"]),
        "appid": API_KEY,
    }
    r = requests.get(API_URL, params=params)
    data: WeatherResponse = r.json()

    return data["current"]


def get_cities(city):
    params = {"q": city, "limit": 5, "appid": API_KEY}
    try:
        r = requests.get(GEO_URL, params)
        cities: List[City] = r.json()
        for city in cities:
            city["region"] = (
                f'{city["state"]}, {city["country"]}'
                if "state" in city
                else city["country"]
            )
            city["full_name"] = f"{city["name"]}, {city["region"]}"
        return cities
    except Exception:
        return []
