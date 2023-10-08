# jarat
The Jira Assets Rest API tooling. Get data from the Atlassian's Assets Rest API in a convenient way.

## What jarat does?
For those who need extracting data from an [Atlassian Asset Inventory](https://www.atlassian.com/software/jira/service-management/product-guide/getting-started/asset-and-configuration-management#how-it-works) in an **elegant way**, jarat might be of great help.
Getting the exact data that you need from the [Atlassian's Assets REST API](https://confluence.atlassian.com/assetapps/assets-rest-api-1168847897.html) might be tricky and time consuming. 
The way Atlassian's API return the queried data might look very polluted and cumbersome at the very first times and some adjustments in the retrieved data might be necessary prior start real work on the data from an asset inventory.

jarat is a more convenient way of getting data from the Assets REST API by:
1. allowing the user to select an specific (or multiple) objects to query and
2. returning the data in a **way more clean** JSON format.

jarat also provides an interactive menu making data discovery and selection really straighforward.

## Usage:

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```
2. Provide the correct information in the `config/config.py` file. Please refer to the Atlassian's documentation on how to use a  [personal access token](https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html).

3. Check the help message for the allowed parameters:

```bash
python get_jira_data.py -h
```
4. Try
```bash
python get_jira_data.py -o output.json -m
```

## Comparing results
jarat can also fetch data exactly as the Assets REST API provides it. For a simple comparision, try to

1. Extract the data **exactly** as the API provides it by
```bash
python get_jira_data.py -o raw_output.json -m -r
```
2. Check the results
```bash
python -m json.tool raw_output.json | less
```
3. Let jarat **clean it for you**
```bash
python parse_raw_data.py -i raw_output.json -o output.json
```
4. Check the results
```bash
python -m json.tool output.json | less
```

## References:
- [Atlassian's API documentation: Get iql objects](https://developer.atlassian.com/cloud/assets/rest/api-group-iql/#api-iql-objects-get)
- [Atlassian's API documentation: Get objectschema list](https://developer.atlassian.com/cloud/assets/rest/api-group-objectschema/#api-objectschema-list-get)
- [Atlassian's API documentation: Get objectschema {id} objecttypes](https://developer.atlassian.com/cloud/assets/rest/api-group-objectschema/#api-objectschema-id-objecttypes-get)

