#! /usr/bin/usr python
# -*- coding: utf-8 -*-

import json


class FacebookCredentials:

    def __init__(self, filename):
        self.filename = filename

    def get_credentials(self):
        json_data = self.__read_configuration_file()
        api_key = json_data["facebook"]["access_token"]
        return api_key

    def __read_configuration_file(self):
        file = open(self.filename, "r")
        data = json.load(file)
        file.close()
        return data
