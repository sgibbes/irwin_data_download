import util
import json
from tabulate import tabulate
import sys
irwinid = '39F9112A-0232-4D3A-802A-EECA2D0579E7'
# reportFromDateTime = '1609511320000' # Friday, January 1, 2021 2:28:40 PM
reportToDateTime = '8/2/2020 17:13:32'

# get token
token = util.get_token()

# start querying capability request table
endpoint_url = 'https://irwin.doi.gov/arcgis/rest/services/Resource/FeatureServer/2/query?includeResource=True'

where = "IrwinID = '{}' AND (FulfillmentStatus = 'Closed' or FulfillmentStatus = 'Filled') AND " \
        "((DemobETD < '{}' OR DemobETD is null) AND DemobETA < '{}')".format(irwinid,
                                                                             reportToDateTime, reportToDateTime)


matchingCRs = util.query_api(endpoint_url, token, where)

capabilityRequest = matchingCRs['features'][0]['attributes']
resource = (matchingCRs['features'][0]['capability']['resource'])
capability = (matchingCRs['features'][0]['capability']['attributes'])
iriwnCTID = capability['IrwinCTID']
# get capability type:
capTypewhere = "IrwinCTID = '{}'".format(iriwnCTID)
captypeRecord = util.query_api('https://irwin.doi.gov/arcgis/rest/services/Resource/FeatureServer/3/query?',
                               token, capTypewhere)

headers = ['IrwinID', 'Operational Name', 'Resource Kind', 'DemobETA', 'DemobETD', 'Operational Status', 'Fulfillment Status']
tableRows = []
for cr in matchingCRs['features']:

    requestList = []

    capabilityRequest = cr['attributes']
    irwinID = capabilityRequest['IrwinID']
    resource = cr['capability']['resource']['attributes']
    demobETA = capabilityRequest['DemobETA']
    demobETD = capabilityRequest['DemobETD']
    fulfillmentStatus = capabilityRequest['FulfillmentStatus']
    operationalName = resource['OperationalName']
    operationalStatus = resource['OperationalStatus']
    resourceKind = resource['ResourceKind']
    capability = cr['capability']['attributes']
    iriwnCTID = capability['IrwinCTID']

    requestList.extend([irwinID, operationalName, resourceKind, demobETA, demobETD, operationalStatus, fulfillmentStatus])

    tableRows.append(requestList)

print(tabulate(tableRows, headers=headers, tablefmt='orgtbl'))


