import requests

"""
    :param {String} sub_api: Name of Api part being called
    :param {String} version: Version of the api
    :param {String} api_key: Api Key from https://steamcommunity.com/dev/apikey
    :param {Int} input: Parameter to go through the whole list of item, required in /GetSchemaItems/
"""


def api_request(sub_api, version, api_key=None, input=None):

    api = {
        'url': 'http://api.steampowered.com/',
        'interface': 'IEconItems_440',
        'sub_api': sub_api,
        'version': version,
        'key': api_key,
    }
    if input is not None and input != 0:
        result = requests.get(
            f'{api["url"]}{api["interface"]}/{api["sub_api"]}/{api["version"]}/?key={api["key"]}&start={input}'
        )
    else:
        result = requests.get(
            f'{api["url"]}{api["interface"]}/{api["sub_api"]}/{api["version"]}/?key={api["key"]}'
        )
    code = result.status_code
    if code == 200:
        return result.json()
    else:
        print(f'Request failed with code: {code}, returned None')
        return
