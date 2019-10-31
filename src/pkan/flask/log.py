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

except Exception as exc:
    print(exc)
    LOGGER = getLogger("eprofile")
    FORMATTER = Formatter(
        '%(asctime)s [%(process)d] %(levelname)-8s %(message)s',
        "%Y-%m-%d %H:%M:%S")

ROT_FILE_HANDLER = TimedRotatingFileHandler(
    cfg.PKAN_LOG_FILE, "D", 1, 15)
FILE_HANDLER_FORMATTER = FORMATTER
ROT_FILE_HANDLER.setFormatter(FILE_HANDLER_FORMATTER)
ROT_FILE_HANDLER.setLevel(cfg.LOG_LEVEL_FILE)

CONSOL_HANDLER = StreamHandler(stdout)
# formatter = Formatter('%(asctime)s %(levelname)-8s %(message)s',
#                      "%Y-%m-%d %H:%M:%S")
CONSOLE_FORMATTER = FORMATTER
CONSOL_HANDLER.setFormatter(CONSOLE_FORMATTER)
CONSOL_HANDLER.setLevel(cfg.LOG_LEVEL_CONSOLE)

LOGGER.addHandler(ROT_FILE_HANDLER)
LOGGER.addHandler(CONSOL_HANDLER)

LOGGER.propagate = False
LOGGER.setLevel(DEBUG)
