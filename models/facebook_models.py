# ! /usr/bin/env python
# -*- coding: utf-8 -*-


class FacebookUser:

    def __init__(self, data):
        self.id = data["id"]
        self.username = data["username"]
        self.name = data["name"]
        city = data["location"]["city"]
        country = data["location"]["country"]
        state = data["location"]["state"]
        self.location = "{}, {}, {}".format(city, country, state)


class FacebookStatus:

    def __init__(self, data):
        self.status_type = data["status_type"]
        self.updated_time = data["updated_time"]

        if "message" in data:
            self.message = data["message"].strip()
        else:
            self.message = ""

        if "link" in data:
            self.link = data["link"]
        else:
            self.link = ""