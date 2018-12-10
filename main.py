#!/usr/bin/env python

import os
import psycopg2
import momoko
import json
from tornado import gen, web, auth, escape
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.httpclient import AsyncHTTPClient
import tornado.options as Options

from classification import classification

Options.define("port", default=5000, help="run on the given port", type=int)

class HomeHandler(web.RequestHandler):
    def get(self):
        self.write('Cyber Bullying Detection System!')
        self.finish()

DATABASE_URL = os.getenv('DATABASE_URL', 'dbname=toei_test host=localhost port=5432')
# FACEBOOK_APP_ID = os.getenv('FACEBOOK_APP_ID')
# FACEBOOK_APP_SECRET = os.getenv('FACEBOOK_APP_SECRET')

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

    # id integer NOT NULL,
    # user_id integer NOT NULL,
    # user_name character varying,
    # post_time timestamp without time zone,
    # is_bullying boolean DEFAULT false,
    # bullying_words character varying[] DEFAULT array[]::varchar[]

POST_CREATE_QUERY = ("INSERT INTO posts (user_id, user_facebook_id, user_name, user_pic, post_time, post_body, is_bullying, bullying_words) "
    "VALUES (%s, %s, %s, %s, TO_TIMESTAMP(%s), %s, %s, %s)")

class PostHandler(web.RequestHandler):
    def initialize(self, database):
        self.database = database

    async def find_user_by_facebook_id(self, facebook_id):
        cursor = await self.database.execute(
            "SELECT id, facebook_id, user_name, user_pic FROM users WHERE facebook_id = '{}'".format(facebook_id))
        user = cursor.fetchone()
        return ({
            'id': user[0],
            'facebook_id': user[1],
            'user_name': user[2],
            'user_pic': user[3]
        })

    async def ban_user(self, user_id):
        await self.database.execute("UPDATE users SET banned = True WHERE id="+str(user_id))

    async def fetch_total_bulling_post_of_user(self, user_id):
        cursor = await self.database.execute(
            "SELECT COUNT(id) FROM posts WHERE is_bullying = True AND user_id = '{}'".format(user_id))
        return cursor.fetchone()[0]

    async def create_post(self, user_id, user_facebook_id, user_name, user_pic, post_time, post_body, is_bullying, bullying_words):
        await self.database.execute(
            POST_CREATE_QUERY, 
            (user_id, user_facebook_id, user_name, user_pic, post_time, post_body, is_bullying, bullying_words))

    async def post(self):
        try:
            body = escape.json_decode(self.request.body)

            user_facebook_id = body['loginId']
            post_body = body['post']
            post_time = body['timestamp']

            user = await self.find_user_by_facebook_id(user_facebook_id)
            user_id = user['id']
            user_name = user['user_name']
            user_pic = user['user_pic']

            total_bullying_post_count = await self.fetch_total_bulling_post_of_user(user_id)

            if total_bullying_post_count >= 3:
                self.write({'success': False, 'total_bullying_post_count': total_bullying_post_count})
            else:
                # TODO: TOEI ADD CLASSIFACTION
                bullying_words = classification(post_body)
                is_bullying = len(bullying_words) != 0

                # Ban user
                if is_bullying and total_bullying_post_count == 2:
                    await self.ban_user(user_id)

                await self.create_post(
                    user_id, user_facebook_id, user_name, user_pic, post_time, post_body, is_bullying, bullying_words)

                self.write({'success': True, 'total_bullying_post_count': total_bullying_post_count})

        except (psycopg2.Warning, psycopg2.Error) as e:
            self.set_status(400)
            self.write({'success': False})
            print(str(e))

        self.finish()


class FeedHandler(web.RequestHandler):
    def initialize(self, database):
        self.database = database

    async def fetch_all_posts(self):
        cursor = await self.database.execute(
            "SELECT id, user_facebook_id, user_name, user_pic, post_body, is_bullying, bullying_words, post_time FROM posts")
        allposts = []
        # return cursor.fetchall()
        for post in cursor.fetchall():
            allposts.append({
                'id': post[0],
                'loginId': post[1],
                'username': post[2],
                'userpic': post[3],
                'post': post[4],
                'isBully': post[5],
                'bullyWords': post[6],
                'postedTime': post[7].strftime('%-I:%M %p'),
                })
        return allposts;
        
    async def get(self):
        try:
           allposts = await self.fetch_all_posts();
           # self.write(json.dump(allposts))
           self.write({'posts': allposts})
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
        (r'/post', PostHandler, dict(database=database)),
        (r'/feed', FeedHandler, dict(database=database)),
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