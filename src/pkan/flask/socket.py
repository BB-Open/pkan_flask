"""
    Websocket Api
"""
from functools import partial

import simplejson as sj
from flask import Flask
from flask_socketio import SocketIO, emit
from socketio.packet import Packet

from pkan.flask.log import LOGGER
from pkan.flask.sparql_db import DBManager

# Monkey Patch to use sj for socketio
Packet.json = sj
sj.dumps = partial(sj.dumps, ignore_nan=True)

APP = Flask(__name__)
SOCKETIO = SocketIO(APP)

DB_MANAGER = DBManager()


# DATA OBJECTS

@SOCKETIO.on('request_vocab')
def request_vocab(data=None):
    """
    Request a vocabulary for selecting in frontend
    :param data:
    :return:
    """
    LOGGER.info('request_vocab')
    params = data['params']
    namespace = data['namespace']
    transaction_id = data['transaction_id']
    LOGGER.info(params)
    data = {}
    # icon can be None

    if params['vocab'] == 'category':
        data['vocab'] = DB_MANAGER.get_category_vocab()
    else:
        data['vocab'] = DB_MANAGER.get_sorting_options()
    data['transaction_id'] = transaction_id
    LOGGER.info('request_vocab finished')
    emit(namespace, sj.dumps(data))


@SOCKETIO.on('request_search_results')
def request_search_results(data=None):
    """
    Request results of current search
    :param data:
    :return:
    """
    LOGGER.info('request_search_results')
    params = data['params']
    namespace = data['namespace']
    transaction_id = data['transaction_id']
    LOGGER.info(params)
    data = {}
    data['results'] = DB_MANAGER.get_search_results(params)
    data['transaction_id'] = transaction_id
    LOGGER.info('request_search_results finished')
    emit(namespace, sj.dumps(data))


@SOCKETIO.on('request_items_title_desc')
def request_items_title_desc(data=None):
    """
    Request title and description of a dcat element
    :param data:
    :return:
    """
    LOGGER.info('request_items_title_desc')
    params = data['params']
    namespace = data['namespace']
    transaction_id = data['transaction_id']
    LOGGER.info(params)
    data = {}
    obj_id = params['id']
    data['title'] = DB_MANAGER.get_title(obj_id)
    data['description'] = DB_MANAGER.get_description(obj_id)
    data['type'] = DB_MANAGER.get_type(obj_id)
    data['id'] = obj_id
    data['transaction_id'] = transaction_id
    LOGGER.info('request_items_title_desc finished')
    emit(namespace, sj.dumps(data))


@SOCKETIO.on('request_label')
def request_label(data=None):
    """
    Request title for a field label
    :param data:
    :return:
    """
    LOGGER.info('request label')
    params = data['params']
    namespace = data['namespace']
    transaction_id = data['transaction_id']
    LOGGER.info(params)
    data = {}

    obj_id = params['id']

    data['label'] = DB_MANAGER.get_field_label(obj_id)
    data['id'] = obj_id
    data['transaction_id'] = transaction_id
    LOGGER.info('request label finished')
    emit(namespace, sj.dumps(data))


@SOCKETIO.on('request_items_detail')
def request_items_detail(data=None):
    """
    Request items detail as rdf ttl
    :param data:
    :return:
    """
    LOGGER.info('request_items_detail')
    params = data['params']
    namespace = data['namespace']
    transaction_id = data['transaction_id']
    LOGGER.info(params)
    data = {}
    data['rdf_ttl'] = DB_MANAGER.get_items_detail(params['id'])
    data['transaction_id'] = transaction_id
    LOGGER.info('request_items_detail finished')
    emit(namespace, sj.dumps(data))
