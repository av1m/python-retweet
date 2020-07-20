#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import randint
from time import sleep

import tweepy

from configuration.logger import Logger

try:
    from configuration.credentials_test import Configuration  # for testing
except ImportError:
    from configuration.credentials import Configuration


def is_good_tweet(status):
    """Used to indicate whether the tweet should be retweeted
    Here, a tweet is acceptable if: (according to our criteria)
    - The sum of these hashtags, mentions and URLS is less than or equal to 8
    - The number of hashtags does not exceed 5
    - The language is French or English
    - If the information on the sensitive of the tweet is available,
      it must be False

    Args:
        status ([tweepy.Status]): The tweet to analyze
            (i.e. on which we evaluate our criteria)

    Returns:
        [bool]: True if the tweet should be retweeted, False otherwise
    """
    # We convert Status to JSON to better process the information
    entities = {"hashtags": len(status._json['entities']['hashtags']),
                'user_mentions': len(
                    status._json['entities']['user_mentions']),
                'urls': len(status._json['entities']['urls'])}
    # Critetions
    bool_entities = sum(entities.values()) <= 8 and entities['hashtags'] <= 5
    bool_lang = status._json['lang'].lower() in ['fr', 'en']
    bool_sensitive = not bool('possibly_sensitive' in status._json and bool(
        status._json['possibly_sensitive']))
    return bool_entities and bool_lang and bool_sensitive


if __name__ == '__main__':
    # API connection
    conf = Configuration()
    authentification = tweepy.OAuthHandler(
        conf.CONSUMER_KEY, conf.CONSUMER_SECRET)
    authentification.set_access_token(
        conf.ACCESS_TOKEN, conf.ACCESS_TOKEN_SECRET)
    api = tweepy.API(authentification)
    log = {}  # Used for logs, sending by mail, sms ...
    TIME_SLEEP, TOTAL_RT, MAX_RECOVERED = 10, 3, 50
    recovered, send = 0, 1
    while True:
        # Randomly selected a request contained in the `SEARCH` variable
        random_query = '(' + conf.SEARCH[randint(0, len(conf.SEARCH) - 1)
                                         ] + ') lang:en OR lang:fr filter:safe'
        print(random_query)
        for tweet in tweepy.Cursor(
                api.search, q=random_query,
                result_type="recent").items(TOTAL_RT):
            recovered += 1
            if recovered > MAX_RECOVERED:
                print("Too much research !!")
                log['error'] = {"error": True,
                                "message": "Too much research !!"}
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
        if send >= TOTAL_RT:
            break

    # Create and send LOG
    logger = Logger()
    logger.file(log)
