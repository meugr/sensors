import json


class Config:
    _CONFPATH = "config.json"
    _config = None

    listen_port: int
    csv_file: str
    storage_size: int

    def __init__(self):
        with open(self._CONFPATH) as file:
            self._config = json.load(file)

    def __getattr__(self, item):
        try:
            return getattr(self, '_config')[item]
        except KeyError as e:
            raise AttributeError(str(e))
