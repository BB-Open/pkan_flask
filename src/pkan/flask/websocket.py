"""
    Websocket Api
"""
import functools
import sys
import traceback
from functools import partial

import simplejson as sj
from flask import Flask
from flask_socketio import SocketIO, emit

from pkan.flask.log import LOGGER
from pkan.flask.sparql_db import DBManager

try:
    import pkan.flask.configs.config as cfg
except ImportError:
    import pkan.flask.configs.config_default as cfg

import logging

logging.getLogger('flask_cors').level = logging.DEBUG

app = Flask(__name__)

SOCKETIO = SocketIO(app, cors_allowed_origins="*")

DB_MANAGER = DBManager()


def pkan_status(f):
    @functools.wraps(f)
    def wrapped(data=None):
        namespace = data['namespace']
        res_data = {}
        res_data['transaction_id'] = data['transaction_id']
        res_data['response_code'] = cfg.REQUEST_OK
        res_data['error_message'] = ''
        try:
            res_data.update(f(data=data))
        except Exception as e:
            res_data['response_code'] = cfg.INTERNAL_SERVER_ERROR
            res_data['error_message'] = cfg.INTERNAL_SERVER_ERROR_MSG
            exc_type, exc_value, exc_traceback = sys.exc_info()
            LOGGER.error("Request failed with Error %s %s " % (exc_type, exc_value))
            for line in traceback.format_tb(exc_traceback):
                LOGGER.error("%s" % (line[:-1]))
        emit(namespace, sj.dumps(res_data))
    return wrapped

# DATA OBJECTS

@SOCKETIO.on('request_vocab')
@pkan_status
def request_vocab(data=None):
    """
    Request a vocabulary for selecting in frontend
    :param data:
    :return:
    """
    LOGGER.info('request_vocab')
    params = data['params']
    LOGGER.info(params)
    data = {}

    vocab = params['vocab']

    if vocab == 'category':
        data['vocab'] = DB_MANAGER.get_category_vocab()
    elif vocab == 'file_format':
        data['vocab'] = DB_MANAGER.get_file_format_vocab()
    elif vocab == 'license':
        data['vocab'] = DB_MANAGER.get_license_vocab()
    elif vocab == 'publisher':
        data['vocab'] = DB_MANAGER.get_publisher_vocab()
    else:
        data['vocab'] = DB_MANAGER.get_sorting_options()
    LOGGER.info('request_vocab finished')
    return data


@SOCKETIO.on('request_search_results')
@pkan_status
def request_search_results(data=None):
    """
    Request results of current search
    :param data:
    :return:
    """
    LOGGER.info('request_search_results')
    params = data['params']
    
    LOGGER.info(params)
    data = {}
    data['results'], data['number_results'] = DB_MANAGER.get_search_results(params)
    data['batch_start'] = params['batch_start']
    data['batch_end'] = params['batch_end']
    LOGGER.info('request_search_results finished')
    return data

@SOCKETIO.on('request_search_results_sparql')
@pkan_status
def request_search_results_sparql(data=None):
    """
    Request results of current search
    :param data:
    :return:
    """
    LOGGER.info('request_search_results_sparql')
    params = data['params']
    
    LOGGER.info(params)
    data = {}
    data['results'], data['number_results'], data['error_message'] = DB_MANAGER.get_search_results_sparql(params)
    if data['error_message']:
        LOGGER.info(data['error_message'])
        data['response_code'] = cfg.BAD_REQUEST
    data['batch_start'] = params['batch_start']
    data['batch_end'] = params['batch_end']
    LOGGER.info('request_search_results_sparql finished')
    return data


@SOCKETIO.on('request_items_title_desc')
@pkan_status
def request_items_title_desc(data=None):
    """
    Request title and description of a dcat element
    :param data:
    :return:
    """
    LOGGER.info('request_items_title_desc')
    params = data['params']

    LOGGER.info(params)
    data = {}
    obj_id = params['id']
    data['title'] = DB_MANAGER.get_title(obj_id)
    data['description'] = DB_MANAGER.get_description(obj_id)
    data['type'] = DB_MANAGER.get_type(obj_id)
    data['id'] = obj_id
    LOGGER.info('request_items_title_desc finished')
    return data


@SOCKETIO.on('request_label')
@pkan_status
def request_label(data=None):
    """
    Request title for a field label
    :param data:
    :return:
    """
    LOGGER.info('request label')
    params = data['params']

    LOGGER.info(params)
    data = {}

    obj_id = params['id']

    data['label'] = DB_MANAGER.get_field_label(obj_id)
    data['id'] = obj_id
    LOGGER.info('request label finished')
    return data


@SOCKETIO.on('request_items_detail')
@pkan_status
def request_items_detail(data=None):
    """
    Request items detail as rdf ttl
    :param data:
    :return:
    """
    LOGGER.info('request_items_detail')
    params = data['params']

    LOGGER.info(params)
    data = {}
    data['rdf_ttl'] = DB_MANAGER.get_items_detail(params['id'])
    LOGGER.info('request_items_detail finished')
    return data
