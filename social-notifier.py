#! /usr/bin/usr python
# -*- coding: utf-8 -*-

from credentials.facebook_credentials import FacebookCredentials
from api.facebook_api import FacebookAPI
from datetime import datetime
from agents import fetch_agent, facebook_agent


class SocialNotifier():

    def __init__(self, filename):
        self.credentials_filename = filename

    def start(self):
        #agent = fetch_agent.TwitterFetchAgent("agent@127.0.0.1", "secret", "nikolamajcen", time=120, period=15)
        agent = facebook_agent.FacebookAgent("agent@127.0.0.1", "secret", "nikolamajcen", time=120, period=15)
        agent.start()

if __name__ == "__main__":
    notifier = SocialNotifier("credentials.json")
    notifier.start()