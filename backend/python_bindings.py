import urllib.parse

import requests
from typing import Literal

'''
state
pause
play
add_media
get_queue
clear_queue
stop
next
set_rate
skip
get_time
set_volume
get_volume

'''
class BackendConnector:
    def __init__(self,
                 base_url: str = 'http://localhost',
                 port: int = 8000,
                 backend_version: int = -1) -> None:
        """
        :param url: The url where your backend is running. Default is localhost
        :param port: The port that the backend is listening on. Default is 8000
        :param backend_version: The Version of the backend. -1 is not known. Every other version
            is documented in the wiki. It provides additional data on how the backend works under the hood.
        """
        self.base_url: str = base_url
        self.port: int = port
        self.backend_version: backend_version
        self.session = requests.session()

    @property
    def backend_url(self):
        return f'{self.base_url}:{self.port}'

    def play(self, url: str | None = None):
        self.session.get(url=f'{self.backend_url}/play', params={
            'url': urllib.parse.quote(url)
        }) if url else requests.get(f'{self.backend_url}/play')

    def stop(self):
        self.session.get(url=f'{self.backend_url}/stop')

    def pause(self):
        self.session.get(url=f'{self.backend_url}/pause')

    def add_media(self, url):
        self.session.get(url=f'{self.backend_url}/add_media', params={
            'url': urllib.parse.quote(url)
        })

    def get_queue(self):
        response = self.session.get(f'{self.backend_url}/get_queue')
        return response.json()

    def clear_queue(self):
        self.session.get(f'{self.backend_url}/clear_queue')

    def next(self):
        self.session.get(f'{self.backend_url}/next')

    def get_state(self):
        return self.session.get(f'{self.backend_url}/state').json()

    def get_volume(self):
        return int(self.session.get(f'{self.backend_url}/get_volume').text)

    def set_volume(self, volume: float | int):
        self.session.get(f'{self.backend_url}/set_volume/{volume}')

    def get_time(self):
        return float(self.session.get(f'{self.backend_url}/get_time').text)

    def skip(self, seconds):
        self.session.get(f'{self.backend_url}/skip/{seconds}')

    def set_rate(self, rate: float):
        self.session.get(f'{self.backend_url}/set_rate/{rate}')


