import vlc
import flask
import queue
import time
import urllib.parse

api: flask.Flask = flask.Flask(__name__)

instance: vlc.Instance = vlc.Instance()
player: vlc.MediaPlayer = instance.media_player_new()
event_manager: vlc.EventManager = player.event_manager()

player_queue: queue.Queue[vlc.Media] = queue.Queue()


@api.route('/state')
def state():
    match player.get_state():
        case vlc.State.Paused:
            return {'state': 'paused'}, 200
        case vlc.State.Playing:
            return {'state': 'playing'}, 200
        case vlc.State.Stopped:
            return {'state': 'stopped'}, 200
        case vlc.State.Ended:
            return {'state': 'ended'}, 200
        case vlc.State.Error:
            return {'state': 'error'}, 500
        case _:
            return {'state': 'unknown'}, 400


@api.route('/pause')
def pause():
    player.pause()
    return flask.Response(status=200)


@api.route('/play')
def play():
    url = flask.request.args.get('url')
    if url:
        decoded_media_url = urllib.parse.unquote(url)
        new_media: vlc.Media = instance.media_new(decoded_media_url)
        player.set_media(new_media)
    else:
        player.set_media(player_queue.get())
    player.play()
    return flask.Response(status=200)


@api.route('/add_media/')
def add_media():
    url: str | None = flask.request.args.get('url')
    if url is None:
        return flask.Response(status=404)
    player_queue.put(instance.media_new(urllib.parse.unquote(url)))
    return flask.Response(status=200)


@api.route('/get_queue')
def get_queue():
    return {
        'queue': [str(media.get_mrl()) for media in player_queue.queue]
    }


@api.route('/clear_queue')
def clear_queue():
    player_queue.queue.clear()
    return flask.Response(status=200)


@api.route('/stop')
def stop():
    player.stop()
    return flask.Response(status=200)


@api.route('/next')
def next():
    player.stop()
    player.set_media(instance.media_new(player_queue.get()))


@api.route('/rate/<float:rate>')
def set_rate(rate: float):
    player.set_rate(rate)


@api.route('/skip/<int:skip_time>')
def skip(skip_time: int):
    player.set_time(player.get_time() + skip_time * 1000)
    return flask.Response(status=200)


@api.route('/get_time')
def get_time():
    return str(player.get_time() / 1000), 200


@api.route('/set_volume/<int:volume>')
def set_volume(volume: int):
    player.audio_set_volume(volume)
    return flask.Response(status=200)


@api.route('/get_volume')
def get_volume():
    return str(player.audio_get_volume()), 200


if __name__ == '__main__':
    api.run()
