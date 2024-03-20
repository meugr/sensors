class Deque:
    def __init__(self, data: list, maxlen: int):
        # TODO если len(data) > maxlen давать ошибку или отрезать лишнее
        self._data: list = data
        self._limit: int = maxlen

    def get(self) -> list:
        return self._data

    def append(self, value):
        if len(self._data) >= self._limit:
        # TODO while len(self._data) >= self._limit:
            self._data.pop(0)
        self._data.append(value)


def splitlist(data: list, chunksize: int):
    for i in range(0, len(data), chunksize):
        yield data[i:i + chunksize]
