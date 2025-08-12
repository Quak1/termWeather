from textual.app import App, ComposeResult
from textual.containers import VerticalScroll, Container
from textual.widgets import Button, Footer, Header

from app.city_weather_card import CityWeatherCard
from app.city_search import CitySearch
from config import load_cities, save_city


class WeatherApp(App):
    CSS_PATH = "styles.tcss"

    BINDINGS = [("a", "search_city", "Add city")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        with VerticalScroll(can_focus=False):
            yield WeatherCardContainer(id="card-container")
            yield Button("+", "success", id="btn-add-card")

    def on_mount(self):
        for city in load_cities():
            self.query_one("#card-container").mount(
                CityWeatherCard(city, classes="city-weather")
            )

    def action_search_city(self):
        def selected(cities):
            for city in cities:
                self.query_one("#card-container").mount(
                    CityWeatherCard(city, classes="city-weather")
                )

        self.push_screen(CitySearch(classes="modal"), selected)

    def on_button_pressed(self, message: Button.Pressed):
        if message.button.id == "btn-add-card":
            self.action_search_city()


class WeatherCardContainer(Container, can_focus=False):
    BINDINGS = [
        ("t", "move_card_top", "Move to the top"),
        ("s", "save_city", "Save"),
        ("d", "remove_weather_card", "Delete"),
        ("u", "update_city_weather", "Force update"),
    ]

    def action_move_card_top(self):
        focused = self.app.focused
        if focused and "city-weather" in focused.classes:
            self.move_child(focused, before=0)

    def action_remove_weather_card(self):
        focused = self.app.focused
        if focused and "city-weather" in focused.classes:
            focused.remove()

    def action_save_city(self):
        focused = self.app.focused
        if focused and "city-weather" in focused.classes:
            msg = save_city(focused.city)
            if msg.startswith("Success"):
                self.notify(msg)
            else:
                self.notify(msg, severity="error")

    async def action_update_city_weather(self):
        focused = self.app.focused
        if focused and "city-weather" in focused.classes:
            await focused.update_weather_info()
