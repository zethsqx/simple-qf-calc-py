# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 22:21:39 2017

@author: shtang.2014
"""
import pandas_datareader.data as pdr
import numpy as np
import quandl
import cmath as math
from datetime import datetime
from dateutil.relativedelta import relativedelta
from CustomExceptions import *

stockGlobalMap = {}

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

    df = getStockDF(stock)
    #    print(df)

    returnList = []

    #get a list of close values within the time period for the calculation for Sharpe ratio
    #calculate the average returns based on the current day's price and the previous day price
    for i in range(len(list(df['Close']))):
        if(i < len(list(df['Close'])) - 1):
            first = list(df['Close'])[i]
            second = list(df['Close'])[i + 1]
            averageReturn = (second - first) / first
            returnList.append(averageReturn)

    global stockGlobalMap #declaring it global to update the list for access
    stockGlobalMap.update({stock:returnList})
#    stockGlobalMap[stock] = returnList
    return returnList;

def getStockDF(stock):
    today = datetime.now()
    noOfYears = 1
    one_year_ago = datetime.now() - relativedelta(years=noOfYears)

    #EXAMPLE- retrieve data for Apple
#    df = pdr.DataReader(stock, 'yahoo', one_year_ago, today)
    try:
        df = pdr.DataReader(stock, 'yahoo', one_year_ago, today)
    except RemoteDataError:
        raise ApplicationException('Too many API requests','')
    return df

def sharpe(returns):
    """
    Sharpe ratio = (Mean Return - Risk Free Rate)/(Risk)
    Risk is calculated using Standard Deviation. Essentially, sharpe ratio is interpreted as amount of return per unit of risk.
    The higher the sharpe ratio, the better.
    Risk free rate is based on US 1-year treasury bill.
    252 is the number of trading days in a year for annualisation
    """
    Mean_Return = (np.mean(returns))*100*252
    rf = quandl.get("FRED/TB1YR", authtoken="VV_5NSuUzyPxy8sgZkzp")
    Risk_Free = (rf['Value'][-1])
    Risk = (np.std(returns))*100*((252)**0.5)
    return (Mean_Return - Risk_Free)/(Risk)
def covMatrix(stockList):
    if(len(stockList)>2):
        a = getStock(stockList[0])
        b = getStock(stockList[1])
        vStackArray = np.vstack((a,b))
        for i in range(2,len(stockList))):
            currentStock = getStock(stockList[i])
            vStackArray = np.vstack((vStackArray,currentStock))
    return np.cov(vStackArray,ddof=0)

def portfolioRisk(matrix,weightage):
    result = 0.0
    for a in range(0,len(matrix)):
        for b in range (0,a+1):
            if(b==a):
                result += weightage[b]**2*matrix[a,b]
            else:
                result += matrix[a,b]*weightage[a]*weightage[b]*2
    return math.sqrt(result)

def portfolioCorrelation(matrix,weightage,risk):
    result=risk**2
    bottom=0.0
    for a in range (0,len(matrix)):
        result -= (weightage[a]**2)*(matrix[a,a])
        for b in range (0,a):
            bottom += weightage[a]*weightage[b]*math.sqrt(matrix[a,a])*math.sqrt(matrix[b,b])*2
    result = result/bottom
    print(type(result))
    return result

#simple calculation for double checking
#stockList = getStock("AAPL")
#print(stockGlobalMap)
#print("Mean", np.mean(stockList))
#print("Std", np.std(stockList))

#value = sharpe(stockList)
#print("sharpe ratio:", value)
