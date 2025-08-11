import os
import requests
from typing import List

from config import config
from weather_types import WeatherResponse, GeoCity

API_URL = config.get("API", "BaseUrl")
GEO_URL = config.get("API", "GeoUrl")
API_KEY = os.getenv("API_KEY")


async def get_current_weather(coords=(None, None), *, city=None):
    if city:
        city = get_cities(city)[0]
        coords = (city["lat"], city["lon"])

    params = {
        "lat": coords[0],
        "lon": coords[1],
        "units": config.get("API", "units"),
        "exclude": ",".join(["minutely", "alerts"]),
        "appid": API_KEY,
    }
    try:
        r = requests.get(API_URL, params=params)
        data: WeatherResponse = r.json()
        return data
    except Exception:
        return None


def get_cities(city):
    params = {"q": city, "limit": 5, "appid": API_KEY}
    try:
        r = requests.get(GEO_URL, params)
        cities: List[GeoCity] = r.json()
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
