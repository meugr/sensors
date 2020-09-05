import time

from typing import List

from utils import Deque
from database import Database


class SensorsData:
    def __init__(self, payload: str):
        self.time, self.co2, self.temp, self.hum, self.press = payload.split(";")


class DataStorage:
    """
    При ините сервера загружать сюда В инфу за последний месяц (интервал в конфиге) из базы.
    При добавлении новых данных удалять отсюда старые. Хранить данные, средние за 5-10-ти минутные интервалы.

    """
    _storage: Deque

    @classmethod
    def init(cls, size):
        cls._storage: Deque = Deque([], maxlen=size)

        for data in Database.readlines(size):
            cls._storage.append(SensorsData(data))

    @classmethod
    def add_data(cls, data_list: list):
        """
        Пишем в базу и добавляем в DataStorage
        """
        to_db = []
        for data in data_list:
            data = f'{int(time.time())};{data}'
            cls._storage.append(SensorsData(data))
            to_db.append(data)
        Database.writelines(to_db)

    @classmethod
    def get_data(cls, start=None, end=None) -> List['SensorsData']:
        """
        Возвращаем данные в интервале [start:end]
        Последнее значение - get_data(-1)
        """
        return cls._storage.get()[start: end]  # TODO обрабатывать IndexError
