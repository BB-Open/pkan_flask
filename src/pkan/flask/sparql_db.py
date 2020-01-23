"""
DB Manager for Sparql Queries
"""
try:
    import pkan.flask.configs.config as cfg
except ImportError:
    import pkan.flask.configs.config_default as cfg
from pkan.flask.log import LOGGER

from pkan.blazegraph.api import Tripelstore, SPARQL


class DBManager():
    """
    DB Manager Class providing API
    """

    def __init__(self):
        """
        Init
        """
        self.tripel_store = Tripelstore(cfg.BLAZEGRAPH_BASE)
        self.tripel_store.generate_namespace_uri('govdata')

    def get_category_vocab(self):
        """
        Provide a vocab including the categories
        :return:
        """

        sparql_query = """
            prefix foaf: <http://xmlns.com/foaf/0.1/>
            prefix skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX dct: <http://purl.org/dc/terms/>
            SELECT ?s ?css ?title
            WHERE
            {?s a skos:Concept.
            ?s foaf:depiction?css.
            ?s dct:title ?title.
            FILTER(lang(?title) = 'de')
            }
        """

        sparql = self.tripel_store.sparql_for_namespace(cfg.PLONE_SKOS_CONCEPT_NAMESPACE)
        res = sparql.query(sparql_query)

        data = []

        for x in res.bindings:
            uri = x['s'].value
            icon_class = x['css'].value
            title = x['title'].value
            data.append({
                'text': title,
                'id': uri,
                'icon_class': icon_class
            })

        return data

    def get_file_format_vocab(self):
        """
        Provide a vocab including the categories
        :return:
        """
        sparql_query = """
            PREFIX dct: <http://purl.org/dc/terms/>
            SELECT ?s ?title
            WHERE
            {?s a dct:MediaTypeOrExtent.
             ?s dct:title ?title.
             FILTER(lang(?title) = 'de')
            }
        """

        sparql = self.tripel_store.sparql_for_namespace(cfg.PLONE_DCAT_NAMESPACE)
        res = sparql.query(sparql_query)

        data = []

        for x in res.bindings:
            uri = x['s'].value
            title = x['title'].value
            data.append({
                'text': title,
                'id': uri,
                'icon_class': None
            })

        return data

    def get_publisher_vocab(self):
        """
        Provide a vocab including the categories
        :return:
        """
        sparql_query = """
            prefix foaf: <http://xmlns.com/foaf/0.1/>
            SELECT ?s ?title
            WHERE
            {?s a foaf:Agent.
             ?s foaf:name ?title.
             FILTER(lang(?title) = 'de')
            }
                """

        sparql = self.tripel_store.sparql_for_namespace(cfg.PLONE_DCAT_NAMESPACE)
        res = sparql.query(sparql_query)

        data = []

        for x in res.bindings:
            uri = x['s'].value
            title = x['title'].value
            data.append({
                'text': title,
                'id': uri,
                'icon_class': None
            })

        return data

    def get_license_vocab(self):
        """
        Provide a vocab including the categories
        :return:
        """
        sparql_query = """
            PREFIX dct: <http://purl.org/dc/terms/>
            SELECT ?s ?title
            WHERE
            {?s a dct:LicenseDocument.
             ?s dct:title ?title.
             FILTER(lang(?title) = 'de')
            }
        """

        sparql = self.tripel_store.sparql_for_namespace(cfg.PLONE_DCAT_NAMESPACE)
        res = sparql.query(sparql_query)

        data = []

        for x in res.bindings:
            uri = x['s'].value
            title = x['title'].value
            data.append({
                'text': title,
                'id': uri,
                'icon_class': None
            })

        return data

    def get_sorting_options(self):
        """
        Get a Vocab with the Sorting Options like Newest
        :return:
        """
        # todo: which options are suported?
        return [
            {'text': 'Relevanz',
             'id': 'score_desc',
             'icon_class': None},
            {'text': 'Datum aufsteigend',
             'id': 'date_asc',
             'icon_class': None},
            {'text': 'Datum absteigend',
             'id': 'date_desc',
             'icon_class': None},
            {'text': 'Alphabetisch aufsteigend',
             'id': 'title_asc',
             'icon_class': None},
            {'text': 'Alphabetisch absteigend',
             'id': 'title_desc',
             'icon_class': None},
        ]

    def sorting_option_to_sparql(self, params):
        """
        Build up the sparql filter to add to sparql query
        :param title:
        :return:
        """
        if params['order_by']:
            field, order = params['order_by'].split('_')
        else:
            field, order = 'score', 'desc'
        order_by = """ORDER BY {order}(?{field})desc(?default_score)""".format(field=field, order=order)

        return order_by

    def get_namespaces(self):
        namespaces = """
prefix dcat: <http://www.w3.org/ns/dcat#>
prefix dct: <http://purl.org/dc/terms/>
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix bds: <http://www.bigdata.com/rdf/search#>"""
        return namespaces

    def get_values(self, params):
        #  'order_by': 'date_asc', 'sparql': '', 'batch_start': 0, 'batch_end': 1, 'last_change': ['2020-01-02T13:35:00.000Z', '2020-01-04T13:35:00.000Z']}
        query = ''

        neg_pos_fields = ['file_format', 'category', 'publisher', 'license']

        for field in neg_pos_fields:
            if params[field]:
                if params[field]['value_pos']:
                    values = '<' + '> <'.join(params[field]['value_pos']) + '>'
                    query += '\nVALUES ?' + field + '_pos {' + values + '} .'
                if params[field]['value_neg']:
                    values = '<' + '> <'.join(params[field]['value_neg']) + '>'
                    query += '\nVALUES ?' + field + '_neg {' + values + '} .'

        return query

    def get_search_results_dataset(self, params, values):
        query = ''
        # params example

        # SELECT
        select = """\nSELECT DISTINCT ?id ?date ?title ?default_score"""
        query += select

        # WHERE
        where = """
                WHERE {"""
        query += where

        # Values
        # VALUES ?type { dcat:Dataset dcat:Catalog } .
        query += values

        # WHERE TYPE
        where_base_fields = """
            ?id a dcat:Dataset .
            ?id dct:title ?title .
            ?id dct:modified ?date ."""

        query += where_base_fields

        filters = """"""

        if 'publisher' in values:
            filters += """
            ?catalog a dcat:Catalog .
            ?catalog dcat:dataset ?id ."""
            if 'publisher_pos' in values:
                filters += """
            ?catalog dct:publisher ?publisher_pos ."""
            if 'publisher_neg' in values:
                filters += """
            FILTER(NOT EXISTS { ?catalog dct:publisher ?publisher_neg . })"""

        if 'license' in values or 'file_format' in values:
            filters += """
            ?distribution a dcat:Distribution .
            ?id dcat:distribution ?distribution ."""
            if 'license_pos' in values:
                filters += """
            ?distribution dct:license ?license_pos ."""
            if 'license_neg' in values:
                filters += """
            FILTER(NOT EXISTS { ?distribution dct:license ?license_neg . })"""
            if 'file_format_pos' in values:
                filters += """
            ?distribution dct:format ?file_format_pos ."""
            if 'file_format_neg' in values:
                filters += """
            FILTER(NOT EXISTS { ?distribution dct:license ?file_format_neg . })"""
        
        if 'category' in values:
            if 'category_pos' in values:
                filters += """
                ?id dcat:theme ?category_pos ."""
            if 'category_neg' in values:
                filters += """
                FILTER(NOT EXISTS { ?id dcat:theme ?category_neg . })"""

        if params['last_change']:
            start, end = params['last_change']
            if start:
                filters += '''
            FILTER(?date >= "''' + start + '''"^^xsd:dateTime )'''
            if end:
                filters += '''
            FILTER(?date >= "''' + end + '''"^^xsd:dateTime )'''

        query += filters

        # we set a store to order results which are placed in the same position
        query += '''
                    bind( 0.7 as ?default_score)'''

        # todo: how to deal with sparql

        # WHERE_END
        where_end = """
        }"""
        query += where_end

        return query
    
    def get_search_results_catalog(self, params, values):
        query = ''
        # params example

        # SELECT
        select = """\nSELECT DISTINCT ?id ?date ?title ?default_score"""
        query += select

        # WHERE
        where = """
                WHERE {"""
        query += where

        # Values
        # VALUES ?type { dcat:Dataset dcat:Catalog } .
        query += values

        # WHERE TYPE
        where_base_fields = """
            ?id a dcat:Catalog .
            ?id dct:title ?title .
            ?id dct:modified ?date ."""

        query += where_base_fields

        filters = """"""

        if 'publisher' in values:
            if 'publisher_pos' in values:
                filters += """
            ?id dct:publisher ?publisher_pos ."""
            if 'publisher_neg' in values:
                filters += """
            FILTER(NOT EXISTS { ?id dct:publisher ?publisher_neg . })"""

        if 'license' in values or 'file_format' in values:
            filters += """
            ?dataset a dcat:Dataset .
            ?id dcat:dataset ?dataset .
            ?distribution a dcat:Distribution .
            ?dataset dcat:distribution ?distribution ."""
            if 'license_pos' in values:
                filters += """
            ?distribution dct:license ?license_pos ."""
            if 'license_neg' in values:
                filters += """
            FILTER(NOT EXISTS { ?distribution dct:license ?license_neg . })"""
            if 'file_format_pos' in values:
                filters += """
            ?distribution dct:format ?file_format_pos ."""
            if 'file_format_neg' in values:
                filters += """
            FILTER(NOT EXISTS { ?distribution dct:license ?file_format_neg . })"""

        if 'category' in values:
            filters += """
                ?dataset a dcat:Dataset .
                ?id dcat:dataset ?dataset ."""
            if 'category_pos' in values:
                filters += """
                ?dataset dcat:theme ?category_pos ."""
            if 'category_neg' in values:
                filters += """
                FILTER(NOT EXISTS { ?dataset dcat:theme ?category_neg . })"""

        if params['last_change']:
            start, end = params['last_change']
            if start:
                filters += '''
            FILTER(?date >= "''' + start + '''"^^xsd:dateTime )'''
            if end:
                filters += '''
            FILTER(?date >= "''' + end + '''"^^xsd:dateTime )'''

        query += filters

        # we set a store to order results which are placed in the same position
        query += '''
            bind( 0.8 as ?default_score)'''

        # todo: how to deal with sparql

        # WHERE_END
        where_end = """
        }"""
        query += where_end

        return query

    def get_search_results(self, params):
        """
        Get Search results from sparql store
        :param params:
        :return:
        """
        values = self.get_values(params)
        sparql = self.tripel_store.sparql_for_namespace(cfg.PLONE_ALL_OBJECTS_NAMESPACE)
        query = ''

        # Namespaces
        query += self.get_namespaces()

        # SELECT

        query +="""
SELECT DISTINCT ?id ?date ?title ?score ?default_score WHERE {
{ """
        # SUBQUERIES

        query += self.get_search_results_dataset(params, values)

        query += '} UNION {'

        # todo: replace by catalog if implemented
        query += self.get_search_results_catalog(params, values)

        query += '}'

        # KEYWORDS

        if params['textline_keywords']:
            query += '''
            ?o bds:search "''' + params['textline_keywords'] + '''" .
            ?o bds:relevance ?score .
            ?o bds:matchAllTerms "false" .
          	?o bds:minRelevance "0.25" .
            ?id ?p ?o .'''

        query += '}'

        query += self.sorting_option_to_sparql(params)

        # we need this to know how many pages of results we have
        all_res = sparql.query(query)

        # BATCHING
        limit = """
                LIMIT {limit}
                OFFSET {offset}
                """
        batch_start = params['batch_start'] * cfg.BATCH_SIZE
        batch_end = params['batch_end'] * cfg.BATCH_SIZE

        query += limit.format(
            limit=batch_end - batch_start + 1,
            offset=batch_start
        )

        res = sparql.query(query)

        LOGGER.info('Execute Sparql')
        LOGGER.info(query)

        data = []

        for obj in res.bindings:
            obj_uri = obj['id'].value
            obj_title = obj['title'].value
            data.append({
                'id': obj_uri,
                'title': obj_title,
                'description': self.get_description(obj_uri),
                'type': self.get_type(obj_uri)
            })

        LOGGER.info(data)

        return data, len(all_res.bindings)

    def get_title(self, obj_uri):
        """
        Get the title related to a id
        :param obj_uri:
        :return:
        """

        prefixes = 'PREFIX ' + '\nPREFIX '.join(cfg.TITLE_PREFIXES)

        fields = '|'.join(cfg.TITLE_FIELDS)

        sparql = self.tripel_store.sparql_for_namespace(cfg.PLONE_ALL_OBJECTS_NAMESPACE)

        sparql_query = cfg.TITLE_QUERY_LANG.format(
            uri=obj_uri,
            prefix=prefixes,
            fields=fields,
            lang='de')

        res = sparql.query(sparql_query)

        if len(res.bindings) > 0:
            title = res.bindings[0]['title'].value
        else:
            sparql_query = cfg.TITLE_QUERY.format(
                    uri=obj_uri,
                    prefix=prefixes,
                    fields=fields,
                    lang='de')

            res = sparql.query(sparql_query)
            if len(res.bindings) > 0:
                title = res.bindings[0]['title'].value
            else:
                title = obj_uri

        return title

    def get_description(self, obj_uri):
        """
        Get the description related to a obj_id
        :param obj_id:
        :return:
        """

        prefixes = 'PREFIX ' + '\nPREFIX '.join(cfg.DESCRIPTION_PREFIXES)

        fields = '|'.join(cfg.DESCRIPTION_FIELDS)

        sparql = self.tripel_store.sparql_for_namespace(cfg.PLONE_ALL_OBJECTS_NAMESPACE)

        sparql_query = cfg.TITLE_QUERY_LANG.format(
            uri=obj_uri,
            prefix=prefixes,
            fields=fields,
            lang='de')

        res = sparql.query(sparql_query)

        if len(res.bindings) > 0:
            desc = res.bindings[0]['title'].value
        else:
            sparql_query = cfg.TITLE_QUERY.format(
            uri=obj_uri,
            prefix=prefixes,
            fields=fields,
            lang='de')

            res = sparql.query(sparql_query)
            if len(res.bindings) > 0:
                desc = res.bindings[0]['title'].value
            else:
                desc = ''

        return desc

    def get_type(self, obj_uri):
        """
        Get the type related to a obj_id
        :param obj_uri:
        :return:
        """
        sparql = self.tripel_store.sparql_for_namespace(cfg.PLONE_ALL_OBJECTS_NAMESPACE)

        sparql_query = """
                    PREFIX dct:<http://purl.org/dc/terms/>
                    SELECT ?type
                    WHERE
                    {{
                    <{uri}> a ?type.
                    }}
                """.format(uri=obj_uri)

        res = sparql.query(sparql_query)

        if len(res.bindings) > 0:
            type = res.bindings[0]['type'].value
            type_label = self.get_field_label(type)
        else:
            type_label = 'Kein Datentyp gefunden'

        return type_label

    def get_field_label(self, label_uri):
        """
        Get the label for a field id
        :param label_uri:
        :return:
        """

        # todo: not tested yet

        sparql_query = cfg.TITLE_QUERY_LANG

        prefixes = 'PREFIX ' + '\nPREFIX '.join(cfg.LABEL_PREFIXES)

        fields = '|'.join(cfg.LABEL_FIELDS)

        sparql = self.tripel_store.sparql_for_namespace(cfg.PLONE_ALL_OBJECTS_NAMESPACE)

        sparql_query_de = cfg.TITLE_QUERY_LANG.format(
            uri=label_uri,
            prefix=prefixes,
            fields=fields,
            lang='de')

        res_de = sparql.query(sparql_query_de)

        if res_de.bindings:
            label = res_de.bindings[0]['title'].value
            return label

        sparql_query_en = cfg.TITLE_QUERY_LANG.format(
            uri=label_uri,
            prefix=prefixes,
            fields=fields,
            lang='en')

        res_en = sparql.query(sparql_query_en)

        if res_en.bindings:
            label = res_en.bindings[0]['title'].value
            return label

        return label_uri

    def get_items_detail(self, _obj_id):
        """
        Get details of an item for detail view
        :param _obj_id:
        :return:
        """
        # todo: real query
        query = 'CONSTRUCT  WHERE { ?s ?p ?o }'

        data = self.tripel_store.get_turtle_from_query(cfg.PLONE_ALL_OBJECTS_NAMESPACE, query)

        return data

    def get_download_file(self, params):
        file_path = 'test_data/test.txt'
        file_name = 'test.txt'

        # todo

        return file_path, file_name
