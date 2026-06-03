---
title: "how to backtest crypto strategies"
description: "Step-by-step: how to backtest crypto strategies"
date: "2026-05-15"
category: "cryptocurrency-trading-strategies-and-technical-analysis"
tags:
  - cryptocurrency-trading-strategies-and-technical-analysis
  - how-to-backtest-crypto-strategies
draft: false
readingTime: "1 min"
---

# How to Backtest Crypto Strategies: A Practical Guide  

This guide walks you through collecting reliable historical market data, coding a simple moving‑average crossover strategy in Python, running the backtest with **Backtrader**, and interpreting key performance metrics—such as total return, Sharpe ratio, and max drawdown—to validate whether a strategy has historically been profitable. By following the eight concrete steps below, you will be able to repeat the process for any token‑pair, timeframe, or set of rules, and you will learn how to avoid common pitfalls like over‑fitting and unrealistic cost assumptions.  

## Step‑by‑Step Instructions  


![Hero image for how to backtest crypto strategies](https://picsum.photos/seed/how-to-backtest-crypto-strategies-hero/1200/630)


### 1. Define Your Trading Hypothesis and Strategy Rules  
Before you write a single line of code, write a clear hypothesis.  
- **Example:** “Bitcoin tends to bounce back within 48 hours after a 20 % intraday drop.”  
- **Translate it into entry/exit logic:**  
  - **Entry:** Buy when the close is ≥ 20 % below the previous day’s high.  
  - **Exit:** Sell after 48 hours (or when a 5 % trailing stop is hit).  
- **Specify position sizing:** 2 % of equity per trade, max 10 % total exposure.  
- **Document risk controls:** stop‑loss at 1.5 % below entry, maximum drawdown tolerance 20 %.  

### 2. Choose a Data Source and Retrieve Clean OHLCV Data  
Reliable data is the foundation of a trustworthy backtest.  

1. **Select an exchange:** Binance, Coinbase Pro, Kraken, or any that offers a public API.  
2. **Fetch daily (or 15‑minute) candles for BTC/USDT from 2020‑01‑01 to 2023‑12‑31:**  
   ```python
   import ccxt, pandas as pd

   exchange = ccxt.binance()
   ohlcv = exchange.fetch_ohlcv('BTC/USDT', '1d',
                                since=exchange.parse8601('2020-01-01T00:00:00Z'),
                                limit=1461)   # ~4 years of daily bars
   df = pd.DataFrame(ohlcv, columns=['timestamp','open','high','low','close','volume'])
   df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
   df.set_index('timestamp', inplace=True)
   # Remove duplicates, handle missing rows
   df = df[~df.index.duplicated(keep='first')]
   df = df.resample('1D').agg({'open':'first','high':'max','low':'min','close':'last','volume':'sum'})
   df.fillna(method='ffill', inplace=True)
   ```  
3. **Store the cleaned CSV** for later use (`btc_daily_2020_2023.csv`).  

### 3. Set Up Your Backtesting Environment  
- **Python 3.10+**  
- **Install required libraries:**  
  ```bash
  pip install backtrader pandas numpy matplotlib ccxt
  ```  
- **Create a script `backtest_runner.py`** with the following imports:  
  ```python
  import backtrader as bt
  import pandas as pd
  import numpy as np
  ```  

### 4. Implement the Strategy Logic in Code  
Below is a minimal **Backtrader** strategy that follows the moving‑average crossover rule (fast SMA 10, slow SMA 30).  

```python
class SmaCross(bt.Strategy):
    params = (('fast', 10), ('slow', 30),)

    def __init__(self):
        sma_fast = bt.ind.SMA(period=self.p.fast)
        sma_slow = bt.ind.SMA(period=self.p.slow)
        self.crossover = bt.ind.CrossOver(sma_fast, sma_slow)