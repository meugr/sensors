from typing import List


class Deque:
    def __init__(self, data, maxlen):
        self._data: List = data
        self._limit: int = maxlen

    def get(self):
        return self._data

    def append(self, value):
        if len(self._data) >= self._limit:
            self._data.pop(0)
        self._data.append(value)
