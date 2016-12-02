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
        self.__twitter_search()
        #self.__facebook_search()

    def __twitter_search(self):
        twitter_credentials = TwitterCredentials(self.credentials_filename)
        twitter_api = TwitterAPI(twitter_credentials.get_credentials())

        # User activity search
        print "TWEET SEARCH"
        tweets = twitter_api.search_tweets("kimkardashian")
        for tweet in tweets:
            print "Name: " + tweet.name
            print "Username: " + tweet.username
            print "Created at: " + tweet.created_at + "(" + tweet.location + ")"
            print "Text: " + tweet.text
            print ""
        print ""

        # Hashtag search
        print "HASHTAG SEARCH"
        hashtags = twitter_api.search_hashtag("#python")
        for hashtag in hashtags:
            print "Name: " + hashtag.name
            print "Username: " + hashtag.username
            print "Created at: " + hashtag.created_at + " (" + hashtag.location + ")"
            print "Text: " + hashtag.text
            print ""

    def __facebook_search(self):
        facebook_credentials = FacebookCredentials(self.credentials_filename)
        facebook_api = FacebookAPI(facebook_credentials.get_credentials())
        facebook_api.search_posts("kimkardashian")


if __name__ == "__main__":
    notifier = SocialNotifier("credentials.json")
    notifier.start()