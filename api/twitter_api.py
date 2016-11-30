#! /usr/bin/env python

import requests
import requests_oauthlib


class TwitterAPI:

    def __init__(self, credentials):
        self.__credentials = credentials

    def search_tweets(self, username):
        url = "https://api.twitter.com/1.1/search/tweets.json"
        params = {"q": username}
        auth = requests_oauthlib.OAuth1(*self.__credentials)
        request = requests.get(url, params=params, auth=auth)
        return request.json()