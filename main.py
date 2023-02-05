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


class SearchResult(Static):
    CSS_PATH = 'SearchResult.css'

    def __init__(self, titel: str,*args, **kwargs):
        self.titel: str = titel
        super().__init__(args, kwargs)

    def compose(self) -> ComposeResult:
        yield Container(Static(self.titel))


class MusicPlayer(App):
    BINDINGS = [("q", "quit", "Close the app")]

    def compose(self) -> ComposeResult:
        self.settings = Settings('settings.json')  # noqa
        yield Footer()
        yield Input(placeholder='🔍 Search... ', id='search')
        yield Content(Container(Window(Static(id='actual_content')), id='results'),
                      id="results-container")

    async def on_input_submitted(self, message: Input.Changed):
        if message.value:
            self.fetch_result(message.value)

    def fetch_result(self, keywords: str):
        print(type(self.settings))
        search_result = YoutubeSearch(keywords, max_results=self.settings['max_results']).to_dict()
        from pprint import pprint
        video_one = search_result[0]
        titel = video_one['title']
        self.query_one('#actual_content', Static).mount(SearchResult(titel, id=f'{video_one["id"]}result'))


if __name__ == "__main__":
    app = MusicPlayer()
    app.run()
