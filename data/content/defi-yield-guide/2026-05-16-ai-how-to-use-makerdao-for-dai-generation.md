---
title: "how to use makerdao for dai generation"
description: "Step-by-step: how to use makerdao for dai generation"
date: "2026-05-16"
category: "decentralized-finance-yield-farming-defi-guide"
tags:
  - decentralized-finance-yield-farming-defi-guide
  - how-to-use-makerdao-for-dai-generation
draft: false
readingTime: "3 min"
---

# How to Use MakerDAO for DAI Generation  

This guide walks you through opening a MakerDAO Vault, depositing collateral, and minting DAI, covering wallet setup, collateral selection, risk parameters, and fee management as of early 2024.  

## Step‑by‑Step Instructions  

### Step 1: Set Up a Web3 Wallet  
1. **Choose a wallet** – MetaMask, Coinbase Wallet, or any Web3‑compatible wallet that supports Ethereum mainnet.  
2. **Install the browser extension** and create a secure password.  
3. **Back up your seed phrase** offline (e.g., on paper) and store it in a safe place.  
4. **Switch to Ethereum Mainnet** (Settings → Networks → Ethereum).  

*Tip*: Ensure your wallet has enough ETH to cover transaction gas. As of Feb 2024, average gas for a Vault open/close transaction is ~150 k gas (~0.006 ETH at 30 gwei).  

### Step 2: Acquire and Transfer Collateral  
- **ETH** is the most common collateral, but MakerDAO also supports **WBTC, USDC, UNI, LINK, AAVE**, and more.  
- Purchase ETH on an exchange (e.g., Coinbase, Binance).  
- Withdraw to the address shown in your wallet (double‑check the network).  
- Confirm the transaction on Etherscan.  

*Numbers*: ETH‑A collateral type (ETH) has a **liquidation ratio of 150 %** and a **debt ceiling of 500 million DAI** (as of Jan 2024).  

### Step 3: Connect to the MakerDAO Interface  
1. Go to **https://app.makerdao.com/** (official MakerDAO portal).  
2. Click **“Connect Wallet”** and select your wallet provider.  
3. Approve the connection request in your wallet pop‑up.  
4. You will see the main dashboard with “Open Vault” and a list of supported collateral types.  

### Step 4: Select Collateral Type and Set Parameters  
- Choose the **collateral type** (e.g., **ETH‑A**). Each type has its own stability fee, liquidation ratio, and debt ceiling.  
- **Stability Fee (SF)**: the annual interest you pay on the DAI you generate. As of Feb 2024:  
  - ETH‑A: **2.5 % per year**  
  - WBTC‑A: **3.0 % per year**  
  - USDC‑P (Pegged): **0.1 % per year** (requires a separate PSM vault).  
- **Collateralization Ratio (CR)**: you must keep your vault’s CR above the liquidation ratio; a **200 % CR** is a safe target to avoid liquidation.  
- **Debt Ceiling**: the maximum amount of DAI you can generate for that collateral type (visible in the UI).  

*Tip*: If you need more borrowing power, you can add more collateral later, but you cannot exceed the debt ceiling.  

### Step 5: Deposit Collateral and Generate DAI  
1. Click **“Open Vault”** for the selected collateral.  
2. **Deposit** the amount of collateral you wish to lock (e.g., 1 ETH).  
3. **Set the DAI amount** you want to mint. The UI will show the resulting collateralization ratio in real‑time.  
4. Review the **estimated stability fee** and the **liquidation price**.  
5. Click **“Generate DAI”** and confirm the transaction in your wallet.  
6. After the transaction is mined (≈1 minute on Ethereum), your DAI appears in your wallet and your vault shows the locked collateral.  

*Example*: Locking 1 ETH at a price of $2,000 (≈$2,000 collateral) and generating 1,000 DAI yields a **CR of 200 %** (200 % = $2,000 / $1,000).  

### Step 6: Monitor Your Vault and Manage Risk  
- **Dashboard** displays:  
  - Current collateral amount and USD value.  
  - Outstanding DAI debt.  
  - Current collateralization ratio.  
  - Liquidation price (price at which your ratio hits 150 %).  
- **If the ratio approaches 150 %**, you can:  
  - **Add more collateral** (increase the denominator).  
  - **Repay some DAI** (decrease the numerator).  

*Numbers*: MakerDAO’s **Liquidation Penalty** is 13 % (as of 2024). If your vault is liquidated, 13 % of the collateral is sold at a discount to cover the debt.  

### Step 7: Withdraw Collateral or Repay DAI  
1. Open your vault in the MakerDAO UI.  
2. To **withdraw collateral**, you must first ensure the resulting CR stays above the liquidation ratio.  
3. To **repay DAI**, transfer DAI back to the vault’s “Payback” button; the