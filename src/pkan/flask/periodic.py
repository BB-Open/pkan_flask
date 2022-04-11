"""Scheduler for Cronjobs"""
import sys
import time
from traceback import format_tb

import schedule
from iso2dcat.solr.rdf2solr import main as solr_main
from pkan.flask.log import LOGGER
from pkan_config.config import get_config


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


start_scheduler()
