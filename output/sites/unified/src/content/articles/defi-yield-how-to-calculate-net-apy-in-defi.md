---
niche: "defi-yield"
title: "how to calculate net apy in defi"
description: "Step-by-step: how to calculate net apy in defi"
date: "2026-05-16"
category: "decentralized-finance-yield-farming-defi-guide"
tags:
  - decentralized-finance-yield-farming-defi-guide
  - how-to-calculate-net-apy-in-defi
draft: false
readingTime: "2 min"
---
# How to Calculate Net APY in DeFi

Net APY in DeFi represents your actual annualized return after accounting for fees, incentives, and compounding effects. Calculating net APY requires subtracting all costs from gross yields and accounting for compounding frequency, which can mean the difference between claimed 12% returns and actual 8% gains. This guide provides the step-by-step formula, real protocol examples, and tools to determine your true earning potential.

## What Is the Difference Between Gross APY and Net APY?

Gross APY refers to the advertised yield before any costs are deducted. Protocols typically advertise gross yields to attract liquidity, but these numbers rarely reflect what you actually earn. Net APY subtracts trading fees, protocol fees, gas costs, and any incentive tokens that may depreciate in value.

For example, a liquidity pool might advertise 15% gross APY, but after deducting a 0.3% swap fee, 0.05% protocol fee, and $15 average weekly gas costs, your net APY could drop to 9.2%. The difference becomes even more pronounced when token incentives are included, since their value can fluctuate dramatically based on market conditions.

Understanding this distinction is crucial because DeFi protocols often highlight impressive gross numbers in their marketing materials while burying fee disclosures in documentation that most users never read thoroughly.

## How Do You Calculate Net APY From Gross APY?

The core net APY formula accounts for fees, costs, and compounding frequency. Start with your gross yield, then apply the following deductions:

**Net APY Formula:**
```
Net APY = (Gross APY - Total Fee Percentage - Gas Cost Percentage) × Compounding Multiplier
```

Consider this scenario: You provide liquidity to an ETH/USDC pair on Uniswap V3 with a gross APY of 12%. The protocol charges a 1% management fee, liquidity providers pay 0.3% per trade, and your weekly gas costs average $20. With $10,000 invested and earning $1,200 annually in gross fees, your calculations would be:

- Gross earnings: $1,200
- Protocol fee (1%): -$120
- LP fees (estimated): -$200
- Gas costs (52 weeks × $20): -$1,040
- **Total deductions: $1,360**
- **Net earnings: -$160**

In this scenario, your net APY would actually be negative at approximately -1.6%, meaning you lose money despite the attractive 12% gross rate.

![Diagram showing the breakdown of gross APY vs net APY with fees, gas costs, and token incentives deducted at each step](https://example.com/net-apy-calculation-diagram.jpg)

The compounding frequency also significantly impacts your results. Daily compounding produces higher effective yields than annual compounding, so protocols that compound rewards more frequently will generate better net returns even with identical advertised rates.

## What Factors Most Commonly Reduce Your Actual APY?

Several hidden costs systematically erode DeFi yields, and understanding each one helps you make more accurate calculations before committing capital.

**Protocol Fees**: Most decentralized exchanges charge between 0.05% and 1% annually on earned yields. According to Dune Analytics (2024), the average DeFi protocol fee is 0.17% for lending platforms and 0.25% for AMMs.

**Gas Costs**: Transaction fees vary dramatically by network. Ethereum mainnet average gas costs reached $15-40 per transaction in 2024, while Arbitrum and Optimism typically charge under $1. Network congestion can spike costs by 500% or more during volatile periods.

**Slippage and Impermanent Loss**: For liquidity providers, price divergence between pooled assets creates impermanent loss that effectively functions as a negative fee. A 50% price increase in one asset can result in a 5.7% impermanent loss, according to research from Binance Academy.

**Token Incentive Volatility**: Many protocols offer additional rewards in governance tokens. If these tokens depreciate 40% after claiming, your net APY drops proportionally. According to Token Terminal (2024), the average token incentive represents 45% of advertised yields in governance token-based protocols.

**Minimum Liquidity Thresholds**: Some protocols require minimum lock periods or liquidity commitments that reduce capital efficiency, effectively lowering your annualized returns.

## How Can You Use Tools to Calculate Net APY Accurately?

Several specialized tools help you calculate net APY with greater precision than manual calculations. DefiLlama provides comprehensive yield aggregation that includes fee disclosures and historical performance data. According to DefiLlama's methodology documentation (2024), they calculate net APY by sourcing raw data from protocol contracts and applying standardized fee deductions.

APY.vision offers portfolio tracking that automatically deducts gas costs and calculates impermanent loss for Uniswap V3 positions. Their analytics platform aggregates transaction history across multiple wallets, providing real-time net APY calculations that account for your specific trading patterns.

For manual calculations, use this streamlined formula when comparing opportunities:

| Factor | Example Value | Impact on APY |
|--------|---------------|---------------|
| Gross APY | 15.0% | Baseline |
| Protocol Fee | -0.25% | 14.75% |
| LP Trading Fees | -0.4% | 14.35% |
| Gas Costs (weekly) | -$20 ($10k position) | -1.04% |
| Token Incentive (depreciation) | -2.5% | 10.81% |
| **Net APY** | | **10.81%** |

This table demonstrates how advertised yields can drop by 28% once all costs are incorporated.

## Frequently Asked Questions

### How often should I recalculate my net APY in DeFi?

Recalculate at least weekly, since gas costs fluctuate with network congestion, token incentive values change daily, and protocol fees may adjust. Major yield shifts often occur within 48 hours during market volatility, making real-time monitoring essential for capital allocation decisions.

### Does compound frequency affect net APY calculations?

Yes, significantly. A 12% gross APY with daily compounding produces an effective 12.75% annual yield, while annual compounding delivers exactly 12%. When calculating net APY, always verify the compounding interval and adjust your baseline accordingly.

### Can net APY ever exceed gross APY?

In rare cases, if token incentives appreciate substantially or compounding bonuses exceed fee costs, net returns can occasionally surpass gross estimates. However, this typically requires favorable market conditions and active management of positions to optimize timing of claims and reinvestments.

## Sources

- DefiLlama Methodology Documentation (2024)
- Dune Analytics DeFi Fee Report (2024)
- Token Terminal Protocol Metrics (2024)
- Binance Academy Impermanent Loss Guide (2024)

## Conclusion

Calculating net APY requires moving beyond advertised figures and incorporating all associated costs—protocol fees, gas expenses, impermanent loss, and token depreciation. By applying the formulas and tools outlined in this guide, you can make data-driven decisions that align with your actual risk-adjusted return expectations. Remember that the highest gross APY rarely represents the best opportunity once true costs are accounted for.