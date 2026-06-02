---
title: "crypto basis trading strategies"
description: "Answers to your questions about crypto basis trading strategies"
date: "2026-05-16"
category: "cryptocurrency-trading-strategies-and-technical-analysis"
tags:
  - cryptocurrency-trading-strategies-and-technical-analysis
  - crypto-basis-trading-strategies
draft: false
readingTime: "1 min"
---

# Crypto Basis Trading Strategies

Crypto basis trading is a strategy that profits from the difference between the price of a cryptocurrency’s futures contract and its spot price. The core metric is the **basis**, calculated as **Futures Price – Spot Price**, often expressed as an annualized percentage to enable comparison across contracts. Historical data from Glassnode (2023) show that Bitcoin (BTC) quarterly‑futures basis typically ranges from **5 % to 20 % per annum**, while Ethereum (ETH) futures basis has averaged **8 %–14 %** in the same period. Effective basis trading requires precise timing, low‑fee execution, and robust risk controls, as the basis can widen sharply during market stress. Below are eight key questions that cover the mechanics, strategies, risks, and tools needed to run a successful crypto basis trading operation.

## 1. What is crypto basis trading and how does the basis work?

**Crypto basis trading exploits the price gap between a cryptocurrency’s futures price and its spot price.** The basis can be positive (contango) or negative (backwardation) and is usually quoted as an annualized figure:  

\[
\text{Annualized Basis} = \frac{\text{Futures Price} - \text{Spot Price}}{\text{Spot Price}} \times \frac{365}{\text{Days to Expiry}} \times 100\%
\]

- **Contango**: Futures price > Spot price → positive basis.  
- **Backwardation**: Futures price < Spot price → negative basis.  

According to a 2022 Skew report, the average annualized basis for BTC quarterly futures on the Chicago Mercantile Exchange (CME) was **12.5 %**, while perpetual‑swap funding rates on Binance averaged **0.01 % per 8‑hour period** (≈0.03 % daily). Traders monitor this metric because the basis tends to converge to zero at contract expiry, offering a predictable profit opportunity if the cost of carry is lower than the captured basis.

## 2. How does cash‑and‑carry arbitrage capture the basis?

**Cash‑and‑carry buys the underlying spot asset and simultaneously sells a futures contract to lock in the basis.** The profit equals the locked‑in basis minus transaction costs (fees, funding, storage). The basic steps