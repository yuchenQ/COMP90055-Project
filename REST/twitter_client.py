#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import tweepy


def get_twitter_oauth_auth():
    """
    Setup Twitter authentication.
    Return: tweepy.OAuthHandler object
    """
    try:
        consumer_key = os.environ['TWITTER_CONSUMER_KEY']
        consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
        access_token = os.environ['TWITTER_ACCESS_TOKEN']
        access_secret = os.environ['TWITTER_ACCESS_SECRET']
    except KeyError:
        sys.exit('Cannot found the twitter environment variables!\n')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth


def get_twitter_app_auth():
    """
    Setup Twitter authentication.
    Return: tweepy.AppAuthHandler object
    """
    try:
        consumer_key = os.environ['TWITTER_CONSUMER_KEY']
        consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    except KeyError:
        sys.exit('Cannot found the twitter environment variables!\n')
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    return auth


def get_twitter_oauth_api():
    """
    Setup Twitter OAuth API client.
    Return: tweepy.OAuth API object
    """
    auth = get_twitter_oauth_auth()
    api = tweepy.API(auth)
    return api


def get_twitter_app_api():
        """
        Setup Twitter App API client.
        Return: tweepy.App API object
        """
        auth = get_twitter_app_auth()
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        if not api:
            print("Can't Authenticate")
            sys.exit(-1)
        return api
