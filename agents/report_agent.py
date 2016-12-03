#! /usr/bin/usr python
# -*- coding: utf-8 -*-

import json

from spade import Agent
from spade import Behaviour

from social.shared import report_message


class ReportAgent(Agent.Agent):

    class RegisterBehaviour(Behaviour.EventBehaviour):
        print "Registered"
        # TODO:  Add agent to array

    class NotifyBehaviour(Behaviour.EventBehaviour):

        def _process(self):
            received_message = self._receive()
            if received_message:
                content = received_message.getContent()
                notify_message = report_message.ReportMessage()
                notify_message.load_json(json.loads(content))
                print "Network: " + notify_message.network
                print "Type: " + notify_message.message_type
                print "Keyword: " + notify_message.keyword
                print "Name: " + notify_message.name
                print "Username: " + notify_message.username
                print "Created at: " + notify_message.date
                print "Text: " + notify_message.text
                print ""

    class ReportBehaviour(Behaviour.EventBehaviour):

        def _process(self):
            received_message = self._receive()
            if received_message:
                print "Create report"
                # TODO: Remove fetch agent from array
                # TODO: When is array emtpy, kill report agent

    def _setup(self):
        print "Report agent is online."
        register_template = Behaviour.ACLTemplate()
        register_template.setOntology("register")
        self.addBehaviour(self.RegisterBehaviour(), register_template)

        notify_template = Behaviour.ACLTemplate()
        notify_template.setOntology("notify")
        self.addBehaviour(self.NotifyBehaviour(), notify_template)

        report_template = Behaviour.ACLTemplate()
        report_template.setOntology("report")
        self.addBehaviour(self.ReportBehaviour(), report_template)
