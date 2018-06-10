#!/usr/bin/env python

__author__ = "Kevin & Samuel"
__version__ = "0.1.0"

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tweepy
import time
from util_libs import common_functions
from datetime import datetime
import logging
import logging.config
from datetime import datetime, timezone
import pytz
from util_libs import db_manager
from util_libs import config_parser

# Get configuration from setting.ini file
cf_parser=config_parser.get_settings()
consumer_key=cf_parser.get('TWITTERAPI', 'consumer_key')
consumer_secret=cf_parser.get('TWITTERAPI', 'consumer_secret')
access_token=cf_parser.get('TWITTERAPI', 'access_token')
access_token_secret=cf_parser.get('TWITTERAPI', 'access_token_secret')

logging_directory=cf_parser.get('DEFAULT', 'logging_directory')


# Get logging setting
logging.config.fileConfig(logging_directory)
logger_name = "crawler"
logger = logging.getLogger(logger_name)

# Set up twitter api connection
logger.info('set up twitter api')
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
logger.info('set up twitter api done')

# sleep 15 mins if reach api limitation
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.TweepError as e:
            logger.info(str(e))
            print("Sleeping 15 mins...")
            for i in range(1,15):
                if i%5==1 and i > 1:
                    common_functions.print_no_newline(' ')
                common_functions.print_no_newline('*')
                time.sleep(60)
        except Exception as e:
            if not str(e):
                pass
            logger.info(str(e))
            raise

db_client=db_manager.db_manager()
cur = db_client.get_cursor()
cnx=db_client.get_connect()
max_db_id=db_client.get_max_id()
# TODO move all sql into lib functions
add_tweet = ("INSERT INTO doubi.Demo(id, text, followers_count, favorite_count, retweet_count,created_at) VALUES (%s, %s, %s, %s, %s, %s)")
logger.info("Starting dump into mysql")
for status in limit_handled(tweepy.Cursor(api.search,
                            q='Tesla',
                            include_entities=True,
                            since_id=max_db_id,
                            lang="en").items()):
    try:
        created_at_eastern=status.created_at.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')
        tweet= (status.id, status.text.strip(), status.user.followers_count, status.favorite_count, status.retweet_count, created_at_eastern)
        cur.execute(add_tweet,tweet)
        cnx.commit()
    except Exception as e:
        logger.info(str(e))

db_client.close()
print("Crawler Done")
