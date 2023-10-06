"""
parse_raw_data.py

Parse the Jira API data fetched by get_jira_data.py.
"""

import json
import sys

from pprint import pprint

from lib.handle import write_json
from lib.data_parser import parse_data


def parse_input():
    result = dict()

    msg = f"Usage: python {sys.argv[0]} -i <input file> -o [output file].\n"
    msg = msg + '    -i: input file (.json) from get_jira_data.py.\n'
    msg = msg + '    -o: output file (.json) to save parsed data.\n'
    msg = msg + 'Exiting.'

    if '-h' in sys.argv:
        print(msg)
        sys.exit(1)

    if '-i' in sys.argv:
        idx = sys.argv.index('-i')
        result['input_file'] = sys.argv[idx + 1]
    else:
        print(msg)
        sys.exit(1)

    if '-o' in sys.argv:
        idx = sys.argv.index('-o')
        result['output_file'] = sys.argv[idx + 1]
    else:
        result['output_file'] = None

    return result

def read_data(input_file):
    result = list()

    with open(input_file) as f:
        data = json.load(f)
        result = parse_data(data)

    return result

if __name__=='__main__':

    files = parse_input()
    input_file = files['input_file']
    output_file = files['output_file']

    result = read_data(input_file)

    if output_file:
        write_json(result, output_file)
    else:
        pprint(result)
        print(f'Total entries: {len(result)}')
