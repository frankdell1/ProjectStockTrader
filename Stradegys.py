# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 18:16:51 2021

@author: Frank Garcia
"""


import talib

from Indicator import tester

buy_signals = []
buy_signals2 = []
buy_signalsG = []
sell_signalsG = []




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
            
    def redAndBlue(self):
        name='redAndBlue'
        pos=0
        num=0
        total=0
        for i in self.straPack.index:
            
            cmin=min(self.straPack["EMA_3"][i],self.straPack["EMA_5"][i],self.straPack["EMA_8"][i],self.straPack["EMA_10"][i],self.straPack["EMA_12"][i],self.straPack["EMA_15"][i],)
            cmax=max(self.straPack["EMA_30"][i],self.straPack["EMA_35"][i],self.straPack["EMA_40"][i],self.straPack["EMA_45"][i],self.straPack["EMA_50"][i],self.straPack["EMA_60"][i],)
            
            close=self.straPack["Adj Close"][i]
            
            if(cmin>cmax):
                if(pos==0):
                    bp=close
                    pos=1
                    
                    buy_signalsG.append(self.straPack["Adj Close"][i])
                    print("Buying now at "+str(bp))
                    
            elif(cmin<cmax):
                if(pos==1):
                    pos=0
                    sp=close
                    sell_signalsG.append(self.straPack["Adj Close"][i])
                    print("Selling now at "+str(sp))
                    total+=1
                    
            if(num==self.straPack['Adj Close'].count()-1 and pos==1):
                pos=0
                sp=close
                print("Selling now at "+str(sp))
                total+=1
                sell_signalsG.append(self.straPack["Adj Close"][i])
                    
            num+=1
            
        return buy_signalsG,sell_signalsG,total,name


            
gameplan=Stradegys(tester).bolStra()
gameplanB=Stradegys(tester).basicMaStra()    
gameplanG=Stradegys(tester).redAndBlue()  
# print(gameplanG)
    
       
 
