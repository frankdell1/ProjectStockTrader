# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 23:52:16 2021

@author: Frank Garcia
"""


import talib

import datetime
datet=datetime.datetime.today()

from stockData import stockChoice
from Indicator import tester
from Stradegys import gameplan
from Stradegys import gameplanB
from Stradegys import gameplanG

dateLister = []
dateLister2 = []
priceSeller = []
priceSeller2 = []
percentchange=[]
sellingG=[]
buyingB=[]

j=0
z=0

class BuyerandSeller():
    def __init__(self,betBot,gameplan,gameplanB,gameplanG):
        self.betBot=betBot
        
    def date(self):
        z=0
        for i in range(1,len(self.betBot['Adj Close'])):
            if z< len(gameplan):
                if gameplan[z]==self.betBot['Close'][i]:
                    dateLister2.append(tester.index[i])
                    dateLister2.append(tester.index[i])
                    priceSeller2.append(tester['Close'][i]*1.02 )
                    priceSeller2.append(tester['Close'][i]*1.02 )

                    z=z+1
        return dateLister2,priceSeller2
    
    def dateB(self):
        j=0
        for i in range(1,len(self.betBot['Low'])):
            if j< len(gameplanB):
                if gameplanB[j]==self.betBot['Low'][i]:
                    dateLister.append(self.betBot.index[i])
                    priceSeller.append(self.betBot['Low'][i]*1.02 )

                    j=j+1

        return dateLister,priceSeller
    
    def placer(self):
        sellingG=gameplanG[1]
        buyingB=gameplanG[0]
        ridr=str(gameplanG[2])

        for i in range(int(ridr)):
            pc=(sellingG[i]/buyingB[i]-1)*100
            percentchange.append(pc)
            
        return percentchange
    
    def profitAndLose(self):
        percentchange=self.placer()
        print(percentchange)
        gains=0
        ng=0
        losses=0
        nl=0
        totalR=1
        
        for i in percentchange:
            if(i>0):
                gains+=i
                ng+=1
            else:
                losses+=i
                nl+=1
            totalR=totalR*((i/100)+1)
            
        totalR=round((totalR-1)*100,2)
        
        if(ng>0):
            avgGain=gains/ng
            maxR=str(max(percentchange))
        else:
            avgGain=0
            maxR="undefined"
            
        if(nl>0):
            avgLoss=losses/nl
            maxL=str(min(percentchange))
            ratio=str(-avgGain/avgLoss)
        else:
            avgLoss=0
            maxL='undefined'
            ratio='inf'
            
        if(ng>0 or nl>0):
            battingAvg=ng/(ng+nl)
        else:
            battingAvg=0
            
        print()
        print("Stradegy Used: "+gameplanG[3])
        print("Results for "+ stockChoice +" going back to "+str(self.betBot.index[0])+", Sample size: "+str(ng+nl)+" trades")
        # print("EMAs used: "+str(emasUsed))
        print("Batting Avg: "+ str(battingAvg))
        print("Gain/loss ratio: "+ ratio)
        print("Average Gain: "+ str(avgGain))
        print("Average Loss: "+ str(avgLoss))
        print("Max Return: "+ maxR)
        print("Max Loss: "+ maxL)
        print("Total return over "+str(ng+nl)+ " trades: "+ str(totalR)+"%" )
        #print("Example return Simulating "+str(n)+ " trades: "+ str(nReturn)+"%" )
        print()
        
        return totalR
        

execute=BuyerandSeller(tester,gameplan,gameplanB,gameplanG).date()
executeB=BuyerandSeller(tester,gameplan,gameplanB,gameplanG).dateB()
executeG=BuyerandSeller(tester,gameplan,gameplanB,gameplanG).profitAndLose()
    
print(executeG)        
