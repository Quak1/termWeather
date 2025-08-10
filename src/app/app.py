from textual import on, selection
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll, Center
from textual.css.query import NoMatches
from textual.widgets import Button, Digits, Footer, Header, Input, Label, SelectionList

from weather_api import get_cities


class WeatherApp(App):
    CSS_PATH = "styles.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield VerticalScroll(CityWeather())
        yield CitySearch(id="city-search")


class CityWeather(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield CityName(classes="name")
        yield CityTemp(classes="temp")
        yield CityExtra(classes="extra")


class CityName(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Los Angeles", classes="bold")
        yield Label("California, US", classes="country")


class CityTemp(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Center(
            Digits("19", classes="digits"),
            Label("○", classes="circle"),
            classes="container",
        )
        yield Label("↑27° | ↓18°", classes="center")


class CityExtra(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label(" Cloudy")
        yield Label("UVI: 0.5")
        yield Label("Humidity: 20%")
        yield Label("Feels like: 19°")


class CitySearch(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Enter a city and country:")
        yield Input(id="city-search-input")

    async def on_input_submitted(self, event: Input.Submitted):
        event.input.disabled = True

        try:
            notice = self.query_one("#notice")
            await notice.remove()
        except NoMatches:
            pass

        cities = get_cities(event.value)
        if not cities:
            self.mount(
                Label(
                    "It seems your search returned no matches, please try again.",
                    id="notice",
                )
            )
            event.input.disabled = False
            event.input.value = ""
            event.input.focus()
            return

        self.cities = cities
        selection_list = SelectionList(id="city-search-list", compact=True)
        for i, city in enumerate(cities):
            selection_list.add_option((city["full_name"], i))

        self.mount(Label("Choose one or multiple cities from the list:"))
        self.mount(selection_list)
        self.mount(Button("Submit", id="city-search-submit"))
        selection_list.focus()

    @on(Button.Pressed, "#city-search-submit")
    def handle_submit(self):
        selection = self.query_one("#city-search-list")
        for obj in selection.selected:
            print(self.cities[obj])

        self.remove()
