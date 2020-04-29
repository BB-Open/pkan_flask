# -*- coding: utf-8 -*-
"""Simple Flask bases websocket demo."""

# Initialize Flask.
from flask_cors import CORS

from pkan.flask.websocket import (
    SOCKETIO, app)
# need import for routing
import pkan.flask.routing

cors = CORS(app, resources={r"*": {"origins": "*"}})

if __name__ == '__main__':
#    SOCKETIO.run(app, debug=True)
    app.run()
