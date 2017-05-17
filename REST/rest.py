#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# usage:
# Scraping via REST_API with cities and query
# localhost:
# python3 Rest_api/rest.py -g new_york -l en -db db_us &
# python3 Rest_api/rest.py -g los_angeles -l en -db db_us

import re
import time
import tweepy
import argparse
from textblob import TextBlob
from info import city, db_info
from db_manager import DataBaseManager
from twitter_client import get_twitter_oauth_api, get_twitter_app_api

maxTweets = 1000000000
tweetsPerQry = 100
tweetCount = 0
max_id = -1
num = 0


def get_parser():
    """
    Get parser for command line arguments.
    Return: parser obj
    """
    parser = argparse.ArgumentParser(description="REST API Downloader")
    parser.add_argument("-g",
                        "--geo",
                        dest="geo",
                        help="geocode",
                        default='-')
    parser.add_argument("-l",
                        "--lang",
                        dest="lang",
                        help="set_language",
                        default='-')
    parser.add_argument("-db",
                        "--database",
                        dest="database",
                        help="database",
                        default='-')
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


def main():
    global tweetsPerQry
    global tweetCount
    global maxTweets
    global max_id
    global num

    oauth_api = get_twitter_oauth_api()
    app_api = get_twitter_app_api()
    user = oauth_api.me()

    arg_parser = get_parser()
    args = arg_parser.parse_args()
    db = DataBaseManager(args.database)
    location = args.geo
    query = city[location]['query']
    print("-- Name: {} -- ID: {}".format(user.name, user.id))
    print("-- Geo scope: {} {}".format(location, city[location]['geocode']))
    print("Start Downloading max {} tweets...\n".format(maxTweets))

    while tweetCount < maxTweets:
        try:
            if max_id <= 0:
                new_tweets = app_api.search(q=query, lang=args.lang, count=tweetsPerQry,
                                            geocode=city[location]['geocode'])
            else:
                new_tweets = app_api.search(q=query, count=tweetsPerQry,
                                            lang=args.lang, max_id=str(max_id - 1),
                                            geocode=city[location]['geocode'])
            if not new_tweets:
                print("[Warning!] No more relevant tweets found!")
                print('Reset searching index...\n')
                time.sleep(60)
                max_id = -1
                continue

            for status in new_tweets:
                format_tweet = info_select(status, TextBlob(status.text))
                if db.not_exist(format_tweet['_id']):
                    db.save_tweet(format_tweet)
                    num = add(1)

            tweetCount += len(new_tweets)
            print(" -- Processing: Scraping {0}-{1} tweets"
                  .format(str(tweetCount-len(new_tweets)), tweetCount))
            print(" -- Processing: Collecting {} tweets\n".format(str(num)))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("[TweepError!] : " + str(e))
            time.sleep(10)
            continue
        except KeyboardInterrupt as ex:
            # Or however you want to exit this loop
            print('You cancel the program! {}\n'.format(ex))
            print("Temporary Results:")
            print("Scraped all {0} tweets, collected {1} of them, "
                  "saved to {2}".format(tweetCount, str(num), db_info[args.database]['uri']))
            break
        except Exception as exx:
            print("[Exception!] : " + str(exx))
            continue

    print("Final Results:")
    print("Scraped all {0} tweets, collected {1} of them, "
          "saved to {2}".format(tweetCount, str(num), db_info[args.database]['uri']))


if __name__ == '__main__':
    main()
