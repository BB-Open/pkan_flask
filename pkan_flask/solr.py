import pprint

import requests
import simplejson as sj
from pkan_config.config import get_config

from pkan_flask.constants import REGEX_QUERY, REGEX_FACET, FACET_LIMIT_PUBLISHER, FACET_LIMIT_LICENSE, \
    FACET_LIMIT_FORMAT, FACET_LIMIT_THEME, FACET_LIMIT_TYPE
from pkan_flask.log import LOGGER

cfg = get_config()
def query_results(in_params):
    LOGGER.debug('request_data:' + pprint.pformat(in_params))

    out_params = {}

    if 'sort' in in_params:
        sort = in_params['sort']
        if sort == "score":
            out_params['sort'] = 'score desc, inq_priority desc'
        elif sort == "asc":
            out_params['sort'] = 'sort asc'
        elif sort == "desc":
            out_params['sort'] = 'sort desc'
        else:
            # standard Fallback
            out_params['sort'] = 'score desc, inq_priority desc'
    else:
        out_params['sort'] = 'score desc, inq_priority desc'

    query_str = in_params['q']
    query_str = REGEX_QUERY.sub('', query_str)
    LOGGER.debug(query_str)
    query_tokens = query_str.split(' ')
    query_tokens_clean = []
    for token in query_tokens:
        query_tokens_clean.append('search:*{}*'.format(token))

    for facet_name, choices in in_params['choices'].items():
        for choice in choices:
            choice = REGEX_FACET.sub('', choice)
            query_tokens_clean.append('{}:"{}"'.format(facet_name, choice))

    out_params['start'] = int(in_params['start'])
    out_params['rows'] = int(in_params['rows'])

    out_params['q'] = ' AND '.join(query_tokens_clean)

    out_params['facet'] = 'true'
    out_params['json.facet'] = sj.dumps({
        'dct_publisher_facet': {
            'terms': {'field': 'dct_publisher_facet',
                      'limit': FACET_LIMIT_PUBLISHER},
        },
        'dct_license_facet': {
            'terms': {'field': 'dct_license_facet',
                      'limit': FACET_LIMIT_LICENSE}
        },
        'dct_format_facet': {
            'terms': {'field': 'dct_format_facet',
                      'limit': FACET_LIMIT_FORMAT}
        },
        'dcat_theme_facet': {
            'terms': {'field': 'dcat_theme_facet',
                      'limit': FACET_LIMIT_THEME}
        },
        'rdf_type': {
            'terms': {'field': 'rdf_type',
                      'limit': FACET_LIMIT_TYPE}
        },
    })
    LOGGER.debug('solr_param:' + pprint.pformat(out_params))

    result = requests.post(
        cfg.SOLR_SELECT_URI,
        data=sj.dumps({'params': out_params}),
        headers={"Content-type": "application/json; charset=utf-8"}
    )
    return result