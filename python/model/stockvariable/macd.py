#!/usr/bin/env python
__author__ = "Kevin & Samuel"
__version__ = "0.1.0"

# Class calculate MACD

import pandas as pd
import datetime

# Calculate EMA based on historical data
def get_EMA(df,N):  
    for i in range(len(df)):  
        if i==0:  
            df.ix[i,'ema']=df.ix[i,'Close']  
#            df.ix[i,'ema']=0  
        if i>0:  
            df.ix[i,'ema']=(2*df.ix[i,'Close']+(N-1)*df.ix[i-1,'ema'])/(N+1)  
    ema=list(df['ema'])  
    return ema  

# Return calculated macd value
def get_MACD(df,fast_period=12,slow_period=26,signal_period=9):  
    a=get_EMA(df,fast_period)  
    b=get_EMA(df,slow_period)  
    df['diff']=pd.Series(a)-pd.Series(b)  
    #print(df['diff'])  
    for i in range(len(df)):  
        if i==0:  
            df.ix[i,'dea']=df.ix[i,'diff']  
        if i>0:  
            df.ix[i,'dea']=((signal_period-1)*df.ix[i-1,'dea']+2*df.ix[i,'diff'])/(signal_period+1)  
    df['macd']=2*(df['diff']-df['dea'])  
    return df  

# Set string value to macd flag
def get_macd_flag(macd_value):
	if (macd_value>=0):
		return 'Bullish'
	else:
		return 'Bearish'

# Return macd historical accuracy 
def get_macd_accuracy(macd_result):
    reversed_macd_df = macd_result.iloc[::-1]
    checkpoint = 0
    current_flag = ""
    for index, row in reversed_macd_df.iterrows():
    	macd = row[10]
    	if ( current_flag!= "" and get_macd_flag(macd)!=current_flag):
    		break
    	current_flag = get_macd_flag(macd)
    	checkpoint+=1
#    print("checkpoint:"+str(checkpoint))
#    print("current_flag:"+str(current_flag))

    successful_times=0
    failure_times=0
    temp_checkpoint=0
    temp_flag = ""
    temp_close_price = 0
    find_right_position = False
    for index, row in macd_result.iterrows():    	
    	close_price = row[2]
    	macd = row[10]
    	flag = get_macd_flag(macd)
#    	print("date: "+str(row[1]))
#    	print("close_price:"+str(close_price))
#    	print("flag:"+str(flag))
#    	print("macd:" +str(macd))
#   	print("temp_close_price:"+str(temp_close_price))
#    	print("temp_flag:"+str(temp_flag))
    	   	
    	if (temp_flag==""):
#    		print("inital")
    		temp_flag=flag
    		temp_close_price = close_price
    	else:
    		if temp_flag==flag:
    			temp_checkpoint+=1
#    			print("temp_checkpoint:"+str(temp_checkpoint))
    			if find_right_position:
    				if(temp_close_price<=close_price):
    					successful_times+=1
#    					print("Bullish")
    				else:
    					failure_times+=1
#    					print("Bearish")    					
    				find_right_position=False
    		else:
    			temp_checkpoint=0


    	if temp_flag==current_flag and temp_checkpoint==checkpoint:
    		find_right_position=True
 #   		print("___________________________right position")

    	temp_close_price = close_price
    	temp_flag = flag
  #  	print("****************************************")


    if 	successful_times>0:
    	return str(round(successful_times/(successful_times+failure_times)*100,2))+"%("+str((successful_times+failure_times))+")"
    else:
    	return "NULL"


def buy(price,amount):
	left = amount%price
	share = (amount-left)/price
	amount = amount-share*price
	return share,amount

def sell(price,amount,share):
	amount+=price*share
	share = 0
	return share,amount

def get_macd_chance(macd_result):
    amount=10000
    share=0
    previous_flag = ""
    previous_close_price = ""
    buy_flag=False
    sell_flag=False
    first_year = 0
    number_of_trade=0
    for index, row in macd_result.iterrows():  

    	close_price = row[2]
    	start_price = row[5]
    	macd = row[10]
    	date = row[1]
    	if first_year==0:
    		first_year=str(date)[0:4]
    	print("date: "+str(date)+"start_price: "+str(start_price)+" close_price: "+str(close_price)+" macd: "+str(macd))
    	flag = get_macd_flag(macd)	
    	if buy_flag:
    		share,amount = buy(start_price,amount)
    		print("BUY "+str(share)+" shares, money left:"+ str(amount))
    		buy_flag=False
    		number_of_trade+=1

    	if sell_flag:
    		print("Sell "+str(share)+" shares")
    		share,amount = sell(start_price,amount,share)
    		print("Amount:"+ str(amount))
    		sell_flag=False
    		number_of_trade+=1

    	if(previous_flag == "" and flag=="Bullish" and share==0):
    		buy_flag=True

    	if(previous_flag!= flag and flag=="Bullish" and share==0):
    		buy_flag=True

    	if(previous_flag!= flag and flag=="Bearish" and share!=0):
    		sell_flag=True    		

    	previous_flag = flag
    	previous_close_price = close_price

    print("after all amount:"+str(amount+share*previous_close_price))
    rate = (amount+share*previous_close_price)/10000
    today = datetime.datetime.now()
    currentYear = today.year
    year = currentYear-int(first_year)
    annual_gain = pow(rate,1.0/year)-1
    return str(round(annual_gain,4)*100)+"%("+str(number_of_trade)+")"


