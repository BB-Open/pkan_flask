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

# BASE URI of RDF4J
RDF4J_BASE = 'http://192.168.122.193:8080/rdf4j-server/'

ADMIN_USER = 'admin'
ADMIN_PASS = 'pw1'

EDITOR_USER = 'editor'
EDITOR_PASS = 'pw2'

VIEWER_USER = 'viewer'
VIEWER_PASS = 'pw3'

PLONE_SKOS_CONCEPT_NAMESPACE = 'skos_concepts'
PLONE_DCAT_NAMESPACE = 'dcat_store'
PLONE_ALL_OBJECTS_NAMESPACE = 'complete_store'

TITLE_FIELDS = [
    'dct:title', 'foaf:name'
]

TITLE_PREFIXES = [
    'dct: <http://purl.org/dc/terms/>',
    'foaf: <http://xmlns.com/foaf/0.1/>',
]

DESCRIPTION_FIELDS = [
    'dct:description'
]

DESCRIPTION_PREFIXES = [
    'dct: <http://purl.org/dc/terms/>',
]

LABEL_FIELDS = [
    'dct:title',
    'skos:prefLabel',
    'rdfs:label',
]

LABEL_PREFIXES = [
    'dct: <http://purl.org/dc/terms/>',
    'skos: <http://www.w3.org/2004/02/skos/core#>',
    'rdfs: <http://www.w3.org/2000/01/rdf-schema#>'
]

TITLE_QUERY_LANG = """
                    {prefix}
                    SELECT ?title
                    WHERE {{
                     <{uri}> {fields} ?title.
                     FILTER(lang(?title) = '{lang}')
                    }}
                """

TITLE_QUERY = """
                    {prefix}
                    SELECT ?title
                    WHERE {{
                     <{uri}> {fields} ?title.
                    }}
                """

BAD_REQUEST = 400
INTERNAL_SERVER_ERROR = 500
INTERNAL_SERVER_ERROR_MSG = 'Es gab einen internen Serverfehler. ' \
                            'Versuchen Sie die Seite neu zu laden ' \
                            'oder wenden Sie sich an den Admin der Seite'
REQUEST_OK = 200

FORBIDDEN_SPARQL_KEYWORDS = ['modify', 'delete', 'insert', 'clear', 'drop', 'create', 'update']

# Perodic scheduler for harveting
HARVEST_URL = 'https://backend.datenadler.de/real_run_cron'
HARVEST_PERIOD = 120  # seconds
SCHEDULER_PERIOD = 60  # seconds
HARVEST_USER = 'XXX'
HARVEST_PASS = 'XXX'

# LANGUAGES

FIRST_LANGUAGE = 'de'
SECOND_LANGUAGE = 'en'

# Mail Settings

EMAIL_TEMPLATE = """
Auf dem Datenadler wurde ein Problem gemeldet.

Nachricht:
{message}

URL:
{link}
"""

EMAIL_SUBJECT = "Datenadler Problem gemeldet"
# todo

MAIL_CONFIG = {
    'MAIL_USERNAME': 'username',
    'MAIL_PASSWORD': 'pw',
    'MAIL_PORT': 25,
    'MAIL_SERVER': 'server',
}

# Types not displayed as type
IGNORED_TYPES = [
    'http://www.w3.org/ns/dcat#Resource',
    'http://www.w3.org/2000/01/rdf-schema#Resource',
    'http://www.w3.org/2002/07/owl#Thing'
]

# How many subelements should be included, in detail page download
QUERY_DEPTH = 7
