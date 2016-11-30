#! /usr/bin/env python

from credentials.twitter_credentials import TwitterCredentials
from api.twitter_api import TwitterAPI


class SocialNotifier():

    def __init__(self, filename):
        self.__credentialsFilename = filename

    def start(self):
        twitterCredentials = TwitterCredentials(self.__credentialsFilename)
        credentials = twitterCredentials.getCredentials()

        twitterApi = TwitterAPI(credentials)
        twitterApi.searchTweets("nikolamajcen")


if __name__ == "__main__":
    notifier = SocialNotifier("credentials.json")
    notifier.start()