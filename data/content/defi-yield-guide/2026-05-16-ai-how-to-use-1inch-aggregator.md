---
title: "how to use 1inch aggregator"
description: "Comprehensive guide to how to use 1inch aggregator"
date: "2026-05-16"
category: "decentralized-finance-yield-farming-defi-guide"
tags:
  - decentralized-finance-yield-farming-defi-guide
  - how-to-use-1inch-aggregator
draft: false
readingTime: "2 min"
---

# How to Use the 1inch Aggregator: A Comprehensive Guide

The 1inch aggregator sources the best token‑swap prices across dozens of decentralized exchanges (DEXs) and can save you 5‑15 % on each trade compared with manual single‑DEX swaps. To use it, connect a compatible wallet, select the token pair, enter the amount, review the displayed route and fees, and confirm the transaction. Below is a detailed, data‑driven guide to help you navigate every step and leverage 1inch’s advanced features.

---

## 1. What Is 1inch and Why Should You Use It?

1inch is a DeFi aggregation protocol that automatically routes trades through the optimal combination of DEXs (e.g., Uniswap, SushiSwap, Curve) to minimize price impact and slippage. According to 1inch’s 2023 year‑end report, the platform has facilitated over **$50 billion** in cumulative trading volume since its launch in 2020 (source: 1inch Blog, Jan 2023). Independent analytics from Dune Analytics (2023) show that orders routed through 1inch’s **Pathfinder** algorithm achieve an average **5‑15 % better execution price** versus single‑DEX swaps, especially for larger trades.  

**Actionable tip:** Always compare the “Best Price” shown by 1inch with the rate you’d get on a single DEX; the difference often exceeds the protocol’s modest 0.3 % fee, making aggregation worthwhile.

---

## 2. Getting Started: Wallet Connection and Interface Overview

### Supported Wallets & Networks
1inch works with **MetaMask, WalletConnect, Coinbase Wallet, Trust Wallet**, and several other EVM‑compatible wallets. As of 2024, the aggregator supports **10+ networks**: Ethereum, BNB Chain, Polygon, Arbitrum, Optimism, Gnosis Chain, Avalanche, Fantom, Klaytn, and Harmony (source: 1inch Documentation, 2024).  

### Interface Walkthrough
- **Token Selector** – Click “Select a token” to open a searchable list of ERC‑20 assets on the chosen network.  
- **Amount Input** – Enter the amount you wish to spend; the “You receive” estimate updates in real time.  
- **Route Display** – Shows each leg of the trade (e.g., DAI → USDC via Uniswap V3, then USDC → WETH via Curve).  
- **Gas Settings** – Optional: you can set a custom max‑fee or use “Fast”/“Average” presets.  

**Actionable tip:** Double‑check that your wallet is on the **same network** as the token you’re trading; a mismatch will cause the transaction to revert.

---

## 3. Finding the Best Rate: How 1inch’s Pathfinder Algorithm Works

The **Pathfinder** algorithm splits an order into multiple sub‑orders and routes each through the DEX offering the highest liquidity at that moment. In Q4 2023, internal analytics reported that this split routing reduced slippage by an average of **12 %** for orders exceeding $10 k (source: 1inch Analytics, 2024).  

### Liquidity Sources
- **Uniswap V2/V3** (concentrated liquidity)  
- **SushiSwap** (broad token coverage)  
- **Curve** (stablecoin & wrapped‑asset pairs)  
- **Balancer** (weighted pools)  

**Actionable tip:** For volatile pairs (e.g., ETH/MATIC), enable **“Auto‑Route”** to let Pathfinder decide the split; for predictable pairs, you can manually specify a preferred DEX to avoid extra gas.

---

## 4. Executing a Swap: Step‑by‑Step Process

1. **Connect Wallet** – Click “Connect Wallet,” select your provider, and approve the connection in the wallet popup.  
2. **Select Tokens** – Choose the “From” token and the “To” token. If you hold a token not yet imported, search by contract address.  
3. **Enter Amount** – Type the quantity you want to sell. The platform instantly shows the estimated “To” amount, fee breakdown, and price impact.  
4. **Review Route & Fees** – Verify the displayed route (e.g., “USDT → WETH via Uniswap V3, then WETH → UNI via SushiSwap”). Check the protocol fee (0.3 %) and gas estimate.  
5. **Click “Swap”** – The button turns from gray to blue when all inputs are valid