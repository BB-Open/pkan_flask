import sys
from logging import StreamHandler, getLogger, Formatter, DEBUG, INFO
from logging.handlers import TimedRotatingFileHandler
from sys import stdout

import os

try:
    import pkan.flask.configs.config as cfg
except:
    import pkan.flask.configs.config_default as cfg

if not os.path.exists(cfg.PKAN_LOG_DIR):
    print(
            "Log file directory does not exists %s, please create it " %
            cfg.PKAN_LOG_DIR)
    import getpass
    username = getpass.getuser()
    print("become superuser: su ")
    print("excecute: mkdir -p %s " % cfg.PKAN_LOG_DIR)
    print("excecute: chown %s:%s %s " % (
    username, username, cfg.PKAN_LOG_DIR))
    sys.exit(1)

try:
    import colorlog
    from colorlog import ColoredFormatter

    formatter = ColoredFormatter(
            "%(log_color)s%(asctime)s [%(process)d] %(levelname)-8s %("
            "message)s",
            datefmt=None,
            reset=True,
            log_colors=cfg.log_colors,
            secondary_log_colors={},
            style='%'
    )
    logger = colorlog.getLogger("eprofile")

except Exception as e:
    print(e)
    logger = getLogger("eprofile")
    formatter = Formatter(
            '%(asctime)s [%(process)d] %(levelname)-8s %(message)s',
            "%Y-%m-%d %H:%M:%S")


timedRotatingFileHandler = TimedRotatingFileHandler(cfg.pkan_log_file, "D", 1, 15)
timedRotatingFileHandlerFormatter = formatter
timedRotatingFileHandler.setFormatter(timedRotatingFileHandlerFormatter)
timedRotatingFileHandler.setLevel(cfg.log_level_file)

consoleHandler = StreamHandler(stdout)
#formatter = Formatter('%(asctime)s %(levelname)-8s %(message)s',
#                      "%Y-%m-%d %H:%M:%S")
consoleFormatter = formatter
consoleHandler.setFormatter(consoleFormatter)
consoleHandler.setLevel(cfg.log_level_console)

logger.addHandler(timedRotatingFileHandler)
logger.addHandler(consoleHandler)

logger.propagate = False
logger.setLevel(DEBUG)