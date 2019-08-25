from tornado.web import RequestHandler, Application
import tornado.ioloop
import os.path
import data
import json


class MainHandler(RequestHandler):
    def get(self):
        self.render("index.html")

class DataHandler(RequestHandler):
    def get(self):
        res = data.read_data()
        self.write({'response': json.loads(res)})

settings = dict(
    template_path = os.path.join(os.path.dirname(__file__),'templates'),
    # static_path = os.path.join(os.path.dirname(__file__),'static'),
    debug=True
)


def make_app():
    return Application(
    [
        (r'/', MainHandler),
        (r'/data', DataHandler),
        (r'/(.*)', tornado.web.StaticFileHandler, {"path": ""}),

    ],**settings)


if __name__ == '__main__':
    print("Server is running at 9000")
    app = make_app()
    app.listen(9000)
    tornado.ioloop.IOLoop.current().start()