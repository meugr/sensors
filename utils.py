class Deque:
    def __init__(self, data: list, maxlen: int):
        self._data: list = data
        self._limit: int = maxlen

    def get(self) -> list:
        return self._data

    def append(self, value):
        if len(self._data) >= self._limit:
            self._data.pop(0)
        self._data.append(value)
