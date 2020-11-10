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
        payload ={
            'last': data[-1],
            'old_data': data[-1:-21:-1],  # данные для таблички
            'co2_averages': list(),
            'co2_ranges': list(),
            'hum_averages': list(),
            'hum_ranges': list(),
            'temp_averages': list(),
            'temp_ranges': list()
        }

        for interval in splitlist(data, 6 * 15):  # интервалы по 15 минут
            interval_co2 = []
            interval_hum = []
            interval_temp = []
            for i in interval:
                interval_co2.append(i.co2)
                interval_hum.append(i.hum)
                interval_temp.append(i.temp)

            payload['co2_averages'].append([int(interval[len(interval) // 2].time) + (60 * 60 * conf.timezone), sum(interval_co2) // len(interval_co2)])
            payload['co2_ranges'].append([int(interval[len(interval) // 2].time) + (60 * 60 * conf.timezone), min(interval_co2), max(interval_co2)])

            payload['hum_averages'].append([int(interval[len(interval) // 2].time) + (60 * 60 * conf.timezone), f"{sum(interval_hum) / len(interval_hum):.2f}"])
            payload['hum_ranges'].append([int(interval[len(interval) // 2].time) + (60 * 60 * conf.timezone), min(interval_hum), max(interval_hum)])

            payload['temp_averages'].append([int(interval[len(interval) // 2].time) + (60 * 60 * conf.timezone), f"{sum(interval_temp) / len(interval_temp):.2f}"])
            payload['temp_ranges'].append([int(interval[len(interval) // 2].time) + (60 * 60 * conf.timezone), min(interval_temp), max(interval_temp)])


        await self.render("index.html", title="My title", **payload)


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
