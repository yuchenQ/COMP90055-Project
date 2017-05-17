#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import couchdb
from info import db_info


class DataBaseManager(object):
    def __init__(self, database):
        couchdb_uri = db_info[database]['uri']
        db_name = db_info[database]['db_name']
        try:
            self.server = couchdb.Server(couchdb_uri)
            self.db = self.server.create(db_name)
        except couchdb.http.PreconditionFailed:
            self.db = self.server[db_name]

    def save_tweet(self, tw):
        """save tweets to couchdb"""
        try:
            self.db.save(tw)
        except couchdb.HTTPError as e:
            print("[Error!] on couchdb: {}".format(e))

    def not_exist(self, tid):
        """check replicated tweets"""
        return self.db.get(tid) is None
