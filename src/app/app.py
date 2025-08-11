from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from app.city_weather_card import CityWeatherCard
from app.city_search import CitySearch


class WeatherApp(App):
    CSS_PATH = "styles.tcss"

    BINDINGS = [("a", "search_city", "Add another city")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield CitySearch(id="city-search")

    def on_city_search_cities_selected(self, message: CitySearch.CitiesSelected):
        for city in message.cities:
            self.mount(CityWeatherCard(city, classes="city-weather"))

    def action_search_city(self):
        self.mount(CitySearch(id="city-search"))
