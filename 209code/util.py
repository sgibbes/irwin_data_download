import requests
import json
import csv
from urllib.parse import urlencode


def get_creds():
    with open('creds.json') as f:
        usr_data = json.load(f)
    return usr_data['username'], usr_data['password']


def get_token():
    with open('creds.json') as f:
        usr_data = json.load(f)

    data = {'f': 'json',
              'username': usr_data['username'],
              'password': usr_data['password'],
              }

    response = requests.post('https://irwin.doi.gov/arcgis/tokens/generateToken?', data)

    response = response.json()

    return response['token']


def query_api(url, token, where):

    payload = urlencode({'f': 'json',
                         'token': token,
                         'where': where,
                         'outFields': '*'})

    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Referer': 'local', "x-ig-capabilities": "36oD"}

    r = requests.post(url=url, data=payload, headers=headers)

    print(r)
    try:
        response = r.content.decode('utf-8')
    except UnicodeDecodeError:
        response = r.content.decode('GB18030')

    response = response.replace(r'\n', ' ').replace(r'\t', ' ').replace(r'\r', ' ')

    x = json.loads(response)

    return x