import util
import page_api
from util import *

# enter credentials to generate a token
username = util.get_creds()[0]
password = util.get_creds()[1]

# get token
token = util.get_token(username, password)

# the IRWIN hosted feature service to query
endpoint_url = 'https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/IRWIN_Incidents/' \
               'FeatureServer/0/query?resultOffset={}'

# the where clause to narrow down results
where = "ModifiedOnDateTime > 1591707599000"

offset = 2000

# return all results in a list of dictionaries
feature_collection = page_api.page_api(token, endpoint_url, where, offset)

# start the result offset at 0, increase by "offset" each iteration
result_offset = 0

# create empty list to store each record json
feature_coll = {'features': []}

# set this to True to start the while loop
limit_exceeded = True

while limit_exceeded:

    # query api using result offset
    next_batch = query_api(endpoint_url.format(result_offset), token, where)

    # catch any errors returned by API
    if 'error' in next_batch.keys():
        print(next_batch['error'])

    # append results to feature collection
    feature_coll['features'].extend(next_batch['features'])

    # increment result offset to get the next n records
    result_offset += offset

    # set the value for limit_exceeded
    if 'exceededTransferLimit' in next_batch.keys():
        limit_exceeded = next_batch['exceededTransferLimit']

    else:
        limit_exceeded = False


# write the feature collection to a csv file
csv_file = 'data.csv'
util.response_to_dict(feature_collection, csv_file)
