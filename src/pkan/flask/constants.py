"""
Default Config for Pkan Flask
"""
from logging import INFO
from os.path import join

# SPARQL RESULT BATCHING
BATCH_SIZE = 10

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
                     filter (
                    !isLiteral(?title) ||
                    langmatches(lang(?title), '{lang}') 
                    || (langmatches(lang(?title), '{second_lang}') && not exists {{
             <{uri}> {fields} ?other.
                            filter(isLiteral(?other) && langmatches(lang(?other), '{lang}')) 
                    }})
                    || (langmatches(lang(?title), "") && not exists {{
                            <{uri}> {fields} ?other_again.
                            filter(isLiteral(?other_again) && (langmatches(lang(?other_again), '{lang}'
                            ) || langmatches(lang(?other_again), '{second_lang}')))
                    }})
                    )     
                    }}
"""

LANG_FILTER = """filter (
                    !isLiteral(?{field}) ||
                    langmatches(lang(?{field}), '{lang}') 
                    || (langmatches(lang(?{field}), '{second_lang}') && not exists {{
             {id} {fields} ?other{field}.
                            filter(isLiteral(?other{field}) && langmatches(lang(?other{field}), '{lang}')) 
                    }})
                    || (langmatches(lang(?{field}), "") && not exists {{
                            {id} {fields} ?other_again{field}.
                            filter(isLiteral(?other_again{field}) && (langmatches(lang(?other_again{field}), '{lang}'
                            ) || langmatches(lang(?other_again{field}), '{second_lang}')))
                    }})
                    )     """

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

EMAIL_TEMPLATE = """
Auf dem Datenadler wurde ein Problem gemeldet.

Nachricht:
{message}

URL:
{link}
"""

# Types not displayed as type
IGNORED_TYPES = [
    'http://www.w3.org/ns/dcat#Resource',
    'http://www.w3.org/2000/01/rdf-schema#Resource',
    'http://www.w3.org/2002/07/owl#Thing'
]

# How many subelements should be included, in detail page download
QUERY_DEPTH = 7

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


