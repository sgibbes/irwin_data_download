from util import *


def page_api(token, endpoint_url, where, offset):

    # use the REST api's resultOffset parameter to increment returned results by 2,000
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

    return feature_coll

