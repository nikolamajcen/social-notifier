#! /usr/bin/usr python
# -*- coding: utf-8 -*-

import json

from spade import Agent
from spade import Behaviour

from social.shared import report_message


class ReportAgent(Agent.Agent):

    class RegisterBehaviour(Behaviour.EventBehaviour):

        def _process(self):
            received_message = self._receive()
            if received_message:
                agent_name = received_message.getContent()
                self.myAgent.agents.append(agent_name)
                print "[" + self.myAgent.getName() + "] New agent (" + agent_name + ") started fetching."
            print "[" + self.myAgent.getName() + "] No. of agents working: " + str(len(self.myAgent.agents))

    class NotifyBehaviour(Behaviour.EventBehaviour):

        def _process(self):
            received_message = self._receive()
            if received_message:
                print "[" + self.myAgent.getName() + "] Received message from: " + received_message.getSender().getName()
                content = received_message.getContent()
                notify_message = report_message.ReportMessage()
                notify_message.load_json(json.loads(content))
                print "[" + self.myAgent.getName() + "] Network: " + notify_message.network
                print "[" + self.myAgent.getName() + "] Type: " + notify_message.message_type
                print "[" + self.myAgent.getName() + "] Keyword: " + notify_message.keyword
                print "[" + self.myAgent.getName() + "] Name: " + notify_message.name
                print "[" + self.myAgent.getName() + "] Username: " + notify_message.username
                print "[" + self.myAgent.getName() + "] Created at: " + notify_message.date
                print "[" + self.myAgent.getName() + "] Text: " + notify_message.text
                print ""

    class ReportBehaviour(Behaviour.EventBehaviour):

        def _process(self):
            received_message = self._receive()
            if received_message:
                agent_name = received_message.getContent()
                if agent_name in self.myAgent.agents:
                    self.myAgent.agents.remove(agent_name)
                    print  "[" + self.myAgent.getName() + "] Agent (" + agent_name + ") stopped fetching."
            print "[" + self.myAgent.getName() + "] No. of agents working: " + str(len(self.myAgent.agents))

    def _setup(self):
        print "[" + self.getName() + "] Report agent is online."
        self.agents = []

        register_template = Behaviour.ACLTemplate()
        register_template.setOntology("register")
        self.addBehaviour(self.RegisterBehaviour(), register_template)

        notify_template = Behaviour.ACLTemplate()
        notify_template.setOntology("notify")
        self.addBehaviour(self.NotifyBehaviour(), notify_template)

        report_template = Behaviour.ACLTemplate()
        report_template.setOntology("report")
        self.addBehaviour(self.ReportBehaviour(), report_template)
