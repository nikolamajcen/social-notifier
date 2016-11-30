#! /usr/bin/env python

from credentials.twitter_credentials import TwitterCredentials
from api.twitter_api import TwitterAPI


class SocialNotifier():

    def __init__(self, filename):
        self.__credentials_filename = filename

    def start(self):
        twitter_credentials = TwitterCredentials(self.__credentials_filename)
        credentials = twitter_credentials.get_credentials()

        twitter_api = TwitterAPI(credentials)
        twitter_api.search_tweets("nikolamajcen")


if __name__ == "__main__":
    notifier = SocialNotifier("credentials.json")
    notifier.start()