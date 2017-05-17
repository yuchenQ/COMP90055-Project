#!/bin/sh
sudo apt-get update && sudo apt-get -y upgrade

sudo apt install vim -y
sudo apt install curl -y

sudo apt-get install python3-pip -y
sudo pip3 install --upgrade pip
sudo pip3 install tweepy
sudo pip3 install CouchDB
sudo pip3 install -U textblob
python3 -m textblob.download_corpora

# collector-0:
#python3 Rest_api/rest.py -g melbourne -l en -db db_au &
#python3 streaming/stream.py -db db_au -l en -c melbourne

# collector-1:
#python3 Rest_api/rest.py -g sydney -l en -db db_au &
#python3 streaming/stream.py -db db_au -l en -c sydney

# collector-2:
#python3 Rest_api/rest.py -g brisbane -l en -db db_au &
#python3 Rest_api/rest.py -g perth -l en -db db_au &
#python3 streaming/stream.py -db db_au -l en -c brisbane

# collector-3:
#python3 Rest_api/rest.py -g adelaide -l en -db db_au &
#python3 Rest_api/rest.py -g canberrra -l en -db db_au &
#python3 streaming/stream.py -db db_au -l en -c perth

# couchdb:
#python3 Rest_api/rest.py -g chicago -l en -db db_us &
#python3 Rest_api/rest.py -g houston -l en -db db_us &
#python3 streaming/stream.py -db db_au -l en -c adelaide &
#python3 streaming/stream.py -db db_au -l en -c canberrra &
#python3 streaming/stream.py -db db_us -l en -c new_york &
#python3 streaming/stream.py -db db_us -l en -c los_angeles

# localhost:
#python3 Rest_api/rest.py -g new_york -l en -db db_us &
#python3 Rest_api/rest.py -g los_angeles -l en -db db_us &
#python3 Rest_api/rest_c.py -q au_query -l en -db db_au &
#python3 Rest_api/rest_c.py -q us_query -l en -db db_us &
#python3 streaming/stream.py -db db_us -l en -c chicago &
#python3 streaming/stream.py -db db_us -l en -c houston &
