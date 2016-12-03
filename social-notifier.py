#! /usr/bin/usr python
# -*- coding: utf-8 -*-

from agents import facebook_agent
from agents import twitter_agent
from agents import report_agent


class SocialNotifier:

    def __init__(self, filename):
        self.credentials_filename = filename

    def start(self):
        reporter = report_agent.ReportAgent("reporter@127.0.0.1", "secret")
        reporter.start()
        agent = twitter_agent.TwitterFetchAgent("agent@127.0.0.1", "secret", "#trump", "hashtag", time=60, period=15)
        #agent = facebook_agent.FacebookAgent("agent@127.0.0.1", "secret", "kimkardashian", time=30, period=15)
        agent.start()

if __name__ == "__main__":
    notifier = SocialNotifier("credentials.json")
    notifier.start()
