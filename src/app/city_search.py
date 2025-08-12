from textual import on
from textual.app import ComposeResult
from textual.css.query import NoMatches
from textual.widgets import Button, Input, Label, SelectionList
from textual.screen import ModalScreen

from weather_api import get_cities


class CitySearch(ModalScreen):
    BINDINGS = [("escape", "close_modal", "Close search window")]

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
        selection = self.query_one("#city-search-list", SelectionList)

        selected_cities = [self.cities[i] for i in selection.selected]
        self.dismiss(selected_cities)

    def action_close_modal(self):
        self.dismiss([])
