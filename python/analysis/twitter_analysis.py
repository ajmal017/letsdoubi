import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from util_libs import common_functions
from util_libs import db_manager
from model.twitter import tweet_sentiment
from datetime import date, timedelta

db_client=db_manager.db_manager()

for n in range(1, 2):
    ndate = date.today() - timedelta(n)
    year = str(ndate.year)
    month = str('%02d' % ndate.month)
    day = str('%02d' % ndate.day)
    print(year+ "-" + month + "-" + day)
    db_client.get_count_by_period(1,ndate,1,15)
