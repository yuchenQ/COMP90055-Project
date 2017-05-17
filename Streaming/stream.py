#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# usage:
# python3 streaming/stream.py -db local_au -l en -c melbourne
# python3 streaming/stream.py -db local_us -l en -c melbourne
# python3 streaming/stream.py -db db_au -l en -c melbourne
# python3 streaming/stream.py -db db_us -l en -c melbourne

import re
import sys
import time
import random
import argparse
from tweepy import Stream
from textblob import TextBlob
from http.client import IncompleteRead
from db_manager import DataBaseManager
from tweepy.streaming import StreamListener
from twitter_client import get_twitter_auth, get_twitter_api
from info import city, queries


def get_parser():
    """
    Get parser for command line arguments.
    Return: parser obj
    """
    parser = argparse.ArgumentParser(description="Streaming_backup Downloader")
    parser.add_argument("-db",
                        "--database",
                        dest="database",
                        help="database",
                        default='-')
    parser.add_argument("-l"
                        "--lang",
                        dest="lang",
                        help="set_language",
                        default="en")
    parser.add_argument("-c"
                        "--city",
                        dest="city",
                        help="set_city",
                        default="-")
    return parser


def underline_to_space(query_string):
    """
     Convert underline in word to space
     Return: string
    """
    if "_" in query_string:
        return query_string.replace("_", " ")
    else:
        return query_string


def add(n, total=[]):
    """
    count the num to make index
    Return: the next index
    """
    m = 0
    if total:
        m = total[-1]
    total.append(m + n)
    return total[-1]


def judge():
    """
    random demo
    """
    if random.random() > 0.5:
        return True
    else:
        return False


def get_coords(status, place_dict=dict(), place_coords=dict()):
    """
     get the coordinates from dict status._json, if it is not None
     Return: coordinates or None
    """
    status_dict = status._json
    if status_dict['coordinates'] is not None:
        xy = status_dict['coordinates']
        return xy
    elif status_dict['place'] is not None:
        place_dict.update(status_dict['place'])
        place_coords.update(place_dict['bounding_box'])
        box = place_coords['coordinates'][0]
        xy = [(box[0][0] + box[2][0]) / 2, (box[0][1] + box[2][1]) / 2]
        return xy
    else:
        return None


def get_country(status, place_dict=dict()):
    """
     get the country from dict status._json, if it is not None
     Return: country name or None
    """
    status_dict = status._json
    if status_dict['place'] is not None:
        place_dict.update(status_dict['place'])
        return place_dict['country']
    else:
        return None


def get_city(status, place_dict=dict()):
    """
    get the city from dict status._json, if it is not None
    Return: city name or None
    """
    status_dict = status._json
    if status_dict['place'] is not None:
        place_dict.update(status_dict['place'])
        return place_dict['name']
    else:
        return None


def get_lang(status):
    """
    get the language from dict status._json, if it is not None
    Return: language type
    """
    status_dict = status._json
    return status_dict['lang']


def get_date(str_time):
    """
    Get the only date, such as 2017-04-11 08:12:38.
    Return: only date without time, such that 2017-04-11
    """
    str_lst = str_time.split(' ', 1)
    return str_lst[0]


def remove_emoji(text):
    """
     replace the emoji in string by '--emoji--'
     Return: a string without emoji
     """
    highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    text_noem = highpoints.sub('--emoji--', text)
    return text_noem


def info_select(status, testimonial):
    """
    select the info we need and wrap it by json format
    Return: a dict all_info
    """
    all_info = dict()
    # set the tweet id
    all_info['_id'] = status.id_str
    # set the content of tweet
    all_info['tweet_text'] = remove_emoji(status.text)
    # set the time for tweet
    all_info['created_at'] = str(status.created_at)
    all_info['date'] = get_date(str(status.created_at))
    # set user screen_name
    all_info['screen_name'] = status.user.screen_name
    # set the favorite_count
    all_info['favorite_count'] = str(status.favorite_count)
    # set the retweet_count
    all_info['retweet_count'] = str(status.retweet_count)
    # set the polarity
    all_info['polarity'] = testimonial.sentiment.polarity
    # set the subjectivity
    all_info['subjectivity'] = testimonial.sentiment.subjectivity
    return all_info


def is_trump_tweet(query, format_tweet):
    """
    check whether the tweet is related to trump
    Return: True or False
    """
    for q in query:
        if q in format_tweet['tweet_text']:
            return True
    return False


class MyListener(StreamListener):
    """
    Subclass of StreamListener for streaming data
    """
    def __init__(self, api, lang, db):
        self.api = api
        self.lang = lang
        self.db = db
        super(StreamListener, self).__init__()

    def on_status(self, status):
        try:
            format_tweet = info_select(status, TextBlob(status.text))
            # make sure english tweets and no duplicated tweets
            if get_lang(status) == self.lang and \
                    self.db.not_exist(format_tweet['_id']):
                # filter tweets which is not relative to trump
                if is_trump_tweet(queries, format_tweet):
                    self.db.save_tweet(format_tweet)
                    num = add(1)
                    print(" -- No.%s statu/tweet has been collected --" % str(num))
                else:
                    pass
            else:
                pass
        except BaseException as e:
            sys.stderr.write("[Error!] on_status: {}\n".format(e))
            time.sleep(30)

        return True

    def on_error(self, status_code):
        """if error 420 happens, comtinue the program running"""
        if status_code == 420:
            sys.stderr.write("[Error!] Rate limit exceeded\n".format(status_code))
            time.sleep(15*60)
            return True
        else:
            sys.stderr.write("[Error!] {}\n".format(status_code))
            return True

    def on_timeout(self):
        """Don't kill the stream"""
        sys.stderr.write("[Warning!] Timeout...")
        time.sleep(30)
        return True


def main():
    api = get_twitter_api()
    user = api.me()
    sys.stderr.write("-- Name: %s -- ID: %s \n" % (user.name, user.id))
    arg_parser = get_parser()
    args = arg_parser.parse_args()

    auth = get_twitter_auth()
    sys.stderr.write("Start scraping tweets:...\n")
    while True:
        try:
            # start using Streaming API to collect data:
            twitter_stream = \
                Stream(auth, MyListener(api, args.lang, DataBaseManager(args.database)))
            twitter_stream.filter(locations=city[args.city])
        except IncompleteRead as e:
            sys.stderr.write('[Error!] on IncompleteRead {}\n'.format(e))
            time.sleep(10)
            continue
        except KeyboardInterrupt as ex:
            # Or however you want to exit this loop
            sys.stderr.write('You cancel the program! {}\n'.format(ex))
            break
        except Exception as ept:
            sys.stderr.write('[Error!] on Exception {}\n'.format(ept))
            time.sleep(10)
            continue

if __name__ == '__main__':
    main()
