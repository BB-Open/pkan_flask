"""
Default Config for Pkan Flask
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

# SPARQL RESULT BATCHING
BATCH_SIZE = 10

# BASE URI of Blazegraph
BLAZEGRAPH_BASE = 'http://localhost:9999'

PLONE_SKOS_CONCEPT_NAMESPACE = 'skos_concepts'
PLONE_DCAT_NAMESPACE = ''
PLONE_ALL_OBJECTS_NAMESPACE = ''


