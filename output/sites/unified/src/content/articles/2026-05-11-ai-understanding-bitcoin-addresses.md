---
title: "understanding bitcoin addresses"
description: "Curated picks for understanding bitcoin addresses"
date: "2026-05-11"
category: "bitcoin-basics-beginner-guide"
tags:
  - bitcoin-basics-beginner-guide
  - understanding-bitcoin-addresses
draft: false
readingTime: "2 min"
niche: "bitcoin-beginners"
---

# Understanding Bitcoin Addresses  

The most practical Bitcoin address formats for typical users are **Legacy (P2PKH)**, **SegWit (P2WPKH)** and **Native SegWit (Bech32)**, each offering a balance of security, low fees, and broad wallet support. For advanced needs such as privacy or multisig, **Taproot (P2TR)**, **Multi‑Signature**, and **HD‑Wallet‑derived addresses** provide extra features, albeit with slightly higher complexity.

---

## 1. Legacy (P2PKH) Address  

**Pros**  
- Universal compatibility with all Bitcoin software since 2009.  
- Proven security track record (≈ 9/10 rating).  

**Cons**  
- Largest transaction size → highest fees (≈ 0.00015 BTC ≈ $5.00 on 2025‑01‑25).  
- Slower validation for SPV wallets.  

**Details & Data**  
Legacy addresses start with `1` and use the Pay‑to‑Public‑Key‑Hash format. In 2024, about **12 %** of all Bitcoin UTXOs were stored in P2PKH addresses (source: bitinfocharts.com). Transaction size averages **~ 226 bytes**, which translates to fees of **$4–$6** during normal network activity.  

**Best for** Users who need absolute backwards‑compatibility or are running older node software.

---

## 2. P2SH (Pay‑to‑Script‑Hash) Address  

**Pros**  
- Supports multi‑signature and other advanced scripts while keeping the address format short (`3`).  
- Enables **M‑of‑N** setups without exposing the full script on‑chain.  

**Cons**  
- Slightly larger script size than pure SegWit, leading to fees ~ 0.00012 BTC (≈ $4.10).  
- Requires the recipient to provide the correct redeem script.  

**Details & Data**  
P2SH addresses constitute roughly **31 %** of all Bitcoin addresses as of Q4 2024 (source: blockchain.com). A typical 2‑of‑3 multisig transaction weighs **~ 250 bytes**, costing **~$4.00** in fees at a median fee rate of **15 sats/vB**.  

**Best for** Services that need multisig (e.g., escrow, corporate treasuries) while maintaining a familiar `3` prefix.

---

## 3. Native SegWit (P2WPKH) Address  

**Pros**  
- Reduces transaction weight by ~ 40 % → fees drop to **0.00008 BTC** (≈ $2.70).  
- Faster SPV verification and better compatibility with modern hardware wallets.  

**Cons**  
- Some legacy Bitcoin ATMs and older mobile wallets still lack full support.  

**Details & Data**  
Addresses begin with `bc1q` and are defined by BIP‑84. On 2025‑01‑25 the median fee rate was **10 sats/vB**, making a typical 1‑input, 2‑output P2WPKH transaction **~ 140 bytes** → **~$2.70**. Native SegWit now accounts for **~ 44 %** of all on‑chain addresses (source: mempool.space).  

**Best for** Everyday spending, HODLing, and any user wanting the best fee‑to‑privacy ratio.

---

## 4. SegWit‑v1 (P2TR / Taproot) Address  

**Pros**  
- **Single‑key** and **multi‑key** spends look identical → enhanced privacy (1/10 privacy boost).  
- Up to **50 %** reduction in total transaction size for complex scripts.  

**Cons**  
- Newer standard; wallet support still rolling out (≈ 85 % of major wallets as of early 2025).  
- Requires **BIP‑341** & **BIP‑342** compliance.  

**Details & Data**  
Taproot addresses start with `bc1p`. A typical 1‑input, 1‑output P2TR transaction is **~ 110 bytes**, costing **≈ $1.90** at 10 sats/vB. According to a 2024 analysis by Bitcoin Optech, Taproot adoption reached **≈ 12 %** of new outputs, with a projected growth to **30 %** by 2026.  

**Best for** Power users seeking maximum privacy and the ability to bundle complex scripts (e.g., Lightning Network‑ready channels).

---

## 5. Multi‑Signature (M‑of‑N) Address  

**Pros**  
- Distributed control reduces single‑point‑of‑failure risk (security rating **9.5/10**).  
- Configurable quorum (e.g., 2‑of‑3, 3‑of‑5).  

**Cons**  
- Larger transaction size → fees ~ 0.00016 BTC (≈ $5.40) for a 2‑of‑3 spend.  
- Requires coordination among signers.  

**Details & Data**  
Multi‑sig addresses (usually P2SH or P2WSH) can be created with tools like **Electrum** or **Casa**. A 2‑of‑3 P2WSH transaction