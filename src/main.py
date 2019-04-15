# -*- coding: utf-8 -*-
"""Simple Flask bases websocket demo."""

# Initialize Flask.
from pkan.flask.socket import (
    socketio, app)


if __name__ == '__main__':
    socketio.run(app, debug=True)
