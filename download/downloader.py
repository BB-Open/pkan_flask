import rdflib
from pkan_config.config import get_config
from pkan_config.namespaces import NAMESPACES
from pyrdf4j.rdf4j import RDF4J
from requests.auth import HTTPBasicAuth

from download.constants import CONSTRUCT_FIELDS_DATASET, ADDITIONAL_CONSTRUCTS, CONSTRUCT_DATASET, \
    CONSTRUCT_FIELDS_DATASERVICE, CONSTRUCT_DATASERVICE, CONSTRUCT_DATASET_FOR_SERVICE

cfg = get_config()


class BaseDownloader:
    def __init__(self):
        self.rdf4j = RDF4J(rdf4j_base=cfg.RDF4J_BASE)
        self.auth = HTTPBasicAuth(cfg.ADMIN_USER, cfg.ADMIN_PASS)
        self.construct = None
        self.prefixes = ''
        self.query_data = {}
        self.subqueries = []
        self.prepare_query()

    def prepare_query(self):
        pass

    def get_data(self, repo_id, query, mime_type):
        return self.rdf4j.get_triple_data_from_query(repo_id, query, auth=self.auth, mime_type=mime_type)

    def run(self, ids, mimetype, graph=None):
        if graph is None:
            graph = rdflib.graph.Graph()
        values = '<' + '> <'.join(ids) + '>'
        query = self.prefixes + self.construct.format(**self.query_data, values=values)
        data = self.get_data(cfg.RDF2SOLR_SOURCE, query, mimetype)
        graph.parse(data)
        for sub in self.subqueries:
            query = self.prefixes + self.construct.format(**sub, values=values)
            data = self.get_data(cfg.RDF2SOLR_SOURCE, query, mimetype)
            graph.parse(data)

        return graph


class DatasetDownloader(BaseDownloader):

    def __init__(self):
        super().__init__()
        self.construct = CONSTRUCT_DATASET

    def prepare_query(self):
        prefixes = []
        for short, uri in NAMESPACES.items():
            prefixes.append(f"{short}: <{uri}>")
        self.prefixes = 'PREFIX ' + '\nPREFIX '.join(prefixes)
        construct_fields = ''
        where_fields = ''
        for field in CONSTRUCT_FIELDS_DATASET:
            construct = f"?dataset_uri {field} ?dataset_{field.replace(':', '_').replace('?', '')} ."
            construct_fields += construct + '\n'
            where_fields += f"OPTIONAL {{ {construct} }} \n"
        for field in ADDITIONAL_CONSTRUCTS:
            construct = f"?dataset_uri {field} ?dataset_{field.replace(':', '_').replace('?', '')} ."
            construct_fields += construct + '\n'
            where_fields += f"OPTIONAL {{ {construct} }} \n"

        self.query_data = dict(construct_fields=construct_fields,
                               where_fields=where_fields)
        self.subqueries = []
        for field, subfields in ADDITIONAL_CONSTRUCTS.items():
            where_fields = f"?dataset_uri {field} ?field_uri ."
            construct_fields = ''
            for sub in subfields:
                construct_sub = f" ?field_uri {sub} ?field_{sub.replace(':', '_').replace('?', '')} ."
                construct_fields += construct_sub + '\n'
                where_fields += f"OPTIONAL {{ {construct_sub} }} .\n"
            query = dict(construct_fields=construct_fields,
                         where_fields=where_fields)
            self.subqueries.append(query)


class DataServiceDownloader(BaseDownloader):

    def __init__(self):

        super().__init__()
        self.construct = CONSTRUCT_DATASERVICE
    def prepare_query(self):
        prefixes = []
        for short, uri in NAMESPACES.items():
            prefixes.append(f"{short}: <{uri}>")
        self.prefixes = 'PREFIX ' + '\nPREFIX '.join(prefixes)
        construct_fields = ''
        where_fields = ''
        for field in CONSTRUCT_FIELDS_DATASERVICE:
            construct = f"?dataservice_uri {field} ?dataservice_{field.replace(':', '_').replace('?', '')} ."
            construct_fields += construct + '\n'
            where_fields += f"OPTIONAL {{ {construct} }} \n"
        for field in ADDITIONAL_CONSTRUCTS:
            construct = f"?dataservice_uri {field} ?dataservice_{field.replace(':', '_').replace('?', '')} ."
            construct_fields += construct + '\n'
            where_fields += f"OPTIONAL {{ {construct} }} \n"

        self.query_data = dict(construct_fields=construct_fields,
                               where_fields=where_fields)
        self.subqueries = []
        for field, subfields in ADDITIONAL_CONSTRUCTS.items():
            where_fields = f"?dataservice_uri {field} ?field_uri ."
            construct_fields = ''
            for sub in subfields:
                construct_sub = f" ?field_uri {sub} ?field_{sub.replace(':', '_').replace('?', '')} ."
                construct_fields += construct_sub + '\n'
                where_fields += f"OPTIONAL {{ {construct_sub} }} .\n"
            query = dict(construct_fields=construct_fields,
                         where_fields=where_fields)
            self.subqueries.append(query)

class DataSetForServiceDownloader(DatasetDownloader):

    def __init__(self):
        super().__init__()
        self.construct = CONSTRUCT_DATASET_FOR_SERVICE


if '__name__' == '__main__':
    d = DataServiceDownloader()
    g = d.run(['https://geobasis-bb.de#dcat_DataService_37b46011-1e9e-4952-9d32-4a24fe54bb15'], 'text/turtle')
    g.serialize('dataservice.ttl')
    d = DatasetDownloader()
    g = d.run(['https://backend.datenadler.de/harvester-intern/mwfk/metadaten/dcat_catalog/katalog-open-data-des-ministeriums-fuer-wissenschaft-forschung-und-kultur-des-landes-brandenburg'], 'text/turtle')
    g.serialize('dataset_test.ttl')
    d = DataSetForServiceDownloader()
    g = d.run(['https://geobasis-bb.de#dcat_DataService_37b46011-1e9e-4952-9d32-4a24fe54bb15'], 'text/turtle')
    g.serialize('datset_dataservice.ttl')