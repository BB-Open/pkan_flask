"""Scheduler for Cronjobs"""
import time
import requests
from requests.auth import HTTPBasicAuth
import schedule

from pkan.flask.log import LOGGER

try:
    import pkan.flask.configs.config as cfg
except ImportError:
    import pkan.flask.configs.config_default as cfg


def plone_harvest():
    """
    Harvest Plone Objects and transfer dem in sparql-store
    :return:
    """
    LOGGER.info('Initiate harvesting')
    response = requests.get(cfg.HARVEST_URL, auth=HTTPBasicAuth(cfg.HARVEST_USER, cfg.HARVEST_PASS))
    if response.status_code == 200:
        LOGGER.info('Harvesting initiated')
        LOGGER.info('Harvesting Response is: %s', response)
    else:
        LOGGER.warning('Failed to initiate Harvesting. Error Code: %s', response)


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
    LOGGER.info('Initializing the scheduler')
    schedule.every(cfg.HARVEST_PERIOD).seconds.do(plone_harvest)
    LOGGER.info('Scheduler intitialized')

    LOGGER.info('Starting scheduler loop')
    scheduler_loop()
    LOGGER.info('Scheduler loop started')


start_scheduler()
