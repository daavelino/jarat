import requests
import json

from config.config import ACCESS_TOKEN

def connect(method, url, data):
    result = None

    s = requests.Session()
    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }

    try:
        r = requests.request(method, url, headers=header, params=data)
    except:
        print(f'Unable to connect to {url}. Exiting')
        return None

    result = json.loads(r.content)

    return result

def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def stringify_list(selected):
    """
    Return a string with all selected OTIs
    passed via otis, for the iql filter.
    """
    result = '('
    for i in selected:
        result = result + i + ','
    result = result[:-1]
    result = result + ')'

    return result
