import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
from mysql.connector import errorcode
from textblob import TextBlob
import statistics
from util_libs import common_functions
from util_libs import config_parser
# TODO dn management should not call this ...
from model.twitter import tweet_sentiment
from datetime import date, datetime, time, timedelta

class db_manager:
    # inistialized database
    def __init__(self):
        cf_parser = config_parser.get_settings()
        usr = cf_parser.get('MYSQL', 'user')
        pswd = cf_parser.get('MYSQL', 'password')
        hst = cf_parser.get('MYSQL', 'host')
        db = cf_parser.get('MYSQL', 'database')
        try:
            self.cnx = mysql.connector.connect(user=usr, password=pswd,host=hst,database=db)
        except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    self.connected=0
                    self.connectInfo="failed to connect to "+hst+", authentication fails"
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    self.connected=0
                    self.connectInfo="failed to connect to "+hst+" for databse:"+db
                else:
                    self.connected=0
                    self.connectInfo="failed to connect to "+hst
        else:
            self.connected=1
            self.connectInfo="succeed!"
            self.cur = self.cnx.cursor()
            #make sure cur is using utfmb4
            self.cur.execute('SET NAMES utf8mb4')
            self.cur.execute("SET CHARACTER SET utf8mb4")
            self.cur.execute("SET character_set_connection=utf8mb4")

    def close(self):
        self.cur.close()
        self.cnx.close()

    def get_connect(self):
        return self.cnx

    def get_cursor(self):
        return self.cur

    def get_count_by_date(self,ignore_zero,year,month,date):
        self.cur.execute("select text,followers_count from Demo where created_at>"+"'"+year+"-"+month+"-"+date+"' and created_at<"+"'"+year+"-"+month+"-"+date+" 99:99:99'")
        plain_count=0
        tweet_polarity=list()
        tweet_weight_polarity = list()
        for(text) in self.cur:
            polarity=TextBlob(text[0]).sentiment.polarity
            if ignore_zero==0:
              tweet_polarity.append(polarity)
              tweet_weight_polarity.append(polarity * text[1])
            else:
               if polarity!=0.0:
                   tweet_polarity.append(polarity)
                   tweet_weight_polarity.append(polarity * text[1])
               else:
                  plain_count += 1
        median = statistics.median(tweet_polarity)
        mean = statistics.mean(tweet_polarity)
        weighted_median=statistics.median(tweet_weight_polarity)
        weight_mean=statistics.mean(tweet_weight_polarity)
        count = len(tweet_polarity)
        result = tweet_sentiment.tweet_sentiment(median, mean,weighted_median,weight_mean,count, plain_count)
        return result

    #get the count by some period like per 15 mintes,ignore_zero is the flag to ignore polarity 0.0 (1,1,15)
    def get_count_by_period(self, ignore_zero, date, days_block, minutes_block):
        add_twitterAnalysisByFifteenMin = ("INSERT INTO doubi.TeslaTwitterAnalysisBy"+common_functions.int_to_en(days_block)+"Day"+common_functions.int_to_en(minutes_block)+"Min(date,yyyymm,day,hour,quarters,median,mean,weighted_median,weighted_mean,count,zero_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s , %s, %s, %s)")
        begin_date = datetime(int(date.year), int(date.month), int(date.day), 0, 0)
        end_date = begin_date + timedelta(days=days_block)
        # from 1 to 4
        quarters = 0
        while begin_date < end_date:
            #initial list each loop
            tweet_polarity = list()
            tweet_weight_polarity = list()
            zero_count = 0
            sql=("select text,followers_count from Demo where created_at>='" + str(begin_date) + "'" + " and created_at<'" + str(begin_date + timedelta(minutes=minutes_block)) + "'")
            self.cur.execute(sql)
            #tweet_info[0]:text  tweet_info[1]:followers_count
            for(tweet_info) in self.cur:
                polarity=TextBlob(tweet_info[0]).sentiment.polarity
                if ignore_zero==0:
                  tweet_polarity.append(polarity)
                  tweet_weight_polarity.append(polarity * tweet_info[1])
                else:
                   if polarity!=0.0:
                       tweet_polarity.append(polarity)
                       tweet_weight_polarity.append(polarity * tweet_info[1])
                   else:
                      zero_count += 1
            if len(tweet_polarity) == 0:
                median=0
                mean=0
            else:
                median = statistics.median(tweet_polarity)
                mean = statistics.mean(tweet_polarity)
            if len(tweet_weight_polarity) == 0:
                weighted_median=0
                weight_mean=0
            else:
                weighted_median=statistics.median(tweet_weight_polarity)
                weight_mean=statistics.mean(tweet_weight_polarity)

            count = len(tweet_polarity)
            twitterAnalysis=(str(begin_date + timedelta(minutes=minutes_block)-timedelta(seconds=1)),(str( '%02d' % begin_date.year)+"-"+str( '%02d' % begin_date.month)),'%02d' % begin_date.day,'%02d' % begin_date.hour,(quarters%4+1),median,mean,weighted_median,weight_mean,count,zero_count)
            self.cur.execute(add_twitterAnalysisByFifteenMin, twitterAnalysis)
            quarters+=1
            begin_date += timedelta(minutes=minutes_block)
        self.cnx.commit()


    def get_max_id(self):
        self.cur.execute("select max(id) from Demo")
        return self.cur.fetchone()[0]
