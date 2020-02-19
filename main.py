from schemafy import Schema
import time
import threading


class TF2:

    """
    :param {String} api_key: Api key for SteamWebApi https://steamcommunity.com/dev/apikey
    :param {Boolean} update: True if you want automatic updates in the background, False if not
    :param {Int} update_interval: How many seconds to wait between updates
    """
    def __init__(self, api_key=None, update=True, update_interval=3600):
        self.api_key = api_key if api_key is not None else None
        self.update = update
        self.update_interval = update_interval
        self.schema = None
        self.current_time = None
        self.ready = self.get_schema()

        if self.update is True:
            print(
                'Starting autoupdate in the background, '
                'the schema will update each: {} seconds'.format(self.update_interval)
            )
            thread = threading.Thread(target=self.run)
            thread.daemon = True
            thread.start()

    """
        Runs updates in the background
    """

    def run(self):
        while True:
            self.current_time = time.time()
            if self.current_time - self.schema.time >= self.update_interval:
                print('Updating Schema')
                self.get_schema(self.current_time)
            time.sleep(self.update_interval)

    def set_schema(self, data=None):
        if not isinstance(data, dict):
            raise ValueError('Schema is not a dictionary')
        else:
            self.schema = Schema(data)

    """
        Gets schema from steam web api
    """
    def get_schema(self, call_time=None):
        if self.api_key is None:
            raise Exception('Api key not defined')
        raw = {}
        if call_time is not None:
            raw['time'] = call_time
        overview = Schema.get_overview(self.api_key)
        items = Schema.get_items(self.api_key)
        items_game = Schema.get_items_game(self.api_key)
        raw['raw'] = {
            'schema': {
                'overview': overview,
                'items': items
            },
            'items_game': items_game['items_game']
        }
        self.set_schema(raw)

