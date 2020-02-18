# python-tf2-schema


Get TF2 schema from SteamWebApi or github
Find items by defindex

## What is TF2 Schema

All item name, effects, qualities etc associated with unique numbers.

## Examples

```py
from main import TF2

# Grabs the Schema but doesnt auto update
a = TF2(api_key, update=False)

# Object format
a.schema.raw['raw'] = {
  'schema': {
    'overview': overview of schema
    'items': all items
    },
  'items_game': items_game.txt file
}
```

```py
from main import TF2

# functions
a = TF2()

# Find item record by defindex (5021 = Mann Co. Supply Crate Key)
result = a.schema.get_item_by_defindex(5021)

print(result)

{'name': 'Decoder Ring', 'defindex': 5021, 'item_class': 'tool', 'item_type_name': '#TF_T', 'item_name': '#TF_Tool_DecoderRing', 'item_description': '#TF_Tool_DecoderRing_Desc', 'proper_name': False, 'model_player': None, 'item_quality': 6, 'image_inventory': 'backpack/player/items/crafting/key', 'min_ilevel': 5, 'max_ilevel': 5, 'image_url': 'http://media.steampowered.com/apps/440/icons/key.be0a5e2cda3a039132c35b67319829d785e50352.png', 'image_url_large': 'http://media.steampowered.com/apps/440/icons/key_large.354829243e53d73a5a75323c88fc5689ecb19359.png', 'craft_class': 'tool', 'craft_material_type': 'tool', 'capabilities': {'can_gift_wrap': True, 'can_craft_mark': True, 'can_be_restored': True, 'strange_parts': True, 'can_card_upgrade': True, 'can_strangify': True, 'can_killstreakify': True, 'can_consume': True}, 'tool': {'type': 'decoder_ring', 'usage_capabilities': {'decodable': True}}, 'used_by_classes': [], 'attributes': [{'name': 'always tradable', 'class': 'always_tradable', 'value': 1}]}


# Get overview, grabs overview from API
overview = a.schema.get_overview(api_key)

# Get items, grabs items from API
items = a.schema.get_items(api_key)

# et items game, grabs items_game.txt, Github = True, grabs from github, Github = False, grabs from API
items_game = a.schema.get_items_game(api_key, github)

# To json returns whole object as json
dict = a.schema.to_json()




