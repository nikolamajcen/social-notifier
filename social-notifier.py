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
        reporter_parser = subparsers.add_parser("reporter",
                                                help="Creates social reporter")
        reporter_parser.add_argument("-config",
                                     default="config.json",
                                     action="store",
                                     help="Configuration filename")

        # Twitter
        twitter_parser = subparsers.add_parser("twitter",
                                               help="Creates a Twitter fetch agent")
        twitter_parser.add_argument("keyword",
                                    action="store",
                                    help="Defines search keyword (username or hashtag)")
        twitter_parser.add_argument("type",
                                    action="store",
                                    help="Defines search type ('tweet' or 'hashtag')")
        twitter_parser.add_argument("-credentials",
                                    default="credentials.json",
                                    action="store",
                                    help="Credentials filename")
        twitter_parser.add_argument("-config",
                                    default="config.json",
                                    action="store",
                                    help="Configuration filename")
        twitter_parser.add_argument("-time", default=120, action="store",
                                    help="Length of agent lifetime in secods",
                                    type=int)
        twitter_parser.add_argument("-period", default=15, action="store",
                                    help="Lenght of period in seconds",
                                    type=int)

        # Facebook
        facebook_parser = subparsers.add_parser("facebook",
                                                help="Creates a Facebook fetch agent")
        facebook_parser.add_argument("keyword",
                                     action="store",
                                     help="Defines search keyword (username)")
        facebook_parser.add_argument("-credentials",
                                     default="credentials.json",
                                     action='store',
                                     help="Credentials filename")
        facebook_parser.add_argument("-config",
                                     default="config.json",
                                     action="store",
                                     help="Configuration filename")
        facebook_parser.add_argument("-time",
                                     default=120,
                                     help="Length of agent lifetime in secods",
                                     type=int)
        facebook_parser.add_argument("-period",
                                     default=15,
                                     help="Lenght of period in seconds",
                                     type=int)

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
        name, password = self.__read_config_file(result.config)
        reporter = ReportAgent(name, password)
        reporter.start()

    def __start_twitter_fetch(self, result):
        reporter_name, _ = self.__read_config_file(result.config)
        agent = TwitterFetchAgent(reporter_name, result.keyword,
                                  result.type, result.credentials,
                                  result.time, result.period)
        agent.start()

    def __start_facebook_fetch(self, result):
        reporter_name, _ = self.__read_config_file(result.config)
        agent = FacebookAgent(reporter_name, result.keyword,
                              result.credentials, result.time,
                              result.period)
        agent.start()

    def __read_config_file(self, filename):
        file = open(filename, "r")
        json_data = json.load(file)
        agent_name = json_data["agent_name"]
        agent_password = json_data["agent_password"]
        file.close()
        return agent_name, agent_password


if __name__ == "__main__":
    social_notifier = SocialNotifier()
