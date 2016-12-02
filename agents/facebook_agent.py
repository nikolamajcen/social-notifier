#! /usr/bin/usr python
# -*- coding: utf-8 -*-

from spade import Agent
from spade import Behaviour
from datetime import datetime, timedelta
from api.facebook_api import *
from credentials.facebook_credentials import *


class FacebookAgent(Agent.Agent):

    class FetchBehaviour(Behaviour.PeriodicBehaviour):

        def __init__(self, time, period, credentials_filename):
            Behaviour.PeriodicBehaviour.__init__(self, period)
            self.periods = time / period
            self.current_date = datetime.now()
            facebook_credentials = FacebookCredentials(credentials_filename)
            self.facebook_api = FacebookAPI(facebook_credentials.get_credentials())

        def onStart(self):
            print "Status activity fetch started."

        def onEnd(self):
            print "Status activity fetch ended."

        def _onTick(self):
            if self.periods > 0:
                self.periods -= 1
                self.__fetch_data()
            else:
                self.kill()

        def __fetch_data(self):
            print "Fetching statuses... (No. of periods left: " + str(self.periods) + ")"
            results = self.facebook_api.search_posts(self.myAgent.keyword)

            for status in results:
                if (status.date - self.current_date) > timedelta(seconds=1):
                    self.current_date = status.date
                    # TODO: Notify report agent
                    print "Name: " + status.name
                    print "Username: " + status.username
                    print "Created at: " + datetime.strftime(status.date, "%a %b %d %H:%M:%S %Y") + " (" + status.location + ")"
                    print "Text: " + status.text
                    print ""

    def __init__(self, agentjid, password, keyword, credentials_filename="credentials.json", time=60, period=10):
        Agent.Agent.__init__(self, agentjid, password)
        self.keyword = keyword
        self.credentials_filename = credentials_filename
        self.time = time
        self.period = period

    def _setup(self):
        print "Facebook fetch agent is starting..."
        fetch_behaviour = self.FetchBehaviour(self.time, self.period, self.credentials_filename)
        self.addBehaviour(fetch_behaviour)