"""
DB Manager for Sparql Queries
"""
from pkan.flask.configs.config_default import BATCH_SIZE, PLONE_DCAT_NAMESPACE, PLONE_SKOS_CONCEPT_NAMESPACE, \
    PLONE_ALL_OBJECTS_NAMESPACE, TITLE_PREFIXES, TITLE_FIELDS, DESCRIPTION_PREFIXES, DESCRIPTION_FIELDS, \
    TRANSLATION_SPARQL_QUERY_RAW, LABEL_PREFIXES, LABEL_FIELDS
from pkan.flask.log import LOGGER

from pkan.blazegraph.api import tripel_store


class DBManager():
    """
    DB Manager Class providing API
    """

    def __init__(self):
        """
        Init
        """

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

        sparql = tripel_store.sparql_for_namespace(PLONE_SKOS_CONCEPT_NAMESPACE)
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

        sparql = tripel_store.sparql_for_namespace(PLONE_DCAT_NAMESPACE)
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

        sparql = tripel_store.sparql_for_namespace(PLONE_DCAT_NAMESPACE)
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

        sparql = tripel_store.sparql_for_namespace(PLONE_DCAT_NAMESPACE)
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

        # todo

        _sorting = self.sorting_option_to_sparql(params)
        _categorie = self.category_id_to_sparql(params)

        ids = [
            'https://datenadler.de/kataloge/mik/dcat_catalog',
            'https://datenadler.de/kataloge/mik/dcat_catalog/kommunalverzeichnis-land-brandenburg'
        ]
        ids = ids * 80
        ids.append('http://publications.europa.eu/resource/authority/data-theme/GOVE')

        batch_start = params['batch_start']
        batch_end = params['batch_end']
        ids_displayed = ids[batch_start * BATCH_SIZE:batch_end * BATCH_SIZE]

        data = []

        for obj_id in ids_displayed:
            data.append({
                'id': obj_id,
                'title': self.get_title(obj_id),
                'description': self.get_description(obj_id),
                'type': self.get_type(obj_id)
            })

        LOGGER.info(data)

        return data, len(ids)

    def get_title(self, obj_uri):
        """
        Get the title related to a id
        :param obj_uri:
        :return:
        """

        prefixes = 'PREFIX ' + '\nPREFIX '.join(TITLE_PREFIXES)

        fields = '|'.join(TITLE_FIELDS)

        sparql = tripel_store.sparql_for_namespace(PLONE_ALL_OBJECTS_NAMESPACE)

        sparql_query = TRANSLATION_SPARQL_QUERY_RAW.format(
            uri=obj_uri,
            prefix=prefixes,
            fields=fields,
            lang='de')

        res = sparql.query(sparql_query)

        if res.bindings:
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

        sparql = tripel_store.sparql_for_namespace(PLONE_ALL_OBJECTS_NAMESPACE)

        sparql_query = TRANSLATION_SPARQL_QUERY_RAW.format(
            uri=obj_uri,
            prefix=prefixes,
            fields=fields,
            lang='de')

        res = sparql.query(sparql_query)

        if res.bindings:
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
        sparql = tripel_store.sparql_for_namespace(PLONE_ALL_OBJECTS_NAMESPACE)

        sparql_query = """
                    PREFIX dct:<http://purl.org/dc/terms/>
                    SELECT ?type
                    WHERE
                    {{
                    <{uri}> a ?type.
                    }}
                """.format(uri=obj_uri)

        res = sparql.query(sparql_query)

        if res.bindings:
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

        sparql_query = TRANSLATION_SPARQL_QUERY_RAW

        prefixes = 'PREFIX ' + '\nPREFIX '.join(LABEL_PREFIXES)

        fields = '|'.join(LABEL_FIELDS)

        sparql = tripel_store.sparql_for_namespace(PLONE_ALL_OBJECTS_NAMESPACE)

        sparql_query_de = TRANSLATION_SPARQL_QUERY_RAW.format(
            uri=label_uri,
            prefix=prefixes,
            fields=fields,
            lang='de')
        
        res_de = sparql.query(sparql_query_de)

        if res_de.bindings:
            label = res_de.bindings[0]['title'].value
            return label

        sparql_query_en = TRANSLATION_SPARQL_QUERY_RAW.format(
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

        data = tripel_store.get_turtle_from_query(PLONE_ALL_OBJECTS_NAMESPACE, query)

        return data

    def get_download_file(self, params):
        file_path = 'test_data/test.txt'
        file_name = 'test.txt'

        # todo

        return file_path, file_name
