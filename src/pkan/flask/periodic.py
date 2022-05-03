"""Scheduler for Cronjobs"""
import shutil
import sys
import tempfile
import time
from pathlib import Path
from traceback import format_tb

import requests
from pyrdf4j.rdf4j import RDF4J
from requests.auth import HTTPBasicAuth
import schedule
from iso2dcat.solr.rdf2solr import main as solr_main

from pkan.flask.log import LOGGER
from pkan_config.config import get_config
import pkan.flask.constants as const


FORMATS = {
    'application/rdf+json': '.json',
    'application/x-turtle': '.ttl',
    'application/rdf+xml': '.rdf'
}

def download_file():
    cfg = get_config()
    rdf4j = RDF4J(rdf4j_base=cfg.RDF4J_BASE)
    prefixes = 'PREFIX ' + '\nPREFIX '.join(const.ALL_PREFIXES)
    auth = HTTPBasicAuth(cfg.VIEWER_USER, cfg.VIEWER_PASS)
    path = Path(cfg.DOWNLOAD_DIR) / cfg.DOWNLOAD_FILENAME

    for mime_type in FORMATS:
        try:
            LOGGER.info('Working on ' + mime_type)
            file = tempfile.NamedTemporaryFile()
            query = prefixes + '\nCONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o }'
            data = rdf4j.get_triple_data_from_query(cfg.PLONE_DCAT_NAMESPACE, query, mime_type=mime_type,
                                                         auth=auth)
            file.write(data)
            file.flush()
            shutil.copyfile(file.name, str(path) + FORMATS[mime_type])
            file.close()
        except Exception:
            LOGGER.error('Could not generate download file')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            msg = u"GET termiated due to error %s %s" % (exc_type, exc_value)
            LOGGER.error(msg)
            for line in format_tb(exc_traceback):
                LOGGER.error(line)


def plone_harvest():
    """
    Harvest Plone Objects and transfer dem in sparql-store
    :return:
    """
    cfg = get_config()

    LOGGER.info('Initiate harvesting')
    try:
        response = requests.get(cfg.HARVEST_URL, auth=HTTPBasicAuth(cfg.HARVEST_USER, cfg.HARVEST_PASS))
    except requests.exceptions.ConnectionError:
        # retry one time
        response = requests.get(cfg.HARVEST_URL, auth=HTTPBasicAuth(cfg.HARVEST_USER, cfg.HARVEST_PASS))
    #
    if response.status_code == 200:
        LOGGER.info('Harvesting initiated')
        LOGGER.info('Harvesting Response is: %s', response)
    else:
        LOGGER.warning('Failed to initiate Harvesting. Error Code: %s', response)

    LOGGER.info('Start Solr Export')
    try:
        solr_main()
    except Exception:
        LOGGER.error('Could not write to Solr')
        exc_type, exc_value, exc_traceback = sys.exc_info()
        msg = u"GET termiated due to error %s %s" % (exc_type, exc_value)
        LOGGER.error(msg)
        for line in format_tb(exc_traceback):
            LOGGER.error(line)

    LOGGER.info('Finished Solr Export')
    LOGGER.info('Generate Download Files')
    try:
        download_file()
    except Exception:
        LOGGER.error('Could not generate Download File')
        exc_type, exc_value, exc_traceback = sys.exc_info()
        msg = u"GET termiated due to error %s %s" % (exc_type, exc_value)
        LOGGER.error(msg)
        for line in format_tb(exc_traceback):
            LOGGER.error(line)
    LOGGER.info('Finished Generate Download File')


def scheduler_loop():
    """
    Main Loop
    :return:
    """
    while True:
        schedule.run_pending()
        time.sleep(5)


def start_scheduler():
    """
    start the scheduler
    :return:
    """
    cfg = get_config()

    LOGGER.info('Initializing the scheduler')
    schedule.every(cfg.HARVEST_PERIOD).seconds.do(plone_harvest)
    LOGGER.info('Scheduler intitialized')

    LOGGER.info('Starting scheduler loop')
    scheduler_loop()
    LOGGER.info('Scheduler loop started')


plone_harvest()
start_scheduler()
