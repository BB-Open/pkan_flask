"""
Log Settings for Pkan Flask
"""
import os
import sys
from logging import StreamHandler, getLogger, Formatter, DEBUG
from logging.handlers import TimedRotatingFileHandler
from sys import stdout

try:
    import pkan.flask.configs.config as cfg
except ImportError:
    import pkan.flask.configs.config_default as cfg

if not os.path.exists(cfg.PKAN_LOG_DIR):
    print(
        "Log file directory does not exists %s, please create it " %
        cfg.PKAN_LOG_DIR)
    import getpass

    USERNAME = getpass.getuser()
    print("become superuser: su ")
    print("excecute: mkdir -p %s " % cfg.PKAN_LOG_DIR)
    print("excecute: chown %s:%s %s " % (
        USERNAME, USERNAME, cfg.PKAN_LOG_DIR))
    sys.exit(1)

try:
    import colorlog
    from colorlog import ColoredFormatter

    FORMATTER = ColoredFormatter(
        "%(log_color)s%(asctime)s [%(process)d] %(levelname)-8s %("
        "message)s",
        datefmt=None,
        reset=True,
        log_colors=cfg.LOG_COLOURS,
        secondary_log_colors={},
        style='%'
    )
    LOGGER = colorlog.getLogger("eprofile")

except Exception as e:
    print(e)
    LOGGER = getLogger("eprofile")
    FORMATTER = Formatter(
        '%(asctime)s [%(process)d] %(levelname)-8s %(message)s',
        "%Y-%m-%d %H:%M:%S")

timedRotatingFileHandler = TimedRotatingFileHandler(
    cfg.PKAN_LOG_FILE, "D", 1, 15)
timedRotatingFileHandlerFormatter = FORMATTER
timedRotatingFileHandler.setFormatter(timedRotatingFileHandlerFormatter)
timedRotatingFileHandler.setLevel(cfg.LOG_LEVEL_FILE)

consoleHandler = StreamHandler(stdout)
# formatter = Formatter('%(asctime)s %(levelname)-8s %(message)s',
#                      "%Y-%m-%d %H:%M:%S")
consoleFormatter = FORMATTER
consoleHandler.setFormatter(consoleFormatter)
consoleHandler.setLevel(cfg.LOG_LEVEL_CONSOLE)

LOGGER.addHandler(timedRotatingFileHandler)
LOGGER.addHandler(consoleHandler)

LOGGER.propagate = False
LOGGER.setLevel(DEBUG)
