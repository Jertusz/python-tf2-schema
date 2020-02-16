import requests


def api_request(sub_api, version, api_key=None):

    api = {
        'url': 'http://api.steampowered.com/',
        'interface': 'IEconItems_440',
        'sub_api': sub_api,
        'version': version,
        'key': api_key
    }

    result = requests.get(f'{api["url"]}{api["interface"]}/{api["sub_api"]}/{api["version"]}/?key={api["key"]}')
    code = result.status_code
    if code == 200:
        return result.json()
    else:
        print(f'Request failed with code: {code}, returned None')
        return
