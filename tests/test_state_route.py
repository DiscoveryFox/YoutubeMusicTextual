import unittest
import requests
import subprocess
import time
import os
import json


class TestStateRoute(unittest.TestCase):

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

    def test_state_route(self):
        response = requests.get('http://localhost:8000/state')
        state = json.loads(response.text)['state']
        self.assertIn(state, ['paused', 'playing', 'stopped', 'ended', 'error', 'unknown'])


if __name__ == '__main__':
    unittest.main()
