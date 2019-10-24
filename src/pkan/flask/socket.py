from functools import partial

import simplejson as sj
from flask import Flask
from flask_socketio import SocketIO, emit
from pkan.flask.log import logger
# Monkey patch to let socketio use simplejson
# Crucial!!!
from pkan.flask.namespaces import INIT_NS
from rdflib import Graph, URIRef
from rdflib.namespace import NamespaceManager
from socketio.packet import Packet

Packet.json = sj
sj.dumps = partial(sj.dumps, ignore_nan=True)

app = Flask(__name__)
socketio = SocketIO(app)


# DATA OBJECTS

@socketio.on('request_vocab')
def request_vocab(data=None):
    # todo: category, ordering, ...
    logger.info('request_vocab')
    params = data['params']
    namespace = data['namespace']
    transaction_id = data['transaction_id']
    logger.info(params)
    data = {}
    # icon can be None
    # query for vocab category
    # all german skos:Concept Titles
    # PREFIX dct: < http: // purl.org / dc / terms / >
    # PREFIX rdf: < http: // www.w3.org / 1999 / 02 / 22 - rdf - syntax - ns  # >
    # PREFIX skos: < http: // www.w3.org / 2004 / 02 / skos / core  # >
    # SELECT ?title
    # WHERE
    # {
    #   ?object dct: title ?title .
    #   ?object rdf: type skos:Concept .
    #   FILTER(lang(?title) = 'de')
    # }

    if params['vocab'] == 'category':
        data['vocab'] = [
            {'text': 'Value 1',
             'icon': 'Value 2', },
            {'text': 'Value 3',
             'icon': 'Value 4'},
            {'text': 'Value 5',
             'icon': 'Value 6'},
        ]
    else:
        data['vocab'] = [
            {'text': 'Value 1',
             'icon': None},
            {'text': 'Value 3',
             'icon': None},
            {'text': 'Value 5',
             'icon': None},
        ]
    data['transaction_id'] = transaction_id
    logger.info('request_vocab finished')
    emit(namespace, sj.dumps(data))


@socketio.on('request_search_results')
def request_search_results(data=None):
    # todo: ...
    logger.info('request_search_results')
    params = data['params']
    namespace = data['namespace']
    transaction_id = data['transaction_id']
    logger.info(params)
    data = {}
    data['results'] = [
        {
            'id': 'https://datenadler.de/kataloge/mik/dcat_catalog',
            'title': 'my-title',
            'description': 'my-description',
            'type': 'Ich bin der Type z.b. Dcat-Dataset'
        },
        {
            'id': 'https://datenadler.de/kataloge/mik/dcat_catalog',
            'title': 'my-title2',
            'description': 'my-description2',
            'type': 'Ich bin der Type z.b. Dcat-Dataset'
        }
    ]
    data['transaction_id'] = transaction_id
    logger.info('request_search_results finished')
    emit(namespace, sj.dumps(data))


@socketio.on('request_items_title_desc')
def request_items_title_desc(data=None):
    # todo: ...
    logger.info('request_items_title_desc')
    params = data['params']
    namespace = data['namespace']
    transaction_id = data['transaction_id']
    logger.info(params)
    data = {}
    data['title'] = params['id']
    data['description'] = 'Ich bin die Beschreibung'
    data['type'] = 'Ich bin der Type z.b. Dcat-Dataset'
    data['id'] = params['id']
    data['transaction_id'] = transaction_id
    logger.info('request_items_title_desc finished')
    emit(namespace, sj.dumps(data))


@socketio.on('request_label')
def request_label(data=None):
    # todo: ...
    logger.info('request label')
    params = data['params']
    namespace = data['namespace']
    transaction_id = data['transaction_id']
    logger.info(params)
    data = {}

    id = params['id']

    # testing
    namespace_manager = NamespaceManager(Graph())
    for prefix, ns in INIT_NS.items():
        namespace_manager.bind(prefix, ns)

    u = URIRef(id)

    namespace_manager.graph.parse('https://raw.githubusercontent.com/w3c/dxwg/gh-pages/dcat/rdf/dcat.rdf', format='application/rdf+xml')

    label_de = namespace_manager.graph.preferredLabel(u, lang='de', labelProperties=(
        URIRef('http://www.w3.org/2004/02/skos/core#prefLabel'),
        URIRef('http://www.w3.org/2000/01/rdf-schema#label'),
    ))

    label_en = namespace_manager.graph.preferredLabel(u, lang='en', labelProperties=(
        URIRef('http://www.w3.org/2004/02/skos/core#prefLabel'),
        URIRef('http://www.w3.org/2000/01/rdf-schema#label'),
    ))

    if label_de:
        label = label_de[0][1]
    elif label_en:
        label = label_en[0][1]
    else:
        label = id

    data['label'] = label
    data['id'] = id
    data['transaction_id'] = transaction_id
    logger.info('request label finished')
    emit(namespace, sj.dumps(data))


@socketio.on('request_items_detail')
def request_items_detail(data=None):
    # todo: ...
    logger.info('request_items_detail')
    params = data['params']
    namespace = data['namespace']
    transaction_id = data['transaction_id']
    logger.info(params)
    data = {}
    data['rdf_ttl'] = """@prefix adms: <http://www.w3.org/ns/adms#> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dcatde: <http://dcat-ap.de/def/dcatde/1_0> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> .
@prefix ns1: <http://dcat-ap.de/def/dcatde/1> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://datenadler.de/kataloge/mik/dcat_catalog> a dcat:Catalog ;
    dct:description "Land Brandenburg: Alle Datensätze des MIK. Auch für Govdata.de"@de ;
    dct:identifier "https://datenadler.de/kataloge/mik/dcat_catalog" ;
    dct:language "de" ;
    dct:license <http://dcat-ap.de/def/licenses/dl-zero-de/2.0> ;
    dct:publisher <https://datenadler.de/publishers/mik> ;
    dct:title "Gesamtkatalog Ministerium des Innern und für Kommunales (MIK)"@de ;
    adms:identifier "https://datenadler.de/kataloge/mik/dcat_catalog" ;
    dcat:dataset <https://datenadler.de/kataloge/mik/dcat_catalog/behoerdenverzeichnis-land-brandenburg>,
        <https://datenadler.de/kataloge/mik/dcat_catalog/kommunalverzeichnis-land-brandenburg> ;
    foaf:homepage "https://mik.brandenburg.de" .

<http://publications.europa.eu/resource/authority/data-theme/GOVE> a skos:Concept ;
    dct:identifier "http://publications.europa.eu/resource/authority/data-theme/GOVE" ;
    dct:title "Правителство и публичен сектор"@bul,
        "Vláda a veřejný sektor"@cs,
        "Regeringen og den offentlige sektor"@dan,
        "Regierung und öffentlicher Sektor"@de,
        "Κυβέρνηση και δημόσιος τομέας"@ell,
        "Government and public sector"@en,
        "Valitsus ja avalik sektor"@eth,
        "Valtioneuvosto ja julkinen sektori"@fin,
        "Gouvernement et secteur public"@fr,
        "Rialtas agus earnáil phoiblí"@gle,
        "Vlada i javni sektor"@hrv,
        "Kormányzat és közszféra"@hun,
        "Governo e settore pubblico"@ita,
        "Valdība un sabiedriskais sektors"@lav,
        "Vyriausybė ir viešasis sektorius"@lit,
        "Gvern u settur pubbliku"@mlt,
        "Overheid en publieke sector"@nld,
        "Forvaltning og offentlig sektor"@nor,
        "Rząd i sektor publiczny"@pl,
        "Governo e setor público"@por,
        "Guvern şi sector public"@ron,
        "Vláda a verejný sektor"@slk,
        "Vlada in javni sektor"@slv,
        "Gobierno y sector público"@spa,
        "Regeringen och den offentliga sektorn"@swe ;
    rdfs:isDefinedBy "http://publications.europa.eu/resource/authority/data-theme/GOVE" ;
    skos:inScheme "{http://publications.europa.eu/resource/authority/data-theme : http://www.w3.org/2004/02/skos/core#ConceptScheme}" ;
    adms:identifier "https://datenadler.de/concepts/GOVE" .

<http://publications.europa.eu/resource/authority/data-theme/REGI> a skos:Concept ;
    dct:identifier "http://publications.europa.eu/resource/authority/data-theme/REGI" ;
    dct:title "Региони и градове"@bul,
        "Regiony a města"@cs,
        "Regioner og byer"@dan,
        "Regionen und Städte"@de,
        "Περιφέρειες και πόλεις"@ell,
        "Regions and cities"@en,
        "Piirkonnad ja linnad"@eth,
        "Alueet ja kaupungit"@fin,
        "Régions et villes"@fr,
        "Réigiúin agus cathracha"@gle,
        "Regije i gradovi"@hrv,
        "Régiók és városok"@hun,
        "Regioni e città"@ita,
        "Reģioni un pilsētas"@lav,
        "Regionai ir miestai"@lit,
        "Reġjuni u bliet"@mlt,
        "Regio's en steden"@nld,
        "Regioner og byer"@nor,
        "Regiony i miasta"@pl,
        "Regiões e cidades"@por,
        "Regiuni şi orașe"@ron,
        "Regióny a mestá"@slk,
        "Regije in mesta"@slv,
        "Regiones y ciudades"@spa,
        "Regioner och städer"@swe ;
    rdfs:isDefinedBy "http://publications.europa.eu/resource/authority/data-theme/REGI" ;
    skos:inScheme "{http://publications.europa.eu/resource/authority/data-theme : http://www.w3.org/2004/02/skos/core#ConceptScheme}" ;
    adms:identifier "https://datenadler.de/concepts/REGI" .

<https://datenadler.de/kataloge/mik/dcat_catalog/behoerdenverzeichnis-land-brandenburg> a dcat:Dataset ;
    ns1:_0contributorID "MIK"@de ;
    ns1:_0geocodingText "Brandenburg"@de ;
    ns1:_0politicalGeocodingLevelURI "http://dcat-ap.de/def/politicalGeocoding/Level/state" ;
    ns1:_0politicalGeocodingURI "http://dcat-ap.de/def/politicalGeocoding/stateKey/12" ;
    dct:contributor "3ead3922cbde4098877ebc5ac6dc522f" ;
    dct:description "Dieses Verzeichnis gibt es als Webseite und im CSV-Format. Es beinhaltet Anschriften, Telefonnummern und E-Mail-Adressen von Anstalten des öffentlichen Rechts, Behörden der Landkreise und kreisfreien Städte, Fachhochschulen, Finanzämter, Handwerkskammern, Hochschulen und Universitäten, Industrie- und Handelskammern, Justizvollzugsanstalten, Körperschaften des öffentlichen Rechts, Landesämter, Landesbetriebe, Ministerien, Stiftungen des öffentlichen Rechts, Zweckverbände aber auch Gerichte und Staatsanwaltschaften. (Letzter Linktest: 21.06.2018)"@de ;
    dct:identifier "https://datenadler.de/kataloge/mik/dcat_catalog/behoerdenverzeichnis-land-brandenburg" ;
    dct:issued "2007-10-17" ;
    dct:modified "2018-06-21" ;
    dct:publisher <https://datenadler.de/publishers/mik> ;
    dct:title "Behördenverzeichnis Land Brandenburg"@de,
        "wyšnosć"@dsb ;
    adms:identifier "https://datenadler.de/kataloge/mik/dcat_catalog/behoerdenverzeichnis-land-brandenburg" ;
    adms:versionNotes "Linküberprüfung am 21.06.2018 eingearbeitet"@de ;
    dcat:distribution <https://datenadler.de/kataloge/mik/dcat_catalog/behoerdenverzeichnis-land-brandenburg/behoerdenverzeichnis-land-brandenburg.csv>,
        <https://datenadler.de/kataloge/mik/dcat_catalog/behoerdenverzeichnis-land-brandenburg/http-service-brandenburg-de-lis-list-php-page-behoerdenverzeichnis> ;
    dcat:keyword "Adresse",
        "Ansprechpartner",
        "Behörde" ;
    dcat:theme <http://publications.europa.eu/resource/authority/data-theme/GOVE> ;
    foaf:landingpage "http://service.brandenburg.de/" ;
    foaf:page "http://service.brandenburg.de/lis/list.php?page=behoerdenverzeichnis" .

<https://datenadler.de/kataloge/mik/dcat_catalog/behoerdenverzeichnis-land-brandenburg/behoerdenverzeichnis-land-brandenburg.csv> a dcat:Distribution ;
    dct:format "text/csv"@de ;
    dct:identifier "https://datenadler.de/kataloge/mik/dcat_catalog/behoerdenverzeichnis-land-brandenburg/behoerdenverzeichnis-land-brandenburg.csv" ;
    dct:license <http://dcat-ap.de/def/licenses/dl-zero-de/2.0> ;
    dct:title "Behördenverzeichnis Land Brandenburg .CSV"@de ;
    adms:identifier "https://datenadler.de/kataloge/mik/dcat_catalog/behoerdenverzeichnis-land-brandenburg/behoerdenverzeichnis-land-brandenburg.csv" ;
    dcat:downloadURL "http://service.brandenburg.de/sixcms/list.php?page=behoerdenvz_csv" .

<https://datenadler.de/kataloge/mik/dcat_catalog/behoerdenverzeichnis-land-brandenburg/http-service-brandenburg-de-lis-list-php-page-behoerdenverzeichnis> a dcat:Distribution ;
    dct:identifier "https://datenadler.de/kataloge/mik/dcat_catalog/behoerdenverzeichnis-land-brandenburg/http-service-brandenburg-de-lis-list-php-page-behoerdenverzeichnis" ;
    dct:license <http://dcat-ap.de/def/licenses/dl-zero-de/2.0> ;
    dct:title "Behördenverzeichnis als Webseite"@de ;
    adms:identifier "https://datenadler.de/kataloge/mik/dcat_catalog/behoerdenverzeichnis-land-brandenburg/http-service-brandenburg-de-lis-list-php-page-behoerdenverzeichnis" ;
    dcat:accessURL "http://service.brandenburg.de/lis/list.php?page=behoerdenverzeichnis" .

<https://datenadler.de/kataloge/mik/dcat_catalog/kommunalverzeichnis-land-brandenburg> a dcat:Dataset ;
    ns1:_0contributorID "MIK"@de ;
    dct:description "Hier finden Sie ein Verzeichnis der Landkreise, kreisfreien Städte, Ämter sowie der amtsangehörigen und amtsfreien Gemeinden und Städte als Webseite und zum Herunterladen. Die amtsangehörigen Gemeinden liegen in einer eigenen Datei vor."@de ;
    dct:identifier "https://datenadler.de/kataloge/mik/dcat_catalog/kommunalverzeichnis-land-brandenburg" ;
    dct:publisher <https://datenadler.de/publishers/mik> ;
    dct:title "Kommunalverzeichnis Land Brandenburg"@de ;
    adms:identifier "https://datenadler.de/kataloge/mik/dcat_catalog/kommunalverzeichnis-land-brandenburg" ;
    dcat:distribution <https://datenadler.de/kataloge/mik/dcat_catalog/kommunalverzeichnis-land-brandenburg/amtsangehoerige-gemeinden-csv>,
        <https://datenadler.de/kataloge/mik/dcat_catalog/kommunalverzeichnis-land-brandenburg/http-service-brandenburg-de-lis-list-php-page-kommunen_p>,
        <https://datenadler.de/kataloge/mik/dcat_catalog/kommunalverzeichnis-land-brandenburg/landkreise-kreisfreie-staedte-aemter-csv> ;
    dcat:theme <http://publications.europa.eu/resource/authority/data-theme/REGI> .

<https://datenadler.de/kataloge/mik/dcat_catalog/kommunalverzeichnis-land-brandenburg/amtsangehoerige-gemeinden-csv> a dcat:Distribution ;
    dct:identifier "https://datenadler.de/kataloge/mik/dcat_catalog/kommunalverzeichnis-land-brandenburg/amtsangehoerige-gemeinden-csv" ;
    dct:license <http://dcat-ap.de/def/licenses/dl-zero-de/2.0> ;
    dct:title "Amtsangehörige Gemeinden"@de ;
    adms:identifier "https://datenadler.de/kataloge/mik/dcat_catalog/kommunalverzeichnis-land-brandenburg/amtsangehoerige-gemeinden-csv" ;
    dcat:accessURL "https://datenadler.de/kataloge/dcat_catalog/kommunalverzeichnis-land-brandenburg/amtsangehoerige-gemeinden-csv" ;
    dcat:downloadURL "http://service.brandenburg.de/sixcms/list.php?page=kommunalvz_ag_csv" .

<https://datenadler.de/kataloge/mik/dcat_catalog/kommunalverzeichnis-land-brandenburg/http-service-brandenburg-de-lis-list-php-page-kommunen_p> a dcat:Distribution ;
    dct:format "text/html"@de ;
    dct:identifier "https://datenadler.de/kataloge/mik/dcat_catalog/kommunalverzeichnis-land-brandenburg/http-service-brandenburg-de-lis-list-php-page-kommunen_p" ;
    dct:license <http://dcat-ap.de/def/licenses/dl-zero-de/2.0> ;
    dct:title "Kommunalverzeichnis als Webseite"@de ;
    adms:identifier "https://datenadler.de/kataloge/mik/dcat_catalog/kommunalverzeichnis-land-brandenburg/http-service-brandenburg-de-lis-list-php-page-kommunen_p" ;
    dcat:accessURL "http://service.brandenburg.de/lis/list.php?page=kommunen_p" .

<https://datenadler.de/kataloge/mik/dcat_catalog/kommunalverzeichnis-land-brandenburg/landkreise-kreisfreie-staedte-aemter-csv> a dcat:Distribution ;
    dct:identifier "https://datenadler.de/kataloge/mik/dcat_catalog/kommunalverzeichnis-land-brandenburg/landkreise-kreisfreie-staedte-aemter-csv" ;
    dct:license <http://dcat-ap.de/def/licenses/dl-zero-de/2.0> ;
    dct:title "Kommunalverzeichnis als CSV"@de ;
    adms:identifier "https://datenadler.de/kataloge/mik/dcat_catalog/kommunalverzeichnis-land-brandenburg/landkreise-kreisfreie-staedte-aemter-csv" ;
    dcat:accessURL "https://datenadler.de/kataloge/dcat_catalog/kommunalverzeichnis-land-brandenburg/landkreise-kreisfreie-staedte-aemter-csv" ;
    dcat:downloadURL "http://service.brandenburg.de/sixcms/list.php?page=kommunalvz_csv" .

<https://datenadler.de/publishers/mik> a foaf:Agent ;
    dct:identifier "https://datenadler.de/publishers/mik" ;
    adms:identifier "https://datenadler.de/publishers/mik" ;
    foaf:name "Ministerium des Innern und für Kommunales (MIK) "@de .

<http://dcat-ap.de/def/licenses/dl-zero-de/2.0> a dct:LicenseDocument ;
    dct:description "Datenlizenz Deutschland – Zero – Version 2.0"@de ;
    dct:identifier "http://dcat-ap.de/def/licenses/dl-zero-de/2.0" ;
    dct:title "dl-zero-de/2.0"@de ;
    rdfs:isDefinedBy "http://dcat-ap.de/def/licenses/dl-zero-de/2.0" ;
    adms:identifier "https://datenadler.de/licenses/dl-zero-de-2-0" .
    """
    data['transaction_id'] = transaction_id
    logger.info('request_items_detail finished')
    emit(namespace, sj.dumps(data))

# @socketio.on('request_related_items')
# def request_related_items(data=None):
#     # todo: ...
#     logger.info('request_related_items')
#     params = data['params']
#     namespace = data['namespace']
#     transaction_id = data['transaction_id']
#     logger.info(params)
#     data = {}
#     data['results'] = [
#         {
#             'id': 'my-id',
#             'title': 'my-title',
#             'description': 'my-description'
#         },
#         {
#             'id': 'my-id2',
#             'title': 'my-title2',
#             'description': 'my-description2'
#         }
#     ]
#     data['transaction_id'] = transaction_id
#     logger.info('request_related_items finished')
#     emit(namespace, sj.dumps(data))
