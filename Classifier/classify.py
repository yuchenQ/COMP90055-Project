#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# usage:
# Extract from local database:

# Writing the amount of data into csv file:
# python3 Get_data/classify.py -db local -m 0

# Writing the info of AU from database au into csv file:
# python3 Get_data/classify.py -db local -m 1

# Writing the info of USA from database us into csv file:
# python3 Get_data/classify.py -db local -m 2

# Get the number of different attitudes in AU:
# python3 Get_data/classify.py -db local -m 3

# Get the number of different attitudes in USA:
# python3 Get_data/classify.py -db local -m 4

# Get the number of objective/subjective tweets which support/oppose in AU:
# python3 Get_data/classify.py -db local -m 5

# Get the number of objective/subjective tweets which support/oppose in USA:
# python3 Get_data/classify.py -db local -m 6

# Get the number of different attitudes in AU with like and retweet:
# python3 Get_data/classify.py -db local -m 7

# Get the number of different attitudes in USA with like and retweet:
# python3 Get_data/classify.py -db local -m 8

# Get the number of objective/subjective tweets which support/oppose in AU with retweet:
# python3 Get_data/classify.py -db local -m 9

# Get the number of objective/subjective tweets which support/oppose in USA with retweet:
# python3 Get_data/classify.py -db local -m 10

# Extract from local database:
# python3 Get_data/classify.py -db db -m 0...

import csv
import couchdb
import argparse
from config import db_info, dates


def get_parser():
    """
    Get parser for command line arguments.
    Return: parser obj
    """
    parser = argparse.ArgumentParser(description="Data Analysis Processor")
    parser.add_argument("-db",
                        dest="db",
                        help="database",
                        default='-')
    parser.add_argument("-m",
                        dest="m",
                        help="mission",
                        default='-')
    return parser


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


def get_date(str_time):
    """
    Get the only date, such as 2017-04-11 08:12:38.
    Return: only date without time, such that 2017-04-11
    """
    str_lst = str_time.split(' ', 1)
    return str_lst[0]


def chart_amount_0(db_au, db_us):
    """
    Writing the amount of data into csv file.
    """
    au_count = str(db_au.info()['doc_count'])
    us_count = str(db_us.info()['doc_count'])
    headers = ['au_count', 'us_count']
    rows = [(au_count, us_count)]

    with open('Data/0_chart_amount_tweets.csv', 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows)

    print('-- Mission 0 Accomplished!')


def chart_au_info_1(db_au):
    """
    Writing the info of AU from database au into csv file.
    """
    headers = ['au', 'subjectivity', 'polarity', 'created_at', 'date']
    with open('Data/1_chart_au_info.csv', 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        for t_id in db_au:
            tweet = db_au.get(t_id)
            subjectivity = tweet['subjectivity']
            polarity = tweet['polarity']
            created_at = tweet['created_at']
            date = tweet['date']

            rows = [('au', subjectivity, polarity, created_at, date)]
            f_csv.writerows(rows)
            print('- No.{} tweet has been preserved!'.format(add(1)))

    print('-- Mission 1 Accomplished!')


def chart_us_info_2(db_us):
    """
    Writing the info of USA from database us into csv file.
    """
    headers = ['us', 'subjectivity', 'polarity', 'created_at', 'date']
    with open('Data/2_chart_us_info.csv', 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        for t_id in db_us:
            tweet = db_us.get(t_id)
            subjectivity = tweet['subjectivity']
            polarity = tweet['polarity']
            created_at = tweet['created_at']
            date = tweet['date']

            rows = [('us', subjectivity, polarity, created_at, date)]
            f_csv.writerows(rows)
            print('- No.{} tweet has been preserved!'.format(add(1)))

    print('-- Mission 2 Accomplished!')


def chart_num_attitude_au_3(db_au):
    """
    Get the number of different attitudes in AU
    """
    headers = ['au', 'date', 'num_pos', 'num_neg', 'num_neu', 'num_all']
    with open('Data/3_chart_num_attitude_au.csv', 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)

    for day in dates:
        pos = 0
        neg = 0
        neu = 0
        map_fun_pos = '''function(doc) {
                    if (doc.date=="%s" && doc.polarity>0)
                    emit(doc.polarity);
                    };''' % day
        map_fun_neg = '''function(doc) {
                    if (doc.date=="%s" && doc.polarity<0)
                    emit(doc.polarity);
                    };''' % day
        map_fun_neu = '''function(doc) {
                    if (doc.date=="%s" && doc.polarity==0)
                    emit(doc.polarity);
                    };''' % day

        for row in db_au.query(map_fun_pos):
            pos += 1
        for row in db_au.query(map_fun_neg):
            neg += 1
        for row in db_au.query(map_fun_neu):
            neu += 1
        num_all = pos + neg + neu

        with open('Data/3_chart_num_attitude_au.csv', 'a') as f:
            rows = [('au', day, pos, neg, neu, num_all)]
            f_csv = csv.writer(f)
            f_csv.writerows(rows)

    print('-- Mission 3 Accomplished!')


def chart_num_attitude_us_4(db_us):
    """
    Get the number of different attitudes in USA
    """
    headers = ['us', 'date', 'num_pos', 'num_neg', 'num_neu', 'num_all']
    with open('Data/4_chart_num_attitude_us.csv', 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)

    for day in dates:
        pos = 0
        neg = 0
        neu = 0
        map_fun_pos = '''function(doc) {
                    if (doc.date=="%s" && doc.polarity>0)
                    emit(doc.polarity);
                    };''' % day
        map_fun_neg = '''function(doc) {
                    if (doc.date=="%s" && doc.polarity<0)
                    emit(doc.polarity);
                    };''' % day
        map_fun_neu = '''function(doc) {
                    if (doc.date=="%s" && doc.polarity==0)
                    emit(doc.polarity);
                    };''' % day

        for row in db_us.query(map_fun_pos):
            pos += 1
        for row in db_us.query(map_fun_neg):
            neg += 1
        for row in db_us.query(map_fun_neu):
            neu += 1
        num_all = pos + neg + neu

        with open('Data/4_chart_num_attitude_us.csv', 'a') as f:
            rows = [('us', day, pos, neg, neu, num_all)]
            f_csv = csv.writer(f)
            f_csv.writerows(rows)

    print('-- Mission 4 Accomplished!')


def chart_attitude_obj_au_5(db_au):
    """
    Get the number of objective/subjective tweets which support/oppose in AU
    """
    sup_obj = 0
    sup_sub = 0
    ops_obj = 0
    ops_sub = 0

    map_fun_sup_obj = '''function(doc) {
                if (doc.subjectivity<0.5 && doc.polarity>0)
                emit(doc.subjectivity, doc.polarity);
                };'''
    map_fun_sup_sub = '''function(doc) {
                if (doc.subjectivity>0.5 && doc.polarity>0)
                emit(doc.subjectivity, doc.polarity);
                };'''
    map_fun_ops_obj = '''function(doc) {
                if (doc.subjectivity<0.5 && doc.polarity<0)
                emit(doc.subjectivity, doc.polarity);
                };'''
    map_fun_ops_sub = '''function(doc) {
                if (doc.subjectivity>0.5 && doc.polarity<0)
                emit(doc.subjectivity, doc.polarity);
                };'''

    for row in db_au.query(map_fun_sup_obj):
        sup_obj += 1
    for row in db_au.query(map_fun_sup_sub):
        sup_sub += 1
    for row in db_au.query(map_fun_ops_obj):
        ops_obj += 1
    for row in db_au.query(map_fun_ops_sub):
        ops_sub += 1
    sup_num_all = sup_obj + sup_sub
    ops_num_all = ops_obj + ops_sub

    with open('Data/5_chart_attitude_obj_au.csv', 'w') as f:
        headers = ['au_attitude', 'num_obj', 'num_sub', 'num_all']
        row_1 = [('support', sup_obj, sup_sub, sup_num_all)]
        row_2 = [('oppose', ops_obj, ops_sub, ops_num_all)]

        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(row_1)
        f_csv.writerows(row_2)

    print('-- Mission 5 Accomplished!')


def chart_attitude_obj_us_6(db_us):
    """
    Get the number of objective/subjective tweets which support/oppose in USA
    """
    sup_obj = 0
    sup_sub = 0
    ops_obj = 0
    ops_sub = 0

    map_fun_sup_obj = '''function(doc) {
                if (doc.subjectivity<0.5 && doc.polarity>0)
                emit(doc.subjectivity, doc.polarity);
                };'''
    map_fun_sup_sub = '''function(doc) {
                if (doc.subjectivity>0.5 && doc.polarity>0)
                emit(doc.subjectivity, doc.polarity);
                };'''
    map_fun_ops_obj = '''function(doc) {
                if (doc.subjectivity<0.5 && doc.polarity<0)
                emit(doc.subjectivity, doc.polarity);
                };'''
    map_fun_ops_sub = '''function(doc) {
                if (doc.subjectivity>0.5 && doc.polarity<0)
                emit(doc.subjectivity, doc.polarity);
                };'''

    for row in db_us.query(map_fun_sup_obj):
        sup_obj += 1
    for row in db_us.query(map_fun_sup_sub):
        sup_sub += 1
    for row in db_us.query(map_fun_ops_obj):
        ops_obj += 1
    for row in db_us.query(map_fun_ops_sub):
        ops_sub += 1
    sup_num_all = sup_obj + sup_sub
    ops_num_all = ops_obj + ops_sub

    with open('Data/6_chart_attitude_obj_us.csv', 'w') as f:
        headers = ['au_attitude', 'num_obj', 'num_sub', 'num_all']
        row_1 = [('support', sup_obj, sup_sub, sup_num_all)]
        row_2 = [('oppose', ops_obj, ops_sub, ops_num_all)]

        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(row_1)
        f_csv.writerows(row_2)

    print('-- Mission 6 Accomplished!')


def chart_num_attitude_retweet_au_7(db_au):
    """
    Get the number of different attitudes in AU with like and retweet count
    """
    headers = ['au', 'date', 'num_pos', 'num_neg', 'num_neu', 'num_all']
    with open('Data/7_chart_num_attitude_retweet_au.csv', 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)

    for day in dates:
        pos = 0
        neg = 0
        neu = 0
        map_fun_pos = '''function(doc) {
                    if (doc.date=="%s" && doc.polarity>0)
                    emit(doc.favorite_count,doc.retweet_count);
                    };''' % day
        map_fun_neg = '''function(doc) {
                    if (doc.date=="%s" && doc.polarity<0)
                    emit(doc.favorite_count,doc.retweet_count);
                    };''' % day
        map_fun_neu = '''function(doc) {
                    if (doc.date=="%s" && doc.polarity==0)
                    emit(doc.favorite_count,doc.retweet_count);
                    };''' % day

        for row in db_au.query(map_fun_pos):
            pos += int(row.key) + int(row.value) + 1
        for row in db_au.query(map_fun_neg):
            neg += int(row.key) + int(row.value) + 1
        for row in db_au.query(map_fun_neu):
            neu += int(row.key) + int(row.value) + 1
        num_all = pos + neg + neu

        with open('Data/7_chart_num_attitude_retweet_au.csv', 'a') as f:
            rows = [('au', day, pos, neg, neu, num_all)]
            f_csv = csv.writer(f)
            f_csv.writerows(rows)

    print('-- Mission 7 Accomplished!')


def chart_num_attitude_retweet_us_8(db_us):
    """
    Get the number of different attitudes in USA with like and retweet count
    """
    headers = ['us', 'date', 'num_pos', 'num_neg', 'num_neu', 'num_all']
    with open('Data/8_chart_num_attitude_retweet_us.csv', 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)

    for day in dates:
        pos = 0
        neg = 0
        neu = 0
        map_fun_pos = '''function(doc) {
                    if (doc.date=="%s" && doc.polarity>0)
                    emit(doc.favorite_count,doc.retweet_count);
                    };''' % day
        map_fun_neg = '''function(doc) {
                    if (doc.date=="%s" && doc.polarity<0)
                    emit(doc.favorite_count,doc.retweet_count);
                    };''' % day
        map_fun_neu = '''function(doc) {
                    if (doc.date=="%s" && doc.polarity==0)
                    emit(doc.favorite_count,doc.retweet_count);
                    };''' % day

        for row in db_us.query(map_fun_pos):
            pos += int(row.key) + int(row.value) + 1
        for row in db_us.query(map_fun_neg):
            neg += int(row.key) + int(row.value) + 1
        for row in db_us.query(map_fun_neu):
            neu += int(row.key) + int(row.value) + 1
        num_all = pos + neg + neu

        with open('Data/8_chart_num_attitude_retweet_us.csv', 'a') as f:
            rows = [('us', day, pos, neg, neu, num_all)]
            f_csv = csv.writer(f)
            f_csv.writerows(rows)

    print('-- Mission 8 Accomplished!')


def chart_attitude_obj_retweet_au_9(db_au):
    """
    Get the number of objective/subjective tweets which support/oppose in AU with retweet
    """
    sup_obj = 0
    sup_sub = 0
    ops_obj = 0
    ops_sub = 0

    map_fun_sup_obj = '''function(doc) {
                if (doc.subjectivity<0.5 && doc.polarity>0)
                emit(doc.favorite_count,doc.retweet_count);
                };'''
    map_fun_sup_sub = '''function(doc) {
                if (doc.subjectivity>0.5 && doc.polarity>0)
                emit(doc.favorite_count,doc.retweet_count);
                };'''
    map_fun_ops_obj = '''function(doc) {
                if (doc.subjectivity<0.5 && doc.polarity<0)
                emit(doc.favorite_count,doc.retweet_count);
                };'''
    map_fun_ops_sub = '''function(doc) {
                if (doc.subjectivity>0.5 && doc.polarity<0)
                emit(doc.favorite_count,doc.retweet_count);
                };'''

    for row in db_au.query(map_fun_sup_obj):
        sup_obj += int(row.key) + int(row.value) + 1
    for row in db_au.query(map_fun_sup_sub):
        sup_sub += int(row.key) + int(row.value) + 1
    for row in db_au.query(map_fun_ops_obj):
        ops_obj += int(row.key) + int(row.value) + 1
    for row in db_au.query(map_fun_ops_sub):
        ops_sub += int(row.key) + int(row.value) + 1
    sup_num_all = sup_obj + sup_sub
    ops_num_all = ops_obj + ops_sub

    with open('Data/9_chart_attitude_obj_retweet_au.csv', 'w') as f:
        headers = ['au_attitude', 'num_obj', 'num_sub', 'num_all']
        row_1 = [('support', sup_obj, sup_sub, sup_num_all)]
        row_2 = [('oppose', ops_obj, ops_sub, ops_num_all)]

        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(row_1)
        f_csv.writerows(row_2)

    print('-- Mission 9 Accomplished!')


def chart_attitude_obj_retweet_us_10(db_us):
    """
    Get the number of objective/subjective tweets which support/oppose in USA with retweet
    """
    sup_obj = 0
    sup_sub = 0
    ops_obj = 0
    ops_sub = 0

    map_fun_sup_obj = '''function(doc) {
                if (doc.subjectivity<0.5 && doc.polarity>0)
                emit(doc.favorite_count,doc.retweet_count);
                };'''
    map_fun_sup_sub = '''function(doc) {
                if (doc.subjectivity>0.5 && doc.polarity>0)
                emit(doc.favorite_count,doc.retweet_count);
                };'''
    map_fun_ops_obj = '''function(doc) {
                if (doc.subjectivity<0.5 && doc.polarity<0)
                emit(doc.favorite_count,doc.retweet_count);
                };'''
    map_fun_ops_sub = '''function(doc) {
                if (doc.subjectivity>0.5 && doc.polarity<0)
                emit(doc.favorite_count,doc.retweet_count);
                };'''

    for row in db_us.query(map_fun_sup_obj):
        sup_obj += int(row.key) + int(row.value) + 1
    for row in db_us.query(map_fun_sup_sub):
        sup_sub += int(row.key) + int(row.value) + 1
    for row in db_us.query(map_fun_ops_obj):
        ops_obj += int(row.key) + int(row.value) + 1
    for row in db_us.query(map_fun_ops_sub):
        ops_sub += int(row.key) + int(row.value) + 1
    sup_num_all = sup_obj + sup_sub
    ops_num_all = ops_obj + ops_sub

    with open('Data/10_chart_attitude_obj_retweet_us.csv', 'w') as f:
        headers = ['au_attitude', 'num_obj', 'num_sub', 'num_all']
        row_1 = [('support', sup_obj, sup_sub, sup_num_all)]
        row_2 = [('oppose', ops_obj, ops_sub, ops_num_all)]

        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(row_1)
        f_csv.writerows(row_2)

    print('-- Mission 10 Accomplished!')


def missions(db_au, db_us, args_m):
    """
    Aim to allocate the mission to relevant functions.
    """
    if args_m is '0':
        chart_amount_0(db_au, db_us)
    elif args_m is '1':
        chart_au_info_1(db_au)
    elif args_m is '2':
        chart_us_info_2(db_us)
    elif args_m is '3':
        chart_num_attitude_au_3(db_au)
    elif args_m is '4':
        chart_num_attitude_us_4(db_us)
    elif args_m is '5':
        chart_attitude_obj_au_5(db_au)
    elif args_m is '6':
        chart_attitude_obj_us_6(db_us)
    elif args_m is '7':
        chart_num_attitude_retweet_au_7(db_au)
    elif args_m is '8':
        chart_num_attitude_retweet_us_8(db_us)
    elif args_m is '9':
        chart_attitude_obj_retweet_au_9(db_au)
    else:
        chart_attitude_obj_retweet_us_10(db_us)
        exit(0)


def main():

    arg_parser = get_parser()
    args = arg_parser.parse_args()

    if args.db == 'local':
        print('----------------------------------------------------------')
        print("Processing data from {}".format(db_info['local_au']['uri']))
        print('----------------------------------------------------------')
        print('-- Start mission {}...'.format(args.m))

        server = couchdb.client.Server(db_info['local_au']['uri'])
        db_au = server[db_info['local_au']['db_name']]
        db_us = server[db_info['local_us']['db_name']]
        missions(db_au, db_us, args.m)
    elif args.db == 'db':
        print("Processing data from {}".format(db_info['db_au']['uri']))
        print('Start mission {}'.format(args.m))

        server = couchdb.client.Server(db_info['db_au']['uri'])
        db_au = server[db_info['db_au']['db_name']]
        db_us = server[db_info['db_us']['db_name']]
        missions(db_au, db_us, args.m)
    else:
        print("[Error!] when direct to the database!")
        exit(0)


if __name__ == '__main__':
    main()
