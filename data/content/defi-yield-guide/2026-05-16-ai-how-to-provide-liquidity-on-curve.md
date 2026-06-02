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

# How to Provide Liquidity on Curve Finance: A Step‑by‑Step Guide

This guide walks you through the exact steps to provide liquidity on Curve Finance—including wallet setup, selecting a pool, depositing assets, and staking LP tokens—so you can start earning swap fees and CRV rewards within minutes. By the end you’ll have a live position that you can monitor on‑chain and manage as market conditions change.

---

## Step‑by‑Step Instructions

### 1. Set Up a Web3 Wallet
- **Choose a compatible wallet:** MetaMask, Trust Wallet, or any WalletConnect‑compatible wallet.
- **Add the Ethereum Mainnet network:**  
  - RPC URL: `https://mainnet.infura.io/v3/YOUR_INFURA_KEY` (or use public RPCs like `https://eth.llamarpc.com`)  
  - Chain ID: `1`  
  - Symbol: `ETH`  
  - Block explorer: `https://etherscan.io`
- **Secure your seed phrase** and enable two‑factor authentication if your wallet supports it.
- **Fund the wallet** with enough ETH to cover gas (at least 0.01 ETH; a typical deposit transaction on Ethereum costs ~150 k gas, which at 30 gwei translates to ≈ 0.0045 ETH ≈ $5 as of March 2025).

### 2. Acquire Stablecoins for the Pool
- **Select a stablecoin pair** that matches the pool you want to join. The most popular pools are:
  - **3pool (USDC/USDT/DAI)** – ideal for pure stable‑coin exposure.
  - **stETH/ETH** – for ETH‑paired liquidity.
  - **Polygon (USDC/USDT)** – lower gas fees on Layer 2.
- **Use a DEX (Uniswap, SushiSwap) or a centralized exchange** to convert ETH into the needed stablecoins. For the 3pool you’ll need roughly equal values of USDC, USDT, and DAI.
- **Check gas costs** before swapping; performing the conversion during low‑traffic periods (e.g., weekend evenings UTC) can save 30‑50 % on fees.

### 3. Connect to Curve Finance
- Open **[curve.fi](https://curve.fi)** in your browser.
- Click **“Connect Wallet”** in the top‑right corner.
- Select your wallet (MetaMask, WalletConnect, etc.) and approve the connection.
- Ensure the network displayed in the header matches the blockchain you intend to use (Ethereum mainnet by default).

### 4. Choose a Liquidity Pool
- Navigate to the **“Pools”** page.
- **Filter by asset type** (e.g., “Stablecoin”, “ETH”) and **network** (Ethereum, Polygon, Arbitrum).
- **Key metrics to examine (as of March 2025):**
  - **Total Value Locked (TVL):** Higher TVL usually means deeper liquidity and lower slippage. For the 3pool, TVL ≈ $4.2 B.
  - **Annual Percentage Rate (APR):** Includes both swap fees and CRV incentives. The 3pool APR ≈ 9.5 % (≈ 7 % from swap fees + ≈ 2.5 %