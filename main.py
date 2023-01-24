import json

from textual.app import App, ComposeResult
from textual.containers import Container, Content
from textual.widgets import Footer, Static, Input
from rich.json import JSON
from youtube_search import YoutubeSearch


class Settings:
    def __init__(self, filepath: str):
        with open(filepath, 'r') as settings_file:
            self.settings = json.load(settings_file)

    def __getitem__(self, item):
        return self.settings[item]

class Window(Container):
    pass

class SearchBar(Static):

    def compose(self) -> ComposeResult:
        yield


class MusicPlayer(App):
    BINDINGS = [("q", "quit", "Close the app")]

    def compose(self) -> ComposeResult:
        self.settings = Settings('settings.json') # noqa

        yield Footer()
        yield Input(placeholder='🔍 Search... ', id='search')
        yield Content(Container(Window(Static(id='actual_content')), id='results'),
        id="results-container")

    async def on_input_submitted(self, message: Input.Changed):
        if message.value:
            self.fetch_result(message.value)

    def fetch_result(self, keywords: str):
        search_result = YoutubeSearch(keywords, max_results=self.settings['max_results']).to_json()
        from pprint import pprint
        pprint(search_result)
        self.query_one('#actual_content', Static).update((JSON(str(search_result))))


if __name__ == "__main__":
    app = MusicPlayer()
    app.run()
