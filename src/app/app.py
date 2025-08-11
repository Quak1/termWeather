from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Footer, Header

from app.city_weather_card import CityWeatherCard
from app.city_search import CitySearch


class WeatherApp(App):
    CSS_PATH = "styles.tcss"

    BINDINGS = [("a", "search_city", "Add another city")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield WeatherCardContainer(id="card-container")
        yield CitySearch(id="city-search")

    def on_city_search_cities_selected(self, message: CitySearch.CitiesSelected):
        for city in message.cities:
            self.query_one("#card-container").mount(
                CityWeatherCard(city, classes="city-weather")
            )

    def action_search_city(self):
        self.mount(CitySearch(id="city-search"))

    def action_print_children(self):
        print("children: ")
        print(self.children)


class WeatherCardContainer(VerticalScroll):
    BINDINGS = [("t", "move_card_top", "Move to the top")]

    def action_move_card_top(self):
        focused = self.app.focused
        if focused and "city-weather" in focused.classes:
            self.move_child(focused, before=0)
