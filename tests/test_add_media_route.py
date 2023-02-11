import unittest
import requests
import os
import subprocess
import urllib.parse


class TestPlayRoute(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        env = os.environ.copy()
        env['PATH'] = env['VIRTUAL_ENV'] + '/Scripts/' + env['PATH']
        cls.api_server = subprocess.Popen(
            ["waitress-serve", '--port', '8000', "vlc_controller:api"],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)

    @classmethod
    def tearDownClass(cls):
        cls.api_server.terminate()
        cls.api_server.wait()

    def test_add_media_route(self):
        media = 'https://file-examples.com/storage/fe863385e163e3b0f92dc53/2017/11/file_example_MP3_700KB.mp3'
        response = requests.get(f'http://localhost:8000/add_media?url={urllib.parse.quote(media)}')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
