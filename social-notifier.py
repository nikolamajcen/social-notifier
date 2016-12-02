#! /usr/bin/usr python
# -*- coding: utf-8 -*-

from credentials.twitter_credentials import TwitterCredentials
from credentials.facebook_credentials import FacebookCredentials
from api.twitter_api import TwitterAPI
from api.facebook_api import FacebookAPI
from datetime import datetime
from agents import fetch_agent


class SocialNotifier():

    def __init__(self, filename):
        self.credentials_filename = filename

    def start(self):
        #self.__twitter_search()
        #self.__facebook_search()

        agent = fetch_agent.TwitterFetchAgent("agent@127.0.0.1", "secret", keyword="nikolamajcen", time=120, period=15)
        agent.start()

    def __twitter_search(self):
        twitter_credentials = TwitterCredentials(self.credentials_filename)
        twitter_api = TwitterAPI(twitter_credentials.get_credentials())

        # User activity search
        print "TWITTER - TWEET SEARCH"
        tweets = twitter_api.search_tweets("kimkardashian")
        for tweet in tweets:
            print "Name: " + tweet.name
            print "Username: " + tweet.username
            print "Created at: " + datetime.strftime(tweet.date, "%a %b %d %H:%M:%S %Y") +  "(" + tweet.location + ")"
            print "Text: " + tweet.text
            print ""
        print ""

        # Hashtag search
        print "TWITTER - HASHTAG SEARCH"
        hashtags = twitter_api.search_hashtag("#python")
        for hashtag in hashtags:
            print "Name: " + hashtag.name
            print "Username: " + hashtag.username
            print "Created at: " + datetime.strftime(hashtag.date, "%a %b %d %H:%M:%S %Y)") + " (" + hashtag.location + ")"
            print "Text: " + hashtag.text
            print ""

    def __facebook_search(self):
        facebook_credentials = FacebookCredentials(self.credentials_filename)
        facebook_api = FacebookAPI(facebook_credentials.get_credentials())

        # User activity search
        posts = facebook_api.search_posts("kimkardashian")
        print "FACEBOOK - POST SEARCH"
        for post in posts:
            print "Date: " + datetime.strftime(post.date, "%a %b %d %H:%M:%S %Y")
            print "Status type: " + post.status_type
            print "Message: " + post.message
            print "Link: " + post.link
            print ""


if __name__ == "__main__":
    notifier = SocialNotifier("credentials.json")
    notifier.start()