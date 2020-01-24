#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import randint
from time import sleep

import tweepy

from include.logger import Logger

try:
    from configuration.credentials_test import *  # for testing
except ImportError:
    from configuration.credentials import *

authentification = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
authentification.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(authentification)

# https://developer.twitter.com/en/docs/basics/rate-limiting
# http://docs.tweepy.org/en/v3.5.0/api.html

# https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators
# https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets

search = [
    "@github",
    "list:avimimoun/newsdev",   # personnal list
    "list:avimimoun/Followers1"  # personnal list
]

if __name__ == '__main__':
    log, sms = {}, ''  # Used for logs, sending by mail, sms ...
    i, TIME_SLEEP, TOTAL_RT = 1, 10, 10
    random_query = ''
    while_condition = True

    while while_condition:
        # Randomly selected a request contained in the `search` variable
        random_query = '(' + search[randint(0, len(search) - 1)] + ') lang:en OR lang:fr filter:safe'
        print(random_query)
        sms += '\n====> {}\n\n'.format(random_query)
        for tweet in tweepy.Cursor(api.search, q=random_query, result_type="recent").items(TOTAL_RT):
            try:
                tweet.retweet()
                # If we are not catching the except: the tweet is retweeted
                print('Retweet OK : {0}/{1}'.format(i, TOTAL_RT))
                # add to log
                log['tweet{}'.format(i)] = {"query": random_query, "tweet": tweet._json}
                sms += 'tweet{0}  -- @{1}\n\n'.format(i, tweet.user.name)
                # we wait as the rules of Twitter want
                sleep(TIME_SLEEP)
                i += 1  # add counter (we want just `TOTAL_RT` retweet)
            except tweepy.TweepError as error:
                print('An error occurred during the retweet: {0}'.format(error.reason))
            except StopIteration:
                break
        # We do a check if we ever get too many tweets
        if i > TOTAL_RT:
            while_condition = False
            break

    # Create and send LOG
    logger = Logger()
    logger.file(log)
