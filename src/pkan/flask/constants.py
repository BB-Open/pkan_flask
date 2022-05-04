"""
Default Config for Pkan Flask
"""
import string

INTERNAL_SERVER_ERROR = 500
INTERNAL_SERVER_ERROR_MSG = 'Es gab einen internen Serverfehler. ' \
                            'Versuchen Sie die Seite neu zu laden ' \
                            'oder wenden Sie sich an den Admin der Seite'
REQUEST_OK = 200

EMAIL_TEMPLATE = """
Auf dem Datenadler wurde ein Problem gemeldet.

Nachricht:
{message}

URL:
{link}
"""

ALL_PREFIXES = [
    'dct: <http://purl.org/dc/terms/>',
    'skos: <http://www.w3.org/2004/02/skos/core#>',
    'rdfs: <http://www.w3.org/2000/01/rdf-schema#>',
    'dcat: <http://www.w3.org/ns/dcat#>',
    'dcatde: <http://dcat-ap.de/def/dcatde/>',
    'foaf: <http://xmlns.com/foaf/0.1/>',
    'rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>',
    'adms: <http://www.w3.org/ns/adms#>',
    'owl: <http://www.w3.org/2002/07/owl>',
    'schema: <http://schema.org/>',
    'spdx: <http://spdx.org/rdf/terms#>',
    'xsd: <http://www.w3.org/2001/XMLSchema#>',
    'vcard: <http://www.w3.org/2006/vcard/ns#>',
]

ALLOWED_CHARS_QUERY = ' äöüÄÖÜ-_{lower}{upper}{digits}'.format(
    upper=string.ascii_uppercase,
    lower=string.ascii_lowercase,
    digits=string.digits
)
# there are some additional characters allowed in facets
ALLOWED_CHARS_FACET = ',.()' + ALLOWED_CHARS_QUERY
