#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 12:42:03 2024

@author: dami
"""

import yfinance as yf
import pandas as pd

dataF = yf.download("EURUSD=X", start="2024-10-21", end="2024-12-19", interval="15m")
print(dataF.iloc[-1:,:])

def signal_generator(df):
    open = df.Open.iloc[-1]
    close = df.Close.iloc[-1]
    previous_open = df.Open.iloc[-2]
    previous_close = df.Close.iloc[-2]
    
    

    #Bearish
    if (open>close and previous_open<previous_close and close<previous_open and open>previous_close):
        return 1
    #Bullish
    elif (open<close and previous_close<previous_open and open<previous_close and close>previous_open):
        return 2
    
    else:
        return 0
    
signal = []
signal.append(0)
for i in range(1, len(dataF)):
    df = dataF[i-1:i+1]
    signal.append(signal_generator(df))
dataF['Signal'] = signal
print(dataF.Signal.value_counts())

from apscheduler.schedulers.blocking import BlockingScheduler
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import MarketOrderRequest, TakeProfitDetails, StopLossDetails
from oanda_candles import Pair, Gran, CandleClient

access_token = "084ff97e3c6ea6b433ba444c7f3665ef-48775d018d0e1d6f5f3489d4e6fb7ecc"
accountID = "101-004-30575365-001"
def get_candles(n):
    
    client = CandleClient(access_token, real=False)
    collector = client.get_collector(Pair.EUR_USD, Gran.M15)
    candles = collector.grab(n)
    return candles

candles = get_candles(3)
for candle in candles:
    print(float(str(candle.bid.o))>1)
    
def trading_job():
    candles = get_candles(3)
    dfstream = pd.DataFrame(columns=['Open', 'Close', 'High', 'Low'])
    
    for i, candle in enumerate(candles):
        dfstream.loc[i] = {
            'Open': float(str(candle.bid.o)),
            'Close': float(str(candle.bid.c)),
            'High': float(str(candle.bid.h)),
            'Low': float(str(candle.bid.l))
        }
    
    if len(dfstream) < 2:
        print("Insufficient data for signal generation")
        return
    
    signal = signal_generator(dfstream.iloc[:-1])
    client = API(access_token)
    
    SLTPRatio = 2.0
    previous_candleR = max(abs(dfstream['High'].iloc[-2] - dfstream['Low'].iloc[-2]), 0.0020)
    SLBuy = float(str(candle.bid.o)) - previous_candleR
    SLSell = float(str(candle.bid.o)) + previous_candleR
    TPBuy = float(str(candle.bid.o)) + previous_candleR * SLTPRatio
    TPSell = float(str(candle.bid.o)) - previous_candleR * SLTPRatio
    
    print(dfstream.iloc[:-1])
    print(f"TPBuy={TPBuy}, SLBuy={SLBuy}, TPSell={TPSell}, SLSell={SLSell}")
    signal = 1
    if signal == 1:
        mo = MarketOrderRequest(
            instrument="EUR_USD",
            units=-1000,
            takeProfitOnFill=TakeProfitDetails(price=TPSell).data,
            stopLossOnFill=StopLossDetails(price=SLSell).data
        )
        r = orders.OrderCreate(accountID, data=mo.data)
        rv = client.request(r)
        print(rv)
    elif signal == 2:
        mo = MarketOrderRequest(
            instrument="EUR_USD",
            units=200000,
            takeProfitOnFill=TakeProfitDetails(price=TPBuy).data,
            stopLossOnFill=StopLossDetails(price=SLBuy).data
        )
        r = orders.OrderCreate(accountID, data=mo.data)
        rv = client.request(r)
        print(rv)
        
        
trading_job()

        

        
scheduler = BlockingScheduler()
scheduler.add_job(trading_job, 'cron', day_of_week='mon-fri', hour='00-23', minute='1, 16, 31, 46', start_date='2024-12-19', timezone='Europe/London') 