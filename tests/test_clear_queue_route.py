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

    def test_clear_route(self):
        response = requests.get(f'http://localhost:8000/clear_queue')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
