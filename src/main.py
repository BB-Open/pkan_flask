# -*- coding: utf-8 -*-
"""Simple Flask bases websocket demo."""

# Initialize Flask.
from pkan.flask.socket import (
    SOCKETIO, app)


if __name__ == '__main__':
    SOCKETIO.run(app, debug=True)
