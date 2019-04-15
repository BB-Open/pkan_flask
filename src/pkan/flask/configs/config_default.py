from logging import INFO
from os.path import join

PKAN_LOG_DIR = "/var/log/pkan"
# The logfiles
pkan_log_file = join(PKAN_LOG_DIR, "flask.log")
# The desired loglevel for console output
log_level_console = INFO
# The desired loglevel for the logfile
log_level_file = INFO
# Colors for the log console output (Options see colorlog-package)
log_colors =  {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red,bg_white',
}