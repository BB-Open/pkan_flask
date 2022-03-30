"""
DB Manager for Sparql Queries
"""
import tempfile

import rdflib
from SPARQLWrapper.SPARQLExceptions import QueryBadFormed

import pyrdf4j
from pyrdf4j.rdf4j import RDF4J
from rdflib import Literal
from requests.auth import HTTPBasicAuth

from pkan.flask.log import LOGGER
import pkan.flask.constants as const
from pkan_config.config import get_config

from bs4 import BeautifulSoup


def remove_tags(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()

    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)


def remove_tags_turtle(turtle):
    g = rdflib.Graph()
    new_g = rdflib.Graph()

    g.parse(data=turtle, format='text/turtle')

    # todo: is there a better way to find and replace Literals?
    for triple in g:
        o = triple[2]
        if isinstance(o, Literal):
            o = Literal(remove_tags(o.value))
        new_g.add((triple[0], triple[1], o))

    res = new_g.serialize(format='text/turtle')
    return res


class DBManager:
    """
    DB Manager Class providing API
    """

    def __init__(self):
        """
        Init
        """
        # self.tripel_store = Tripelstore(cfg.BLAZEGRAPH_BASE)
        # self.tripel_store.generate_namespace_uri('govdata')
        self.cfg = get_config()
        self.rdf4j = RDF4J(rdf4j_base=self.cfg.RDF4J_BASE)
        self.auth = HTTPBasicAuth(self.cfg.VIEWER_USER, self.cfg.VIEWER_PASS)

    def get_category_vocab(self):
        """
        Provide a vocab including the categories
        :return:
        """

        sparql_query = """
            prefix foaf: <http://xmlns.com/foaf/0.1/>
            prefix skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX dct: <http://purl.org/dc/terms/>
            SELECT DISTINCT ?s ?css ?title
            WHERE
            {?s a skos:Concept.
            ?s foaf:depiction?css.
            ?s dct:title ?title.
            filter (
            !isLiteral(?title) ||
            langmatches(lang(?title), '""" + self.cfg.FIRST_LANGUAGE + """') 
            || (langmatches(lang(?title), '""" + self.cfg.SECOND_LANGUAGE + """') && not exists {
                    ?s a skos:Concept.
                ?s foaf:depiction?css.
                ?s dct:title ?other.
                    filter(isLiteral(?other) && langmatches(lang(?other), '""" + self.cfg.FIRST_LANGUAGE + """')) 
            })
            || (langmatches(lang(?title), "") && not exists { 
                    ?s a skos:Concept.
                ?s foaf:depiction?css.
                ?s dct:title ?other_again.
                    filter(isLiteral(?other_again) && (langmatches(lang(?other_again), '""" + self.cfg.FIRST_LANGUAGE + """'
                    ) || langmatches(lang(?other_again), '""" + self.cfg.SECOND_LANGUAGE + """')))
            })
            )     
            } 
        """
        data = []

        try:
            res = self.rdf4j.query_repository(self.cfg.PLONE_SKOS_CONCEPT_NAMESPACE, sparql_query, auth=self.auth)
        except pyrdf4j.errors.QueryFailed as e:
            LOGGER.warning('Query for skos:Concepts failed')
            return data

        for x in res['results']['bindings']:
            uri = x['s']['value']
            icon_class = x['css']['value']
            title = x['title']['value']
            data.append({
                'text': remove_tags(title),
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
            prefix foaf: <http://xmlns.com/foaf/0.1/>
            prefix skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX dct: <http://purl.org/dc/terms/>
            SELECT DISTINCT ?s ?title
            WHERE
            {?s a dct:MediaTypeOrExtent.
             ?s dct:title ?title.
            filter (
            !isLiteral(?title) ||
            langmatches(lang(?title), '""" + self.cfg.FIRST_LANGUAGE + """') 
            || (langmatches(lang(?title), '""" + self.cfg.SECOND_LANGUAGE + """') && not exists {
                    ?s a dct:MediaTypeOrExtent.
             ?s dct:title ?other.
                    filter(isLiteral(?other) && langmatches(lang(?other), '""" + self.cfg.FIRST_LANGUAGE + """')) 
            })
            || (langmatches(lang(?title), "") && not exists { 
                    ?s a dct:MediaTypeOrExtent.
             ?s dct:title ?other_again.
                    filter(isLiteral(?other_again) && (langmatches(lang(?other_again), '""" + self.cfg.FIRST_LANGUAGE + """'
                    ) || langmatches(lang(?other_again), '""" + self.cfg.SECOND_LANGUAGE + """')))
            })
            )     
            } 
        """

        res = self.rdf4j.query_repository(self.cfg.PLONE_DCAT_NAMESPACE, sparql_query, auth=self.auth)

        data = []

        for x in res['results']['bindings']:
            uri = x['s']['value']
            title = x['title']['value']
            data.append({
                'text': remove_tags(title),
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
            prefix skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX dct: <http://purl.org/dc/terms/>
            SELECT DISTINCT ?s ?title
            WHERE
            {?s a foaf:Agent.
             ?s foaf:name ?title.
            filter (
            !isLiteral(?title) ||
            langmatches(lang(?title), '""" + self.cfg.FIRST_LANGUAGE + """') 
            || (langmatches(lang(?title), '""" + self.cfg.SECOND_LANGUAGE + """') && not exists {
                    ?s a foaf:Agent.
             ?s foaf:name ?other.
                    filter(isLiteral(?other) && langmatches(lang(?other), '""" + self.cfg.FIRST_LANGUAGE + """')) 
            })
            || (langmatches(lang(?title), "") && not exists {
                    ?s a foaf:Agent.
             ?s foaf:name ?other_again.
                    filter(isLiteral(?other_again) && (langmatches(lang(?other_again), '""" + self.cfg.FIRST_LANGUAGE + """'
                    ) || langmatches(lang(?other_again), '""" + self.cfg.SECOND_LANGUAGE + """')))
            })
            )     
            } 
        """

        res = self.rdf4j.query_repository(self.cfg.PLONE_DCAT_NAMESPACE, sparql_query, auth=self.auth)

        data = []

        for x in res['results']['bindings']:
            uri = x['s']['value']
            title = x['title']['value']
            data.append({
                'text': remove_tags(title),
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
                    prefix foaf: <http://xmlns.com/foaf/0.1/>
                    prefix skos: <http://www.w3.org/2004/02/skos/core#>
                    PREFIX dct: <http://purl.org/dc/terms/>
                    SELECT DISTINCT ?s ?title
                    WHERE
                    {?s a dct:LicenseDocument.
             ?s dct:title ?title.
                    filter (
                    !isLiteral(?title) ||
                    langmatches(lang(?title), '""" + self.cfg.FIRST_LANGUAGE + """') 
                    || (langmatches(lang(?title), '""" + self.cfg.SECOND_LANGUAGE + """') && not exists {
                            ?s a dct:LicenseDocument.
             ?s dct:title ?other.
                            filter(isLiteral(?other) && langmatches(lang(?other), '""" + self.cfg.FIRST_LANGUAGE + """')) 
                    })
                    || (langmatches(lang(?title), "") && not exists { 
                            ?s a dct:LicenseDocument.
             ?s dct:title ?other_again.
                            filter(isLiteral(?other_again) && (langmatches(lang(?other_again), '""" + self.cfg.FIRST_LANGUAGE + """'
                            ) || langmatches(lang(?other_again), '""" + self.cfg.SECOND_LANGUAGE + """')))
                    })
                    )     
                    } 
                """

        res = self.rdf4j.query_repository(self.cfg.PLONE_DCAT_NAMESPACE, sparql_query, auth=self.auth)

        data = []

        for x in res['results']['bindings']:
            uri = x['s']['value']
            title = x['title']['value']
            data.append({
                'text': remove_tags(title),
                'id': uri,
                'icon_class': None
            })

        return data

    def get_sorting_options(self):
        """
        Get a Vocab with the Sorting Options like Newest
        :return:
        """
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
        order_by = """ORDER BY {order}(?{field})desc(?default_score)""".format(
            field=field, order=order)

        return order_by

    def get_namespaces(self):
        """
        Sparql namespaces for sparql query
        :return:
        """
        namespaces = """
prefix dcat: <http://www.w3.org/ns/dcat#>
prefix dct: <http://purl.org/dc/terms/>
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix bds: <http://www.bigdata.com/rdf/search#>
prefix skos: <http://www.w3.org/2004/02/skos/core#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>"""
        return namespaces

    def get_values(self, params):
        """
        values for sparql query from our triple state vocabs
        :param params:
        :return:
        """

        EXCLUDE = -1
        _NEUTRAL = 0
        INCLUDE = 1

        query = ''

        neg_pos_fields = ['file_format', 'category', 'publisher', 'license']

        for field in neg_pos_fields:
            includes = []
            excludes = []
            for param, value in params[field].items():
                if value == INCLUDE:
                    includes.append(param)
                elif value == EXCLUDE:
                    excludes.append(param)
            if includes:
                values = '<' + '> <'.join(includes) + '>'
                query += '\nVALUES ?' + field + '_pos {' + values + '} .'
            if excludes:
                values = '<' + '> <'.join(excludes) + '>'
                query += '\nVALUES ?' + field + '_neg {' + values + '} .'

        return query

    def type_title_desc_query(self):
        # description
        fields = '|'.join(const.DESCRIPTION_FIELDS)

        query = '''OPTIONAL {?id '''+ fields + ''' ?desc. '''
        query += const.LANG_FILTER.format(field='desc', fields=fields, lang=self.cfg.FIRST_LANGUAGE, second_lang=self.cfg.SECOND_LANGUAGE, id='?id')
        query += '}'
        fields_type_title = '|'.join(const.LABEL_FIELDS)
        query += '''OPTIONAL {?type ''' + fields_type_title + ''' ?type_title. '''
        query += const.LANG_FILTER.format(field='type_title', fields=fields_type_title, lang=self.cfg.FIRST_LANGUAGE,
                                        second_lang=self.cfg.SECOND_LANGUAGE, id='?type')
        query += '}'

        return query


    def get_search_results_dataset(self, params, values):
        """
        sparql-query for datasets
        :param params:
        :param values:
        :return:
        """
        query = ''
        # params example

        # SELECT
        select = """\nSELECT DISTINCT ?id ?date ?title ?default_score ?type ?o ?desc ?type_title"""
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
            ?id ?p ?o .
            ?id a dcat:Dataset .
            ?id dct:title ?title .
            ?id a ?type .
            OPTIONAL {?id dct:modified ?date }"""


        query += where_base_fields + self.type_title_desc_query()

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
            ?distribution dct:format|dcat:mediaType ?file_format_pos ."""
            if 'file_format_neg' in values:
                filters += """
            FILTER(NOT EXISTS { ?distribution dct:format|dcat:mediaType ?file_format_neg . })"""

        if 'category' in values:
            if 'category_pos' in values:
                filters += """
                ?id dcat:theme ?category_pos ."""
            if 'category_neg' in values:
                filters += """
                FILTER(NOT EXISTS { ?id dcat:theme ?category_neg . })"""

        if 'search_date_period' in params and params['search_date_period']:
            start, end = params['search_date_period']
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

        # WHERE_END
        where_end = """
        }"""
        query += where_end

        return query

    def get_search_results_catalog(self, params, values):
        """
        Sparql-query for catalogs
        :param params:
        :param values:
        :return:
        """
        query = ''
        # params example

        # SELECT
        select = """\nSELECT DISTINCT ?id ?date ?title ?type ?default_score ?o ?desc ?type_title"""
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
            ?id ?p ?o .
            ?id a dcat:Catalog .
            ?id dct:title ?title .
            ?id a ?type.
            OPTIONAL {?id dct:modified ?date .}""" + self.type_title_desc_query()

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
            ?distribution dct:format|dcat:mediaType ?file_format_pos ."""
            if 'file_format_neg' in values:
                filters += """
            FILTER(NOT EXISTS { ?distribution dct:format|dcat:mediaType ?file_format_neg . })"""

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

        if params['search_date_period']:
            start, end = params['search_date_period']
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
        # sparql = self.tripel_store.sparql_for_namespace(cfg.PLONE_ALL_OBJECTS_NAMESPACE)
        query = ''

        # Namespaces
        query += self.get_namespaces()

        # SELECT

        query += """
SELECT DISTINCT ?id ?date ?title ?type ?score ?default_score ?desc ?type_title WHERE {
{ """
        # SUBQUERIES

        query += self.get_search_results_dataset(params, values)

        query += '} UNION {'

        query += self.get_search_results_catalog(params, values)

        query += '}'

        # KEYWORDS

        if params['search_phrase']:

            search_phrase = params['search_phrase'].split(' ')
            regex = []
            for keyword in search_phrase:
                regex.append('''regex(?o, ".*''' + keyword + '''.*", "i")''')

            condition = ' && '.join(regex)

            query += '''
            FILTER(''' + condition + ''' )\n'''

        query += '}'

        query += self.sorting_option_to_sparql(params)

        # we need this to know how many pages of results we have
        all_res = self.rdf4j.query_repository(self.cfg.PLONE_ALL_OBJECTS_NAMESPACE, query, auth=self.auth)

        # BATCHING
        limit = """
                LIMIT {limit}
                OFFSET {offset}
                """
        batch_start = params['batch_start'] * const.BATCH_SIZE
        batch_end = params['batch_end'] * const.BATCH_SIZE

        query += limit.format(
            limit=batch_end - batch_start,
            offset=batch_start
        )

        LOGGER.info('Execute Sparql')
        LOGGER.info(query)

        res = self.rdf4j.query_repository(cfg.PLONE_ALL_OBJECTS_NAMESPACE, query, auth=self.auth)

        LOGGER.info('Sparql executed. Processing Results')

        data = []

        for obj in res['results']['bindings']:
            obj_uri = obj['id']['value']
            obj_title = remove_tags(obj['title']['value'])
            type_uri = obj['type']['value']
            desc = ''
            if 'desc' in obj:
                desc = remove_tags(obj['desc']['value'])
            type_title = 'Kein Datentyp gefunden'
            if 'type_title' in obj:
                type_title = remove_tags(obj['type_title']['value'])
            if type_uri:
                data.append({
                    'id': obj_uri,
                    'title': obj_title,
                    'description': desc,
                    'type_id': type_uri,
                    'type': type_title
                })
            else:
                data.append({
                    'id': obj_uri,
                    'title': remove_tags(obj_title),
                    'description': desc,
                    'type_id': None,
                    'type': type_title
                })

        LOGGER.info('Results Processed')

        return data, len(all_res['results']['bindings'])

    def get_title(self, obj_uri):
        """
        Get the title related to a id
        :param obj_uri:
        :return:
        """

        prefixes = 'PREFIX ' + '\nPREFIX '.join(const.TITLE_PREFIXES)

        fields = '|'.join(const.TITLE_FIELDS)

        # sparql = self.tripel_store.sparql_for_namespace(cfg.PLONE_ALL_OBJECTS_NAMESPACE)

        sparql_query = const.TITLE_QUERY_LANG.format(
            uri=obj_uri,
            prefix=prefixes,
            fields=fields,
            lang=self.cfg.FIRST_LANGUAGE,
            second_lang = self.cfg.SECOND_LANGUAGE)

        res = self.rdf4j.query_repository(self.cfg.PLONE_ALL_OBJECTS_NAMESPACE, sparql_query, auth=self.auth)

        if len(res['results']['bindings']) > 0:
            title = remove_tags(res['results']['bindings'][0]['title']['value'])
        else:
            title = obj_uri
        return title

    def get_description(self, obj_uri):
        """
        Get the description related to a obj_id
        :param obj_id:
        :return:
        """

        prefixes = 'PREFIX ' + '\nPREFIX '.join(const.DESCRIPTION_PREFIXES)

        fields = '|'.join(const.DESCRIPTION_FIELDS)

        # sparql = self.tripel_store.sparql_for_namespace(cfg.PLONE_ALL_OBJECTS_NAMESPACE)

        sparql_query = const.TITLE_QUERY_LANG.format(
            uri=obj_uri,
            prefix=prefixes,
            fields=fields,
            lang=self.cfg.FIRST_LANGUAGE,
            second_lang=self.cfg.SECOND_LANGUAGE
        )

        res = self.rdf4j.query_repository(self.cfg.PLONE_ALL_OBJECTS_NAMESPACE, sparql_query, auth=self.auth)

        if len(res['results']['bindings']) > 0:
            desc = remove_tags(res['results']['bindings'][0]['title']['value'])
        else:
            desc = ''

        return desc

    def get_type(self, obj_uri, type_uri=False):
        """
        Get the type related to a obj_id
        :param obj_uri:
        :return:
        """
        # sparql = self.tripel_store.sparql_for_namespace(cfg.PLONE_ALL_OBJECTS_NAMESPACE)

        sparql_query = """
                    PREFIX dct:<http://purl.org/dc/terms/>
                    SELECT ?t
                    WHERE
                    {{
                    <{uri}> a ?t.
                    }}
                """.format(uri=obj_uri)

        res = self.rdf4j.query_repository(self.cfg.PLONE_ALL_OBJECTS_NAMESPACE, sparql_query, auth=self.auth)

        type_uri_val = None

        for x in res['results']['bindings']:
            t_type = x['t']['type']
            t_value = x['t']['value']
            if t_value not in const.IGNORED_TYPES and t_type == 'uri':
                type_uri_val = t_value
                break
        if type_uri:
            return type_uri_val

        if type_uri_val is not None:
            label = self.get_field_label(type_uri_val)
        else:
            label = 'Kein Datentyp gefunden'

        return label

    def get_field_label(self, label_uri):
        """
        Get the label for a field id
        :param label_uri:
        :return:
        """
        prefixes = 'PREFIX ' + '\nPREFIX '.join(const.LABEL_PREFIXES)

        fields = '|'.join(const.LABEL_FIELDS)

        # sparql = self.tripel_store.sparql_for_namespace(cfg.PLONE_ALL_OBJECTS_NAMESPACE)

        sparql_query_first_lang = const.TITLE_QUERY_LANG.format(
            uri=label_uri,
            prefix=prefixes,
            fields=fields,
            lang=self.cfg.FIRST_LANGUAGE,
            second_lang=self.cfg.SECOND_LANGUAGE)

        res_de = self.rdf4j.query_repository(self.cfg.PLONE_ALL_OBJECTS_NAMESPACE, sparql_query_first_lang, auth=self.auth)

        if res_de['results']['bindings']:
            label = res_de['results']['bindings'][0]['title']['value']
            return label

        return label_uri

    def get_items_detail(self, obj_id):
        """
        Get details of an item for detail view
        :param obj_id:
        :return:
        """
        prefixes = 'PREFIX ' + '\nPREFIX '.join(const.ALL_PREFIXES)

        query = prefixes + "\nCONSTRUCT { ?s ?p ?o } WHERE {?s ?p ?o. FILTER(?s = <" \
                + obj_id + "> || ?p = <" + obj_id + "> || ?o = <" + obj_id + "> )}"

        # query = 'CONSTRUCT  WHERE { ?s ?p ?o }'

        # data = self.tripel_store.get_turtle_from_query(cfg.PLONE_ALL_OBJECTS_NAMESPACE, query)
        data = self.rdf4j.get_turtle_from_query(self.cfg.PLONE_ALL_OBJECTS_NAMESPACE, query, auth=self.auth)
        return remove_tags_turtle(data)

    def get_download_file(self, params):
        """
        create and return download-file
        :param params:
        :return:
        """
        file = tempfile.NamedTemporaryFile()

        file_name = file.name

        prefixes = 'PREFIX ' + '\nPREFIX '.join(const.ALL_PREFIXES)

        download_name = 'sparql_download'
        if params['format'] == 'rdf/json':
            download_name += '.json'
            mime_type = 'application/ld+json'
        elif params['format'] == 'rdf/ttl':
            download_name += '.ttl'
            mime_type = 'text/turtle'
        else:
            download_name += '.rdf'
            mime_type = 'application/rdf+xml'

        LOGGER.info("Use temporary file")
        LOGGER.info(file_name)

        if params['id']:
            obj_id = params['id']

            triples = []
            triplet_subject = '?s'

            for x in range(const.QUERY_DEPTH):
                triplet_object = '?o' + x * 'o'
                triplet_pradicat = triplet_object + 'p'
                triplet = triplet_subject + ' ' + triplet_pradicat + ' ' + triplet_object
                triplet_subject = triplet_object

                triples.append(triplet)

            construct_arg = '.\n'.join(triples)
            constrct_where = '. \noptional {'.join(triples) + '}' * (const.QUERY_DEPTH - 1)



            query = prefixes + "\nconstruct {" + construct_arg + "} where {" + constrct_where + "\nFILTER(?s = <" + obj_id + ">)}"

            LOGGER.info(query)
            data = self.rdf4j.get_triple_data_from_query(self.cfg.PLONE_ALL_OBJECTS_NAMESPACE, query, mime_type=mime_type,
                                                         auth=self.auth)
        else:
            query = prefixes + '\nCONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o }'
            data = self.rdf4j.get_triple_data_from_query(self.cfg.PLONE_DCAT_NAMESPACE, query, mime_type=mime_type,
                                                         auth=self.auth)
        print(data)
        file.write(data)
        file.flush()

        return file_name, download_name, file, mime_type

    def get_search_results_sparql(self, params):
        """
        Search in Sparql-Store
        :param params:
        :return:
        """
        data = []

        sparql = self.tripel_store.sparql_for_namespace(self.cfg.PLONE_ALL_OBJECTS_NAMESPACE)

        query = params['sparql']

        for word in const.FORBIDDEN_SPARQL_KEYWORDS:
            if word.lower() in query.lower():
                error = 'Das Statement konnte nicht ausgeführt werden. ' \
                        'Sie benutzen ein verbotenes Keyword: ' + word.lower()
                return data, 0, error

        # BATCHING
        limit = """
                        LIMIT {limit}
                        OFFSET {offset}
                        """
        batch_start = params['batch_start'] * const.BATCH_SIZE
        batch_end = params['batch_end'] * const.BATCH_SIZE

        # we need this to know how many pages of results we have
        try:
            all_res = sparql.query(query)
        except QueryBadFormed:
            error = 'Das Statement konnte nicht ausgeführt werden: Query Bad Formed.'
            return data, 0, error

        query += limit.format(
            limit=batch_end - batch_start,
            offset=batch_start
        )
        try:
            res = sparql.query(query)
        except QueryBadFormed:
            error = 'Limit und Offset konnten nicht angehängt werden: Query Bad Formed.'
            return data, 0, error

        LOGGER.info('Execute Sparql')
        LOGGER.info(query)

        for obj in res['results']['bindings']:
            obj_uri = obj['id']['value']
            data.append({
                'id': obj_uri,
                'title': self.get_title(obj_uri),
                'description': self.get_description(obj_uri),
                'type': self.get_type(obj_uri)
            })

        LOGGER.info(data)

        return data, len(all_res['results']['bindings']), None

    def get_simple_view_objects(self, query):

        res = self.rdf4j.query_repository(self.cfg.PLONE_ALL_OBJECTS_NAMESPACE, query, auth=self.auth)
        objects = []
        for obj in res['results']['bindings']:
            obj_uri = obj['s']['value']
            objects.append({
                'id': obj_uri,
                'title': self.get_title(obj_uri),
                'description': self.get_description(obj_uri)
            }
            )

        # sort on title
        objects = sorted(objects, key=lambda k: k['title'])

        return objects

    def get_simple_view_fields(self, query, is_url=False):
        res = self.rdf4j.query_repository(self.cfg.PLONE_ALL_OBJECTS_NAMESPACE, query, auth=self.auth)

        formats = []
        for obj in res['results']['bindings']:
            obj_value = obj['s']['value']
            obj_type = obj['s']['type']
            if obj_type == 'uri' and not is_url:
                formats.append(self.get_title(obj_value))
            else:
                formats.append(obj_value)

        return formats

    def get_simple_view_catalog(self, id):

        query = """prefix dcat: <http://www.w3.org/ns/dcat#>
Select DISTINCT ?s 
WHERE {
  <""" + id + """> ?o ?s .
  ?s a dcat:Dataset . }"""

        datasets = self.get_simple_view_objects(query)

        return {
            'title': self.get_title(id),
            'description': self.get_description(id),
            'datasets': datasets,
        }

    def get_simple_view_dataset(self, id):
        query = """prefix dcat: <http://www.w3.org/ns/dcat#>
        Select DISTINCT ?s 
        WHERE {
          ?s ?o <""" + id + """> .
          ?s a dcat:Catalog . }"""

        catalogs = self.get_simple_view_objects(query)

        query = """prefix dcat: <http://www.w3.org/ns/dcat#>
                Select DISTINCT ?s 
                WHERE {
                  <""" + id + """> ?o ?s.
                  ?s a dcat:Distribution . }"""

        distributions = self.get_simple_view_objects(query)
        for element in distributions:
            element_id = element['id']
            query = """prefix dcat: <http://www.w3.org/ns/dcat#>
                            PREFIX dct: <http://purl.org/dc/terms/>
                            Select DISTINCT ?s 
                            WHERE {
                              <""" + element_id + """> dct:format|dcat:mediaType ?s. }"""
            formats = self.get_simple_view_fields(query, is_url=False)
            element['formats'] = '; '.join(set(formats))

        return {
            'title': self.get_title(id),
            'description': self.get_description(id),
            'catalogs': catalogs,
            'distributions': distributions,
        }

    def get_simple_view_distribution(self, id):
        query = """prefix dcat: <http://www.w3.org/ns/dcat#>
        Select DISTINCT ?s 
        WHERE {
          ?s ?o <""" + id + """> .
          ?s a dcat:Dataset . }"""

        datasets = self.get_simple_view_objects(query)

        query = """prefix dcat: <http://www.w3.org/ns/dcat#>
                Select DISTINCT ?s 
                WHERE {
                  ?s ?o ?d .
                  ?s a dcat:Catalog .
                  ?d ?od <""" + id + """> .
                  ?d a dcat:Dataset . }"""

        catalogs = self.get_simple_view_objects(query)

        result_fields = []
        query = """prefix dcat: <http://www.w3.org/ns/dcat#>
                PREFIX dct: <http://purl.org/dc/terms/>
                Select DISTINCT ?s 
                WHERE {
                  <""" + id + """> dct:format|dcat:mediaType ?s. }"""
        formats = self.get_simple_view_fields(query, is_url=False)
        if formats:
            result_fields.append({
                'field': 'Format',
                'value': '; '.join(set(formats)),
                'is_url': False,
            })

        query = """prefix dcat: <http://www.w3.org/ns/dcat#>
                        PREFIX dct: <http://purl.org/dc/terms/>
                        Select DISTINCT ?s 
                        WHERE {
                          <""" + id + """> dct:license ?s. }"""

        formats = self.get_simple_view_fields(query, is_url=False)
        if formats:
            result_fields.append({
                'field': 'Lizenz',
                'value': '; '.join(set(formats)),
                'is_url': False,
            })

        query = """prefix dcat: <http://www.w3.org/ns/dcat#>
                        PREFIX dct: <http://purl.org/dc/terms/>
                        Select DISTINCT ?s 
                        WHERE {
                          <""" + id + """> dcat:accessURL ?s. }"""
        urls = self.get_simple_view_fields(query, is_url=True)
        if urls:
            result_fields.append({
                'field': 'Zugang',
                'value': '; '.join(set(urls)),
                'is_url': True,
            })

        query = """prefix dcat: <http://www.w3.org/ns/dcat#>
                                PREFIX dct: <http://purl.org/dc/terms/>
                                Select DISTINCT ?s 
                                WHERE {
                                  <""" + id + """> dcat:downloadURL ?s. }"""
        urls = self.get_simple_view_fields(query, is_url=True)
        if urls:
            result_fields.append({
                'field': 'Download',
                'value': '; '.join(set(urls)),
                'is_url': True,
            })

        return {
            'title': self.get_title(id),
            'description': self.get_description(id),
            'datasets': datasets,
            'catalogs': catalogs,
            'result_fields': result_fields
        }

    def get_simple_view_publisher(self, id):
        query = """prefix dcat: <http://www.w3.org/ns/dcat#>
                Select DISTINCT ?s 
                WHERE {
                  ?s ?o <""" + id + """> .
                  ?s a dcat:Catalog . }"""

        catalogs = self.get_simple_view_objects(query)

        query = """prefix dcat: <http://www.w3.org/ns/dcat#>
                Select DISTINCT ?s 
                WHERE {
                  ?s ?o <""" + id + """> .
                  ?s a dcat:Dataset . }"""

        datasets = self.get_simple_view_objects(query)
        return {
            'title': self.get_title(id),
            'description': self.get_description(id),
            'catalogs': catalogs,
            'datasets': datasets,
        }
