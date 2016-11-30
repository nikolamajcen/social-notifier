#! /usr/bin/env python

import json


class TwitterCredentials:

    def __init__(self, filename):
        self.__filename = filename

    def changeCredentialsFile(self, filename):
        self__filename = filename

    def getCredentials(self):
        jsonData = self.__readConfigurationFile()
        api_key = jsonData["twitter"]["api_key"]
        api_key_secret = jsonData["twitter"]["api_key_secret"]
        access_token = jsonData["twitter"]["access_token"]
        access_token_secret = jsonData["twitter"]["access_token_secret"]
        return api_key, api_key_secret, access_token, access_token_secret

    def __readConfigurationFile(self):
        file = open(self.__filename, "r")
        data = json.load(file)
        file.close()
        return data