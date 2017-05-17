#!/usr/bin/env python3
# -*- coding: utf-8 -*-

db_info = {
    'local_au': {
        'uri': 'http://yuchenq:qiaoyc17@127.0.0.1:5984/',
        'db_name': 'au'
    },
    'local_us': {
        'uri': 'http://yuchenq:qiaoyc17@127.0.0.1:5984/',
        'db_name': 'us'
    },
    'db_au': {
        'uri': 'http://yuchenq:qiaoyc17@115.146.93.126:5984/',
        'db_name': 'au'
    },
    'db_us': {
        'uri': 'http://yuchenq:qiaoyc17@115.146.93.126:5984/',
        'db_name': 'us'
    },
}

queries = ['trump','#PresidentTrump',
           '#TRUMP','#DonaldJTrump',
           'US President','Donald Trump',
           'Mr. President','@realDonaldTrump',
           '@POTUS','#Trumprussia']

city = {
    'melbourne': [144.74,-37.93,145.21,-37.76],
    'sydney': [150.98,-33.96,151.29,-33.76],
    'brisbane': [152.91,-27.55,153.09,-27.34],
    'perth': [115.70,-32.03,116,-31.79],
    'adelaide': [138.46,-35.15,138.65,-34.81],
    'canberra': [149.04,-35.35,149.14,-35.25],
    'new_york': [-74,40,-73,41],
    'los_angles': [-118.42,33.92,-118.47,34.12],
    'chicago': [-87.73,41.74,-87.62,41.91],
    'houston': [-95.61,29.66,-95.25,29.87]
}

