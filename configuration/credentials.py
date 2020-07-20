#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Configuration(object):
    def __init__(self):
        self.CONSUMER_KEY = None
        self.CONSUMER_SECRET = None
        self.ACCESS_TOKEN = None
        self.ACCESS_TOKEN_SECRET = None
        self.SEARCH = [
            "@github",
            "list:avimimoun/n3W5d3V",   # personnal list
            "list:avimimoun/Followers1"  # personnal list
        ]
        self.FREE_USER = None  # optional
        self.FREE_PASSWORD = None  # optional
        # Name Surname<contact@domain.com>
        self.MAIL_FROM = None  # optional
        # Name Surname<contact@domain.com>
        self.MAIL_TO = None  # optional
        self.MAIL_LOCATION = None  # optional
        self.LOG_LOCATION = None  # optional
