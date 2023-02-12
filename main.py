import json

from textual.app import App, ComposeResult, RenderableType, events
from textual.containers import Container, Widget, Horizontal
from textual.widgets import Footer, Static, Input, Button, Header
from youtube_search import YoutubeSearch
import vlc
import yt_dlp
from rich.syntax import Syntax
import backend.python_bindings as backend


def sanitize_video_id(video_id):
    video_id = ''.join(c if c.isalnum() or c in '_-' else '_' for c in video_id)
    if video_id[0].isdigit():
        video_id = '_' + video_id
    return video_id


def unsanitize_video_id(component_id):
    if component_id[0] == '_':
        component_id = component_id[1:]
    return component_id.replace('_', '')


def get_streaming_url(id: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        url = f'https://www.youtube.de/watch?v={id}'
        info = ydl.extract_info(url, download=False)
        return info.get('url', None)


class Settings:
    def __init__(self, filepath: str):
        with open(filepath, 'r') as settings_file:
            self.settings = json.load(settings_file)

    def __getitem__(self, item):
        return self.settings[item]


class SearchResult(Static):
    def __init__(
            self,
            renderable: RenderableType = "",
            titel: str = '',
            vid_id: str = '',
            expand: bool = False,
            shrink: bool = False,
            markup: bool = True,
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
    ):
        super().__init__(renderable, expand=expand, shrink=shrink, markup=markup,
                         name=name,
                         id=id, classes=classes)
        self.titel = titel
        self.vid_id = vid_id
        self.sanitized_id = sanitize_video_id(vid_id)

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == 'play':
            instance = vlc.Instance()
            player = instance.media_player_new()
            media = instance.media_new(get_streaming_url(self.vid_id))

            player.set_media(media)
            player.play()

    def compose(self) -> ComposeResult:
        yield Static(self.titel)
        yield Button('Play', id='play')


class MusicPlayer(App):
    BINDINGS = [
        ("q", "quit", "Close the app"),
        ('b', 'reverse_skip', '⏮️'),
        ('f', 'forward_skip', '⏭️')
    ]

    CSS_PATH = 'MusicPlayer.css'

    def compose(self) -> ComposeResult:
        self.settings = Settings('settings.json')  # noqa
        yield Header()
        yield Input(placeholder='🔍 Search... ', id='search')
        yield Container(id='actual_content')
        yield Footer()

    async def on_input_submitted(self, message: Input.Changed):
        if message.value:
            self.fetch_result(message.value)

    def fetch_result(self, keywords: str):
        print(type(self.settings))
        search_result = YoutubeSearch(keywords, max_results=self.settings['max_results']).to_dict()

        #  self.query_one('#actual_content', Container).remove()
        #  self.mount(Container(id='actual_content'))

        for result in search_result:
            title = result['title']
            vid_id = result['id']
            self.query_one('#actual_content', Container).mount(SearchResult(titel=title,
                                                                            vid_id=vid_id,
                                                                            id=sanitize_video_id(
                                                                                vid_id)))

    def action_forward_skip(self):
        ...

    def action_reverse_skip(self):
        ...


'''
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(stream_url)
    player.set_media(media)
    player.play()
'''
if __name__ == "__main__":
    app = MusicPlayer()
    app.run()
