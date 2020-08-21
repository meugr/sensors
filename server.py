import tornado.web
import tornado.ioloop
import time

from collections import deque

from config import Config

config = Config()


class Database:
    """
    Класс для работы с базой измерений.
    Перенести сюда логику работы с csv, наружу прокинуть интерфейсы
    """


class DataStorage:
    """
    При ините сервера загружать сюда В инфу за последний месяц (интервал в конфиге) из базы.
    При добавлении новых данных удалять отсюда старые. Хранить данные, средние за 5-10-ти минутные интервалы.

    """

    _storage: deque

    @classmethod
    def init(cls):
        with open(config.csv_file) as f:
            cls._storage: deque = deque([], maxlen=config.storage_size)

            for data in f.readlines()[-config.storage_size:]:
                data = data.rstrip("\n")
                cls._storage.append(SensorsData(data))

    @classmethod
    def add_data(cls, data: str):
        """
        Пишем в базу и добавляем в DataStorage
        :return:
        """
        data = f'{int(time.time())};{data}'
        cls._storage.append(SensorsData(data))
        with open(config.csv_file, 'a') as f:
            f.write(f'{data}\n')

    @classmethod
    def get_data(cls, start=None, end=None) -> 'SensorsData':
        """
        Возвращаем данные в интервале [start:end]
        Последнее значение - get_data(-1)
        :return:
        """
        return cls._storage[start:end]


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
        data = DataStorage.get_data(-1)
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
