#! /usr/bin/usr python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta


class TwitterPost:

    def __init__(self, data):
        self.date = datetime.strptime(data["created_at"],
                                      "%a %b %d %H:%M:%S +0000 %Y")
                                        + timedelta(hours=1)
        self.since_id = data["id_str"]
        self.text = data["text"]
        self.username = data["user"]["screen_name"]
        self.name = data["user"]["name"]
        self.location = data["user"]["location"]
