#! /usr/bin/usr python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='social-notifier',
    version='1.0',
    packages=['agents’, ‘social’],
    url='https://nikolamajcen.com',
    license='',
    author='Nikola Majcen',
    author_email='',
    description='Agent based social notifier',
    requires=['spade', 'requests', 'requests_oauthlib', 'facebook-sdk']
)
