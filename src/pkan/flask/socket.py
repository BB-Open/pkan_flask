from functools import partial

import simplejson as sj
from flask import Flask
from flask_socketio import SocketIO, emit
from pkan.flask.log import LOGGER
# Monkey patch to let socketio use simplejson
# Crucial!!!
from pkan.flask.sparql_db import DBManager
from socketio.packet import Packet

Packet.json = sj
sj.dumps = partial(sj.dumps, ignore_nan=True)

app = Flask(__name__)
socketio = SocketIO(app)

db_manager = DBManager()


# DATA OBJECTS

@socketio.on('request_vocab')
def request_vocab(data=None):
    # todo: category, ordering, ...
    LOGGER.info('request_vocab')
    params = data['params']
    namespace = data['namespace']
    transaction_id = data['transaction_id']
    LOGGER.info(params)
    data = {}
    # icon can be None

    if params['vocab'] == 'category':
        data['vocab'] = db_manager.get_category_vocab()
    else:
        data['vocab'] = db_manager.get_sorting_options()
    data['transaction_id'] = transaction_id
    LOGGER.info('request_vocab finished')
    emit(namespace, sj.dumps(data))


@socketio.on('request_search_results')
def request_search_results(data=None):
    LOGGER.info('request_search_results')
    params = data['params']
    namespace = data['namespace']
    transaction_id = data['transaction_id']
    LOGGER.info(params)
    data = {}
    data['results'] = db_manager.get_search_results(params)
    data['transaction_id'] = transaction_id
    LOGGER.info('request_search_results finished')
    emit(namespace, sj.dumps(data))


@socketio.on('request_items_title_desc')
def request_items_title_desc(data=None):
    LOGGER.info('request_items_title_desc')
    params = data['params']
    namespace = data['namespace']
    transaction_id = data['transaction_id']
    LOGGER.info(params)
    data = {}
    id = params['id']
    data['title'] = db_manager.get_title(id)
    data['description'] = db_manager.get_description(id)
    data['type'] = db_manager.get_type(id)
    data['id'] = id
    data['transaction_id'] = transaction_id
    LOGGER.info('request_items_title_desc finished')
    emit(namespace, sj.dumps(data))


@socketio.on('request_label')
def request_label(data=None):
    LOGGER.info('request label')
    params = data['params']
    namespace = data['namespace']
    transaction_id = data['transaction_id']
    LOGGER.info(params)
    data = {}

    id = params['id']

    data['label'] = db_manager.get_field_label(id)
    data['id'] = id
    data['transaction_id'] = transaction_id
    LOGGER.info('request label finished')
    emit(namespace, sj.dumps(data))


@socketio.on('request_items_detail')
def request_items_detail(data=None):
    # todo: ...
    LOGGER.info('request_items_detail')
    params = data['params']
    namespace = data['namespace']
    transaction_id = data['transaction_id']
    LOGGER.info(params)
    data = {}
    data['rdf_ttl'] = db_manager.get_items_detail(params['id'])
    data['transaction_id'] = transaction_id
    LOGGER.info('request_items_detail finished')
    emit(namespace, sj.dumps(data))
