# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 23:52:16 2021

@author: Frank Garcia
"""


import talib

import datetime
datet=datetime.datetime.today()

from Indicator import tester
from Stradegys import gameplan
from Stradegys import gameplanB

dateLister = []
dateLister2 = []
priceSeller = []
priceSeller2 = []

j=0
z=0

class BuyerandSeller():
    def __init__(self,betBot,gameplan,gameplanB):
        self.betBot=betBot
        
    def date(self):
        z=0
        for i in range(1,len(self.betBot['Adj Close'])):
            if z< len(gameplan):
                if gameplan[z]==self.betBot['Close'][i]:
                    print('this boy')
                    # print(df.index[i])
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
        pass

execute=BuyerandSeller(tester,gameplan,gameplanB).date()
executeB=BuyerandSeller(tester,gameplan,gameplanB).dateB()
        
        
