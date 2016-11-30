#! /usr/bin/env python

import json


class TwitterCredentials:

    def __init__(self, filename):
        self.__filename = filename

    def change_credentials_file(self, filename):
        self__filename = filename

    def get_credentials(self):
        jsonData = self.__read_configuration_file()
        api_key = jsonData["twitter"]["api_key"]
        api_key_secret = jsonData["twitter"]["api_key_secret"]
        access_token = jsonData["twitter"]["access_token"]
        access_token_secret = jsonData["twitter"]["access_token_secret"]
        return api_key, api_key_secret, access_token, access_token_secret

    def __read_configuration_file(self):
        file = open(self.__filename, "r")
        data = json.load(file)
        file.close()
        return data