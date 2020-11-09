from datetime import datetime as dt
from typing import List

from utils import Deque
from database import Database


class ReadDataException(Exception):
    pass


class SensorsData:
    def __init__(self, payload: str):
        try:
            time, co2, temp, hum, press = payload.strip('\n').split(";")
            self.time: int = int(time)
            self.co2: int = int(co2)
            self.temp: float = float(temp)
            self.hum: float = float(hum)
            self.press: float = float(press)
        except Exception as e:
            print(dt.isoformat(dt.now()), e)
            raise ReadDataException



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
            data = f'{int(dt.timestamp(dt.now()))};{data}'
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
