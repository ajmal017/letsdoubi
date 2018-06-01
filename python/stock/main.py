#!/usr/bin/env python
__author__ = "Kevin & Samuel"
__version__ = "0.1.0"

import os.path  
import tornado.httpserver  
import tornado.web  
import tornado.ioloop  
import tornado.options  
import mysql.connector
import sys
sys.path.append('../lib') 
import mysql_connection 
from tornado.options import define, options  
  
define("port", default=8888, help="run port", type=int)  
define("mysql_host", default="127.0.0.1", help="db host")  
define("mysql_database", default="doubi", help="db name")  
define("mysql_user", default="devUser", help="db user")  
define("mysql_password", default="Doubi12#", help="db password")  
  
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates")  
STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")  
  
l=[] 

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
        self.db = mysql_connection.get_connect(options.mysql_user,options.mysql_password,options.mysql_host,options.mysql_database)
        tornado.web.Application.__init__(self, handlers, **settings)  

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html",items=l)

    def post(self):
        symbol=self.get_argument('symbol')  
        symbol=str(symbol)  
        l.append(symbol)  
        self.render('index.html',title='haha',items=l) 
  
def main():  
    tornado.options.parse_command_line()  
    app = tornado.httpserver.HTTPServer(Application())  
    app.listen(options.port)  
    tornado.ioloop.IOLoop.instance().start()  
  
if __name__ == "__main__":  
    main()  