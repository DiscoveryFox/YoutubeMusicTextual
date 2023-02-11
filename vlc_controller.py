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


@api.route('/play/')
def play():
    media = flask.request.args.get('media')
    if media:
        decoded_media_url = urllib.parse.unquote(media)
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
    player_queue.put(instance.media_new(url))
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


if __name__ == '__main__':
    api.run()
