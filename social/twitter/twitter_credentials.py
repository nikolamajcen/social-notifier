#! /usr/bin/usr python
# -*- coding: utf-8 -*-

import json


class TwitterCredentials:

    def __init__(self, filename):
        self.filename = filename

    def get_credentials(self):
        json_data = self.__read_configuration_file()
        api_key = json_data["twitter"]["api_key"]
        api_key_secret = json_data["twitter"]["api_key_secret"]
        access_token = json_data["twitter"]["access_token"]
        access_token_secret = json_data["twitter"]["access_token_secret"]
        return api_key, api_key_secret, access_token, access_token_secret

    def __read_configuration_file(self):
        file = open(self.filename, "r")
        data = json.load(file)
        file.close()
        return data
