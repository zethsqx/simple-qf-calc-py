# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 22:21:39 2017

@author: shtang.2014
"""
import pandas_datareader.data as pdr
import numpy as np 
import quandl
from datetime import datetime
from dateutil.relativedelta import relativedelta

def getStock(stock):
    ##today = datetime.now()
    #then = today - datetime.timedelta(days=3*365)
    ##noOfYears = 3
    ##three_yrs_ago = datetime.now() - relativedelta(years=noOfYears)
    #print (today)
    #print(three_yrs_ago)
    #stock=pdr.get_data_google('AAPL',three_yrs_ago, today)
    
    #EXAMPLE- retrieve data for Apple
    ##df = pdr.DataReader(stock, 'yahoo', three_yrs_ago, today) 
    
#    print(df)
    df = getStockDF(stock)
    
    returnList = []

    #get a list of close values within the time period for the calculation for Sharpe ratio 
    #calculate the average returns based on the current day's price and the previous day price 
    for i in range(len(list(df['Close']))): 
        if(i < len(list(df['Close'])) - 1):
            first = list(df['Close'])[i]
            second = list(df['Close'])[i + 1]
            averageReturn = (second - first) / first 
            returnList.append(averageReturn)
    
    return returnList;

def getStockDF(stock):
    today = datetime.now()
    noOfYears = 3
    three_yrs_ago = datetime.now() - relativedelta(years=noOfYears)
    
    #EXAMPLE- retrieve data for Apple
    df = pdr.DataReader(stock, 'yahoo', three_yrs_ago, today)
    return df
          
def sharpe(returns):
    """
    Sharpe ratio = (Mean Return - Risk Free Rate)/(Risk)
    Risk is calculated using Standard Deviation. Essentially, sharpe ratio is interpreted as amount of return per unit of risk. 
    The higher the sharpe ratio, the better. 
    Risk free rate is based on US 1-year treasury bill.
    """
    Mean_Return = (np.mean(returns))*100
    rf = quandl.get("FRED/TB1YR", authtoken="VV_5NSuUzyPxy8sgZkzp")
    Risk_Free = (rf['Value'][-1])
    Risk = (np.std(returns))*100
    return (Mean_Return - Risk_Free)/(Risk);

#simple calculation for double checking
#stockList = getStock("AAPL")
#print("Mean", np.mean(stockList))
#print("Std", np.std(stockList))

#value = sharpe(stockList)
#print("sharpe ratio:", value)
    

