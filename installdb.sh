#!/bin/sh
sudo apt-get update
sudo apt-get install software-properties-common -y
sudo add-apt-repository ppa:couchdb/stable -y
sudo apt-get update
sudo apt-get remove couchdb couchdb-bin couchdb-common -yf
sudo apt-get install couchdb -y
sudo stop couchdb
sudo chown -R couchdb:couchdb /usr/lib/couchdb /usr/share/couchdb /etc/couchdb /usr/bin/couchdb
sudo chmod -R 0770 /usr/lib/couchdb /usr/share/couchdb /etc/couchdb /usr/bin/couchdb
sudo start couchdb
sudo couchdb -c