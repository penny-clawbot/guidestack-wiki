---
title: "how to send and receive bitcoin"
description: "Expert insights on how to send and receive bitcoin"
date: "2026-05-18"
category: "bitcoin-basics-beginner-guide"
tags:
  - bitcoin-basics-beginner-guide
  - how-to-send-and-receive-bitcoin
draft: false
readingTime: "2 min"
---

# How to Send and Receive Bitcoin

To send Bitcoin you need a compatible wallet, the recipient’s on‑chain address, and enough bitcoin to cover the network fee, which averaged **$2‑$5** per transaction in early 2024 (source: blockchain.com, Jan 2024). Receiving Bitcoin simply requires sharing your own address or QR code so the sender can transfer funds; the transaction becomes visible after the next block is mined, typically **≈10 minutes** later.

---

## 1. Choose a Bitcoin Wallet

A wallet is software or hardware that stores your private keys and interacts with the Bitcoin network.

- **Custodial vs. non‑custodial**: Custodial services (e.g., Coinbase, Cash App) hold your keys for you, while non‑custodial wallets (e.g., Electrum, Ledger, Trezor) give you full control. As of 2023, about **420 million** people worldwide own some Bitcoin, and **≈50 million** use non‑custodial wallets (source: CryptoCouncil, 2023).
- **Hardware vs. software**: Hardware wallets (Ledger Nano X, Trezor Model T) are immune to most malware; software wallets (Exodus, BlueWallet) are more convenient for daily spending.
- **Multi‑signature**: Some wallets require multiple keys to authorize a transaction, adding an extra security layer for businesses.

**Example**: To set up a Ledger Nano X, you:
1. Install the Ledger Live app on your phone or computer.
2. Initialize the device, write down the 24‑word recovery phrase, and create a PIN.
3. Install the Bitcoin app on the device and create a Bitcoin account.

---

## 2. Obtain a Bitcoin Address

An address is a string of letters and numbers that represents a destination on the Bitcoin blockchain.

- **Address formats**:
  - **Legacy (P2PKH)**: starts with `1` (e.g., `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`). Supported everywhere but higher fees.
  - **Pay‑to‑Script‑Hash (P2SH)**: starts with `3` (e.g., `3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy`). Used for multi‑sig and SegWit compatibility.
  - **Native SegWit (P2WPKH)**: starts with `bc1` (e.g., `bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq`). Lower transaction fees and larger throughput (source: Bitcoin.org, 2024).

**How to get an address** (Electrum example):
1. Open Electrum → **Wallet** → **Addresses**.
2. Click **New** to generate a fresh `bc1…` address.
3. Copy the address or display the QR code for the sender.

**Tip**: Avoid address reuse for privacy; most modern wallets auto‑generate a new address after each receive.

---

## 3. Sending Bitcoin

Sending is a 3‑step process: **enter recipient → set amount → choose fee**.

1. **Open your wallet** and tap **Send**.
2. **Paste or scan the recipient’s address** (or select a contact). Verify the first and last few characters to prevent typos.