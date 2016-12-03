#! /usr/bin/usr python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import json

from spade import Agent
from spade import Behaviour
from spade import AID
from spade import ACLMessage

from social.twitter.twitter_api import TwitterAPI
from social.twitter.twitter_credentials import TwitterCredentials
from social.shared import report_message


class TwitterFetchAgent(Agent.Agent):

    class FetchBehaviour(Behaviour.PeriodicBehaviour):

        def __init__(self, time, period, credentials_filename):
            Behaviour.PeriodicBehaviour.__init__(self, period)
            self.periods = time / period
            self.current_date = datetime.now()
            twitter_credentials = TwitterCredentials(credentials_filename)
            self.twitter_api = TwitterAPI(twitter_credentials.get_credentials())

        def onStart(self):
            print self.myAgent.fetch_type.capitalize() + " activity fetch started."

        def onEnd(self):
            print self.myAgent.fetch_type.capitalize() + " activity fetch ended."

        def _onTick(self):


            if self.periods > 0:
                self.periods -= 1
                self.__fetch_data()
            else:
                self.kill()

        def __fetch_data(self):
            if self.myAgent.fetch_type == "tweet":
                print "Fetching tweets... (No. of periods left: " + str(self.periods) + ")"
                results = self.twitter_api.search_tweets(self.myAgent.keyword)
            else:
                print "Fetching hashtags... (No. of periods left: " + str(self.periods) + ")"
                results = self.twitter_api.search_hashtag(self.myAgent.keyword)

            for tweet in results:
                if True:#(tweet.date - self.current_date) > timedelta(seconds=1):
                    self.current_date = tweet.date
                    receiver = AID.aid(name="reporter@127.0.0.1", addresses=["xmpp://reporter@127.0.0.1"])
                    message = ACLMessage.ACLMessage()
                    message.addReceiver(receiver)
                    message.setOntology("notify")
                    object = report_message.ReportMessage("Twitter", self.myAgent.fetch_type, self.myAgent.keyword,
                                                          "some_username", "some_name", str(datetime.now()), "some_message")
                    value = json.dumps(object.__dict__)
                    message.setContent(value)
                    self.myAgent.send(message)
                    break

    def __init__(self, agentjid, password, keyword, fetch_type="tweet",
                 credentials_filename="credentials.json", time=60, period=10):
        Agent.Agent.__init__(self, agentjid, password)
        self.keyword = keyword
        self.fetch_type = fetch_type
        self.credentials_filename = credentials_filename
        self.time = time
        self.period = period

    def _setup(self):
        print "Twitter fetch agent is starting..."
        fetch_behaviour = self.FetchBehaviour(self.time, self.period, self.credentials_filename)
        self.addBehaviour(fetch_behaviour)
