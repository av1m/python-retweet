#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import urllib.parse
from datetime import datetime
from json import dumps

from requests import post

try:
    from configuration.credentials_test import Configuration  # for testing
except ImportError:
    from configuration.credentials import Configuration


class Logger:
    def __init__(self):
        self.conf = Configuration()
        self.date = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
        self.sendmail_location = self.conf.MAIL_LOCATION
        self.log_location = self.conf.LOG_LOCATION
        self.free_credentials = {
            'user': self.conf.FREE_USER, 'pass': self.conf.FREE_PASSWORD}

    def file(self, json_nodump):
        if not self.log_location:
            raise Exception(
                "You have not configured the settings to save LOG in a file")
        if not os.path.isdir(self.log_location):
            os.mkdir(self.log_location)
        filename = '{}/log_{}'.format(self.log_location, self.date) + '.json'
        with open(filename, 'w') as outfile:
            outfile.write(dumps(json_nodump, indent=4, sort_keys=True))

    def sms(self, data):
        if not self.free_credentials:
            raise Exception(
                "You have not configured the settings to send an SMS")
        if data != '':
            url = "https://smsapi.free-mobile.fr/sendmsg?"
            url += "user={}&pass={}&msg={}".format(
                self.free_credentials['user'],
                self.free_credentials['pass'],
                urllib.parse.quote(str(data))
            )
            print(url)
            r = post(url=url)
            print(r)

    def mail(self, json_nodump):
        if not self.sendmail_location:
            raise Exception(
                "You have not configured the settings to send a mail")
        p = os.popen("%s -t" % self.sendmail_location, "w")
        p.write("From: %s\n" % self.conf.MAIL_FROM)
        p.write("To: %s\n" % self.conf.MAIL_TO)
        p.write("Subject: AUTO RETWEET {}\n".format(str(self.date)))
        p.write("\n")  # blank line separating headers from body
        p.write(dumps(json_nodump, indent=4))
        status = p.close()
        if status != 0:
            print("Sendmail exit status", status)
