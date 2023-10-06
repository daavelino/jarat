"""
Retrieves data from any Jira Insight Object Schema parse it in a key/value
json format.


Please refer to:
https://developer.atlassian.com/cloud/assets/rest/api-group-iql/#api-iql-objects-get
for information on how to fetch data from Jira REST api.
"""

import sys
import copy

from lib.menu import multiple_selection
from lib.handle import connect, write_json, stringify_list
from lib.data_parser import parse_data

from config.config import SERVER, ROOT_OBJECT_SCHEME, ATTRIBUTE_DEEP, RESULTS_PER_PAGE

def parse_input():
    result = dict()

    msg = f'Usage: python {sys.argv[0]} -o <output_file> <-m|-s otis>.\n'
    msg = msg + '    -o: output file (.json) to save fetched data.\n'
    msg = msg + '    -m: interactive menu.\n'
    msg = msg + '    -s: pass the specific OTIs to fetch, ex: -s "2, 56, 9"\n'
    msg = msg + '    -iql: pass a specific iql search."\n'
    msg = msg + '    -r: raw output from the API.\n'
    msg = msg + '    -h: print this message.\n'
    msg = msg + 'Exiting.\n'

    if '-h' in sys.argv:
        print(msg)
        sys.exit(1)

    if '-m' in sys.argv:
        result['interactive'] = True
    else:
        result['interactive'] = False

    if '-o' in sys.argv:
        idx = sys.argv.index('-o')
        result['output_file'] = sys.argv[idx + 1]
    else:
        print(msg)
        sys.exit(1)

    if '-r' in sys.argv:
        result['raw_output'] = True
    else:
        result['raw_output'] = False

    if '-iql' in sys.argv:
        idx = sys.argv.index('-iql')
        result['iql'] = sys.argv[idx + 1]
    else:
        result['iql'] = None

    if '-s' in sys.argv:
        idx = sys.argv.index('-s')
        selected = sys.argv[idx + 1]
        selected = selected.strip()
        result['selection'] = selected.split(',')
    else:
        result['selection'] = None

    if (result['selection'] is None) and (result['interactive']) is False:
        print('\nPlease pass an OTI list (-s) or use the interactive menu (-m).\n')
        print(msg)
        sys.exit(1)

    return result

def get_obj_schema(obj_id):
    """
    https://developer.atlassian.com/cloud/assets/rest/api-group-objectschema/#api-objectschema-list-get
    """
    result = dict()

    server = SERVER
    endpoint = '/rest/insight/1.0/objectschema/list'
    url = server + endpoint
    
    tmp = connect('GET', url, None)
    if not tmp:
        return None

    for i in tmp['objectschemas']:
        obj_name = i['name']
        obj_id = i['id']
        obj_key = i['objectSchemaKey']
        if obj_name not in result.keys():
            result[obj_name] = {
                'id': obj_id,
                'key': obj_key,
            }

    return result

def get_obj_types(obj_schema):
    """
    obj_schema from get_obj_schema()
    https://developer.atlassian.com/cloud/assets/rest/api-group-objectschema/#api-objectschema-id-objecttypes-get
    """
    result = copy.deepcopy(obj_schema)
    
    server = SERVER

    for i in result.keys():
        schema_id = result[i]['id']
        endpoint = f'/rest/insight/1.0/objectschema/{str(schema_id)}/objecttypes'
        url = server + endpoint
        r = connect('GET', url, None)

        obj_types = list()
        if r:
            for t in r:
                name = t['name']
                tid = t['id']
                obj_types.append({'name': name, 'id': tid})

        result[i]['object_types'] = obj_types
  
    return result

def get_data(selected, iql):
    result = None

    server = SERVER
    endpoint = '/rest/insight/1.0/iql/objects'
    url = server + endpoint
    query = {
        'iql': None,
        'resultPerPage': RESULTS_PER_PAGE,
        'includeAttributesDeep': ATTRIBUTE_DEEP,
        'includeTypeAttributes': True
    }
   
    if selected == ['ALL_ENTRIES_IN_JIRA_DATABASE']:
        del query['iql']
    elif iql is None:
        otis = stringify_list(selected)
        query['iql'] = f'objectTypeId IN {otis}'
    else:
        query['iql'] = iql

    result = connect('GET', url, query)
    
    return result

if __name__=='__main__':
    param = parse_input()
    interactive = param['interactive']
    output_file = param['output_file']
    selection = param['selection']
    raw_output = param['raw_output']
    iql = param['iql']

    if interactive:
        root_scheme = get_obj_schema(ROOT_OBJECT_SCHEME)
        obj_types = get_obj_types(root_scheme)
        selected = list()
        selection = multiple_selection(obj_types, selected)

    data = get_data(selection, iql)

    if not raw_output:
        data = parse_data(data)

    write_json(data, output_file)

