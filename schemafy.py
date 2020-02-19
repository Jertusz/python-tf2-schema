import time
import requests
import vdf
import json
from webapi import api_request


class Schema:

    def __init__(self, data=None):

        self.raw = data['raw'] if data is not None else None
        self.time = data['time'] if 'time' in data else time.time()
        self.paint_kits = self.get_paint_kits()

    """
        Gets item by defindex or by item name
        Requires running main.TF2.get_schema first
    """

    def get_item_by_defindex(self, defindex):
        for item in self.raw['schema']['items']:
            if item['defindex'] == defindex:
                return item
        return

    def get_item_by_item_name(self, name):
        if name == 'Mann Co. Supply Crate Key':
            name = 'Decoder Ring'
        for item in self.raw['schema']['items']:
            if item['name'] == name:
                return item
        return

    """
            Gets attribute by defindex
            Requires running main.TF2.get_schema first
    """

    def get_attribute_by_defindex(self, defindex):
        attributes = self.raw['items_game']['attributes']
        for attribute in attributes:
            if attribute == str(defindex):
                row = {
                    defindex: attributes[attribute]
                }
                return row
        return

    """
                Gets quality by defindex or quality name
                Requires running main.TF2.get_schema first
    """

    def get_quality_by_id(self, id):
        qualities = self.raw['items_game']['qualities']
        for quality in qualities:
            if qualities[quality]['value'] == str(id):
                return quality
        return

    def get_quality_by_name(self, name):
        qualities = self.raw['items_game']['qualities']
        for quality in qualities:
            if quality == name:
                return qualities[quality]['value']
        return

    def get_effect_by_id(self, id):
        effects = self.raw['items_game']['attribute_controlled_attached_particles']
        for category in effects:
            for effect in effects[category]:
                if effect == str(id):
                    row = {
                        id: effects[category][effect]
                    }
                    return row
        return

    def get_effect_by_name(self, name):
        effects = self.raw['items_game']['attribute_controlled_attached_particles']
        for category in effects:
            for effect in effects[category]:
                if effects[category][effect]['system'] == name:
                    row = {
                        effect: effects[category][effect]
                    }
                    return row
        return

    def get_skin_by_id(self, id):
        for paint_kit in self.paint_kits:
            if paint_kit == str(id):
                return self.paint_kits[paint_kit]
        return

    def get_skin_by_name(self, name):
        for paint_kit in self.paint_kits:
            if self.paint_kits[paint_kit] == name:
                return self.paint_kits[paint_kit]
        return

    def get_name(self, item):
        schema_item = self.get_item_by_defindex(item['defindex'])
        if schema_item is None:
            print("Item does not exist")
            return

        validated_item = validate_item(item)

        name = ''

        if not validated_item['tradable']:
            name += 'Non-Tradable '
        if not validated_item['craftable']:
            name += 'Non-Craftable '
        if validated_item['quality2'] is not None:
            name += self.get_quality_by_id(validated_item['quality2']) + ' '
        if (validated_item['quality'] != 6 and validated_item['quality'] != 15 and validated_item['quality'] != 15
                or validated_item['quality'] == 5 and validated_item['effect'] is None
                or schema_item['item_quality'] == 5):
            name += self.get_quality_by_id(validated_item['quality']) + ' '
        if validated_item['festive'] is True:
            name += 'Festivized '
        if validated_item['effect'] is not None:
            name += self.get_effect_by_id(validated_item['effect']) + ' '
        if validated_item['killstreak'] is not None and validated_item['killstreak'] > 0:
            ks = ['Killstreak', 'Specialized Killstreak', 'Professional Killstreak']
            name += ks[validated_item['killstreak' - 1]] + ' '
        if validated_item['target'] is not None:
            target = self.get_item_by_defindex(validated_item['target'])
            name += target['name'] + ' '
        if validated_item['output_quality'] is not None and validated_item['output_quality'] != 6:
            name = self.get_quality_by_id(validated_item['output_quality']) + ' ' + name
        if validated_item['output'] is not None:
            output = self.get_item_by_defindex(validated_item['output'])
            name += output['name'] + ' '
        if validated_item['australium'] is True:
            name += 'Australium'
        if validated_item['paint_kit'] is not None:
            paint_kit = self.get_skin_by_id(validated_item['paint_kit'])
            name += paint_kit + ' '

        name += schema_item['name']

        if validated_item['wear'] is not None:
            wear = ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle Scarred']
            name += f'({wear[validated_item["wear"] - 1]})'
        if validated_item['crate_series'] is not None:
            name += ' #' + validated_item['crate_series']

        return name

    @staticmethod
    def get_overview(api_key):
        sub_api = 'GetSchemaOverview'
        version = 'v0001'
        return api_request(sub_api, version, api_key)

    @staticmethod
    def get_items(api_key):
        return get_all_schema_items(api_key)

    """
        Gets items_game.txt
        :param {Boolean} github: True grabs from github repo (3rd party), 
                                False grabs directly from SteamWebApi (Api_key required)
    """

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
                    items_game = vdf.loads(request.text)
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
                items_game = vdf.loads(request.text)
                return items_game
            else:
                return 'Request failed with code {}'.format(request.status_code)

    @staticmethod
    def get_paint_kits():
        request = requests.get('https://raw.githubusercontent.com/SteamDatabase/GameTracking-TF2/master/tf/resource/tf_proto_obj_defs_english.txt')
        protodefs = vdf.loads(request.text)
        protodefs = protodefs['lang']['Tokens']
        paint_kits = {}
        for protodef in protodefs:
            parts = protodef.split('_')
            category = parts[0]
            id = parts[1]
            if int(category) == 9:
                clean = protodefs[protodef].split(' ')
                if clean[0][:len(id)] == id:
                    clean = ''.join(clean[1:])
                    paint_kits[id] = clean
                else:
                    paint_kits[id] = protodefs[protodef]
        return paint_kits

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)


def validate_item(item):
    template = {
        'defindex': 0,
        'quality': 0,
        'craftable': True,
        'tradable': True,
        'killstreak': None,
        'australium': False,
        'effect': None,
        'festive': False,
        'paint_kit': None,
        'wear': None,
        'quality2': None,
        'target': None,
        'output': None,
        'output_quality': None,
        'crate_series': None
    }
    for attribute in template:
        if attribute not in item:
            item[attribute] = template[attribute]

    return item


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
