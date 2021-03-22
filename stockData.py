# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 03:10:14 2021

@author: Frank Garcia
"""

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

startDate="2020-10-01"
endDate=str(datet.date())

stockChoice="BA"


class DataBase():
    def __init__(self,ticker):
        self.ticker = ticker
        
        data=pdr.get_data_yahoo(stockChoice, startDate,endDate,interval = "1d")
        self.df=pd.DataFrame(data)

    def quote(self):
        return self.df
    
    
db=DataBase(stockChoice)
df=db.quote()

# print(df)
# print('Hello')

