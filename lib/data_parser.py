"""
data_parser.py

Parse the Jira API data fetched by get_jira_data.py.
"""

def parse_data(data):
    """
    Returns the attributes from an objectEntries field fetched from Jira API
    in a key/value format.
    data should come from get_jira_data.py output.
    """
    result = dict()

    for entry in data['objectEntries']:
        key = entry['objectKey'].strip()

        result[key] = dict()

        label = None
        if 'label' in entry.keys():
            label = entry['label'].strip()
        result[key]['Label'] = label

        entry_id = None
        if 'id' in entry.keys():
            entry_id = entry['id']
        result[key]['id'] = entry_id

        object_type = None
        if 'objectType' in entry.keys():
            if 'name' in entry['objectType']:
                object_type = entry['objectType']['name']
        result[key]['Object Type'] = object_type

        data = entry['attributes']
        for attr in data:
            if 'objectTypeAttribute' not in attr.keys():
                continue
            if 'objectAttributeValues' not in attr.keys():
                continue

            name = attr['objectTypeAttribute']['name']
            value_list = attr['objectAttributeValues']

            value = None
            for i in value_list:
                if 'displayValue' in i.keys():
                    value = i['displayValue']

            result[key].update({name: value})
            
    return result
