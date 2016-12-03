#! /usr/bin/usr python
# -*- coding: utf-8 -*-


class ReportMessage:

    def __init__(self, network=None, message_type=None, keyword=None, username=None, name=None, date=None, text=None):
        self.network = network
        self.message_type = message_type
        self.keyword = keyword
        self.username = username
        self.name = name
        self.date = date
        self.text = text

    def load_json(self,data):
        print data
        self.network = data["network"]
        self.message_type = data["message_type"]
        self.keyword = data["keyword"]
        self.username = data["username"]
        self.name = data["name"]
        self.date = data["date"]
        self.text = data["text"]
