from textual.app import App, ComposeResult
from textual.containers import VerticalScroll, Container
from textual.widgets import Button, Footer, Header

from app.city_weather_card import CityWeatherCard
from app.city_search import CitySearch


class WeatherApp(App):
    CSS_PATH = "styles.tcss"

    BINDINGS = [("a", "search_city", "Add another city")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield WeatherCardContainer()

    def on_city_search_cities_selected(self, message: CitySearch.CitiesSelected):
        for city in message.cities:
            self.query_one("#card-container").mount(
                CityWeatherCard(city, classes="city-weather")
            )

    def action_search_city(self):
        if not self.query("#city-search"):
            self.mount(CitySearch(id="city-search"))

    def on_button_pressed(self, message: Button.Pressed):
        if message.button.id == "btn-add-card":
            self.action_search_city()


class WeatherCardContainer(VerticalScroll, can_focus=False):
    BINDINGS = [("t", "move_card_top", "Move to the top")]

    def compose(self):
        yield Container(id="card-container")
        yield Button("+", "success", id="btn-add-card")

    def action_move_card_top(self):
        focused = self.app.focused
        if (
            focused
            and "city-weather" in focused.classes
            and focused.id != "btn-add-card"
        ):
            self.move_child(focused, before=0)
