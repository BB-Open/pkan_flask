"""
Default Config for Pkan Flask
"""
import re

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

ALLOWED_CHARS_QUERY = ''.join((
    re.escape(' '),
    re.escape('-'),  # short dash
    re.escape('–'),  # long dash
    re.escape('_'),
    'A-Z',
    'a-z',
    '0-9',
    'äöüÄÖÜß',
))

ALLOWED_CHARS_FACET = ''.join((
    ALLOWED_CHARS_QUERY,
    re.escape(','),
    re.escape('.'),
    re.escape('('),
    re.escape(')'),
    re.escape('/'),

))

REGEX_QUERY = re.compile(r"[^" + ALLOWED_CHARS_QUERY + r"]")
# there are some additional characters allowed in facets
REGEX_FACET = re.compile(r"[^" + ALLOWED_CHARS_FACET + r"]")
