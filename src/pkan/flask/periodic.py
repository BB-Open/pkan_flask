from pkan.flask.log import LOGGER

try:
    import pkan.flask.configs.config as cfg
except ImportError:
    import pkan.flask.configs.config_default as cfg

import requests
from requests.auth import HTTPBasicAuth
import schedule
import time


def plone_harvest():
    LOGGER.info('Initiate harvesting')
    response = requests.get(cfg.HARVEST_URL,  auth=HTTPBasicAuth(cfg.HARVEST_USER, cfg.HARVEST_PASS))
    if response.status_code == 200:
        LOGGER.info('Harvesting initiated')
    else:
        LOGGER.warning('Failed to initiate Harvesting. Error Code: %s' % response)

def scheduler_loop():
    while True:
        schedule.run_pending()
        time.sleep()

def start_scheduler():
    LOGGER.info('Initializing the scheduler')
    schedule.every(cfg.HARVEST_PERIOD).seconds.do(plone_harvest)
    LOGGER.info('Scheduler intitialized')

    LOGGER.info('Starting scheduler loop')
    scheduler_loop()
    LOGGER.info('Scheduler loop started')

start_scheduler()
