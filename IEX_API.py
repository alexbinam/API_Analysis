# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 14:46:00 2018

@author: alexa
"""

import requests


symbol = input("Enter a symbol: ")


##Print current price of stock

url_stock="https://api.iextrading.com/1.0/stock/" + symbol + "/chart/1d"

StockInfo = requests.get(url_stock)

json_StockInfo = StockInfo.json()



print("Current Price: " + '${:,.2f}'.format(json_StockInfo[-1]["marketClose"]))

##Print highest closing price over the last month

url_stock="https://api.iextrading.com/1.0/stock/" + symbol + "/chart/1m"

StockInfo = requests.get(url_stock)

json_StockInfo = StockInfo.json()

value = 0
for i in range(len(json_StockInfo)):
    if json_StockInfo[i]["close"] > value:
        value = json_StockInfo[i]["close"] 
print("Highest Closing Price over Last Month: " + '${:,.2f}'.format(value))
 
##Print highest closing price over the last year

       
url_stock="https://api.iextrading.com/1.0/stock/" + symbol + "/chart/1y"

StockInfo = requests.get(url_stock)

json_StockInfo = StockInfo.json()

value = 0
for i in range(len(json_StockInfo)):
    if json_StockInfo[i]["close"] > value:
        value = json_StockInfo[i]["close"] 
print("Highest Closing Price over Last Year: " + '${:,.2f}'.format(value))

###Prints Gainers, Losers

url_stock="https://api.iextrading.com/1.0/stock/market/list/gainers"

StockInfo = requests.get(url_stock)

json_StockInfo = StockInfo.json()
print("\n")
print("Top Gainers: ")
for i in range(len(json_StockInfo)):
    print(json_StockInfo[i]["companyName"])

url_stock="https://api.iextrading.com/1.0/stock/market/list/losers"

StockInfo = requests.get(url_stock)

json_StockInfo = StockInfo.json()

print("\n")  
print("Top Losers: ")
for i in range(len(json_StockInfo)):
    print(json_StockInfo[i]["companyName"])

#Print Crypto Currencies

url_stock="https://api.iextrading.com/1.0/stock/market/crypto"

StockInfo = requests.get(url_stock)

json_StockInfo = StockInfo.json()

print("\n")
value = 0
value = float(value)
for i in range(len(json_StockInfo)):
    if json_StockInfo[i]["changePercent"] > value:
        value = json_StockInfo[i]["close"] 
        company = json_StockInfo[i]["companyName"]
print("Highest Change in Percent for Cryptocurrency: " + 
      company + "," + str(value))

print("\n")
value = 0
value = float(value)
for i in range(len(json_StockInfo)):
    if json_StockInfo[i]["changePercent"] < value:
        value = json_StockInfo[i]["close"]
        company = json_StockInfo[i]["companyName"]
print("Lowest Change in Percent for Cryptocurrency: " + 
      company + "," + str(value))

