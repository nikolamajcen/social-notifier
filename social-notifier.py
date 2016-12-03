#! /usr/bin/usr python
# -*- coding: utf-8 -*-

import argparse
import sys
import json
from os import path

from agents.facebook_agent import FacebookAgent
from agents.twitter_agent import TwitterFetchAgent
from agents.report_agent import ReportAgent


class SocialNotifier:

    def __init__(self):
        self.parse_parameters()

    def parse_parameters(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        # Reporter
        reporter_parser = subparsers.add_parser("reporter", help="Creates social reporter")
        reporter_parser.add_argument("config", action="store", default="config.json", help="Configuration filename")

        # Twitter
        twitter_parser = subparsers.add_parser("twitter", help="Creates a Twitter fetch agent")
        twitter_parser.add_argument("credentials", action="store", help="Credentials filename")
        twitter_parser.add_argument("-config", action="store", default="config.json", help="Configuration filename")
        twitter_parser.add_argument("-type", default="tweet", action="store", help="Defines search type ('tweet' or 'hashtag')")
        twitter_parser.add_argument("-keyword", action="store", help="Defines search keyword (username or hashtag)")
        twitter_parser.add_argument("-time", default=120, action="store", help="Length of agent lifetime in secods")
        twitter_parser.add_argument("-period", default=15, action="store", help="Lenght of period in seconds")

        # Facebook
        facebook_parser = subparsers.add_parser("facebook", help="Creates a Facebook fetch agent")
        facebook_parser.add_argument("credentials", action='store', help="Credentials filename")
        facebook_parser.add_argument("-config", action="store", default="config.json", help="Configuration filename")
        facebook_parser.add_argument("-keyword", action="store", help="Defines search keyword (username)")
        facebook_parser.add_argument("-time", default=120, help="Length of agent lifetime in secods")
        facebook_parser.add_argument("-period", default=15, help="Lenght of period in seconds")

        result = parser.parse_args()
        if not path.isfile(result.config):
            sys.exit("Error: No configuration file found.")

        if result.command == "reporter":
            self.__start_reporter(result)
        elif result.command == "twitter":
            if not path.isfile(result.credentials):
                sys.exit("Error: No credentials file found.")
            if result.type != "tweet" and result.type != "hashtag":
                sys.exit("Error: Type must be 'tweet' or 'hashtag'.")
            self.__start_twitter_fetch(result)
        elif result.command == "facebook":
            if not path.isfile(result.credentials):
                sys.exit("Error: No credentials file found.")
            self.__start_facebook_fetch(result)
        else:
            sys.exit("Error: Problem with parameters.")

    def __start_reporter(self, result):
        name, password = self.__get_reporter_info(result.config)
        reporter = ReportAgent(name, password)
        reporter.start()

    def __start_twitter_fetch(self, result):
        # TODO: Add reporter name to constructor
        agent = TwitterFetchAgent("agent@127.0.0.1", "secret", result.keyword, result.type, result.credentials, result.time, result.period)
        agent.start()

    def __start_facebook_fetch(self, result):
        # TODO: Add reporter name to constructor
        agent = FacebookAgent("agent@127.0.0.1", "secret", result.keyword, result.time, result.period)
        agent.start()

    def __get_reporter_info(self, filename):
        file = open(filename, "r")
        json_data = json.load(file)
        agent_name = json_data["agent_name"]
        agent_password = json_data["agent_password"]
        file.close()
        return agent_name, agent_password


if __name__ == "__main__":
    social_notifier = SocialNotifier()
