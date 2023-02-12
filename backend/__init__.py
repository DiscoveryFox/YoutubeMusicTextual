import subprocess
import os


class Server:

    def __init__(self, port=8000):
        env = os.environ.copy()
        if env.get('VIRTUAL_ENV') is not None:
            env['PATH'] = env['VIRTUAL_ENV'] + '/Scripts/' + env['PATH']

        self.api_server = subprocess.Popen(
            ["waitress-serve", '--port', str(port), "vlc_controller:api"],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)

    def stop(self):
        self.api_server.terminate()
        self.api_server.wait()