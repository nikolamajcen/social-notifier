#! /usr/bin/usr python
# -*- coding: utf-8 -*-

import json
from datetime import datetime, timedelta

from spade import Agent
from spade import Behaviour
from spade import AID
from spade import ACLMessage

from social.twitter.twitter_api import TwitterAPI
from social.twitter.twitter_credentials import TwitterCredentials
from social.shared.report_message import ReportMessage


class TwitterFetchAgent(Agent.Agent):

    class FetchBehaviour(Behaviour.PeriodicBehaviour):

        def __init__(self, time, period, credentials_filename):
            Behaviour.PeriodicBehaviour.__init__(self, period)
            self.periods = time / period
            self.current_date = datetime.now()
            twitter_credentials = TwitterCredentials(credentials_filename)
            self.twitter_api = TwitterAPI(twitter_credentials.get_credentials())

        def onStart(self):
            print "[" + self.myAgent.getName() + "] "
                + self.myAgent.fetch_type.capitalize()
                + " activity fetch started."
            self.__send_registration_message()

        def onEnd(self):
            print "[" + self.myAgent.getName() + "] "
                + self.myAgent.fetch_type.capitalize()
                + " activity fetch ended."
            self.__send_report_message()

        def _onTick(self):
            if self.periods > 0:
                self.periods -= 1
                self.fetch_data()
            else:
                self.kill()

        def fetch_data(self):
            if self.myAgent.fetch_type == "tweet":
                print "[" + self.myAgent.getName()
                    + "] Fetching tweets... (No. of periods left: "
                    + str(self.periods) + ")"
                results = self.twitter_api.search_tweets(self.myAgent.keyword)
            else:
                print "[" + self.myAgent.getName()
                    + "] Fetching hashtags... (No. of periods left: "
                    + str(self.periods) + ")"
                results = self.twitter_api.search_hashtag(self.myAgent.keyword)

            tweets_found = 0
            for tweet in results:
                if (tweet.date - self.current_date) > timedelta(seconds=1):
                    self.current_date = tweet.date
                    self.__send_tweet_message(tweet)
                    tweets_found += 1
            print "[" + self.myAgent.getName() + "] Found "
                + self.myAgent.fetch_type + "s: " + str(tweets_found)

        def __send_registration_message(self):
            message = ACLMessage.ACLMessage()
            message.addReceiver(self.myAgent.receiver)
            message.setOntology("register")
            message.setContent(self.myAgent.getName())
            self.myAgent.send(message)

        def __send_tweet_message(self, tweet):
            message = ACLMessage.ACLMessage()
            message.addReceiver(self.myAgent.receiver)
            message.setOntology("notify")
            object = ReportMessage("Twitter", self.myAgent.fetch_type,
                                   self.myAgent.keyword,
                                   tweet.username, tweet.name,
                                   tweet.date, tweet.text)
            value = json.dumps(object.__dict__)
            message.setContent(value)
            self.myAgent.send(message)

        def __send_report_message(self):
            message = ACLMessage.ACLMessage()
            message.addReceiver(self.myAgent.receiver)
            message.setOntology("report")
            message.setContent(self.myAgent.getName())
            self.myAgent.send(message)

    class ReportDeliveryBehaviour(Behaviour.EventBehaviour):

        def _process(self):
            received_message = self._receive()
            if received_message:
                content = json.loads(received_message.getContent())
                print ""
                print "[" + self.myAgent.getName()
                    + "] Received message from: "
                    + received_message.getSender().getName()
                print "[" + self.myAgent.getName()
                    + "] Total number of fetched data: "
                    + str(len(content))
                print ""
                for element in content:
                    notify_message = ReportMessage()
                    notify_message.load_json(element)
                    notify_message.print_message()
            self.myAgent.stop()

    def __init__(self, reporter_name, keyword, fetch_type="tweet",
                 credentials_filename="credentials.json", time=60, period=10):
        agent_id, password = self.__generate_agent_credentials()
        Agent.Agent.__init__(self, agent_id, password)
        self.keyword = keyword
        self.fetch_type = fetch_type
        self.credentials_filename = credentials_filename
        self.time = time
        self.period = period
        self.receiver = AID.aid(name=reporter_name,
                                addresses=["xmpp://" + reporter_name])

    def _setup(self):
        print "[" + self.getName() + "] Twitter fetch agent is starting..."
        fetch_behaviour = self.FetchBehaviour(self.time, self.period,
                                              self.credentials_filename)
        self.addBehaviour(fetch_behaviour)
        delivery_template = Behaviour.ACLTemplate()
        delivery_template.setOntology("report_delivery")
        self.addBehaviour(self.ReportDeliveryBehaviour(), delivery_template)

    def __generate_agent_credentials(self):
        agent_name = "twitter_" + datetime.now().strftime("%H%M%S")
                    + "@127.0.0.1"
        return agent_name, "secret"
