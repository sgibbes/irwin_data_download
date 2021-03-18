import requests
import json
import csv
from urllib.parse import urlencode
from tabulate import tabulate
import time


def get_time(epoch):
    s, ms = divmod(epoch, 1000)
    return '%s.%03d' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s)), ms)


def create_table(username, password, irwinid, reportToDateTime):
    token = get_token_inputs(username, password)

    endpoint_url = 'https://irwin.doi.gov/arcgis/rest/services/Resource/FeatureServer/2/query?includeResource=True'

    where = "IrwinID = '{}' AND (FulfillmentStatus = 'Closed' or FulfillmentStatus = 'Filled') AND " \
            "((DemobETD < '{}' OR DemobETD is null) AND DemobETA < '{}')".format(irwinid,
                                                                                 reportToDateTime, reportToDateTime)

    matchingCRs = query_api(endpoint_url, token, where)

    capabilityRequest = matchingCRs['features'][0]['attributes']
    resource = (matchingCRs['features'][0]['capability']['resource'])
    capability = (matchingCRs['features'][0]['capability']['attributes'])
    iriwnCTID = capability['IrwinCTID']
    # get capability type:
    capTypewhere = "IrwinCTID = '{}'".format(iriwnCTID)
    captypeRecord = query_api('https://irwin.doi.gov/arcgis/rest/services/Resource/FeatureServer/3/query?',
                                   token, capTypewhere)

    headers = ['Resource Kind', 'DemobETA', 'DemobETD', 'Operational Status',
               'Fulfillment Status']
    tableRows = []
    for cr in matchingCRs['features']:
        requestList = []

        capabilityRequest = cr['attributes']
        irwinID = capabilityRequest['IrwinID']
        resource = cr['capability']['resource']['attributes']
        demobETA = get_time(capabilityRequest['DemobETA'])

        demobETD = get_time(capabilityRequest['DemobETD'])
        fulfillmentStatus = capabilityRequest['FulfillmentStatus']
        operationalName = resource['OperationalName']
        operationalStatus = resource['OperationalStatus']
        resourceKind = resource['ResourceKind']
        capability = cr['capability']['attributes']
        iriwnCTID = capability['IrwinCTID']

        requestList.extend(
            [resourceKind, demobETA, demobETD, operationalStatus, fulfillmentStatus])

        tableRows.append(requestList)

    return tabulate(tableRows, headers=headers, tablefmt='orgtbl')


def get_creds():
    with open('creds.json') as f:
        usr_data = json.load(f)
    return usr_data['username'], usr_data['password']


def get_token_inputs(username, password):

    data = {'f': 'json',
              'username': username,
              'password': password
              }

    response = requests.post('https://irwinoat.doi.gov/arcgis/tokens/generateToken?', data)

    response = response.json()

    return response['token']


def get_token():
    with open('creds.json') as f:
        usr_data = json.load(f)

    data = {'f': 'json',
              'username': usr_data['username'],
              'password': usr_data['password'],
              }

    response = requests.post('https://irwinoat.doi.gov/arcgis/tokens/generateToken?', data)

    response = response.json()

    return response['token']


def query_api(url, token, where):

    payload = urlencode({'f': 'json',
                         'token': token,
                         'where': where,
                         'outFields': '*'})

    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Referer': 'local', "x-ig-capabilities": "36oD"}

    r = requests.post(url=url, data=payload, headers=headers)

    try:
        response = r.content.decode('utf-8')
    except UnicodeDecodeError:
        response = r.content.decode('GB18030')

    response = response.replace(r'\n', ' ').replace(r'\t', ' ').replace(r'\r', ' ')

    x = json.loads(response)

    return x