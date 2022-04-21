"""
    Websocket Api
"""


import functools
import logging
import sys
import traceback
from urllib.request import urlopen

import simplejson as sj
from flask import Flask, request, jsonify
from flask import send_file
from flask_cors import CORS
from flask_mail import Mail, Message

from pkan.flask.log import LOGGER
from pkan.flask.sparql_db import DBManager
from pkan.flask.constants import BAD_REQUEST, INTERNAL_SERVER_ERROR, INTERNAL_SERVER_ERROR_MSG, REQUEST_OK, EMAIL_TEMPLATE

from pkan_config.config import register_config, get_config

import requests

register_config(env='Production')
cfg = get_config()

logging.getLogger('flask_cors').level = logging.DEBUG

app = Flask(__name__)

CORS(app, resources={r"*": {"origins": "*"}})

DB_MANAGER = DBManager()

app.config.update({
  'MAIL_USERNAME': cfg.MAIL_USERNAME,
  'MAIL_PASSWORD': cfg.MAIL_PASSWORD,
  'MAIL_PORT': cfg.MAIL_PORT,
  'MAIL_SERVER': cfg.MAIL_SERVER
})

mail = Mail(app)


def pkan_status(f):
    """
    Wrapper to give the status code
    :param f:
    :return:
    """
    @functools.wraps(f)
    def wrapped(data=None):
        res_data = {}
        res_data['response_code'] = REQUEST_OK
        res_data['error_message'] = ''
        try:
            res_data.update(f(data=data))
        except Exception as _e:
            res_data['response_code'] = INTERNAL_SERVER_ERROR
            res_data['error_message'] = INTERNAL_SERVER_ERROR_MSG
            exc_type, exc_value, exc_traceback = sys.exc_info()
            LOGGER.error("Request failed with Error %s %s ", exc_type, exc_value)
            for line in traceback.format_tb(exc_traceback):
                LOGGER.error("%s", line[:-1])
        return(sj.dumps(res_data))

    return wrapped

# Email

def send_problem_mail(link, message):
    template = EMAIL_TEMPLATE
    subject = cfg.EMAIL_SUBJECT

    body = template.format(link=link, message=message)

    message = Message(subject)

    message.recipients = [cfg.MAIL_USERNAME]
    message.sender = cfg.MAIL_USERNAME

    message.body = body

    mail.send(message)

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

# # DATA OBJECTS
#
# @app.route('/request_vocab', methods=['POST'])
# def request_vocab(data=None):
#     """
#     Request a vocabulary for selecting in frontend
#     :param data:
#     :return:
#     """
#     LOGGER.info('request')
#     params = sj.loads(request.data)
#     LOGGER.info(params)
#     data = {}
#
#     vocab = params['vocab']
#
#     if vocab == 'category':
#         data['vocab'] = DB_MANAGER.get_category_vocab()
#     elif vocab == 'file_format':
#         data['vocab'] = DB_MANAGER.get_file_format_vocab()
#     elif vocab == 'license':
#         data['vocab'] = DB_MANAGER.get_license_vocab()
#     elif vocab == 'publisher':
#         data['vocab'] = DB_MANAGER.get_publisher_vocab()
#     else:
#         data['vocab'] = DB_MANAGER.get_sorting_options()
#     LOGGER.info('request %s finished', params)
#     LOGGER.info('response is %s ', data)
#     return jsonify(data)
#
#
# @app.route('/request_search_results', methods=['POST'])
# def request_search_results(data=None):
#     """
#     Request results of current search
#     :param data:
#     :return:
#     """
#     LOGGER.info('request_search_results')
#     params = sj.loads(request.data)
#
#     LOGGER.info(params)
#     data = {}
#     try:
#         data['results'], data['result_count'] = DB_MANAGER.get_search_results(params)
#     except Exception as _e:
#         exc_type, exc_value, exc_traceback = sys.exc_info()
#         LOGGER.error("Failed with Error %s %s ",
#                      exc_type, exc_value)
#         for line in traceback.format_tb(exc_traceback):
#             LOGGER.error("Trace: %s", line[:-1])
#         # ToDo: Fix unspecified Exception catch
#         data['results'], data['result_count'] = [], 0
#     data['batch_start'] = params['batch_start']
#     data['batch_end'] = params['batch_end']
#     LOGGER.info('request_search_results finished: %s ', data)
#     return jsonify(data)
#
# @app.route('/request_search_results_sparql', methods=['POST'])
# def request_search_results_sparql(data=None):
#     """
#     Request results of current search
#     :param data:
#     :return:
#     """
#     LOGGER.info('request_search_results_sparql')
#     params = sj.loads(request.data)
#
#     LOGGER.info(params)
#     data = {}
#     data['results'], data['result_count'], data['error_message'] = \
#         DB_MANAGER.get_search_results_sparql(params)
#     if data['error_message']:
#         LOGGER.info(data['error_message'])
#         data['response_code'] = BAD_REQUEST
#     data['batch_start'] = params['batch_start']
#     data['batch_end'] = params['batch_end']
#     LOGGER.info('request_search_results_sparql finished')
#     return jsonify(data)
#
#
# @app.route('/request_items_title_desc', methods=['POST'])
# def request_items_title_desc(data=None):
#     """
#     Request title and description of a dcat element
#     :param data:
#     :return:
#     """
#     LOGGER.info('request_items_title_desc')
#     params = sj.loads(request.data)
#
#     LOGGER.info(params)
#     data = {}
#     obj_id = params['id']
#     data['title'] = DB_MANAGER.get_title(obj_id)
#     data['description'] = DB_MANAGER.get_description(obj_id)
#     data['type'] = DB_MANAGER.get_type(obj_id)
#     data['id'] = obj_id
#     LOGGER.info('request_items_title_desc finished')
#     return jsonify(data)
#
#
# @app.route('/request_label', methods=['POST'])
# def request_label(data=None):
#     """
#     Request title for a field label
#     :param data:
#     :return:
#     """
#     LOGGER.info('request label')
#     params = sj.loads(request.data)
#
#     LOGGER.info(params)
#     data = {}
#
#     obj_id = params['id']
#
#     data['label'] = DB_MANAGER.get_field_label(obj_id)
#     data['id'] = obj_id
#     LOGGER.info('request label finished')
#     return jsonify(data)
#
#
# @app.route('/request_items_detail', methods=['POST'])
# def request_items_detail(data=None):
#     """
#     Request items detail as rdf ttl
#     :param data:
#     :return:
#     """
#     LOGGER.info('request_items_detail')
#     params = sj.loads(request.data)
#
#     LOGGER.info(params)
#     data = {}
#     data['rdf_ttl'] = DB_MANAGER.get_items_detail(params['id'])
#     LOGGER.info(data)
#     LOGGER.info('request_items_detail finished')
#     return jsonify(data)
#
# @app.route('/send_email', methods=['Post'])
# def send_email(data=None):
#     LOGGER.info('send_email')
#     params = sj.loads(request.data)
#
#     LOGGER.info(params)
#
#     link = params['link']
#     message = params['message']
#
#     send_problem_mail(link, message)
#
#     LOGGER.info('send_email finished')
#     data = {}
#     return jsonify(data)
#
# @app.route('/request_simple_view_catalog', methods=['Post'])
# def request_simple_view_catalog(data=None):
#     LOGGER.info('request_simple_view_catalog')
#     params = sj.loads(request.data)
#     LOGGER.info(params)
#
#     id = params['id']
#
#     data = DB_MANAGER.get_simple_view_catalog(id)
#
#     LOGGER.info('request_simple_view_catalog finished')
#     return data
#
# @app.route('/request_simple_view_dataset', methods=['Post'])
# def request_simple_view_dataset(data=None):
#     LOGGER.info('request_simple_view_dataset')
#     params = sj.loads(request.data)
#     LOGGER.info(params)
#
#     id = params['id']
#
#     data = DB_MANAGER.get_simple_view_dataset(id)
#
#     LOGGER.info('request_simple_view_dataset finished')
#     return data
#
# @app.route('/request_simple_view_distribution', methods=['Post'])
# def request_simple_view_distribution(data=None):
#     LOGGER.info('request_simple_view_distribution')
#     params = sj.loads(request.data)
#     LOGGER.info(params)
#
#     id = params['id']
#
#     data = DB_MANAGER.get_simple_view_distribution(id)
#
#     LOGGER.info('request_simple_view_distribution finished')
#     return data
#
# @app.route('/request_simple_view_publisher', methods=['Post'])
# def request_simple_view_publisher(data=None):
#     LOGGER.info('request_simple_view_publisher')
#     params = sj.loads(request.data)
#     LOGGER.info(params)
#
#     id = params['id']
#
#     data = DB_MANAGER.get_simple_view_publisher(id)
#
#     LOGGER.info('request_simple_view_publisher finished')
#     return data


@app.route('/solr_search', methods=['Post'])
def solr_search(data=None):
    """Wrapper between SOLR and the frontend"""
    LOGGER.debug('solr search')
    LOGGER.debug(request.data)
    params = sj.loads(request.data)

    query_str = params['q']
    query_tokens = query_str.split(' ')
    query_tokens_clean = []
    for token in query_tokens:
        query_tokens_clean.append('search:*{}*'.format(token))

    for facet_name, choices in params['choices'].items():
        for choice in choices:
            query_tokens_clean.append('{}:"{}"'.format(facet_name, choice))

    params['q'] = ' AND '.join(query_tokens_clean)

    params['sort'] = 'score desc, inq_priority desc'

    params['facet'] = 'true'
    params['json.facet'] = sj.dumps({
        'dct_publisher_facet': {
            'terms': 'dct_publisher_facet'
        },
        'dct_license_facet': {
            'terms': 'dct_license_facet'
        },
        'dct_format_facet': {
            'terms': 'dct_format_facet'
        },
        'dcat_theme_facet': {
            'terms': 'dcat_theme_facet'
        },
        'rdf_type': {
            'terms': 'rdf_type'
        },
    })

    LOGGER.info('Query Solr:')
    LOGGER.info(params['q'])

    result = requests.post(
        cfg.SOLR_SELECT_URI,
        data=sj.dumps({'params': params}),
        headers={"Content-type": "application/json; charset=utf-8"}
    )
    LOGGER.debug('Response {}'.format(result.content))

    LOGGER.debug('solr search finished')

    return result.content


@app.route('/solr_suggest', methods=['post'])
def solr_suggest(data=None):
    """Minimal wrapper between SOLR and the frontend"""
    LOGGER.debug('solr suggest')

    result = requests.get(
        cfg.SOLR_SUGGEST_URI,
        data=request.data,
        headers={"Content-type": "application/json; charset=utf-8"}
    )

    LOGGER.debug('solr suggest finished')
    return result.content

@app.route('/solr_suggest2', methods=['post'])
def solr_suggest2(data=None):
    """Minimal wrapper between SOLR and the frontend"""
    LOGGER.debug('solr suggest')

    result = requests.get(
        cfg.SOLR_SUGGEST_URI,
        data=request.data,
        headers={"Content-type": "application/json; charset=utf-8"}
    )
    req_term = sj.loads(request.data)['params']['suggest.q']
    data = sj.loads(result.content)
    terms = [i['term'] for i in data['suggest']['mySuggester'][req_term]['suggestions']]
    out_terms = []
    for term in terms:
        result = requests.post(
           cfg.SOLR_SELECT_URI,
            data=sj.dumps({'params': {'q': 'search:{}'.format(term)}}),
            headers={"Content-type": "application/json; charset=utf-8"}
        )
        data = sj.loads(result.content)
        if data['response']['numFound'] == 0:
            out_terms.append(term)
        else:
            out_terms.append(data['response']['docs'][0])

        a=10

    LOGGER.debug('solr suggest finished')
    return result.content



@app.route('/solr_pick', methods=['Post'])
def solr_pick(data=None):
    """Wrapper between SOLR and the frontend"""
    LOGGER.debug('solr pick')
    LOGGER.debug(request.data)
    params = sj.loads(request.data)
    id = params['q']
    params['q'] = 'id:"{}"'.format(id)

    result = requests.post(
        cfg.SOLR_SELECT_URI,
        data=sj.dumps({'params': params}),
        headers={"Content-type": "application/json; charset=utf-8"}
    )

    LOGGER.debug('Response {}'.format(result.content))
    LOGGER.debug('solr pick finished')

    return result.content
