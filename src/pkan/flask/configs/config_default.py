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
