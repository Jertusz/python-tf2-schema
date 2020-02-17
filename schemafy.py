import time
import requests
import vdf
import json
import os
from webapi import api_request


class Schema:

    def __init__(self, data=None):

        self.raw = data['raw'] if data is not None else None
        self.time = data['time'] if 'time' in data else time.time()

    def get_item_by_defindex(self, defindex):
        for item in self.raw['schema']['items']:
            if item['defindex'] == defindex:
                return item
        return

    @staticmethod
    def get_overview(api_key):
        sub_api = 'GetSchemaOverview'
        version = 'v0001'
        return api_request(sub_api, version, api_key)

    @staticmethod
    def get_items(api_key):
        return get_all_schema_items(api_key)

    @staticmethod
    def get_items_game(api_key=None, github=True):
        sub_api = 'GetSchemaUrl'
        version = 'v0001'
        if github is False and api_key is not None:
            url = api_request(sub_api, version, api_key)
            if url is not None:
                url = url['result']['items_game_url']
                request = requests.get(url)
                if request.status_code == 200:
                    items_game = vdf_to_dict(request.content)
                    return items_game
                else:
                    return 'Request failed with code {}'.format(request.status_code)

            elif github is False and api_key is None:
                print('Api key not provided, returning None')
                return
            else:
                return
        else:
            request = requests.get('https://raw.githubusercontent.com/SteamDatabase/GameTracking-TF2/master/tf/scripts/items/items_game.txt')
            if request.status_code == 200:
                items_game = vdf_to_dict(request.content)
                return items_game
            else:
                return 'Request failed with code {}'.format(request.status_code)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)


def get_all_schema_items(api_key):
    sub_api = 'GetSchemaItems'
    version = 'v0001'
    items = []
    next_start = 0
    while next_start is not None:
        result = api_request(sub_api, version, api_key, next_start)
        if 'next' in result['result']:
            next_start = result['result']['next']
        else:
            next_start = None
        items.extend(result['result']['items'])
    return items


def vdf_to_dict(data):

    open('tmp.txt', 'wb').write(data)
    data = vdf.load(open('tmp.txt'))
    os.remove('tmp.txt')

    return data


