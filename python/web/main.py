#!/usr/bin/env python
__author__ = "Kevin & Samuel"
__version__ = "0.1.0"

# Class shows stock analyze on web
import time
import datetime
import os.path
import tornado.httpserver  
import tornado.web  
import tornado.ioloop  
import tornado.options  
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from util_libs import stock_info
from tornado.options import define, options  
from util_libs import forecast_result
from model.stock_variable import macd

define("port", default=8888, help="run port", type=int)
define("mysql_host", default="127.0.0.1", help="db host")
define("mysql_database", default="doubi", help="db name")
define("mysql_user", default="devUser", help="db user")
define("mysql_password", default="Doubi12#", help="db password")
  
# setting web related folder 
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates")  
STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")  

# Initial related configuration such as database
class Application(tornado.web.Application):  
    def __init__(self):  
        handlers = [  
            (r"/", MainHandler),   
        ]  
        settings = dict(  
            template_path = TEMPLATE_PATH,   
            static_path = STATIC_PATH,  
            debug = True  
        )  
        #self.db = mysql_connection.get_connect(options.mysql_user,options.mysql_password,options.mysql_host,options.mysql_database)
        tornado.web.Application.__init__(self, handlers, **settings)  

# change the data to the price that could be read by the UI frame
def changeDataFormat(prices):
    trim_prices = prices[['Date','Close','High','Low','Open','Volume']]
    resultStr="{\"data\":["
    for index, row in trim_prices.iterrows():
        date = row[0]
        date = time.mktime(datetime.datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S").timetuple())
        date = str(round(int(date)))+'000'
        open_price = row[4]
        close_price = row[1]
        high_price = row[2]
        low_price = row[3]
        volume = row[5]
        rowStr = "[%s,%s,%s,%s,%s,%s]," % (date,open_price,high_price,low_price,close_price,volume)
        resultStr=resultStr+rowStr
    resultStr=resultStr[:-1] + "]}"
    return resultStr

# TODO, single stock only now..will update to query by stock symbol
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        datas = []
        prices = stock_info.get_stock_daily_info_by_symbol('TSLA')
        resultStr = changeDataFormat(prices)
        with open("static/data/tsla.json", "w") as text_file:
            text_file.write(resultStr)

        # Get macd result
        #macd_result = macd.get_MACD(prices)
        #macd_flag = macd.get_macd_flag(round(macd_result.iloc[-1]['macd'],2))
        #macd_accuracy = macd.get_macd_accuracy(macd_result)
        #gain_chance = macd.get_macd_chance(macd_result)
        #data = forecast_result.make_result("MACD",macd_flag,macd_accuracy,gain_chance)
        data = forecast_result.make_result("MACD", "TBD", "TBD", "TBD")
        datas.append(data)

        print("refresh")
        self.render("index.html", datas=datas)

    def post(self):
        btd="TBD"


# main method
def main():  
    tornado.options.parse_command_line()  
    app = tornado.httpserver.HTTPServer(Application())  
    app.listen(options.port)  
    tornado.ioloop.IOLoop.instance().start()  
  
if __name__ == "__main__":  
    main()  