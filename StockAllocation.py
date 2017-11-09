# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 23:27:15 2017

@author: shtang.2014
"""
from copy import deepcopy

PercentageGlobalMap = {}

def getInvestDecision(StockMap, selection, Amount):
    #StockMap = {'AAPL': -0.882234433136, 'MSFT': -0.895106903701, 'AZPN': -0.767119686675}
    s = sorted(StockMap.items(), key=lambda x: x[1], reverse = True) #sorting by value - descending; if reverse = false, its ascending 

    #selection = 3 #varies according to UI selection 
    selectedStockMap = {}
    #looping through for loop from the first element 
    for i in range(0, selection): 
        value = s[i] 
        selectedStockMap[value[0]] = value[1]

    print(selectedStockMap)

    #deep copy to ensure stock name and its original sharpe ratio remains unchanged 
    PercentageMap = deepcopy(selectedStockMap) 
    AllocationMap = deepcopy(selectedStockMap)

    Total_Sharpe = sum(selectedStockMap.values())
    print (Total_Sharpe)

    for k,v in PercentageMap.items():
        Weightage = v/Total_Sharpe
        PercentageMap.update({k:Weightage})
    
    global PercentageGlobalMap
    PercentageGlobalMap = PercentageMap 
    print (PercentageMap)

    #for example if user enter $100,000 into Amount
    #Amount = 100_000
    for k,v in PercentageMap.items():
        Allocation = Amount*v
        AllocationMap.update ({k:Allocation})

    print (AllocationMap)
    print(selectedStockMap)
    #return {'AZPN': 30.14861220456742, 'AAPL': 34.67274306753944, 'MSFT': 35.178644727893136}
    return AllocationMap

#getInvestDecision({'AAPL': -0.882234433136, 'MSFT': -0.895106903701, 'AZPN': -0.767119686675}, 1212)

