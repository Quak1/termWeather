from dotenv import load_dotenv

load_dotenv()

from weather_api import get_current_weather


def main():
    city = "Los Angeles, US"
    current = get_current_weather(city=city)

    print(city)
    print(f'{current["temp"]} C')
    print(current["weather"][0]["main"])


if __name__ == "__main__":
    main()
