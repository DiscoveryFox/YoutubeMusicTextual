from youtube_search import YoutubeSearch

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Button, Header, Footer, Static

class SearchBar(Static):

    def compose(self) -> ComposeResult:
        yield 


class MusicPlayer(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Container()

    def action_toggle_dark(self):
        self.dark: bool = not self.dark


if __name__ == "__main__":
    app = MusicPlayer()
    app.run()
