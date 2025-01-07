# Forex-Signal-Generator-and-Trading-Bot
## Overview

This project implements a simple forex trading strategy using a signal generator based on candlestick patterns. It collects real-time EUR/USD data, generates trading signals, and executes trades through the OANDA API. The bot runs on a scheduling mechanism, ensuring it checks for trading opportunities at specified intervals.

## Features

- **Signal Generator**: The bot generates trading signals based on the last two candlesticks:
  - **Bearish Signal**: Triggered when a bearish candlestick pattern is detected.
  - **Bullish Signal**: Triggered when a bullish candlestick pattern is detected.
  
- **Trade Execution**: Once a signal is generated, the bot places a market order with calculated Stop Loss (SL) and Take Profit (TP) levels based on previous price action.

- **Scheduler**: Uses the `APScheduler` library to run the trading job at regular intervals, ensuring continuous monitoring and trade execution during market hours (Monday to Friday).

## Dependencies

- `yfinance`: To download historical EUR/USD data.
- `pandas`: For data manipulation and analysis.
- `apscheduler`: To schedule trading jobs.
- `oandapyV20`: OANDA API for order placement and managing trading operations.
- `oanda_candles`: Custom package to retrieve real-time forex candles.

## Setup

1. Install required libraries using `pip`:
   ```bash
   pip install yfinance pandas apscheduler oandapyV20
