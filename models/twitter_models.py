#! /usr/bin/usr python

import json


class TwitterUser():

    def __init__(self, data):
        self.created_at = data["created_at"]
        self.since_id = data["id_str"]
        self.text = data["text"]
        self.username = data["user"]["screen_name"]
        self.name = data["user"]["name"]
        self.location = data["user"]["location"]


class TwitterHashtag():

    def __init__(self, data):
        self.created_at = data["created_at"]
        self.since_id = data["id_str"]
        self.text = data["text"]
        self.hashtag = data["entities"]["hashtags"][0]["text"]
        self.username = data["user"]["screen_name"]
        self.name = data["user"]["name"]
        self.location = data["user"]["location"]