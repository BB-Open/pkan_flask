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

@socketio.on('request_vocab')
def request_vocab(data=None):
    # todo: category, ordering, ...
    logger.info('request_vocab')
    params = data['params']
    namespace = data['namespace']
    transaction_id = data['transaction_id']
    logger.info(params)
    data = {}
    data['vocab'] = ['Value 1', 'Value 2', 'Value 3', 'Value 4', 'Value 5', 'Value 6']
    data['transaction_id'] = transaction_id
    logger.info('request_vocab finished')
    emit(namespace, sj.dumps(data))
    
@socketio.on('request_search_results')
def request_search_results(data=None):
    # todo: ...
    logger.info('request_search_results')
    params = data['params']
    namespace = data['namespace']
    transaction_id = data['transaction_id']
    logger.info(params)
    data = {}
    data['results'] = [
        {
            'id': 'my-id',
            'title': 'my-title',
            'description': 'my-description'
        },
        {
            'id': 'my-id2',
            'title': 'my-title2',
            'description': 'my-description2'
        }
    ]
    data['transaction_id'] = transaction_id
    logger.info('request_search_results finished')
    emit(namespace, sj.dumps(data))

@socketio.on('request_items_detail')
def request_items_detail(data=None):
    # todo: ...
    logger.info('request_items_detail')
    params = data['params']
    namespace = data['namespace']
    transaction_id = data['transaction_id']
    logger.info(params)
    data = {}
    data['title'] = 'Ich bin der Titel'
    data['description'] = 'Ich bin die Beschreibung'
    data['fields'] = [
        {
            'field': 'Data',
            'type': 'url',
            'value': 'my-description',
            'title': 'My Description'
        },
        {
            'field': 'ein Feld',
            'type': 'text',
            'value': 'Ich bin ein Text'
        }
    ]
    data['transaction_id'] = transaction_id
    logger.info('request_items_detail finished')
    emit(namespace, sj.dumps(data))
    
@socketio.on('request_related_items')
def request_related_items(data=None):
    # todo: ...
    logger.info('request_related_items')
    params = data['params']
    namespace = data['namespace']
    transaction_id = data['transaction_id']
    logger.info(params)
    data = {}
    data['results'] = [
        {
            'id': 'my-id',
            'title': 'my-title',
            'description': 'my-description'
        },
        {
            'id': 'my-id2',
            'title': 'my-title2',
            'description': 'my-description2'
        }
    ]
    data['transaction_id'] = transaction_id
    logger.info('request_related_items finished')
    emit(namespace, sj.dumps(data))
