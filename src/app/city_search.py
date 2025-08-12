from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.css.query import NoMatches
from textual.widgets import Button, Input, Label, SelectionList
from textual.screen import ModalScreen

from weather_api import get_cities


class CitySearch(ModalScreen):
    BINDINGS = [("escape", "close_modal", "Close search window")]

    def compose(self) -> ComposeResult:
        with Container():
            yield Label("Enter a city:", id="title")
            yield Input(id="city-search-input")

    async def on_input_submitted(self, event: Input.Submitted):
        event.input.disabled = True

        try:
            notice = self.query_one("#notice")
            await notice.remove()
        except NoMatches:
            pass

        cities = get_cities(event.value)
        container = self.query_one(Container)
        if not cities:
            container.mount(
                Label(
                    "It seems your search returned no matches,\nplease try again.",
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

        container.mount(Label("Choose at least one city from the list:"))
        container.mount(selection_list)
        container.mount(Button("Submit", id="city-search-submit", variant="success"))
        container.mount(Button("Cancel", id="city-search-cancel", variant="error"))
        selection_list.focus()

    @on(Button.Pressed, "#city-search-submit")
    def handle_submit(self):
        selection = self.query_one("#city-search-list", SelectionList)

        selected_cities = [self.cities[i] for i in selection.selected]
        self.dismiss(selected_cities)

    @on(Button.Pressed, "#city-search-cancel")
    def action_close_modal(self):
        self.dismiss([])
