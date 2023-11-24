import rdflib
from pkan_config.config import get_config
from pkan_config.namespaces import NAMESPACES
from pyrdf4j.rdf4j import RDF4J
from requests.auth import HTTPBasicAuth

cfg = get_config()

ALL_DATASETS = """
prefix bds: <http://www.bigdata.com/rdf/search#>
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX dct: <http://purl.org/dc/terms/>
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix skos: <http://www.w3.org/2004/02/skos/core#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix inq: <http://inqbus.de/ns>


SELECT DISTINCT ?s ?dt ?dd ?type ?prio
    WHERE {
        VALUES ?type { dcat:Dataset dcat:DataService }
        ?s a ?type .
    } LIMIT 1
"""

CONSTRUCT_FIELDS_DATASET = [
    'dct:title',
    'dct:description',
    'dct:identifier',
    'dcat:keyword',
    'dct:issued',
    'dct:modified',
    'dct:language',
    'dcat:theme',
    'dcatde:contributorID'
]

ADDITIONAL_CONSTRUCTS_DATASET = {
    'dcat:contactPoint':  ['a', 'vcard:fn', 'vcard:hasEmail', 'vcard:email'],
    # 'dct:publisher': ['a', 'foaf:name', 'foaf:homepage'],
    'dct:publisher': ['?p'],
    'dct:temporal': ['a', 'dcat:startDate', 'dcat:endDate'],
    'dcat:distribution': ['a', 'dct:license', 'dcat:accessURL', 'dct:language', 'dcat:mediaType', 'dct:format', 'dct:issued', 'dct:modified']
}

CONSTRUCT_DATASET = """
CONSTRUCT {{
    ?dataset_uri a dcat:Dataset .
    {construct_fields}
}}
WHERE
 {{
    VALUES ?dataset_uri {{ {values} }} .
    {where_fields}
 }}

"""

class DatasetDownloader:
    def __init__(self):
        self.rdf4j = RDF4J(rdf4j_base=cfg.RDF4J_BASE)
        self.auth = HTTPBasicAuth(cfg.ADMIN_USER, cfg.ADMIN_PASS)
        self.prepare_query()

    def get_data(self, repo_id, query, mime_type):
        return self.rdf4j.get_triple_data_from_query(repo_id, query, auth=self.auth, mime_type=mime_type)

    def prepare_query(self):
        prefixes = []
        for short, uri in NAMESPACES.items():
            prefixes.append(f"{short}: <{uri}>")
        self.prefixes = 'PREFIX ' + '\nPREFIX '.join(prefixes)
        construct_fields = ''
        where_fields = ''
        for field in CONSTRUCT_FIELDS_DATASET:
            construct = f"?dataset_uri {field} ?dataset_{field.replace(':', '_')} ."
            construct_fields += construct + '\n'
            where_fields += f"OPTIONAL {{ {construct} }} \n"
        for field in ADDITIONAL_CONSTRUCTS_DATASET:
            construct = f"?dataset_uri {field} ?dataset_{field.replace(':', '_')} ."
            construct_fields += construct + '\n'
            where_fields += f"OPTIONAL {{ {construct} }} \n"

        self.dataset_query = dict(construct_fields=construct_fields,
                                                    where_fields=where_fields)
        self.dataset_sub_queries = []
        for field, subfields in ADDITIONAL_CONSTRUCTS_DATASET.items():
            where_fields = f"?dataset_uri {field} ?field_uri ."
            construct_fields = ''
            for sub in subfields:
                construct_sub = f" ?field_uri {sub} ?field_{sub.replace(':', '_').replace('?', '')} ."
                construct_fields += construct_sub + '\n'
                where_fields += f"OPTIONAL {{ {construct_sub} }} .\n"
            query = dict(construct_fields=construct_fields,
                                                        where_fields=where_fields)
            self.dataset_sub_queries.append(query)

    def run(self, datasets, mimetype):
        graph = rdflib.graph.Graph()
        values = '<' + '> <'.join(datasets) + '>'
        query = self.prefixes + CONSTRUCT_DATASET.format(**self.dataset_query, values=values)
        data = self.get_data(cfg.RDF2SOLR_SOURCE, query, mimetype)
        graph.parse(data)
        for sub in self.dataset_sub_queries:
            query = self.prefixes + CONSTRUCT_DATASET.format(**sub, values=values)
            data = self.get_data(cfg.RDF2SOLR_SOURCE, query, mimetype)
            graph.parse(data)

        graph.serialize('test.ttl')


def get_dataset_uris(db_name):
    # this is only for testing
    if db_name is None:
        db_name = cfg.RDF2SOLR_SOURCE
    rdf4j = RDF4J(rdf4j_base=cfg.RDF4J_BASE)
    auth = HTTPBasicAuth(cfg.ADMIN_USER, cfg.ADMIN_PASS)
    results = rdf4j.query_repository(db_name, ALL_DATASETS, auth)
    triples = results['results']['bindings']
    dataset_uris = []
    for res in triples:
        s_uri = res['s']['value']
        if s_uri not in dataset_uris:
            dataset_uris.append(s_uri)
    return dataset_uris

if __name__ == '__main__':
    uris = get_dataset_uris(None)
    downloader = DatasetDownloader()
    downloader.run(uris, 'application/x-turtle')