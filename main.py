#!/usr/bin/env python

import os
import psycopg2
import momoko
from tornado import gen, web, auth, escape
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.httpclient import AsyncHTTPClient
import tornado.options as Options

Options.define("port", default=5000, help="run on the given port", type=int)

class HomeHandler(web.RequestHandler):
    def get(self):
        self.write('Cyber Bullying Detection System!')
        self.finish()

DATABASE_URL = os.getenv('DATABASE_URL', 'dbname=toei_test host=localhost port=5432')
FACEBOOK_APP_ID = os.getenv('FACEBOOK_APP_ID')
FACEBOOK_APP_SECRET = os.getenv('FACEBOOK_APP_SECRET')

USER_CREATE_QUERY = ("INSERT INTO users (facebook_id, user_name, user_pic, access_token, banned) "
    "VALUES ('{facebook_id}', '{user_name}', '{user_pic}', '{access_token}', '{banned}')")


class LoginHandler(web.RequestHandler, auth.FacebookGraphMixin):
    def initialize(self, database):
        self.database = database

    async def create_user(self, user):
        return await self.database.execute(
            USER_CREATE_QUERY.format(
                facebook_id=user['facebook_id'],
                user_name=user['user_name'],
                user_pic=user['user_pic'],
                access_token=user['access_token'],
                banned=user['banned'],
            ))
        
    async def find_user_by_facebook_id(self, facebook_id):
        cursor = await self.database.execute("SELECT * FROM users WHERE facebook_id = '{}'".format(facebook_id))
        return cursor.fetchone()

    async def fetch_facebook_user(self, user_access_token):
        print('Call facebook')
        response = await AsyncHTTPClient().fetch('https://graph.facebook.com'
            '/me?fields=id,name,picture&access_token={}'.format(user_access_token))
        return escape.json_decode(response.body)

    async def post(self):
        try:
            body = escape.json_decode(self.request.body)
            facebook_id = body['facebook_id']
            user_access_token = body['access_token']

            if not facebook_id or not user_access_token:
                self.set_status(400)

            user = await self.find_user_by_facebook_id(facebook_id)

            if not user:
                fb_user = await self.fetch_facebook_user(user_access_token)
                if not fb_user:
                    self.set_status(400)
                    self.write('Invalid Request')
                else:
                    user = await self.create_user({
                        'facebook_id': facebook_id,
                        'user_name': fb_user['name'],
                        'user_pic': fb_user['picture']['data']['url'],
                        'access_token': user_access_token,
                        'banned': False,
                    })
            else:
                self.write({'success': True})
        except (psycopg2.Warning, psycopg2.Error) as e:
            self.set_status(400)
            self.write({'success': False})
            print(str(e))

        self.finish()


if __name__ == '__main__':
    Options.parse_command_line()
    ioloop = IOLoop.instance()

    database = momoko.Pool(
        dsn=DATABASE_URL,
        size=1,
        ioloop=ioloop,
    )
    application = web.Application([
        (r'/', HomeHandler),
        (r'/login', LoginHandler, dict(database=database)),
        (r'/register', LoginHandler, dict(database=database)),
    ], debug=True)


    application.db = database
    # this is a one way to run ioloop in sync
    future = database.connect()
    ioloop.add_future(future, lambda f: ioloop.stop())
    ioloop.start()
    future.result()  # raises exception on connection error

    http_server = HTTPServer(application)
    http_server.listen(Options.options.port)
    ioloop.start()