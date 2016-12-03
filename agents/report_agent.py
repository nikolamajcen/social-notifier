#! /usr/bin/usr python
# -*- coding: utf-8 -*-

import json

from spade import Agent
from spade import Behaviour
from spade import ACLMessage
from spade import AID

from social.shared import report_message


class ReportAgent(Agent.Agent):

    class RegisterBehaviour(Behaviour.EventBehaviour):

        def _process(self):
            received_message = self._receive()
            if received_message:
                agent_name = received_message.getContent()
                self.myAgent.agents.append(agent_name)
                self.myAgent.reports[agent_name] = []
                print "[" + self.myAgent.getName() + "] New agent (" + agent_name + ") started fetching."
            print "[" + self.myAgent.getName() + "] No. of agents working: " + str(len(self.myAgent.agents))

    class NotifyBehaviour(Behaviour.EventBehaviour):

        def _process(self):
            received_message = self._receive()
            if received_message:
                content = received_message.getContent()
                notify_message = report_message.ReportMessage()
                notify_message.load_json(json.loads(content))
                self.myAgent.reports[received_message.getSender().getName()].append(notify_message)
                print "[" + self.myAgent.getName() + "] Received message from: " + received_message.getSender().getName()
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
                    self.send_report(agent_name)
                    self.myAgent.agents.remove(agent_name)
                    del(self.myAgent.reports[agent_name])
                    print  "[" + self.myAgent.getName() + "] Agent (" + agent_name + ") stopped fetching."
            print "[" + self.myAgent.getName() + "] No. of agents working: " + str(len(self.myAgent.agents))

        def send_report(self, agent_name):
            report_messages = self.myAgent.reports[agent_name]
            receiver = AID.aid(name=agent_name, addresses=["xmpp://" + agent_name])
            message = ACLMessage.ACLMessage()
            message.addReceiver(receiver)
            message.setOntology("report_delivery")
            message.setContent(json.dumps([obj.__dict__ for obj in report_messages]))
            self.myAgent.send(message)

    def _setup(self):
        print "[" + self.getName() + "] Report agent is online."
        self.agents = []
        self.reports = {}

        register_template = Behaviour.ACLTemplate()
        register_template.setOntology("register")
        self.addBehaviour(self.RegisterBehaviour(), register_template)

        notify_template = Behaviour.ACLTemplate()
        notify_template.setOntology("notify")
        self.addBehaviour(self.NotifyBehaviour(), notify_template)

        report_template = Behaviour.ACLTemplate()
        report_template.setOntology("report")
        self.addBehaviour(self.ReportBehaviour(), report_template)
