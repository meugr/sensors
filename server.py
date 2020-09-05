import tornado.web
import tornado.ioloop

from sensordata import DataStorage
from config import Config
from utils import splitlist


# noinspection PyAbstractClass
class SensorDataHandler(tornado.web.RequestHandler):
    async def post(self):
        content = self.request.body.decode()
        await DataStorage.add_data(content)


# noinspection PyAbstractClass
class LastHandler(tornado.web.RequestHandler):
    async def get(self):
        data = DataStorage.get_data()
        avg_list = []
        min_max_list = []
        for interval in splitlist(data, 10):
            interval_co2 = [int(i.co2) for i in interval]
            print(interval_co2)

            avg_list.append([interval[0].time, sum(interval_co2) // len(interval_co2)])
            min_max_list.append([interval[0].time, min(interval_co2), max(interval_co2)])

        print(avg_list)
        await self.render("html/index.html", title="My title",
                          data=data[0],
                          old_data=data[-1::-1],  # данные для графика
                          averages=avg_list,
                          ranges=min_max_list


                          )


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
