import os

import tornado.web
import tornado.ioloop

from sensordata import DataStorage
from config import Config
from utils import splitlist


# noinspection PyAbstractClass
class SensorDataHandler(tornado.web.RequestHandler):
    async def post(self):
        content: list = self.request.body.decode().split('\n')
        DataStorage.add_data(content)


# noinspection PyAbstractClass
class LastHandler(tornado.web.RequestHandler):
    async def get(self):
        data = DataStorage.get_data(-conf.storage_size)  # получаем N последних показаний
        co2_avg_list = []
        co2_min_max_list = []
        for interval in splitlist(data, 6 * 15):  # интервалы по 15 минут
            interval_co2 = [int(i.co2) for i in interval]

            co2_avg_list.append([int(interval[len(interval) // 2].time) + (60 * 60 * conf.timezone), sum(interval_co2) // len(interval_co2)])
            co2_min_max_list.append([int(interval[len(interval) // 2].time) + (60 * 60 * conf.timezone), min(interval_co2), max(interval_co2)])

        await self.render("index.html", title="My title",
                          data=data[-1],
                          old_data=data[-1:-21:-1],  # данные для таблички
                          averages=co2_avg_list,
                          ranges=co2_min_max_list
                          )


def run():
    DataStorage.init(conf.storage_size)  # TODO check init

    app = tornado.web.Application(
        handlers=[
            (r"/sensors", SensorDataHandler),
            (r"/", LastHandler),
        ],
        static_path=os.path.join(os.path.dirname(__file__), "html", "static"),
        template_path=os.path.join(os.path.dirname(__file__), "html", "templates"))
    app.listen(conf.listen_port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    conf = Config()
    run()
