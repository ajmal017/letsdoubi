#!/usr/bin/env python
__author__ = "Kevin & Samuel"
__version__ = "0.1.0"

# Class that provide stock price related info

import datetime
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web

# Using morningstar as the default provider.
provider = 'morningstar'

# get stock daily info by the stock symbol
def get_stock_daily_info_by_symbol(symbol):
	# get all data after 2000/1/1 to today
	end = datetime.date.today()
	start = end - datetime.timedelta(days=365*50)

	prices = web.DataReader(symbol, provider, start, end)
	prices = prices.reset_index(level=None, drop=False)
	return prices


def get_yahoo_stock_daily_info_by_symbol(symbol):
	# get all data after 2000/1/1 to today
	end = datetime.date.today()
	start = end - datetime.timedelta(days=365)

	prices = web.DataReader(symbol, provider, start, end)
	prices = prices.reset_index(level=None, drop=False)
	return prices

# test use only...
if __name__ == "__main__":  
    prices = get_yahoo_stock_daily_info_by_symbol("TSLA")
    print(prices)