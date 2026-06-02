---
title: "Yield farming impermanent loss guide"
description: "Expert guide to yield farming impermanent loss guide"
date: "2026-05-13"
category: "defi-yield-guide"
tags:
  - defi-yield-guide
  - yield-farming-impermanent-loss-guide
draft: false
readingTime: "5 min"
---

# Yield Farming Impermanent Loss Guide  

Impermanent loss (IL) is the temporary reduction in the value of assets held in a liquidity pool compared with simply holding those assets outside the pool, caused by price divergence between the pool’s assets; it is the primary risk that can offset high yield‑farming returns. IL is realized only when a liquidity provider withdraws funds, and it can range from a fraction of a percent to more than 40 % depending on the magnitude of price movement. Understanding IL, its calculation, and mitigation strategies is essential for anyone participating in DeFi yield farming.

---

## What is impermanent loss in yield farming?  

**Impermanent loss is the difference in value between holding assets in a liquidity pool and holding them in a wallet.** It occurs because AMMs rebalance the token quantities in the pool to maintain a constant product formula, causing the pool’s holdings to drift from the original price ratio. When the price of one asset rises relative to the other, the pool sells a portion of the appreciating asset, so the liquidity provider ends up with less of the asset that increased in value than if they had held it outright. The loss is “impermanent” because if prices revert to the original ratio before withdrawal, the loss disappears; however, if the price change persists, the loss becomes permanent.

---

## How is impermanent loss calculated?  

The classic IL formula for a 50/50 constant‑product AMM (x·y = k) is:

\[
IL = \frac{2\sqrt{r}}{1+r} - 1
\]

where \(r = \frac{P_{final}}{P_{initial}}\) is the price ratio of the two assets. A practical example: if ETH rises from $3,000 to $6,000 (r = 2), the IL is:

\[
IL = \frac{2\sqrt{2}}{1+2} - 1 \approx \frac{2·1.414}{3} - 1 \approx 0.0572 \; (\text{≈ 5.7 %})
\]

The same formula yields roughly 13.4 % for a 3× price change, 25.5 % for a 5× change, and 42.5 % for a 10× change (Bancor Research, 2021).  

**Key points:**  
- IL depends only on the price ratio, not on pool size or fees.  
- Larger price swings produce exponentially larger losses.  

---

## What are typical magnitudes of impermanent loss in major AMMs?  

Empirical data from 2022‑2023 shows IL varies widely by pool type:  

- **Stablecoin pairs (USDT/USDC):** IL is usually <0.1 % per month because price divergence is minimal.  
- **Major volatile pairs (ETH/USDC, WBTC/ETH):** A 10‑20 % price swing typically yields 0.5‑2 % IL (Dune Analytics, 2023).  
- **Alt‑coin/ETH pairs with higher volatility:** IL can exceed 5 % per week during market spikes (Binance Research, 2022).  

A 2023 Binance Research report found the **average annualized IL across Uniswap V2 and V3 pools was 12 %**, while the top‑quartile pools (high‑volatility assets) experienced >20 % annualized IL. In contrast, **SushiSwap’s stablecoin pools showed an average IL of only 0.8 %** over the same period, underscoring the safety of low‑volatility pairs.

---

## How does impermanent loss affect net returns from yield farming?  

Impermanent loss directly subtracts from the gross APY earned from liquidity mining rewards and trading fees. For example, a pool offers **30 % APY** from token incentives and **5 % APY** from fees, but the **annualized IL is 14 %**. The net yield is:

\[
\text{Net APY} = (30\% + 5\%) - 14\% = 21\%
\]

If IL surpasses the combined rewards, the liquidity provider ends up with a net loss. A case study of the **SUSHI/ETH pool on SushiSwap (Q3 2022)** showed a 12 % IL for the quarter, while total farming rewards were 30 % → net profit ≈ 18 % (SushiSwap Analytics, 2022). Thus, **always compare gross yield against estimated IL** before committing capital.

---

## What strategies can mitigate impermanent loss?  

- **Use stablecoin or low‑volatility pairs:** Nearly eliminates IL but introduces de‑peg risk.  
- **Employ hedged positions:** Open a short futures or perpetual position on the volatile asset to offset price exposure (e.g., using dYdX or GMX).  
- **Select pools with high fee tiers:** More fee revenue can offset IL; Uniswap V3’s 0.30 %‑1 % fee tiers generate larger fee APY.  
- **Provide liquidity in concentrated ranges (Uniswap V3):** By narrowing the price range, you earn higher fees per unit of capital, but IL risk increases if the price exits the range.  
- **Use IL protection insurance:** Nexus Mutual and InsurAce offer coverage products that reimburse IL under defined conditions (premiums ≈ 2‑4 % of covered value).  
- **Rebalance or withdraw during extreme volatility:** Actively monitoring price movements and withdrawing before large swings can preserve capital.  

**Example:** A liquidity provider in an ETH/USDC pool opens a 2× short ETH‑perp on the same amount. If ETH rises 50 %, the IL (~13 %) is offset by the short’s profit (~50 % on the hedged notional), resulting in a net gain (subject to funding costs).

---

## How does impermanent loss differ in Uniswap V2, V3, and other AMM designs?  

- **Uniswap V2 (constant‑product):** IL follows the classic formula; all price ranges are equally exposed. Average IL for a 2× move = 5.7 %.  
- **Uniswap V3 (concentrated liquidity):** Liquidity is concentrated within custom price ranges. For the same total capital, a tighter range amplifies both fee earnings and IL. A **0.1 %‑wide ETH/USDC range** can generate 10× more fees but also increase IL by up to 5× for the same price move (Uniswap V3 Developer Docs, 2022).  
- **Curve Finance (stable‑swap):** Uses a hybrid constant‑product/constant‑sum formula, drastically reducing IL for assets with low price divergence (≈ 0.2 % for a 10 % price shift).  
- **Balancer (weighted pools):** Allows non‑50/50 weights (e.g., 80/20), which can reduce IL for the heavier‑weighted asset while increasing exposure to the lighter one.  

**Takeaway:** The AMM design dictates how IL scales with price movements; newer platforms offer tools to trade off IL against fee income.

---

## What tools and resources help track impermanent loss?  

- **IL Calculators:** CoinGecko’s “Impermanent Loss Calculator” and Uniswap’s official calculator provide instant IL estimates based on price ratios and pool type.  
- **Analytics Dashboards:** Dune Analytics, Nansen, and DeBank display real