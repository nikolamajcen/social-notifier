#! /usr/bin/usr python
# -*- coding: utf-8 -*-

from datetime import datetime


class ReportMessage:

    def __init__(self, network=None, message_type=None,
                 keyword=None, username=None,
                 name=None, date=None, text=None):
        self.network = network
        self.message_type = message_type
        self.keyword = keyword
        self.username = username
        self.name = name
        if date:
            self.date = date.strftime("%H:%M:%S, %d.%m.%Y")
        else:
            self.date = date
        self.text = text

    def load_json(self,data):
        self.network = data["network"]
        self.message_type = data["message_type"]
        self.keyword = data["keyword"]
        self.username = data["username"]
        self.name = data["name"]
        self.date = data["date"]
        self.text = data["text"]

    def print_message(self):
        print "network=" + self.network + "; type="
            + self.message_type + "; keyword=" + self.keyword
        print "username=" + self.username + "; name=" + self.name
        print "date=" + self.date
        if self.text == "":
            print "message=<empty_message>"
        else:
            print "message=" + self.text.replace("\n", " ").replace("\r", "")
        print ""
