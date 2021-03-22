# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 03:59:49 2021

@author: Frank Garcia
"""

import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import matplotlib.gridspec as gridspec

import datetime
datet=datetime.datetime.today()

from stockData import df
from Indicator import tester
from Indicator import testerP
from stockData import stockChoice
from BuyerandSeller import execute
from BuyerandSeller import executeB
from Stradegys import gameplan
from Stradegys import gameplanB

class Plotter():
    def __init__(self,stockPlotter,df,testerP,execute,executeB,gameplan,gameplanB):
        self.stockPlotter=stockPlotter
        
    def supRis(self):
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
        
        return x1_high_values,y1_high_values,x1_low_values,y1_low_values,pivot_high_1,pivot_low_1
        
    def display(self):
        x1_high_values,y1_high_values,x1_low_values,y1_low_values,pivot_high_1,pivot_low_1=self.supRis()
        
        fig, ax1 = plt.subplots(figsize=(14,7))
        ax1.set_ylabel('Price in $')
        ax1.set_xlabel('Date')
        ax1.set_title(stockChoice)
        ax1.plot('Adj Close',data=df, label='Close Price', linewidth=0.5, color='blue')
        ax1.plot('SMA_20',data=df, label='SMA 20', linewidth=0.5, color='darkred')
        ax1.plot('SMA_50',data=df, label='SMA 50', linewidth=0.5, color='purple')
        ax1.plot('SMA_100',data=df, label='SMA 100', linewidth=0.5, color='cyan')
        ax1.plot('SMA_200',data=df, label='SMA 200', linewidth=0.5, color='deeppink')
        
        ax1.plot('Upper',data=df, label='High_bol', linewidth=0.9, color='pink')
        ax1.plot('Lower',data=df, label='low_bol', linewidth=0.9, color='pink')
        
        ax1.plot(x1_high_values, y1_high_values, color='g', linestyle='--', linewidth=0.5, label='Trend resistance')
        ax1.plot(x1_low_values, y1_low_values, color='r', linestyle='--', linewidth=0.5, label='Trend support')

        ax1.axhline(y=pivot_high_1, color='g', linewidth=6, label='First resistance line', alpha=0.2)
        ax1.axhline(y=pivot_low_1, color='r', linewidth=6, label='First support line', alpha=0.2)
        trans = transforms.blended_transform_factory(ax1.get_yticklabels()[0].get_transform(), ax1.transData)
        ax1.text(0,pivot_high_1, "{:.2f}".format(pivot_high_1), color="g", transform=trans,ha="right", va="center")
        ax1.text(0,pivot_low_1, "{:.2f}".format(pivot_low_1), color="r", transform=trans,ha="right", va="center")
        
        ax1.plot(executeB[0],gameplanB,'o',data=df, linewidth=0.9, color='green', label='SMA Basic Buy')
        ax1.plot(executeB[0],executeB[1],'o',data=df, linewidth=0.9, color='red', label='SMA Basic Sell')

        ax1.plot(execute[0],gameplan,'o',data=tester, linewidth=0.9, color='black', label='bolliger band Buy')
        ax1.plot(execute[0],execute[1],'o',data=tester, linewidth=0.9, color='orange', label='bolliger band Sell')    
        
        timeD=datetime.timedelta(days=30)
        for index in range(len(testerP[0])):
            print(str(testerP[0][index])+": "+str(testerP[1][index]))
            plt.plot_date([testerP[1][index],testerP[1][index]+timeD],[testerP[0][index],
                      testerP[0][index]],linestyle='-',linewidth=2,marker=',')
        
        ax1.legend()
        ax1.grid()
        
        
displaying=Plotter(tester,df,testerP,execute,executeB,gameplan,gameplanB).display()
        
        
    
        
