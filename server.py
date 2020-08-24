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
        data = DataStorage.get_data(-1)
        old_data = DataStorage.get_data(end=-1)
        await self.render("html/index.html", title="My title", data=data[0], old_data=old_data[::-1])


def run():
    config = Config()
    DataStorage.init(config.storage_size)  # TODO check init

    application = tornado.web.Application([
        (r"/sensors", SensorDataHandler),
        (r"/", LastHandler),
    ])
    application.listen(config.listen_port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run()
