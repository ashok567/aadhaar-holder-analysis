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

class InsightsHandler(RequestHandler):
    def post(self):
        self.set_header("Content-Type", "text/plain")
        state = self.get_body_argument("state")
        res = data.get_insights(state)
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
        (r'/insight', InsightsHandler),
        (r'/(.*)', tornado.web.StaticFileHandler, {"path": ""}),

    ],**settings)


if __name__ == '__main__':
    print("Server is running at 9000")
    app = make_app()
    app.listen(9000)
    tornado.ioloop.IOLoop.current().start()