import tornado.web
import tornado.ioloop

from sensordata import DataStorage
from config import Config


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
        self.write(f"CO2: {data.co2}<br>")
        self.write(f"°C: {data.temp}<br>")
        self.write(f"Влажность: {data.hum}<br>")
        self.write(f"Давление: {data.press}<br>")


def run():
    config = Config()
    DataStorage.init(config.storage_size)  # TODO check init

    application = tornado.web.Application([
        (r"/session", SensorDataHandler),
        (r"/", LastHandler),
    ])
    application.listen(config.listen_port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run()
