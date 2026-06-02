---
title: "how to calculate apy vs apr defi"
description: "Answers to your questions about how to calculate apy vs apr defi"
date: "2026-05-11"
category: "decentralized-finance-yield-farming-defi-guide"
tags:
  - decentralized-finance-yield-farming-defi-guide
  - how-to-calculate-apy-vs-apr-defi
draft: false
readingTime: "3 min"
niche: "defi-yield"
---

# How to Calculate APY vs APR in DeFi

**APY (Annual Percentage Yield) incorporates compounding, while APR (Annual Percentage Rate) does not.** In DeFi lending, borrowing, and liquidity‑mining protocols, APR is typically quoted for simple interest, and APY is used when interest accrues more frequently than once per year. Understanding how to convert one to the other—and when each metric matters—helps you compare real returns across platforms. The core relationship is:  

\[
\text{APY}= \bigl(1+\frac{\text{APR}}{n}\bigr)^{n}-1
\]  

where **n** is the number of compounding periods per year.

---

## 1. What Is APR and Why Does It Matter in DeFi?

**APR is the simple annual interest rate without accounting for compounding.** It tells you the percentage of principal you will earn (or owe) over a one‑year period if interest is calculated only once.

In DeFi, APR is commonly displayed for:

- **Lending markets** (e.g., Aave, Compound)  
- **Borrowing rates** (e.g., MakerDAO, dYdX)  

Because APR ignores reinvestment, it understates the effective return on a deposit that compounds several times per day or per block. As of March 2023, Aave V2 lists a variable APR of **~3.45 %** for aUSDC lending (source: Aave V2 dashboard, https://app.aave.com). Use APR when you need a quick, standardized figure for comparing the cost of borrowing or the raw yield of a lending pool.

---

## 2. How Is APR Calculated in DeFi Lending Protocols?

**APR = (Interest accrued over a period ÷ Principal) × (365 ÷ Days in period).** Most DeFi platforms calculate interest per block, so the formula often uses block‑time conversion.

For example, Compound Finance updates interest every block (~13.2 seconds). The per‑block rate is derived from the supplied/borrowed amounts and the utilization rate. On 1 January 2023, Compound’s cUSDC market displayed an **annual borrow APR of ~2.8 %** and a **supply APR of ~3.1 %** (source: Compound governance forum, “Market Utilization Report Q4 2022”).  

**Steps to compute APR manually:**  

1. Retrieve the current supply or borrow rate (often expressed as a per‑second or per‑block rate).  
2. Multiply by the number of blocks (or seconds) in a year:  
   \[
   \text{APR} = \text{Rate}_{\text{per‑block}} \times 2,628,000\ (\text{blocks per year})
   \]  
3. Verify against the protocol’s displayed APR (most dashboards already do this conversion).

---

## 3. What Is APY and How Does Compounding Affect It?

**APY is the effective annual return that includes the effect of reinvesting interest.** It reflects how much your initial deposit grows when you add earned interest to the principal each compounding interval.

Compounding frequency (**n**) dramatically changes the final number. For **daily** compounding (n = 365):

\[
\text{APY}= \bigl(1+\frac{0.05}{365}\bigr)^{365} - 1 \approx 5.126\%
\]

If interest compounds **continuously**, the formula simplifies to:

\[
\text{APY}= e^{\text{APR}} - 1
\]

In DeFi, many yield aggregators (e.g., Yearn Finance, Beefy Finance) compound rewards **multiple times per day**—sometimes every block—so APY can be significantly higher than the quoted APR.

---

## 4. How to Convert APR to APY Using the Compounding Frequency?

**APY = (1 + APR ÷ n)^{n} − 1** where **n** is the number of compounding periods per year.

If a liquidity pool on Uniswap V3 reports an APR of **8 %** and rewards are claimed **hourly** (n = 8,760), the APY becomes:

\[
\text{APY}= \bigl(1+\frac{0.08}{8760}\bigr)^{8760} - 1 \approx 8.33\%
\]

Conversely, if you know the APY and want the APR:

\[
\text{APR}= n\bigl( (1+\text{APY})^{1/n} - 1 \bigr)
\]

**Typical n values in DeFi:**

- **Daily** (n = 365) – common for lending protocols that accrue interest per block, displayed as daily APY.  
- **Hourly** (n = 8,760) – used by some vault strategies that reinvest rewards every hour.  
- **Per‑block** (n ≈ 2,628,000) – DeFi chains like Ethereum have roughly 2.628 million blocks per year.  

---

## 5. What Is the Formula for APY in DeFi With Variable Rates?

**When rates change over time, the true APY is the geometric mean of the periodic rates.** If you have a series of APRs for successive periods (e.g., week 1: 5 %, week 2: 6 %), compute the product of (1 + rate) for each interval and take the 1‑year root:

\[
\text{APY}= \left(\prod_{i=1}^{m} (1 + r_i)\right)^{\frac{365}{\sum d_i}} - 1
\]

where **r_i** is the APR for period **d_i** days.

For example, a Yearn Finance vault might show:

- Week 1 APR: 12 %  
-