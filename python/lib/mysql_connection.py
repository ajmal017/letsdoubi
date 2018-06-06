import mysql.connector

def get_connect(usr,pswd,hst,db):
	cnx = mysql.connector.connect(user=usr, password=pswd,host=hst,database=db)
	return cnx

def get_cursor(cnx):
	cur = cnx.cursor()
	cur.execute('SET NAMES utf8mb4')
	cur.execute("SET CHARACTER SET utf8mb4")
	cur.execute("SET character_set_connection=utf8mb4")
	return cur