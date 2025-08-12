from datetime import datetime, timezone
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, HorizontalScroll, VerticalGroup
from textual.reactive import reactive
from textual.widgets import Collapsible, DataTable, Digits, Label

from config import config
from weather_api import get_current_weather
from weather_types import GeoCity, WeatherResponse, weather_code_to_icon


class CityWeatherCard(VerticalGroup, can_focus=True):
    def __init__(self, city: GeoCity, classes: str | None = None) -> None:
        super().__init__(classes=classes)
        self.city = city

    def compose(self) -> ComposeResult:
        yield CurrentWeather(self.city, classes="current-weather")
        with Collapsible(title="Extra forecast information"):
            yield Label("Hourly forecast:", classes="bold")
            yield HourlyWeatherContainer(classes="hourly-forecast-container")
            yield Label("Weekly forecast:", classes="bold")
            yield WeeklyWeatherContainer(classes="weekly-forecast-container")

    def on_mount(self):
        self.call_after_refresh(self.update_weather_info)

        interval = config.get("API", "update_time_s")
        self.set_interval(int(interval), self.update_weather_info)

    async def update_weather_info(self):
        self.weather = await get_current_weather((self.city["lat"], self.city["lon"]))
        if self.weather:
            self.query_one(CurrentWeather).weather = self.weather
            self.query_one(HourlyWeatherContainer).weather = self.weather
            self.query_one(WeeklyWeatherContainer).weather = self.weather


class CurrentWeather(HorizontalGroup, can_focus=False):
    weather: reactive[WeatherResponse | None] = reactive(None, recompose=True)

    def __init__(self, city: GeoCity, classes: str | None = None) -> None:
        super().__init__(classes=classes)
        self.city = city

    def compose(self) -> ComposeResult:
        with VerticalGroup(classes="name-container"):
            yield Label(self.city["name"], classes="bold")
            yield Label(self.city["region"], classes="muted")

        if not self.weather:
            group = VerticalGroup()
            group.loading = True
            yield group
            return

        try:
            with VerticalGroup(classes="temp-container"):
                current_temp = round(self.weather["current"]["temp"], 1)
                yield HorizontalGroup(
                    Digits(str(current_temp) or "", classes="digits"),
                    Label("○"),
                    classes="digits-container",
                )

                max_temp = round(self.weather["daily"][0]["temp"]["max"], 1)
                min_temp = round(self.weather["daily"][0]["temp"]["min"], 1)
                yield Label(f"↑{max_temp}° | ↓{min_temp}°", classes="max-min-temp")

            with VerticalGroup(classes="info-container"):
                weather_code = self.weather["current"]["weather"][0]["icon"]
                icon = weather_code_to_icon[weather_code]
                description = self.weather["current"]["weather"][0][
                    "description"
                ].capitalize()
                yield Label(f"{icon} {description}")

                uvi = self.weather["current"]["uvi"]
                yield Label(f"UVI: {uvi}")

                humidity = int(self.weather["daily"][0]["humidity"])
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
                Label(str(round(hour["temp"], 1)) + "°"),
                Label(f" {int(hour['pop']*100)}%"),
                classes="hour-card",
            )


class WeeklyWeatherContainer(DataTable, can_focus=False):
    weather: reactive[WeatherResponse | None] = reactive(None)

    def on_mount(self):
        self.loading = True
        self.add_column("Day")
        self.add_column("Precipitation %")
        self.add_column("Max UV index")
        self.add_column("Max temp")
        self.add_column("Min temp")

    def watch_weather(self, weather: WeatherResponse | None):
        if not weather:
            return

        self.loading = False

        self.clear()
        daily_weather = weather["daily"]
        for i, day in enumerate(daily_weather):
            time = datetime.fromtimestamp(
                day["dt"] + weather["timezone_offset"], timezone.utc
            ).strftime("%a")

            if i == 0:
                time = "Today"

            self.add_row(
                time,
                int(day["pop"] * 100),
                day["uvi"],
                day["temp"]["max"],
                day["temp"]["min"],
            )
