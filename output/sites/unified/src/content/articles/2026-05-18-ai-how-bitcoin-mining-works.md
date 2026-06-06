---
title: "how bitcoin mining works"
description: "Answers to your questions about how bitcoin mining works"
date: "2026-05-18"
category: "bitcoin-basics-beginner-guide"
tags:
  - bitcoin-basics-beginner-guide
  - how-bitcoin-mining-works
draft: false
readingTime: "7 min"
---

# How Bitcoin Mining Works: A Complete Guide

Bitcoin mining is the process by which new transactions are verified and added to the blockchain ledger using specialized computer hardware to solve complex mathematical puzzles, earning newly created bitcoins as rewards. This article answers the eight most common questions about how Bitcoin mining works, its economics, and its environmental impact.

## What is Bitcoin mining and how does it function?


![Hero image for how bitcoin mining works](https://picsum.photos/seed/how-bitcoin-mining-works-hero/1200/630)


Bitcoin mining is the process of adding valid transaction blocks to the Bitcoin blockchain by solving computationally intensive mathematical puzzles called Proof of Work. Miners use specialized hardware called ASICs (Application-Specific Integrated Circuits) to repeatedly hash candidate block headers, adjusting a variable called the "nonce" until the hash output meets the network's difficulty target. When a miner finds a hash below the target, they broadcast the block to the network, and all other nodes verify the solution before accepting the new block. The miner who successfully solves the block first receives the **block reward of 6.25 BTC** (as of April 2024), along with transaction fees from all transactions included in that block. This entire process takes approximately **10 minutes per block** on average.

## How do miners earn rewards and what are the current incentives?

Miners earn two types of rewards: the **block subsidy** (newly minted BTC) and **transaction fees** paid by users. The block subsidy started at 50 BTC in 2009 and halves every 210,000 blocks (approximately every 4 years) — this event is called the "halving." The current subsidy of 6.25 BTC will reduce to 3.125 BTC in 2028. According to Blockchain.com, miners earned approximately **$1.8 billion in combined revenue** in the first quarter of 2026, with transaction fees comprising roughly 15-20% of total miner revenue. Successful miners typically join mining pools to combine their hash power and receive proportional payouts, with major pools including Foundry USA (35% market share), AntPool (15%), and Binance Pool (12%) as of mid-2024.

## What hardware is required for Bitcoin mining?


![Illustration for how bitcoin mining works](https://picsum.photos/seed/how-bitcoin-mining-works-mid/1200/630)


Modern Bitcoin mining requires **ASIC miners**, purpose-built devices designed solely for SHA-256 hashing. Leading manufacturers include Bitmain (Antminer series), MicroBT (WhatsMiner series), and Canaan (Avalon series). Current generation machines like the Bitmain Antminer S21 Pro achieve **335 terahashes per second (TH/s)** with an energy efficiency of approximately **16 joules per terahash (J/TH)**. Older machines such as the Antminer S9 (14 TH/s) are largely unprofitable at current difficulty levels. Prices for top-tier miners range from $2,000 to $15,000 depending on specifications and market conditions. ASIC miners cannot be repurposed for other computing tasks — they exist solely for cryptocurrency mining, which distinguishes them from general-purpose GPUs.

## How does mining difficulty adjust and why does it matter?

Bitcoin's mining difficulty adjusts every **2016 blocks (approximately 14 days)** to maintain a consistent 10-minute block time regardless of total network hash rate. Difficulty increases when more miners join the network (hash rate rises) and decreases when miners leave (hash rate falls). As of 2026, the network's total hash rate exceeds **600 exahashes per second (EH/s)**, according to data from MiningPoolStats and BTC.com. The difficulty target is encoded as a 256-bit number, and miners must find a hash below this target — a probability of approximately **1 in 4 trillion** per hash attempt with current difficulty levels. Higher difficulty means miners need more computational power and electricity to earn the same rewards, directly impacting profitability calculations.

## What are the energy costs and environmental considerations?

Bitcoin mining consumes significant electricity, with the Cambridge Centre for Alternative Finance estimating annual consumption at approximately **120-150 TWh** as of 2026 — comparable to the electricity usage of some small countries. The industry's sustainability has improved: the Bitcoin Mining Council estimates that **59.4% of mining electricity** came from sustainable sources in early 2024, up from 56% in 2023. Mining operations often locate near cheap hydroelectric, solar, or wind power to minimize costs. Critics point to carbon emissions concerns, while supporters note mining can monetize otherwise stranded renewable energy. Major mining companies, including Riot Platforms and Marathon Digital Holdings, have committed to achieving carbon neutrality through renewable energy procurement and carbon credits.

## How profitable is Bitcoin mining, and what factors determine it?

Mining profitability depends on four primary factors: **electricity costs, hardware efficiency, Bitcoin's price, and network difficulty**. The variable is electricity cost, which ranges from $0.03/kWh in countries like Kazakhstan and Iran to over $0.20/kWh in Germany or California. A modern ASIC with 20 J/TH running at $0.05/kWh electricity generates approximately **$0.08 per TH/s per day** in profit (before hardware depreciation). This means a single Antminer S21 Pro (335 TH/s) could generate roughly **$26 daily profit** at current BTC prices and difficulty levels. However, the Bitcoin network's difficulty adjustment means profitability can shift rapidly — during the 2022 bear market, many miners shut down operations as electricity costs exceeded mining revenue. Miners typically calculate payback periods of 18-36 months when purchasing new equipment.

## Can individual users mine Bitcoin profitably?

Individual mining is largely unprofitable without access to extremely cheap electricity and expensive, specialized hardware. Solo mining requires winning an entire block reward (6.25 BTC, worth approximately $400,000 at $64,000 BTC prices) with one machine — statistically improbable for any single consumer device. However, individuals can participate through **cloud mining contracts** (purchasing hash power from large operations), though many such services are scams. Alternatively, users can join **mining pools** to receive small, consistent payouts proportional to their contributed hash power, though pool fees typically range from 1-4%. The minimum viable entry point today requires investing $2,000-5,000 in hardware plus securing electricity costs under $0.08/kWh to compete effectively.

## What is the future outlook for Bitcoin mining?

Bitcoin mining's future involves several trends: **technological efficiency improvements** will continue as manufacturers approach physical limits of silicon; the block reward will halve again in 2028, making transaction fees increasingly important for miner revenue; and regulatory scrutiny will grow as governments classify mining operations under energy and financial regulations. The mining industry is shifting toward **institutionalization**, with publicly traded mining companies (Riot Platforms, Marathon Digital, Cleanspark) controlling growing market share. Some miners are exploring **digital sustainability certificates** and grid services to monetize their flexibility — selling electricity back during peak demand periods. The 2026 halving cycle has seen increased consolidation as less efficient operators exit while better-capitalized companies expand.

## Frequently Asked Questions

### How long does it take to mine one Bitcoin?

With the current network difficulty and average hashrate, it would take a single modern ASIC miner (335 TH/s) approximately **1,200 days** to find a block solo. Mining pools distribute work so participants receive smaller, regular payouts proportional to their contribution.

### Is Bitcoin mining legal?

Bitcoin mining is legal in most countries, including the United States, Canada, and most of Europe. It is banned or heavily restricted in China (as of 2021), and some countries have unclear regulations. Always verify local laws before starting mining operations.

### What happens when all 21 million bitcoins are mined?

The final Bitcoin will be mined approximately in **year 2140**, after which miners will earn only from transaction fees. This gradual transition ensures the network remains secured as the block subsidy disappears, with fees incentivizing miners to continue validating transactions.

### Can mining damage my hardware?

ASIC miners generate substantial heat (requiring proper cooling) and operate continuously at high utilization. With adequate ventilation, temperature control, and maintenance, hardware typically lasts **3-5 years** before becoming uncompetitive. Power surges and overheating are the primary failure causes.

### How do I calculate mining profitability?

Use the formula: **Daily Profit = (Mining Revenue) - (Electricity Cost)**, where mining revenue depends on your share of network hashrate and current BTC price. Online calculators like WhatToMine.com and CryptoCompare provide real-time estimates when you input your specific hardware, electricity cost, and location.

### Does Bitcoin mining use more energy than traditional banking?

According to the Cambridge Centre for Alternative Finance, Bitcoin currently consumes approximately **0.3% of global electricity production**. Studies like Galaxy Digital's 2021 analysis suggest traditional banking's energy footprint (including data centers, branch operations, and ATM networks) may exceed Bitcoin mining's consumption, though direct comparisons remain controversial due to differing methodologies.

### Can I mine Bitcoin on my laptop or phone?

CPU and GPU mining for Bitcoin is completely unprofitable in 2026. The SHA-256 algorithm was specifically designed to be efficiently computed by ASIC hardware, making general-purpose processors millions of times slower than purpose-built miners. Any app claiming to mine Bitcoin on phones or laptops is either fraudulent or mining a different, less profitable cryptocurrency.

### What is a mining pool and how does it work?

Mining pools combine the hash power of multiple miners to find blocks more frequently, then distribute rewards proportionally based on each member's contributed work. Popular pools include Foundry USA, AntPool, and ViaBTC. Pools typically charge fees of **1-4%** of earnings and use payment systems like Pay-Per-Share (PPS) or Full Pay Per Share (FPPS) to guarantee regular payouts.