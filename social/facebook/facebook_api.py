#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json

import facebook

from social.facebook.facebook_models import *


class FacebookAPI:

    def __init__(self, access_token):
        self.access_token = access_token

    def search_posts(self, username):
        user_id, user_username, user_name = self.__fetch_user_details(username)
        if user_id is None:
            print "Token is expired."
            return None

        print user_id
        graph = facebook.GraphAPI(access_token=self.access_token)
        batched_requests = '[{"method": "GET", "relative_url": "' + user_id + '/feed"}]'

        try:
            posts_data = graph.request("", post_args={"batch": batched_requests})
        except:
            print "Token has expired."

        for key, value in posts_data[0].items():
            if key == "body":
                json_posts = json.loads(value)["data"]
                break

        posts = []
        for json_post in json_posts:
            post = FacebookStatus(json_post)
            post.username = user_username
            post.name = user_name
            posts.append(post)
        return posts

    def __fetch_user_details(self, username):
        graph = facebook.GraphAPI(access_token=self.access_token)
        batched_requests = '[ {"method": "GET", "relative_url":  "' + username + '"} ]'
        try:
            user_data = graph.request("", post_args={"batch": batched_requests})
        except:
            return None

        if user_data is None:
            return None

        for key, value in user_data[0].items():
            user = FacebookUser(json.loads(value))
            break
        return user.id, user.username, user.name
