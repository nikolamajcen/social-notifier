#! /usr/bin/usr python
# -*- coding: utf-8 -*-

import json
from datetime import datetime, timedelta

from spade import Agent
from spade import Behaviour
from spade import ACLMessage
from spade import AID

from social.facebook.facebook_api import FacebookAPI
from social.facebook.facebook_credentials import FacebookCredentials
from social.shared.report_message import ReportMessage


class FacebookAgent(Agent.Agent):

    class FetchBehaviour(Behaviour.PeriodicBehaviour):

        def __init__(self, time, period, credentials_filename):
            Behaviour.PeriodicBehaviour.__init__(self, period)
            self.periods = time / period
            self.current_date = datetime.now()
            facebook_credentials = FacebookCredentials(credentials_filename)
            self.facebook_api = FacebookAPI(facebook_credentials.get_credentials())

        def onStart(self):
            print "[" + self.myAgent.getName() + "] Status activity fetch started."

        def onEnd(self):
            print "[" + self.myAgent.getName() + "] Status activity fetch ended."

        def _onTick(self):
            if self.periods > 0:
                self.periods -= 1
                self.fetch_data()
            else:
                self.kill()

        def fetch_data(self):
            print "[" + self.myAgent.getName() + "] Fetching statuses... (No. of periods left: " + str(self.periods) + ")"
            results = self.facebook_api.search_posts(self.myAgent.keyword)

            statuses_found = 0
            for status in results:
                if (status.date - self.current_date) > timedelta(seconds=1):
                    self.current_date = status.date
                    self.__send_status_message(status)
                    statuses_found += 1
            print "[" + self.myAgent.getName() + "] Found statuses: " + str(statuses_found)

        def __send_registration_message(self):
            message = ACLMessage.ACLMessage()
            message.addReceiver(self.myAgent.receiver)
            message.setOntology("register")
            message.setContent(self.myAgent.getName())
            self.myAgent.send(message)

        def __send_status_message(self, post):
            message = ACLMessage.ACLMessage()
            message.addReceiver(self.myAgent.receiver)
            message.setOntology("notify")
            object = ReportMessage("Facebook", post.status_type, self.myAgent.keyword,
                                   post.username, post.name, str(datetime.now()), post.message + " (" + post.link + ")")
            value = json.dumps(object.__dict__)
            message.setContent(value)
            self.myAgent.send(message)

        def __send_report_message(self):
            message = ACLMessage.ACLMessage()
            message.addReceiver(self.myAgent.receiver)
            message.setOntology("report")
            message.setContent(self.myAgent.getName())
            self.myAgent.send(message)

    def __init__(self, agentjid, password, keyword, credentials_filename="credentials.json", time=60, period=10):
        Agent.Agent.__init__(self, agentjid, password)
        self.keyword = keyword
        self.credentials_filename = credentials_filename
        self.time = time
        self.period = period
        self.receiver = AID.aid(name="reporter@127.0.0.1", addresses=["xmpp://reporter@127.0.0.1"])

    def _setup(self):
        print "[" + self.getName() + "] Facebook fetch agent is starting..."
        fetch_behaviour = self.FetchBehaviour(self.time, self.period, self.credentials_filename)
        self.addBehaviour(fetch_behaviour)
