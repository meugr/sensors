import tornado.web
import tornado.ioloop
import time

from typing import List
from collections import deque
from itertools import islice

from config import Config

config = Config()


class Database:
    """
    Класс для работы с базой измерений.
    Перенести сюда логику работы с csv, наружу прокинуть интерфейсы
    """

    @classmethod
    def readlines(cls, size) -> List[str]:
        with open(config.csv_file) as f:
            return f.readlines()[-size:]

    @classmethod
    def writelines(cls, lines: List[str]):
        with open(config.csv_file, 'a') as f:
            f.writelines(map(lambda line: line + '\n', lines))


class DataStorage:
    """
    При ините сервера загружать сюда В инфу за последний месяц (интервал в конфиге) из базы.
    При добавлении новых данных удалять отсюда старые. Хранить данные, средние за 5-10-ти минутные интервалы.

    """

    _storage: deque

    @classmethod
    def init(cls):
        cls._storage: deque = deque([], maxlen=config.storage_size)

        for data in Database.readlines(config.storage_size):
            cls._storage.append(SensorsData(data))

    @classmethod
    def add_data(cls, data: str):
        """
        Пишем в базу и добавляем в DataStorage
        :return:
        """
        data = f'{int(time.time())};{data}'
        cls._storage.append(SensorsData(data))
        Database.writelines([data])

    @classmethod
    def get_data(cls, start=None, end=None) -> List['SensorsData']:
        """
        Возвращаем данные в интервале [start:end]
        Последнее значение - get_data(-1)
        :return:
        """
        return list(islice(cls._storage, start, end))


class SensorsData:
    def __init__(self, payload: str):
        self.time, self.co2, self.temp, self.hum, self.press = payload.split(";")


# noinspection PyAbstractClass
class SensorDataHandler(tornado.web.RequestHandler):
    async def post(self):
        content = self.request.body.decode()
        DataStorage.add_data(content)


# noinspection PyAbstractClass
class LastHandler(tornado.web.RequestHandler):
    async def get(self):
        data = DataStorage.get_data(-1)[0]
        self.write("<H1>Последние показания:</H1>")
        self.write(f"CO2: {data.co2}\n")
        self.write(f"°C: {data.temp}\n")
        self.write(f"Влажность: {data.hum}\n")
        self.write(f"Давление: {data.press}\n")


def run():
    DataStorage.init()  # TODO check init

    application = tornado.web.Application([
        (r"/session", SensorDataHandler),
        (r"/", LastHandler),
    ])
    application.listen(config.listen_port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run()
