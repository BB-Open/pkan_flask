"""
Default Config for Pkan Fla
"""
from logging import INFO
from os.path import join

PKAN_LOG_DIR = "/var/log/pkan"
# The logfiles
PKAN_LOG_FILE = join(PKAN_LOG_DIR, "flask.log")
# The desired loglevel for console output
LOG_LEVEL_CONSOLE = INFO
# The desired loglevel for the logfile
LOG_LEVEL_FILE = INFO
# Colors for the log console output (Options see colorlog-package)
LOG_COLOURS = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red,bg_white',
}
