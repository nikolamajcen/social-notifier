#! /usr/bin/env python
# -*- coding: utf-8 -*-

import facebook
import json
from models.facebook_models import *
import pprint


class FacebookAPI():

    def __init__(self, access_token):
        self.access_token = access_token

    def search_posts(self, username):
        user_id = self.__fetch_user_details(username)
        if user_id is None:
            return None

        graph = facebook.GraphAPI(access_token=self.access_token)
        batched_requests = '[{"method": "GET", "relative_url": "' + user_id +  '/feed"}]'
        posts_data = graph.request("", post_args={"batch": batched_requests})[0]
        for key, value in posts_data.items():
            if key == "body":
                json_posts = json.loads(value)["data"]
                break

        posts = []
        for json_post in json_posts:
            post = FacebookStatus(json_post)
            posts.append(post)
        return posts

    def __fetch_user_details(self, username):
        graph = facebook.GraphAPI(access_token=self.access_token)
        batched_requests = '[ {"method": "GET", "relative_url":  "' + username + '"} ]'
        user_data = graph.request("", post_args={"batch": batched_requests})[0]
        for key, value in user_data.items():
            user = FacebookUser(json.loads(value))
            break
        return user.id