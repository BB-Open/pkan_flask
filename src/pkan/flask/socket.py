from functools import partial
from random import randint

import simplejson as sj
from flask import Flask
from flask_socketio import SocketIO, emit
# Monkey patch to let socketio use simplejson
# Crucial!!!
from socketio.packet import Packet

from pkan.flask.log import logger

Packet.json = sj
sj.dumps = partial(sj.dumps, ignore_nan=True)

app = Flask(__name__)
socketio = SocketIO(app)

# DATA OBJECTS

@socketio.on('request_number')
def request_profile_icons(data=None):
    logger.info('request_number')
    params = data['params']
    namespace = data['namespace']
    transaction_id = data['transaction_id']
    cm_data = {}
    cm_data['number'] = randint(0, 100)
    cm_data['transaction_id'] = transaction_id
    logger.info('request_cm_profile_icons finished')
    emit(namespace, sj.dumps(cm_data))






