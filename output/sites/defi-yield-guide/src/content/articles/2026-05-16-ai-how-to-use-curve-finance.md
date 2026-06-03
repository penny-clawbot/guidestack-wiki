---
title: "how to use curve finance"
description: "Expert insights on how to use curve finance"
date: "2026-05-16"
category: "decentralized-finance-yield-farming-defi-guide"
tags:
  - decentralized-finance-yield-farming-defi-guide
  - how-to-use-curve-finance
draft: false
readingTime: "4 min"
---

# How to Use Curve Finance

Curve Finance is a decentralized exchange (DEX) optimized for stablecoin swaps and low‑slippage trading, boasting over **$21 billion in total value locked (TVL)** as of early 2025 (DeFi Llama). To use it, you connect a Web3 wallet, select a liquidity pool, deposit assets, and earn trading fees plus **CRV** token rewards. Below is a step‑by‑step guide with concrete numbers, pool examples, and advanced tactics.

---

## 1. Understanding Curve Finance’s Core Mechanism


![Hero image for how to use curve finance](https://picsum.photos/seed/how-to-use-curve-finance-hero/1200/630)


Curve operates as an **automated market maker (AMM)** that uses a **stableSwap** invariant, allowing it to execute trades between assets of the same peg with near‑zero slippage. Key metrics:

- **Average trading fee:** 0.04 % for stable‑coin pools (e.g., USDC/USDT) and 0.2 % for volatile pairs.
- **Number of pools:** 200+ across Ethereum, Polygon, Arbitrum, Fantom, and other chains (Curve Dashboard, Jan 2025).
- **TVL share:** ~35 % of all stablecoin DEX volume comes from Curve (CoinGecko, 2024).

Because of this design, Curve can handle **$100 million in a single trade** with slippage often under 0.01 %.

---

## 2. Step‑by‑Step: Connecting Your Wallet and Depositing Assets

### 2.1 Choose a Wallet & Network
- Supported wallets: **MetaMask**, **WalletConnect**, **Coinbase Wallet**, **Trust Wallet**.
- Network: Ethereum mainnet (most pools), Polygon, Arbitrum, Optimism, or Fantom.  
  *Tip:* Gas fees on Ethereum can be 30‑50 gwei during peak times; consider Layer‑2 networks for cheaper transactions.

### 2.2 Access the Platform
1. Navigate to **curve.finance** (or the appropriate chain subdomain, e.g., **arbitrum.curve.finance**).
2. Click **“Connect Wallet”** in the top‑right corner.
3. Approve the wallet pop‑up and select your preferred network.

### 2.3 Select a Pool
- Example: **3pool (USDC/USDT/USDT)** – the most liquid stablecoin pool on Ethereum.  
  - **Annual Percentage Yield (APY):** ~5.5 % (fees) + 2 % (CRV incentives) = **7.5 %** as of Jan 2025.  
- Other popular pools: **stETH/ETH** (Lido staked ETH), **MIM/3pool**, **FRAX/USDC**.

### 2.4 Deposit Funds
- Click **“Deposit”** on the chosen pool.  
- Enter the amount of one or multiple assets; Curve auto‑balances the ratio.  
- Approve token spends and confirm the transaction.  
  *Example:* Depositing **10,000 USDC** into the 3pool yields an immediate share of the pool’s liquidity, currently ~0.04 % of total liquidity.

---

## 3. Providing Liquidity and Maximizing Returns


![Illustration for how to use curve finance](https://picsum.photos/seed/how-to-use-curve-finance-mid/1200/630)


### 3.1 LP Tokens & Fee Collection
- Upon deposit, you receive **LP tokens** (e.g., **3Crv**) representing your share of the pool.  
- Trading fees are automatically added to the pool, increasing the LP token’s underlying value.  
- You can view real‑time earnings on the **Curve Dashboard** under **“My Deposits.”**

### 3.2 Gauge Weights & CRV Rewards
- **CRV** is Curve’s governance token. By **staking** LP tokens in a **gauge**, you earn CRV proportional to the pool’s gauge weight.
- **Gauge weights** are voted on by **veCRV** holders (CRV locked for up to 4 years).  
  *Example:* If a pool receives a 10 % gauge weight and you hold 1 % of its LP tokens, you earn ~0.1 % of the weekly CRV emission.
- To claim, go to **“Rewards”** → **“Claim”**; CRV can be auto‑compounded or sold.

### 3.3 Boosting Rewards with veCRV
- Locking CRV into **veCRV** increases your reward multiplier up to **2.5×**.  
  *Data:* As of Jan 2025, locking **10,000 CRV** for 4 years yields a **~2.0×** boost for pools you provide liquidity in.  
- You can acquire veCRV by converting CRV in the **Lock** tab on the Curve DAO page.

### 3.4 Impermanent Loss (IL) Considerations
- Curve’s stable‑swap design virtually eliminates IL for pegged assets.  
- For volatile pairs (e.g., ETH/stETH), IL is comparable to traditional AMMs; the platform’s **Crypto‑swap** pools handle these with higher fees (0.2 %).

---

## 4. Advanced Strategies: Factory Pools, Leverage, and Cross‑Chain Swaps

### 4.1 Factory Pools
- Curve allows anyone to create **factory pools** for custom token pairs.  
- As of early 2025, **~50 factory pools** exist, offering higher fee tiers (0.2‑0.4 %) to attract liquidity.  
- Example: **Factory V2: LDO/USDC** – provides a 0.3 % fee with a 5 % CRV incentive boost.

### 4.2 Leveraged Yield Farming
- Using **Yearn Finance** or **Convex Finance**, you can borrow assets on **Aave** or **Compound** and supply them to Curve for amplified yields.  
- *Scenario:* Deposit ETH → borrow USDC → supply USDC to the 3pool → earn ~12 % APY (fees + CRV + borrowing interest rebate).  
  *Warning:* Leverage amplifies both gains and losses; liquidations can occur if collateral falls below 150 % LTV.

### 4.3 Cross‑Chain Swaps
- Curve’s **Cross‑Chain Bridge** (via **Stargate** or **Celer**) lets you swap assets between Ethereum, Polygon, and Arbitrum with a single click.  
- Slippage is typically <0.1 % for stablecoins; bridge fees average **0.05 % + $5** network gas.

---

## Frequently Asked Questions

### How do I withdraw my liquidity from a Curve pool?
- Go to the pool’s page, click **“Withdraw,”** select the amount of LP tokens to redeem, and confirm the transaction. You’ll receive the underlying assets (plus accrued fees) directly to your wallet.

### Can I use Curve on a mobile wallet?
- Yes. Curve’s UI is mobile‑friendly and works with wallets like **MetaMask Mobile**, **Trust Wallet**, and **WalletConnect**‑enabled apps. Ensure you switch to the correct.