# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 22:21:39 2017

@author: shtang.2014
"""
import pandas_datareader.data as pdr
from datetime import datetime
from dateutil.relativedelta import relativedelta

today = datetime.now()
#then = today - datetime.timedelta(days=3*365)
noOfYears = 3
three_yrs_ago = datetime.now() - relativedelta(years=noOfYears)
print (today)
print(three_yrs_ago)
#stock=pdr.get_data_google('AAPL',three_yrs_ago, today)

#EXAMPLE- retrieve data for Apple
df = pdr.DataReader("AAPL", 'yahoo', three_yrs_ago, today) 

print(df)
#get a list of close values within the time period for the calculation for Sharpe ratio 
#print(list(df['Close']))

returnList = []

#calculate the average returns based on the current day's price and the previous day price 
for i in range(len(list(df['Close']))): 
    if(i < len(list(df['Close'])) - 1):
        first = list(df['Close'])[i]
        second = list(df['Close'])[i + 1]
        averageReturn = (second - first) / first 
        returnList.append(averageReturn)

print(returnList)
  