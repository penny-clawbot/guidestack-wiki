---
title: "bitcoin sign message verify"
description: "Step-by-step: bitcoin sign message verify"
date: "2026-05-16"
category: "bitcoin-basics-beginner-guide"
tags:
  - bitcoin-basics-beginner-guide
  - bitcoin-sign-message-verify
draft: false
readingTime: "1 min"
---

# Bitcoin Sign Message Verify – A Step‑by‑Step Guide  

This guide walks you through **signing a message with a Bitcoin private key** and **verifying that signature** using popular wallets and command‑line tools. By the end you will be able to prove ownership of any address without moving funds, using the standard Bitcoin message format defined in **BIP‑137** (legacy) and **BIP‑322** (modern).

---

## Step-by-Step Instructions  

### Step 1: Verify Wallet Compatibility  

| Wallet | Minimum Version | Required Settings |
|--------|------------------|-------------------|
| **Bitcoin Core** | 24.0 (released Oct 2023) | Enable `wallet` and `server` |
| **Electrum** | 4.3 + (Apr 2023) | Standard wallet |
| **Ledger Live** | 2.10 + (Jan 2024) | Firmware ≥ 2.1.0 |
| **Trezor Suite** | 22.6 + (Nov 2023) | Firmware ≥ 1.10.0 |

- Ensure you have **a funded address** (any balance is fine) and your **private keys are secured**.  
- For hardware wallets, complete the **initial setup** and **update the firmware** to the latest version (e.g., Ledger firmware 2.1.0 released Feb 2024).  

### Step 2: Sign a Message with Bitcoin Core (GUI)  

1. Open **Bitcoin Core** (v24.0 or later).  
2. Click **File → Sign Message**.  
3. In the dialog, paste the **Bitcoin address** you own.  
4. Enter your message, e.g., `I own this address 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`.  
5. Click **Sign**. The GUI displays a **base64‑encoded signature** (65‑byte ECDSA signature + 1 byte recovery id).  
6. Copy the signature string.  

> **Tip:** Bitcoin Core automatically adds the prefix `\x18Bitcoin Signed Message:\n` followed by the message length, as required by BIP‑137.

### Step 3: Sign a Message with Bitcoin Core CLI  

```bash
# 1️⃣ Create a P2SH‑segwit address (or use an existing one)
bitcoin-cli getnewaddress "my_label" "p2sh-segwit"

# 2️⃣ Sign the message (replace <address> and <message>)
bitcoin-cli signmessage "<address>" "I own this address 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
```

The CLI returns a **base64 signature**, e.g.