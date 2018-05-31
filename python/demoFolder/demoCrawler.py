import tweepy
import time
import mysql.connector
import sys
from datetime import datetime

consumer_key = 'duXvAgTq4VdLcL2iEi539krNQ'
consumer_secret = 'FjZlUXWqeIDLIa02oAgdRZuln6ErQtY1cRWNcZZfkstbdjBTh0'
access_token = '1025683382-AqdI8Wm115vQXhhXz02Lrpg9Xrh9hxAguRryaLX'
access_token_secret = '3jmSNxSCtUmEJ8VmWRRY9iCuOCFze35Epu48L8ssxDNcv'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
logger=open("crawler.log", "a")
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.TweepError as e:
            logger.write(str(datetime.now())+": "+str(e) + "\n")
            time.sleep(15 * 60)
        except Exception as e:
            if not str(e):
                pass
            logger.write(str(datetime.now()) + ": " + str(e) + "\n")
            raise

cnx = mysql.connector.connect(user='devUser', password='Doubi12#',host='127.0.0.1',database='doubi')
cursor = cnx.cursor()

add_tweet = ("INSERT INTO doubi.Demo(id, text, followers_count, favorite_count, retweet_count,created_at) VALUES (%s, %s, %s, %s, %s, %s)")

for status in limit_handled(tweepy.Cursor(api.search,
                            q='gtx 1070',
                            include_entities=True,
                            lang="en").items(10)):
    try:
        tweet= (status.id, status.text, status.user.followers_count, status.favorite_count, status.retweet_count, status.created_at)
        cursor.execute(add_tweet,tweet)
        cnx.commit()
    except Exception as e:
        logger.write(str(datetime.now()) + ": " + str(e) + "\n")

logger.close()
cnx.close()
