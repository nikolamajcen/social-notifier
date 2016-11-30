#! /usr/bin/env python

from credentials.twitter_credentials import TwitterCredentials
from api.twitter_api import TwitterAPI
from models.twitter_models import *
import pprint


class SocialNotifier():

    def __init__(self, filename):
        self.__credentials_filename = filename

    def start(self):
        twitter_credentials = TwitterCredentials(self.__credentials_filename)
        credentials = twitter_credentials.get_credentials()

        twitter_api = TwitterAPI(credentials)

        # User activity search
        print "TWEET SEARCH"
        data = twitter_api.search_tweets("kimkardashian")
        for element in data:
            a = TwitterUser(element)
            print "Name: " + a.name
            print "Username: " + a.username
            print "Created at: " + a.created_at + "(" + a.location + ")"
            print "Text: " + a.text
            print ""

        print ""
        print "HASHTAG SEARCH"
        # Hashtag search
        data = twitter_api.search_hashtag("#python")["statuses"]
        for element in data:
            a = TwitterHashtag(element)
            print "Name: " + a.name
            print "Username: " + a.username
            print "Created at: " + a.created_at + "(" + a.location + ")"
            print "Text: " + a.text
            print ""


if __name__ == "__main__":
    notifier = SocialNotifier("credentials.json")
    notifier.start()