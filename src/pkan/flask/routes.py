"""
    Websocket Api
"""


import functools
import sys
import traceback
import logging

from flask import Flask, request, jsonify
from flask import send_file
from flask_cors import CORS

import simplejson as sj

from pkan.flask.log import LOGGER
from pkan.flask.sparql_db import DBManager

try:
    import pkan.flask.configs.config as cfg
except ImportError:
    import pkan.flask.configs.config_default as cfg


logging.getLogger('flask_cors').level = logging.DEBUG

app = Flask(__name__)

CORS(app, resources={r"*": {"origins": "*"}})

DB_MANAGER = DBManager()


def pkan_status(f):
    """
    Wrapper to give the status code
    :param f:
    :return:
    """
    @functools.wraps(f)
    def wrapped(data=None):
        res_data = {}
        res_data['response_code'] = cfg.REQUEST_OK
        res_data['error_message'] = ''
        try:
            res_data.update(f(data=data))
        except Exception as _e:
            res_data['response_code'] = cfg.INTERNAL_SERVER_ERROR
            res_data['error_message'] = cfg.INTERNAL_SERVER_ERROR_MSG
            exc_type, exc_value, exc_traceback = sys.exc_info()
            LOGGER.error("Request failed with Error %s %s ", exc_type, exc_value)
            for line in traceback.format_tb(exc_traceback):
                LOGGER.error("%s", line[:-1])
        return(sj.dumps(res_data))

    return wrapped

# Download

@app.route('/download')
def return_files_tut():
    """
    Download Files
    :return:
    """
    params = {}
    # id empty means full export
    params['id'] = request.args.get('id', default=None, type=str)
    params['format'] = request.args.get('format', default='rdf/xml', type=str)
    params['type'] = request.args.get('type', default='tree', type=str)
    # ignore on type tree, use on type graph
    params['count'] = request.args.get('count', default='3', type=int)
    file_path, file_name, _file, mimetype = DB_MANAGER.get_download_file(params)
    try:
        return send_file(file_path, attachment_filename=file_name, mimetype=mimetype)
    except Exception as e:
        return str(e)

# DATA OBJECTS

@app.route('/request_vocab', methods=['POST'])
def request_vocab(data=None):
    """
    Request a vocabulary for selecting in frontend
    :param data:
    :return:
    """
    LOGGER.info('request')
    params = sj.loads(request.data)
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
    LOGGER.info('request %s finished', params)
    LOGGER.info('response is %s ', data)
    return jsonify(data)


@app.route('/request_search_results', methods=['POST'])
def request_search_results(data=None):
    """
    Request results of current search
    :param data:
    :return:
    """
    LOGGER.info('request_search_results')
    params = sj.loads(request.data)

    LOGGER.info(params)
    data = {}
    try:
        data['results'], data['result_count'] = DB_MANAGER.get_search_results(params)
    except Exception as _e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        LOGGER.error("Failed with Error %s %s ",
                     exc_type, exc_value)
        for line in traceback.format_tb(exc_traceback):
            LOGGER.error("Trace: %s", line[:-1])
        # ToDo: Fix unspecified Exception catch
        data['results'], data['result_count'] = [], 0
    data['batch_start'] = params['batch_start']
    data['batch_end'] = params['batch_end']
    LOGGER.info('request_search_results finished: %s ', data)
    return jsonify(data)

@app.route('/request_search_results_sparql', methods=['POST'])
def request_search_results_sparql(data=None):
    """
    Request results of current search
    :param data:
    :return:
    """
    LOGGER.info('request_search_results_sparql')
    params = sj.loads(request.data)

    LOGGER.info(params)
    data = {}
    data['results'], data['result_count'], data['error_message'] = \
        DB_MANAGER.get_search_results_sparql(params)
    if data['error_message']:
        LOGGER.info(data['error_message'])
        data['response_code'] = cfg.BAD_REQUEST
    data['batch_start'] = params['batch_start']
    data['batch_end'] = params['batch_end']
    LOGGER.info('request_search_results_sparql finished')
    return jsonify(data)


@app.route('/request_items_title_desc', methods=['POST'])
def request_items_title_desc(data=None):
    """
    Request title and description of a dcat element
    :param data:
    :return:
    """
    LOGGER.info('request_items_title_desc')
    params = sj.loads(request.data)

    LOGGER.info(params)
    data = {}
    obj_id = params['id']
    data['title'] = DB_MANAGER.get_title(obj_id)
    data['description'] = DB_MANAGER.get_description(obj_id)
    data['type'] = DB_MANAGER.get_type(obj_id)
    data['id'] = obj_id
    LOGGER.info('request_items_title_desc finished')
    return jsonify(data)


@app.route('/request_label', methods=['POST'])
def request_label(data=None):
    """
    Request title for a field label
    :param data:
    :return:
    """
    LOGGER.info('request label')
    params = sj.loads(request.data)

    LOGGER.info(params)
    data = {}

    obj_id = params['id']

    data['label'] = DB_MANAGER.get_field_label(obj_id)
    data['id'] = obj_id
    LOGGER.info('request label finished')
    return jsonify(data)


@app.route('/request_items_detail', methods=['POST'])
def request_items_detail(data=None):
    """
    Request items detail as rdf ttl
    :param data:
    :return:
    """
    LOGGER.info('request_items_detail')
    params = sj.loads(request.data)

    LOGGER.info(params)
    data = {}
    data['rdf_ttl'] = DB_MANAGER.get_items_detail(params['id'])
    LOGGER.info('request_items_detail finished')
    return jsonify(data)
