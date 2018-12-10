#!/usr/bin/env python
import os
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import torndb
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')


CRATE_TABLE = """
CREATE TABLE IF NOT EXISTS posts (
    id integer NOT NULL,
    user_id character varying,
    user_name character varying,
    user_pic character varying,
    post_time timestamp without time zone,
    is_bullying boolean DEFAULT false,
    bullying_words character varying[] DEFAULT [],
);


CREATE SEQUENCE IF NOT EXISTS posts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE posts_id_seq OWNED BY posts.id;
"""

# import and define tornado-y things
from tornado.options import define
define("port", default=5000, help="run on the given port", type=int)


# application settings and handle mapping info
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/post", PostHandler)
            (r"/feed", FeedHandler)
        ]
        tornado.web.Application.__init__(self, handlers)

# the main page
class MainHandler(tornado.web.RequestHandler):
    def get(self, q):
        self.write("Hello, world")

'''
Submit API
{
  "loginId": "String",
  "username": "String",
  "post": "String",
  "timestamp": "Number"
}
'''

# post manager
class PostHandler(tornado.web.RequestHandler):
    # TODO: Toei
    def classifier(context):
        return []

    def checkBullingCount():

    def post(self):
        try:
            data = tornado.escape.json_decode(self.request.body)

            message = data["message"]
            parseCommandFrom(message)
        except Exception as e:
            print e.message
        self.write("This is post");

class FeedHandler(tornado.web.RequestHandler):
    def get(self, q):
        # TODO: get from database and return 
        # self.write("Hello, world");

# RAMMING SPEEEEEEED!
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)

    # start it up
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()