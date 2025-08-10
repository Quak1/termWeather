from dotenv import load_dotenv

load_dotenv()

from app.app import WeatherApp
from weather_api import get_current_weather
from menu import choose_city


def main():
    city = choose_city()
    print(f"Getting the weather for {city["name"]}")
    weather = get_current_weather((city["lat"], city["lon"]))
    print(f'{weather["temp"]} C')
    print(weather["weather"][0]["main"])


if __name__ == "__main__":
    # main()
    app = WeatherApp()
    app.run()
