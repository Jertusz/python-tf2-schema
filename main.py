from schemafy import Schema
import time


class TF2:

    def __init__(self, options=None):
        self.api_key = options['api_key'] if options is not None else None
        self.update_time = options['update_time'] if options is not None else 24 * 60 * 1000

        self.ready = False
        self.schema = None

        self.get_schema()

    def set_schema(self, data=None, from_update=False):
        if not isinstance(data, dict) and not from_update:
            return
        if self.schema is not None:
            self.schema['raw'] = data['raw']
            self.schema['time'] = data['time'] if 'time' in data else time.time()
        else:
            self.schema = Schema(data)

    def get_schema(self):
        if self.api_key is None:
            raise Exception('Api key not defined')

        overview = Schema.get_overview(self.api_key)
        items = Schema.get_items(self.api_key)
        items_game = Schema.get_items_game(self.api_key)
        raw = {'raw': {
            'schema': {'overview': overview, 'items': items},
            'items_game': items_game
        }}

        self.set_schema(raw)

