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


def is_good_tweet(tweet):
    """Used to indicate whether the tweet should be retweeted (according to our criteria)
    Here, a tweet is acceptable if:
    - The sum of these hashtags, mentions and URLS is less than or equal to 8, AND
    - The number of hashtags does not exceed 5
    - The language is French or English
    - If the information on the sensitive of the tweet is available, it must be False

    Args:
        tweet ([tweepy.Status]): The tweet to analyze (i.e. on which we evaluate our criteria)

    Returns:
        [bool]: True if the tweet should be retweeted, False otherwise
    """
    tweet = tweet._json  # We convert Status to JSON to better process the information
    entities = {"hashtags": len(tweet['entities']['hashtags']),
                'user_mentions': len(tweet['entities']['user_mentions']),
                'urls': len(tweet['entities']['urls'])}
    return (sum(entities.values()) <= 8 and entities['hashtags'] <= 5) and (tweet['lang'].lower() in ['fr', 'en']) and (False if 'possibly_sensitive' in tweet and bool(tweet['possibly_sensitive']) else True)


if __name__ == '__main__':
    log = {}  # Used for logs, sending by mail, sms ...
    TIME_SLEEP, TOTAL_RT, MAX_RECOVERED = 10, 10, 50
    recovered, send = 0, 1
    while True:
        # Randomly selected a request contained in the `SEARCH` variable
        random_query = '(' + SEARCH[randint(0, len(SEARCH) - 1)
                                    ] + ') lang:en OR lang:fr filter:safe'
        print(random_query)
        for tweet in tweepy.Cursor(api.search, q="node", result_type="recent").items(TOTAL_RT):
            recovered += 1
            if recovered > MAX_RECOVERED:
                print("Too much research !!")
                log['error'] = {"error": True, "message": "Too much research !!"}
                send = MAX_RECOVERED
                break
            if not is_good_tweet(tweet):
                continue
            try:
                tweet.retweet()
                # If we are not catching the except: the tweet is retweeted
                print('Retweet OK : {0}/{1}'.format(send, TOTAL_RT))
                # add to log
                log['tweet{}'.format(send)] = {
                    "query": random_query, "tweet": tweet._json}
                send += 1  # add counter (we want just `TOTAL_RT` retweet)
            except tweepy.RateLimitError:
                # we wait as the rules of Twitter want
                sleep(TIME_SLEEP)
            except tweepy.TweepError as error:
                print('An error occurred during the retweet: {0}'.format(
                    error.reason))
            except StopIteration:
                break
        # We do a check if we ever get too many tweets
        if send > TOTAL_RT:
            break

    # Create and send LOG
    logger = Logger()
    logger.file(log)
