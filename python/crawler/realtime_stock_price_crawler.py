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
sys.path.append('../lib') 
import common_functions
import mysql_connection
import config_parser


# Get configuration from configparser
cfparser=config_parser.get_settings()
mysql_user=cfparser.get('MYSQL', 'user')
mysql_password=cfparser.get('MYSQL', 'password')
mysql_host=cfparser.get('MYSQL', 'host')
mysql_database=cfparser.get('MYSQL', 'database')

nasdaq_url='https://www.nasdaq.com/symbol/%s/real-time'

cnx = mysql_connection.get_connect(mysql_user,mysql_password,mysql_host,mysql_database)
cur = mysql_connection.get_cursor(cnx)


def get_real_stock_price():

    # Read nasdaq file
    f = urllib.request.urlopen(nasdaq_url%"TSLA").read()

    # Change encoding
    encode_type = chardet.detect(f)  
    f = f.decode(encode_type['encoding'])

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

#    print("%s price: %s volume: %s"%(current_time,price,volume-previous_volume))
    return price,volume


# main method
def main():  

    price,volume = get_real_stock_price()
    print(str(price)+str(volume))
  
if __name__ == "__main__":  
    main()  
