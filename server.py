import tornado.web
import tornado.ioloop
import time

from config import Config

config = Config()
last = ""


# noinspection PyAbstractClass
class SensorDataHandler(tornado.web.RequestHandler):
    async def post(self):
        content = self.request.body.decode()
        last = content
        with open(config.csv_file, 'a') as f:
            f.write(f'{int(time.time())};{content}\n')


# noinspection PyAbstractClass
class LastHandler(tornado.web.RequestHandler):
    async def get(self):
        self.write("<H1>Последние показания:</H1>")
        if last:
            self.write(last)
        else:
            with open(config.csv_file) as f:
                self.write(f.readlines()[-1])


def run():
    application = tornado.web.Application([
        (r"/session", SensorDataHandler),
        (r"/now", LastHandler),
    ])
    application.listen(config.listen_port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run()
