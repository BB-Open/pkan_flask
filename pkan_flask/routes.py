"""
    Websocket Api
"""

import functools
import logging
import pprint
import sys
import traceback
from datetime import timedelta, datetime
from pathlib import Path

import requests
import simplejson as sj
from flask import Flask, request, jsonify
from flask import send_file
from flask_cors import CORS
from flask_mail import Mail, Message
from pkan_config.config import register_config, get_config

from pkan_flask.constants import INTERNAL_SERVER_ERROR, \
    INTERNAL_SERVER_ERROR_MSG, \
    REQUEST_OK, \
    EMAIL_TEMPLATE, \
    REGEX_QUERY
from pkan_flask.log import LOGGER
from pkan_flask.solr import query_results

register_config(env='Production')
cfg = get_config()

logging.getLogger('flask_cors').level = logging.DEBUG

app = Flask(__name__)

CORS(app, resources={r"*": {"origins": "*"}})

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
            LOGGER.error("Request failed with Error %s %s ",
                         exc_type,
                         exc_value)
            for line in traceback.format_tb(exc_traceback):
                LOGGER.error("%s", line[:-1])
        return (sj.dumps(res_data))

    return wrapped


# Email

def send_problem_mail(link, message):
    template = EMAIL_TEMPLATE
    subject = cfg.EMAIL_SUBJECT

    body = template.format(link=link, message=message)

    message = Message(subject)

    message.recipients = cfg.MAIL_RECIPIENTS
    message.sender = cfg.MAIL_SENDER

    message.body = body

    mail.send(message)


# Plone

def timed_lru_cache(seconds, maxsize):
    def wrapper_cache(func):
        func = functools.lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache


@timed_lru_cache(seconds=cfg.CACHE_TIME, maxsize=cfg.CACHE_SIZE)
def get_plone_url(url):
    LOGGER.debug('Get Content from Plone')
    headers = {
        "Access-Control-Allow-Origin": "*",
        'Accept': 'application/json',
    }
    resp = requests.get(url, headers=headers)

    return resp.content


# Download

@app.route('/download')
def download():
    """
    Download Files
    :return:
    """
    # id empty means full export
    format = request.args.get('format', default='rdf/xml', type=str)
    download_name = cfg.DOWNLOAD_FILENAME
    if format == 'rdf/json':
        download_name += '.json'
        mime_type = 'application/ld+json'
    elif format == 'rdf/ttl':
        download_name += '.ttl'
        mime_type = 'text/turtle'
    else:
        download_name += '.rdf'
        mime_type = 'application/rdf+xml'

    file_path = Path(cfg.DOWNLOAD_DIR) / download_name

    try:
        return send_file(file_path,
                         download_name=download_name,
                         mimetype=mime_type)
    except Exception as e:
        return str(e)

@app.route('/download_search')
def download_search():
    """
    Download Files
    :return:
    """
    # todo
    # id empty means full export
    format = request.args.get('format', default='rdf/xml', type=str)
    download_name = cfg.DOWNLOAD_FILENAME
    if format == 'rdf/json':
        download_name += '.json'
        mime_type = 'application/ld+json'
    elif format == 'rdf/ttl':
        download_name += '.ttl'
        mime_type = 'text/turtle'
    else:
        download_name += '.rdf'
        mime_type = 'application/rdf+xml'

    file_path = Path(cfg.DOWNLOAD_DIR) / download_name

    try:
        return send_file(file_path,
                         download_name=download_name,
                         mimetype=mime_type)
    except Exception as e:
        return str(e)

@app.route('/download_one')
def download_one():
    """
    Download Files
    :return:
    """
    # todo
    # id empty means full export
    format = request.args.get('format', default='rdf/xml', type=str)
    id = request.args.get('id', default='', type=str)
    if not id:
        return
    download_name = cfg.DOWNLOAD_FILENAME
    if format == 'rdf/json':
        download_name += '.json'
        mime_type = 'application/ld+json'
    elif format == 'rdf/ttl':
        download_name += '.ttl'
        mime_type = 'text/turtle'
    else:
        download_name += '.rdf'
        mime_type = 'application/rdf+xml'

    file_path = Path(cfg.DOWNLOAD_DIR) / download_name

    try:
        return send_file(file_path,
                         download_name=download_name,
                         mimetype=mime_type)
    except Exception as e:
        return str(e)


@app.route('/send_email', methods=['Post'])
def send_email(data=None):
    LOGGER.info('send_email')
    params = sj.loads(request.data)
    LOGGER.info(params)

    link = params['link']
    message = params['message']
    #
    send_problem_mail(link, message)
    #
    LOGGER.info('send_email finished')
    data = {}
    return jsonify(data)


@app.route('/solr_search', methods=['Post'])
def solr_search(data=None):
    """Wrapper between SOLR and the frontend"""
    LOGGER.debug('solr search')
    LOGGER.debug('request_data_json: ' + pprint.pformat(request.data))
    in_params = sj.loads(request.data)

    result = query_results(in_params)

    LOGGER.debug('Response {}'.format(result.content))

    LOGGER.debug('solr search finished')

    return result.content


@app.route('/solr_suggest', methods=['post'])
def solr_suggest(data=None):
    """Minimal wrapper between SOLR and the frontend"""
    LOGGER.debug('solr suggest')

    in_params = sj.loads(request.data)

    LOGGER.debug(in_params)

    suggest_q = in_params['params']['suggest.q']

    suggest_q = REGEX_QUERY.sub('', suggest_q)

    out_params = {'params': {'suggest.q': suggest_q}}

    LOGGER.debug(out_params)

    result = requests.get(
        cfg.SOLR_SUGGEST_URI,
        data=sj.dumps(out_params),
        headers={"Content-type": "application/json; charset=utf-8"}
    )

    LOGGER.debug('solr suggest finished')
    return result.content


@app.route('/solr_pick', methods=['Post'])
def solr_pick(data=None):
    """Wrapper between SOLR and the frontend"""
    LOGGER.debug('solr pick')
    LOGGER.debug(request.data)
    in_params = sj.loads(request.data)

    id = in_params['q']

    LOGGER.debug(in_params)
    out_params = {'q': 'id:"{}"'.format(id)}

    LOGGER.debug(out_params)

    result = requests.post(
        cfg.SOLR_SELECT_URI,
        data=sj.dumps({'params': out_params}),
        headers={"Content-type": "application/json; charset=utf-8"}
    )

    LOGGER.debug('Response {}'.format(result.content))
    LOGGER.debug('solr pick finished')

    return result.content


@app.route('/request_plone', methods=['POST'])
def request_plone(data=None):
    LOGGER.debug('Plone Request')
    params = sj.loads(request.data)
    # use configured Base Url,
    # User can just request already open Plone RestAPI as unauthenticated user
    url = cfg.PLONE_REST_API_QUERY_URL

    LOGGER.debug(params)

    for param in params:
        url += '&{param}={value}'.format(param=param, value=params[param])

    LOGGER.debug(url)

    return get_plone_url(url)


@app.route('/solr_roulette', methods=['POST'])
def request_solr_roulette(data=None):
    LOGGER.debug('Solr Roulette Request')

    params = sj.loads(request.data)

    random_int = int(params['random_int'])

    data = {
      "q":"inq_priority:100\ndct_title:/.{10}.*/\ndct_description:/.{10}.*/\ndct_title_lang:de\ndct_description_lang:de",
      "q.op":"AND",
      "sort":f"random_{random_int} desc",
      "rows":"1",
    }

    result = requests.post(
        cfg.SOLR_SELECT_URI,
        data=sj.dumps({'params': data}),
        headers = {"Content-type": "application/json; charset=utf-8"}
    )

    LOGGER.debug('Response {}'.format(result.content))
    LOGGER.debug('solr pick finished')

    return result.content