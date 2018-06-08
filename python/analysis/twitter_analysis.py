import sys
sys.path.append('../lib')
sys.path.append('../model/twitter')
import common_functions
import configparser
import TweetSentiment
import DBManager
from datetime import date, timedelta
dbClint=DBManager.DBManager()
for n in range(1, 2):
    ndate = date.today() - timedelta(n)
    year = str(ndate.year)
    month = str('%02d' % ndate.month)
    day = str('%02d' % ndate.day)
    print(year+ "-" + month + "-" + day)
    dbClint.get_count_by_period(1,ndate,1,15)
