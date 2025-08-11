from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup, Center
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Digits, Label

from weather_api import get_current_weather
from weather_types import GeoCity, weather_code_to_icon


class CityWeatherCard(HorizontalGroup):
    weather = reactive(None, recompose=True)

    def __init__(
        self,
        city: GeoCity,
        *children: Widget,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
        markup: bool = True,
    ) -> None:
        super().__init__(
            *children,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
            markup=markup,
        )
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

    def on_mount(self):
        self.call_after_refresh(self.update_weather_info)

    async def update_weather_info(self):
        self.weather = await get_current_weather((self.city["lat"], self.city["lon"]))
