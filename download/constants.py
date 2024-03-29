CONSTRUCT_FIELDS_DATASET = [
    # 'dct:title',
    # 'dct:description',
    # 'dct:identifier',
    # 'dcat:keyword',
    # 'dct:issued',
    # 'dct:modified',
    # 'dct:language',
    # 'dcat:theme',
    # 'dcatde:contributorID',
    # 'dcat:endpointURL',
    '?p',
]

CONSTRUCT_FIELDS_DATASERVICE = [
                                 # 'dcat:servesDataset'
                               ] + CONSTRUCT_FIELDS_DATASET

ADDITIONAL_CONSTRUCTS = {
    # 'dcat:contactPoint': ['a', 'vcard:fn', 'vcard:hasEmail', 'vcard:email'],
    'dcat:contactPoint': ['?p'],
    # 'dct:publisher': ['a', 'foaf:name', 'foaf:homepage'],
    'dct:publisher': ['?p'],
    # 'dct:temporal': ['a', 'dcat:startDate', 'dcat:endDate'],
    'dct:temporal': ['?p'],
    # 'dcat:distribution': ['a', 'dct:license', 'dcat:accessURL', 'dcat:downloadURL', 'dct:language', 'dcat:mediaType',
    #                       'dct:format', 'dct:issued', 'dct:modified', 'dct:title', 'dct:description',]
    'dcat:distribution': ['?p'],
}

CONSTRUCT_DATASET = """
CONSTRUCT {{
    ?dataset_uri a dcat:Dataset .
    {construct_fields}
}}
WHERE
 {{
    VALUES ?dataset_uri {{ {values} }} .
    ?dataset_uri a dcat:Dataset .
    {where_fields}
 }}
"""

CONSTRUCT_DATASERVICE = """
CONSTRUCT {{
    ?dataservice_uri a dcat:DataService .
    {construct_fields}
}}
WHERE
 {{
    VALUES ?dataservice_uri {{ {values} }} .
    ?dataservice_uri a dcat:DataService .
    {where_fields}
 }}

"""

CONSTRUCT_DATASET_FOR_SERVICE = """
CONSTRUCT {{
    ?dataset_uri a dcat:Dataset .
    {construct_fields}
}}
WHERE
 {{
    VALUES ?dataservice_uri {{ {values} }} .
    ?dataservice_uri a dcat:DataService .
    ?dataservice_uri dcat:servesDataset ?dataset_uri .
    {where_fields}
 }}

"""
