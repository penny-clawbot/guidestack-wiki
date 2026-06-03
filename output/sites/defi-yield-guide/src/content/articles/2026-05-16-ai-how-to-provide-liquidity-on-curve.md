---
title: "how to provide liquidity on curve"
description: "Step-by-step: how to provide liquidity on curve"
date: "2026-05-16"
category: "decentralized-finance-yield-farming-defi-guide"
tags:
  - decentralized-finance-yield-farming-defi-guide
  - how-to-provide-liquidity-on-curve
draft: false
readingTime: "2 min"
---
# How to Provide Liquidity on Curve

Curve is a decentralized exchange optimized for low-slippage stablecoin and asset‑pegged token swaps. By depositing assets into a Curve liquidity pool, you earn a share of trading fees and can receive CRV token rewards. This guide walks you through the exact steps to become a liquidity provider (LP) on Curve and explains how to evaluate the potential returns and risks.

---

## What Are Curve Pools and Why Provide Liquidity?

Curve’s pools are smart‑contract vaults that aggregate assets for automated market making (AMM). Unlike typical AMMs, Curve uses a **stable‑swap** algorithm that maintains near‑parity between assets, resulting in minimal slippage for pegged tokens. As of Q1 2024, the platform reported a total value locked (TVL) of **$24.5 billion** across its pools, with daily trading volume averaging **$200 million** and base trading fees around **0.04 % per swap** (source: Curve official stats). Providing liquidity lets you capture a portion of these fees and benefit from CRV reward distributions.

---

## How to Connect Your Wallet and Choose a Pool?

1. **Open the Curve app** at [app.curve.fi](https://app.curve.fi) and click **“Connect Wallet”** in the top‑right corner.  
2. Select your wallet provider (MetaMask, WalletConnect, Coinbase Wallet, etc.) and approve the connection.  
3. Once connected, navigate to the **“Pools”** tab. You’ll see a list of available pools with metrics such as **Annual Percentage Yield (APY)**, **TVL**, and **Volume (24 h)**.  

**Example:** The **3pool (USDC/USDT/DAI)** currently offers a **base fee APY of ~4.5 %** and an additional **CRV boost of ~1.2 %**, bringing the total estimated APY to **5.7 %** as of March 2024 (source: Dune Analytics).  

![Curve pool selection UI displaying various liquidity pools](https://example.com/curve-pool-selection.png)

When choosing a pool, consider:

- **Asset volatility:** Stablecoin pools have lower impermanent loss than volatile asset pools.  
- **Reward boost:** Pools with higher CRV weighting can increase total APY by up to **1.5 %** (source: Curve Medium, 2023).  
- **Pool health:** Verify that the pool is not approaching a depeg risk by checking the **“Health”** indicator on the dashboard.

---

## How to Deposit Assets and Monitor Returns?

1. **Select a pool** and click **“Deposit”**.  
2. **Enter the amount** you wish to provide for each asset. You can deposit single assets in some pools using the **“Zap”** feature, which automatically swaps to the required ratio for a small fee.  
3. **Approve the tokens** if prompted; the transaction will request permission to access your funds.  
4. **Confirm the deposit** and sign the transaction in your wallet. After confirmation, you’ll