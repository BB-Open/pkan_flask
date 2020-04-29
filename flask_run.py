# -*- coding: utf-8 -*-
"""Simple Flask bases websocket demo."""

# Initialize Flask.
# need import for routing
import pkan.flask.routing
from pkan.flask.routes import app

if __name__ == '__main__':
    app.run()
