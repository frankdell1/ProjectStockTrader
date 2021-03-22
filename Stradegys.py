# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 18:16:51 2021

@author: Frank Garcia
"""


import talib

from Indicator import tester

buy_signals = []
buy_signals2 = []


class Stradegys():
    def __init__(self,straPack):
        self.straPack=straPack
        
    def maStra(self):
        for i in range(1,len(self.straPack['Adj Close'])-1):        
            buy_price=0.8* self.straPack['SMA_20'][i]
            if buy_price >= self.straPack['Close'][i]:
                buy_signals2.append(self.straPack['Close'][i])
                buy_signals2.append(self.straPack['Close'][i]*1.045)
                print('10% below 20 ma')
        
        return buy_signals2
    
    def bolStra(self):
        for i in range(1,len(self.straPack['Adj Close'])-1):        
            buy_price2=0.98* self.straPack['Lower'][i]
            if buy_price2 >= self.straPack['Close'][i]:
                buy_signals2.append(self.straPack['Close'][i])
                buy_signals2.append(self.straPack['Close'][i]*1.045)
                print('5% below lower bolliger band')
        
        return buy_signals2
    
    def basicMaStra(self):
        for i in range(1,len(self.straPack['Adj Close'])):
            if self.straPack['SMA_20'][i]>self.straPack['Low'][i] and (self.straPack['SMA_20'][i]-self.straPack['Low'][i])>0.03*self.straPack['Low'][i]:
                buy_signals.append(self.straPack['Low'][i])
                
        return buy_signals
            
            
gameplan=Stradegys(tester).bolStra()
gameplanB=Stradegys(tester).basicMaStra()        
    
       
        
