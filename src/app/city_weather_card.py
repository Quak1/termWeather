from datetime import datetime, timezone
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, HorizontalScroll, VerticalGroup, Center
from textual.reactive import reactive
from textual.widgets import Collapsible, Digits, Label

from weather_api import get_current_weather
from weather_types import GeoCity, WeatherResponse, weather_code_to_icon


class CityWeatherCard(VerticalGroup):
    def __init__(self, city: GeoCity, classes: str | None = None) -> None:
        super().__init__(classes=classes)
        self.city = city

    def compose(self) -> ComposeResult:
        yield CurrentWeather(self.city, classes="current-weather")
        with Collapsible():
            yield HourlyWeatherContainer(classes="hourly-weather")

    def on_mount(self):
        self.call_after_refresh(self.update_weather_info)

    async def update_weather_info(self):
        self.weather = await get_current_weather((self.city["lat"], self.city["lon"]))
        if self.weather:
            self.query_one(CurrentWeather).weather = self.weather
            self.query_one(HourlyWeatherContainer).weather = self.weather


class CurrentWeather(HorizontalGroup, can_focus=True):
    weather: reactive[WeatherResponse | None] = reactive(None, recompose=True)

    def __init__(self, city: GeoCity, classes: str | None = None) -> None:
        super().__init__(classes=classes)
        self.city = city

    def compose(self) -> ComposeResult:
        with VerticalGroup():
            yield Label(self.city["name"], classes="city-name")
            yield Label(self.city["region"], classes="city-region")

        if not self.weather:
            yield VerticalGroup(Label("Loading..."))
            return

        try:
            with VerticalGroup():
                current_temp = round(self.weather["current"]["temp"], 1)
                yield Center(
                    Digits(str(current_temp) or "", classes="digits"),
                    Label("○", classes="circle"),
                    classes="container",
                )

                max_temp = round(self.weather["daily"][0]["temp"]["max"], 1)
                min_temp = round(self.weather["daily"][0]["temp"]["min"], 1)
                yield Label(f"↑{max_temp}° | ↓{min_temp}°", classes="center")

            with VerticalGroup():
                weather_code = self.weather["current"]["weather"][0]["icon"]
                icon = weather_code_to_icon[weather_code]
                description = self.weather["current"]["weather"][0][
                    "description"
                ].capitalize()
                yield Label(f"{icon} {description}")

                uvi = self.weather["current"]["uvi"]
                yield Label(f"UVI: {uvi}")

                humidity = int(self.weather["daily"][0]["pop"] * 100)
                yield Label(f"Humidity: {humidity}%")

                feels_like = round(self.weather["current"]["feels_like"], 1)
                yield Label(f"Feels like: {feels_like}°")
        except KeyError:
            with VerticalGroup():
                yield Label("Failed to get weather info.")


class HourlyWeatherContainer(HorizontalScroll):
    weather: reactive[WeatherResponse | None] = reactive(None, recompose=True)

    def compose(self) -> ComposeResult:
        if not self.weather:
            self.loading = True
            return

        self.loading = False

        for i, hour in enumerate(self.weather["hourly"]):
            if i > 24:
                return
            if i % 2 == 0:
                continue

            time = datetime.fromtimestamp(
                hour["dt"] + self.weather["timezone_offset"], timezone.utc
            ).strftime("%-I %p")

            yield VerticalGroup(
                Label(time),
                Label(str(hour["temp"])),
                Label(f"{hour['pop']*100}%"),
                classes="hour-card",
            )
