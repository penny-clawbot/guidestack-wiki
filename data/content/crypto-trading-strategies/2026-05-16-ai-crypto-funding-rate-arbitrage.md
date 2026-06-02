---
title: "crypto funding rate arbitrage"
description: "Step-by-step: crypto funding rate arbitrage"
date: "2026-05-16"
category: "cryptocurrency-trading-strategies-and-technical-analysis"
tags:
  - cryptocurrency-trading-strategies-and-technical-analysis
  - crypto-funding-rate-arbitrage
draft: false
readingTime: "1 min"
---

# Crypto Funding Rate Arbitrage: A Step-by-Step Guide  

This guide shows you how to capture the net spread between funding rates on different exchanges, walk‑through the exact calculations, and execute the trade with proper risk controls. By the end you’ll be able to spot a profitable arbitrage window, size a position, manage margin, and close the trade when the spread narrows.  

## Step-by-Step Instructions  

### Step 1: Choose Exchanges and Open Accounts  

Select **perpetual‑futures‑friendly** platforms that publish real‑time funding data via API. As of **March 2025**, the most liquid markets with publicly quoted funding rates are:  

- **Binance USDT‑M** (BTC, ETH, BNB perps) – funding paid every **8 h** at 00:00, 08:00, 16:00 UTC.  
- **Bybit USDT Perpetual** – same 8‑h cadence.  
- **OKX USDT Swap** – funding settled at 07:30, 15:30, 23:30 UTC.  
- **Deribit BTC‑PERPETUAL** – funding at 08:00 UTC.  

Open **margin accounts** on each (cross‑margin is recommended for easier collateral management). Verify that you can **transfer USDT** between them within the same day to avoid timing gaps.  

### Step 2: Transfer and Align Collateral  

Move a **minimum of 2 % of your total capital** to each exchange as margin buffer. For example, if you plan to risk **$10 000**, deposit **$