# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 03:20:11 2021

@author: Frank Garcia
"""

import datetime
datet=datetime.datetime.today()

from stockData import df

smaUsed=[20,50,100,200]
emaUsed=[21]

pivots=[]
dates=[]

lastPivot=0
 


class Indicator():
    def __init__(self,dataStock):
        self.dataStock=dataStock
    
    def ma(self):
        for x in smaUsed:
            sma=x
            self.dataStock["SMA_"+str(sma)]=round(self.dataStock.iloc[:,4].rolling(window=sma).mean(),2)
        return self.dataStock
            
    
        for x in emaUsed:
            ema=x
            self.dataStock["EMA_"+str(ema)]=round(self.dataStock.iloc[:,4].ewm(span=ema,adjust=False).mean(),2)
        return self.dataStock
    
    def bol(self):
        self.dataStock=self.ma()
        self.dataStock['20dSTD'] = self.dataStock['Close'].rolling(window=20).std() 

        self.dataStock['Upper'] = self.dataStock['SMA_20'] + (self.dataStock['20dSTD'] * 2)
        self.dataStock['Lower'] = self.dataStock['SMA_20'] - (self.dataStock['20dSTD'] * 2)
        return self.dataStock
    
    def pivot(self):
        dateRange=[0,0,0,0,0,0,0,0,0,0]
        Range=[0,0,0,0,0,0,0,0,0,0]
        counter=0
        for i in self.dataStock.index:
            currentMax=max(Range,default=0)
            value=round(self.dataStock["High"][i],2)
            
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
        
        return pivots,dates
    
    def fullPack(self):
        self.dataStock=self.bol()
        return self.dataStock
        

tester=Indicator(df).fullPack()
testerP=Indicator(df).pivot()
print('New World')
print(testerP[0])


        

