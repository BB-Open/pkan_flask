"""
DB Manager for Sparql Queries
"""
from pkan.flask.configs.config_default import (
    BATCH_SIZE, PLONE_DCAT_NAMESPACE,
    PLONE_SKOS_CONCEPT_NAMESPACE,
    PLONE_ALL_OBJECTS_NAMESPACE, TITLE_PREFIXES, TITLE_FIELDS,
    DESCRIPTION_PREFIXES, DESCRIPTION_FIELDS,
    TITLE_QUERY_LANG, LABEL_PREFIXES, LABEL_FIELDS, TITLE_QUERY,
    BLAZEGRAPH_BASE, )
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
        self.tripel_store = Tripelstore(BLAZEGRAPH_BASE)
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

        sparql = self.tripel_store.sparql_for_namespace(PLONE_SKOS_CONCEPT_NAMESPACE)
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

    def category_id_to_sparql(self, _params):
        """
        Build up the sparql filter to add to sparql query
        :param title:
        :return:
        """
        # todo

        return ''

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

        sparql = self.tripel_store.sparql_for_namespace(PLONE_DCAT_NAMESPACE)
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

    def file_format_id_to_sparql(self, _params):
        """
        Build up the sparql filter to add to sparql query
        :param title:
        :return:
        """
        # todo
        return ''

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

        sparql = self.tripel_store.sparql_for_namespace(PLONE_DCAT_NAMESPACE)
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

    def publisher_id_to_sparql(self, _params):
        """
        Build up the sparql filter to add to sparql query
        :param title:
        :return:
        """
        # todo
        return ''

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

        sparql = self.tripel_store.sparql_for_namespace(PLONE_DCAT_NAMESPACE)
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

    def license_id_to_sparql(self, _params):
        """
        Build up the sparql filter to add to sparql query
        :param title:
        :return:
        """
        # todo
        return ''

    def keywords_to_sparql(self, _params):
        """
        Build up the sparql filter to add to sparql query
        :param title:
        :return:
        """
        # todo
        return ''

    def last_change_date_to_sparql(self, _params):
        """
        Build up the sparql filter to add to sparql query
        :param _params:
        :return:
        """
        # todo
        return ''

    def get_sorting_options(self):
        """
        Get a Vocab with the Sorting Options like Newest
        :return:
        """
        # todo: which options are suported?
        return [
            {'text': 'Relevanz',
             'id': 'relevance',
             'icon_class': None},
            {'text': 'Datum aufsteigend',
             'id': 'date_asc',
             'icon_class': None},
            {'text': 'Datum absteigend',
             'id': 'date_desc',
             'icon_class': None},
            {'text': 'Alphabetisch aufsteigend',
             'id': 'letter_asc',
             'icon_class': None},
            {'text': 'Alphabetisch absteigend',
             'id': 'letter_desc',
             'icon_class': None},
        ]

    def sorting_option_to_sparql(self, _params):
        """
        Build up the sparql filter to add to sparql query
        :param title:
        :return:
        """
        # todo
        return ''

    def get_search_results(self, params):
        """
        Get Search results from sparql store
        :param params:
        :return:
        """

        query = ''

        # Namespaces

        namespaces = """
prefix dcat: <http://www.w3.org/ns/dcat#>
prefix dct: <http://purl.org/dc/terms/>"""
        query += namespaces

        # SELECT
        select = """
SELECT ?dataset ?date"""
        query += select

        # WHERE
        where = """
WHERE {"""
        query += where

        # WHERE TYPE
        where_type = """
    ?dataset a dcat:Dataset ."""

        query += where_type

        # FILTER for Category
        where_category = """
    ?dataset dcat:theme <{category}> ."""

        if 'category' in params:
            if len(params['category']['value_pos']) == 1 :
                query += where_category.format(
                        category = params['category']['value_pos'][0]
                )

        # WHERE Date
        where_date = """
    ?dataset dct:modified ?date . """
        query += where_date

        # WHERE_END
        where_end = """
}"""
        query += where_end

        # ORDER BY (date)
        default_order_by = """
ORDER BY (?date)"""
        order_by = """
ORDER BY {order}(?date)"""

        if params['order_by']:
            query += order_by
        else :
            query += default_order_by

        # BATCHING
        limit = """
LIMIT {limit}
OFFSET {offset}
"""
        batch_start = params['batch_start'] * BATCH_SIZE
        batch_end = params['batch_end'] * BATCH_SIZE

        query += limit.format(
               limit = batch_end - batch_start + 1,
               offset = batch_start
        )

        print(query)

        sparql = self.tripel_store.sparql_for_namespace(PLONE_ALL_OBJECTS_NAMESPACE)

        res = sparql.query(query)

        data = []

        for obj in res.bindings:
            obj_uri = obj['dataset'].value
            data.append({
                'id': obj_uri,
                'title': self.get_title(obj_uri),
                'description': self.get_description(obj_uri),
                'type': self.get_type(obj_uri)
            })

        LOGGER.info(data)

        return data, len(res.bindings)

    def get_title(self, obj_uri):
        """
        Get the title related to a id
        :param obj_uri:
        :return:
        """

        prefixes = 'PREFIX ' + '\nPREFIX '.join(TITLE_PREFIXES)

        fields = '|'.join(TITLE_FIELDS)

        sparql = self.tripel_store.sparql_for_namespace(PLONE_ALL_OBJECTS_NAMESPACE)

        sparql_query = TITLE_QUERY_LANG.format(
            uri=obj_uri,
            prefix=prefixes,
            fields=fields,
            lang='de')

        res = sparql.query(sparql_query)

        if len(res.bindings) > 0:
            title = res.bindings[0]['title'].value
        else:
            sparql_query = TITLE_QUERY.format(
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

        prefixes = 'PREFIX ' + '\nPREFIX '.join(DESCRIPTION_PREFIXES)

        fields = '|'.join(DESCRIPTION_FIELDS)

        sparql = self.tripel_store.sparql_for_namespace(PLONE_ALL_OBJECTS_NAMESPACE)

        sparql_query = TITLE_QUERY_LANG.format(
            uri=obj_uri,
            prefix=prefixes,
            fields=fields,
            lang='de')

        res = sparql.query(sparql_query)

        if len(res.bindings) > 0:
            desc = res.bindings[0]['title'].value
        else:
            sparql_query = TITLE_QUERY.format(
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
        sparql = self.tripel_store.sparql_for_namespace(PLONE_ALL_OBJECTS_NAMESPACE)

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

        sparql_query = TITLE_QUERY_LANG

        prefixes = 'PREFIX ' + '\nPREFIX '.join(LABEL_PREFIXES)

        fields = '|'.join(LABEL_FIELDS)

        sparql = self.tripel_store.sparql_for_namespace(PLONE_ALL_OBJECTS_NAMESPACE)

        sparql_query_de = TITLE_QUERY_LANG.format(
            uri=label_uri,
            prefix=prefixes,
            fields=fields,
            lang='de')

        res_de = sparql.query(sparql_query_de)

        if res_de.bindings:
            label = res_de.bindings[0]['title'].value
            return label

        sparql_query_en = TITLE_QUERY_LANG.format(
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

        data = self.tripel_store.get_turtle_from_query(PLONE_ALL_OBJECTS_NAMESPACE, query)

        return data

    def get_download_file(self, params):
        file_path = 'test_data/test.txt'
        file_name = 'test.txt'

        # todo

        return file_path, file_name
