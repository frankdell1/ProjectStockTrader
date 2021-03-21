# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 01:46:51 2021

@author: Frank Garcia
"""
# DOGE-USD
import os, csv
import talib
import yfinance as yf
import pandas as pd
from pandas_datareader import data as pdr
import numpy as np
import sqlite3 as sql
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import matplotlib.gridspec as gridspec

import datetime
datet=datetime.datetime.today()

yf.pdr_override()

startDate="2020-01-01"
endDate=str(datet.date())

stockChoice="BA"

buy_signals = []
buy_signals2 = []
dateLister = []
dateLister2 = []
priceSeller = []
priceSeller2 = []

AvgGain=15
AvgLoss=5
smaUsed=[20,50,100,200]
emaUsed=[21]

j=0
z=0

# data=yf.download(stockChoice, startDate,endDate)

# df=pd.DataFrame(data)


class DataBase():
    def __init__(self,ticker,days):
        self.ticker = ticker
        
        data=pdr.get_data_yahoo(stockChoice, startDate,endDate,interval = "1d")
        self.df=pd.DataFrame(data)
        pd.set_option('display.max_columns',None)
        self.df[self.df.index.dayofweek < 5]
        self.df=self.df[-days:]
        
        
       
        
    def quote(self):
        return self.df
    
    
db=DataBase(stockChoice,252)
df=db.quote()




# timeD=df.timedelta(days=30)
# for index in range(len(pivots)):
#     print(str(pivots[index])+": "+str(dates[index]))
#     plt.plot_date([dates[index],dates[index]+timeD],[pivots[index],
#                       pivots[index]],linestyle='-',linewidth=2,marker=',')


pivots=[]
dates=[]
counter=0
lastPivot=0
 
dateRange=[0,0,0,0,0,0,0,0,0,0]
Range=[0,0,0,0,0,0,0,0,0,0]

close=df["Adj Close"][-1]
maxStop=close*((100-AvgLoss)/100)
Target1R=round(close*((100+AvgGain)/100),2)
Target2R=round(close*((100+(2*AvgGain))/100),2)
Target3R=round(close*((100+(3*AvgGain))/100),2)

for x in smaUsed:
    sma=x
    df["SMA_"+str(sma)]=round(df.iloc[:,4].rolling(window=sma).mean(),2)
    
for x in emaUsed:
    ema=x
    df["EMA_"+str(ema)]=round(df.iloc[:,4].ewm(span=ema,adjust=False).mean(),2)

df['20dSTD'] = df['Close'].rolling(window=20).std() 

df['Upper'] = df['SMA_20'] + (df['20dSTD'] * 2)
df['Lower'] = df['SMA_20'] - (df['20dSTD'] * 2)


sma50=round(df["SMA_50"][-1],2)
sma200=round(df["SMA_200"][-1],2)
ema21=round(df["EMA_21"][-1],2)
low5=round(min(df["Low"].tail(5)),2)

pf50=round(((close/sma50)-1)*100,2)
check50=df["SMA_50"][-1]>maxStop
pf200=round(((close/sma200)-1)*100,2)
check200=((close/df["SMA_200"][-1])-1)*100>100
pf21=round(((close/ema21)-1)*100,2)
check21=df["EMA_21"][-1]>maxStop 
pfl=round(((close/low5)-1)*100,2)
checkl=low5>maxStop 

print()
print("Current Stock: "+stockChoice+" Price: "+str(round(close,2)))
print("21 EMA: "+str(ema21)+ " | 50 SMA: "+str(sma50)+ " | 200 SMA: "+str(sma200)+ " | 5 day Low: "+str(low5))
print("-------------------------------------------------")
print("Max Stop: "+str(round(maxStop,2)))
print("Price Targets:") 
print("1R: "+str(Target1R))
print("2R: "+str(Target2R))
print("3R: "+str(Target3R))
print("From 5 Day Low "+ str(pfl)+ "% -Within Max Stop: "+str(checkl))
print("From 21 day EMA "+ str(pf21)+ "% -Within Max Stop: "+str(check21))
print("From 50 day SMA "+ str(pf50)+ "% -Within Max Stop: "+str(check50))
print("From 200 Day SMA "+ str(pf200)+ "% -In Danger Zone (Over 100% from 200 SMA): "+str(check200))
# print(df['Low'])


for i in range(1,len(df['Adj Close'])):
    if df['SMA_20'][i]>df['Low'][i] and (df['SMA_20'][i]-df['Low'][i])>0.03*df['Low'][i]:
        # print("Hey this one")
        # print(df['Low'][i])
        buy_signals.append(df['Low'][i])
        # print(buy_signals)



for i in df.index:
    currentMax=max(Range,default=0)
    value=round(df["High"][i],2)
           
    Range=Range[1:9]
    Range.append(value)
    dateRange=dateRange[1:9]
    dateRange.append(i)
    
    if currentMax==max(Range,default=0):
        counter+=1
        
    else:
        counter=0
               
    if counter==5:
        lastPivot=currentMax
        dateloc=Range.index(lastPivot)
        lastDate=dateRange[dateloc]
               
        pivots.append(lastPivot)
        dates.append(lastDate)
        
timeD=datetime.timedelta(days=30)

    
# for i in range(1,len(df['Adj Close'])-1):        
#     buy_price=0.8* df['SMA_20'][i]
#     if buy_price >= df['Close'][i]:
#         buy_signals2.append(df['Close'][i])
#         buy_signals2.append(df['Close'][i]*1.045)
#         print('10% below 20 ma')
    
for i in range(1,len(df['Adj Close'])-1):
    buy_price2=0.98*df['Lower'][i]
    # print(buy_price2)
    if buy_price2 >= df['Close'][i]:
        buy_signals2.append(df['Close'][i])
        buy_signals2.append(df['Close'][i]*1.045)
        print('5% below lower bolliger band')
    
for i in range(1,len(df['Low'])):
    # print("Helloosdasd")
    # print(i)
    # print(df['Low'][i])
    if j< len(buy_signals):
        if buy_signals[j]==df['Low'][i]:
            # print(df.index[i])
            dateLister.append(df.index[i])
            priceSeller.append(df['Low'][i]*1.02 )
            # print(dateLister)
            # print(i)
            # print(j)
            j=j+1
    #     print(df['Low'][i])
     # a.c1[a.c1 == 8].index.tolist()
     
     
for i in range(1,len(df['Close'])):
    # print("Helloosdasd")
    # print(i)
    # print(df['Low'][i])
    # print(len(buy_signals2))
    # print(z)
    if z< len(buy_signals2):
        if buy_signals2[z]==df['Close'][i]:
            print('this boy')
            # print(df.index[i])
            dateLister2.append(df.index[i])
            dateLister2.append(df.index[i])
            priceSeller2.append(df['Close'][i]*1.02 )
            priceSeller2.append(df['Close'][i]*1.02 )
            
            # print(i)
            # print(j)
            z=z+1
    #     print(df['Low'][i])
     # a.c1[a.c1 == 8].index.tolist()

# print('this boy lister')
# print(dateLister)
# print('this boy2 buyer')
# print(buy_signals)
# print('this boy2 seller')
# print(priceSeller)

print('this boy lister')
print(dateLister2)
print('this boy2 buyer')
print(buy_signals2)
print('this boy2 seller')
print(priceSeller2)


pivot_high_1=df['High'][-21:-1].max()
pivot_high_2=df['High'][-55:-22].max()
pivot_low_1=df['Low'][-21:-1].min()
pivot_low_2=df['Low'][-55:-22].min()

A=[df['High'][-21:-1].idxmax(), pivot_high_1]
B=[df['High'][-55:-22].idxmax(), pivot_high_2]

A1=[df['Low'][-21:-1].idxmin(), pivot_low_1]
B1=[df['Low'][-55:-22].idxmin(), pivot_low_2]

x1_high_values = [A[0], B[0]]
y1_high_values = [A[1], B[1]]

x1_low_values = [A1[0], B1[0]]
y1_low_values = [A1[1], B1[1]]

 


fig, ax1 = plt.subplots(figsize=(14,7))

ax1.set_ylabel('Price in $')
ax1.set_xlabel('Date')
ax1.set_title('DOGE COIN')
ax1.plot('Adj Close',data=df, label='Close Price', linewidth=0.5, color='blue')
# Adj Close
ax1.plot('SMA_20',data=df, label='SMA 20', linewidth=0.5, color='darkred')
ax1.plot('SMA_50',data=df, label='SMA 50', linewidth=0.5, color='purple')
ax1.plot('SMA_100',data=df, label='SMA 100', linewidth=0.5, color='cyan')
ax1.plot('SMA_200',data=df, label='SMA 200', linewidth=0.5, color='deeppink')
ax1.plot('Lower',data=df, label='low_ball', linewidth=0.5, color='pink')
           
    
# print(buy_signals)
# df['BuyPrice']=buy_signals
ax1.plot(dateLister,buy_signals,'o',data=df, linewidth=0.9, color='green', label='SMA Basic Buy')
ax1.plot(dateLister,priceSeller,'o',data=df, linewidth=0.9, color='red', label='SMA Basic Sell')

# k
ax1.plot(dateLister2,buy_signals2,'o',data=df, linewidth=0.9, color='black', label='bolliger band Buy')
ax1.plot(dateLister2,priceSeller2,'o',data=df, linewidth=0.9, color='orange', label='bolliger band Sell')

ax1.plot(x1_high_values, y1_high_values, color='g', linestyle='--', linewidth=0.5, label='Trend resistance')
ax1.plot(x1_low_values, y1_low_values, color='r', linestyle='--', linewidth=0.5, label='Trend support')

ax1.axhline(y=pivot_high_1, color='g', linewidth=6, label='First resistance line', alpha=0.2)
ax1.axhline(y=pivot_low_1, color='r', linewidth=6, label='First support line', alpha=0.2)
trans = transforms.blended_transform_factory(ax1.get_yticklabels()[0].get_transform(), ax1.transData)
ax1.text(0,pivot_high_1, "{:.2f}".format(pivot_high_1), color="g", transform=trans,ha="right", va="center")
ax1.text(0,pivot_low_1, "{:.2f}".format(pivot_low_1), color="r", transform=trans,ha="right", va="center")

ax1.legend()
ax1.grid()

for index in range(len(pivots)):
    print(str(pivots[index])+": "+str(dates[index]))
    plt.plot_date([dates[index],dates[index]+timeD],[pivots[index],
                      pivots[index]],linestyle='-',linewidth=2,marker=',')
plt.show()

# print(df)

 


