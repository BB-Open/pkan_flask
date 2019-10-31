# -*- coding: utf-8 -*-
"""Simple Flask bases websocket demo."""

# Initialize Flask.
from pkan.flask.socket import (
    SOCKETIO, APP)


if __name__ == '__main__':
    SOCKETIO.run(APP, debug=True)
