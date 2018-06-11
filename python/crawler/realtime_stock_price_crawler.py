#!/usr/bin/env python
__author__ = "Kevin & Samuel"
__version__ = "0.1.0"

import urllib
import urllib.request
import re
import chardet # check encode type
import html
import datetime
import sys
import time
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from util_libs import common_functions
from util_libs import config_parser

from apscheduler.schedulers.blocking import BlockingScheduler

# Get configuration from configparser
cf_parser=config_parser.get_settings()
mysql_user=cf_parser.get('MYSQL', 'user')
mysql_password=cf_parser.get('MYSQL', 'password')
mysql_host=cf_parser.get('MYSQL', 'host')
mysql_database=cf_parser.get('MYSQL', 'database')

nasdaq_url='https://www.nasdaq.com/symbol/%s/real-time'


def get_real_stock_price():
    now = datetime.datetime.now()
    today_930 = now.replace(hour=9, minute=30, second=0, microsecond=0)
    today_400 = now.replace(hour=4, minute=0, second=0, microsecond=0)

    current_minute = datetime.datetime.now().strftime("%H:%M")
    current_date = datetime.datetime.now().strftime("%Y%m%d")

    # Read nasdaq file
    f = urllib.request.urlopen(nasdaq_url%"TSLA").read()

    # Change encoding
    encode_type = chardet.detect(f)  
    f = f.decode(encode_type['encoding'])

    # Get price
    price_reg = r'quotes_content_left__LastSale.{1,50}</span>'
    price_text_re = re.compile(price_reg,re.S)
    price_text_match = re.findall(price_text_re,f)

    for i in range(len(price_text_match)):
        text = price_text_match[i]
        if text and text.strip():
            number_reg = r'>.{1,50}</'
            number_re = re.compile(number_reg,re.S)
            price = re.findall(number_re,text)[0][1:-2]

    # Get volumn
    volume_reg = r'quotes_content_left__Volume.{1,50}</span>'
    volume_re = re.compile(volume_reg,re.S)
    volume_match = re.findall(volume_re,f)

    for i in range(len(volume_match)):
        text = volume_match[i]
        if text and text.strip():
            number_reg = r'>.{1,50}</'
            number_re = re.compile(number_reg,re.S)
            volume = int(re.findall(number_re,text)[0][1:-2].replace(",", ""))

#    print("%s price: %s volume: %s"%(current_minute,price,str(volume)))
#    return price,volume

    if (now>=today_930 and now<=today_400):
        with open('../web/static/data/tesla_'+current_date+'.txt', 'a') as the_file:
            the_file.write(current_minute+','+str(price)+','+str(volume)+'\n')

scheduler = BlockingScheduler()
scheduler.add_job(get_real_stock_price, 'cron', day_of_week='mon-fri', hour='9-17', minute='0-59')
scheduler.start()