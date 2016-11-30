#! /usr/bin/env python

import requests
import requests_oauthlib


class TwitterAPI:

    def __init__(self, credentials):
        self.__credentials = credentials

    def search_hashtag(self, hashtag, since_id=0):
        url = "https://api.twitter.com/1.1/search/tweets.json"
        params = {"q": hashtag, "result_type": "recent", "since_id": since_id}
        auth = requests_oauthlib.OAuth1(*self.__credentials)
        request = requests.get(url, params=params, auth=auth)
        return request.json()

    def search_tweets(self, username, since_id=0):
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        params = {"screen_name": username}
        if since_id > 0:
            params["since_id"] = since_id
        auth = requests_oauthlib.OAuth1(*self.__credentials)
        request = requests.get(url, params=params, auth=auth)
        return request.json()