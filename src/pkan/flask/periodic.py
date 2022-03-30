"""Scheduler for Cronjobs"""
import time
import requests
from requests.auth import HTTPBasicAuth
import schedule

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
    cfg = get_config()

    LOGGER.info('Initializing the scheduler')
    schedule.every(cfg.HARVEST_PERIOD).seconds.do(plone_harvest)
    LOGGER.info('Scheduler intitialized')

    LOGGER.info('Starting scheduler loop')
    scheduler_loop()
    LOGGER.info('Scheduler loop started')


start_scheduler()
