"""
Configuration parameters for get_jira_data.py
"""

SERVER = 'https://...'
ACCESS_TOKEN = None
ROOT_OBJECT_SCHEME=1
ATTRIBUTE_DEEP=1
RESULTS_PER_PAGE=200000 # If lower than 'totalFilterCounter' in the returned results, pagination applies.
