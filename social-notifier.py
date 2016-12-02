#! /usr/bin/env python

from credentials.twitter_credentials import TwitterCredentials
from credentials.facebook_credentials import FacebookCredentials
from api.twitter_api import TwitterAPI
from api.facebook_api import FacebookAPI
from models.twitter_models import *


class SocialNotifier():

    def __init__(self, filename):
        self.credentials_filename = filename

    def start(self):
        # self.__twitter_search()
        self.__facebook_search()

    def __twitter_search(self):
        twitter_credentials = TwitterCredentials(self.credentials_filename)
        twitter_api = TwitterAPI(twitter_credentials.get_credentials())

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

        # Hashtag search
        print "HASHTAG SEARCH"
        data = twitter_api.search_hashtag("#python")["statuses"]
        for element in data:
            a = TwitterHashtag(element)
            print "Name: " + a.name
            print "Username: " + a.username
            print "Created at: " + a.created_at + " (" + a.location + ")"
            print "Text: " + a.text
            print ""

    def __facebook_search(self):
        facebook_credentials = FacebookCredentials(self.credentials_filename)
        facebook_api = FacebookAPI(facebook_credentials.get_credentials())
        facebook_api.search_posts("kimkardashian")


if __name__ == "__main__":
    notifier = SocialNotifier("credentials.json")
    notifier.start()