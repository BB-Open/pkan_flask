# -*- coding: utf-8 -*-
"""Simple Flask bases websocket demo."""

# Initialize Flask.
from pkan.flask.websocket import app
# need import for routing
import pkan.flask.routing

if __name__ == '__main__':
#    SOCKETIO.run(app, debug=True)
    app.run()
