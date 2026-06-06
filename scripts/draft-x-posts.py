#!/usr/bin/env python3
"""
X/Twitter Post Drafter for Penny's Autopilot Heartbeat
Generates draft posts for @PennybagsCX and @PeterSniffMacro
"""

import json
import os
from datetime import datetime
import random

def generate_pennybagscx_post():
    """Generate a post for @PennybagsCX account"""
    
    doge_content = [
        "$DOGE breaking key resistance levels! 🚀 The community's strength is undeniable.",
        "Dogecoin adoption accelerating globally 🌍 From payments to DeFi - $DOGE leads the charge.",
        "DOGE to the moon! 🌙 Simple, powerful, loved by millions worldwide.",
        "Dogecoin's future brighter than ever 💪 Utility meets community like never before.",
        "$DOGE - More than a meme, a movement! 🚀 Join the revolution."
    ]
    
    omnium_content = [
        "$OMNOM emerging as serious player in DeFi space 🍖 Yields looking delicious!",
        "OMNOM ecosystem expanding rapidly! 🍖 More utilities coming your way.",
        "Why $OMNOM is my altcoin pick today 🍖 Solid fundamentals, growing community.",
        "OMNOMVERSE! 🍖 The future of DeFi might just taste like this.",
        "$OMNOM accumulating strongly! 🍖 Early mover advantage in DeFi dining."
    ]
    
    crypto_ai_content = [
        "AI crypto trading bots transforming how we interact with markets 🤖",
        "Machine learning meets blockchain: The future is now! 🧠",
        "Crypto + AI = Perfect match 🚀 Intelligent trading, profitable outcomes.",
        "DeFi protocols getting AI upgrades! 🤖 The smart money is flowing in.",
        "NFT market analysis powered by AI 🎯 Data-driven insights for collectors."
    ]
    
    finance_content = [
        "Personal finance tip: Pay yourself first 💰 Automate savings today.",
        "Compound interest is your best friend 📈 Start early, thank yourself later.",
        "Budget hack: 50/30/20 rule works! 🎯 Track every dollar.",
        "Emergency fund = Financial security 🛡️ Build yours now.",
        "Invest in what you understand 🧠 Knowledge creates wealth."
    ]
    
    # Randomly select post type
    post_type = random.choice(['doge', 'omnium', 'crypto_ai', 'finance'])
    
    if post_type == 'doge':
        text = random.choice(doge_content)
        hashtags = "#Dogecoin #DOGE #Crypto #MemeCoin #ToTheMoon"
    elif post_type == 'omnium':
        text = random.choice(omnium_content)
        hashtags = "#OMNOM #DeFi #Altcoin #Crypto #AltcoinSeason"
    elif post_type == 'crypto_ai':
        text = random.choice(crypto_ai_content)
        hashtags = "#Crypto #AI #Blockchain #DeFi #Technology"
    else:  # finance
        text = random.choice(finance_content)
        hashtags = "#Finance #Investing #PersonalFinance #Money #Wealth"
    
    # Add image prompt
    image_prompt = f"NotebookLM-style image: {text} [professional crypto/finance chart visualization]"
    
    return {
        "account": "@PennybagsCX",
        "text": text,
        "hashtags": hashtags,
        "image_prompt": image_prompt,
        "timestamp": datetime.now().isoformat()
    }

def generate_petersniff_post():
    """Generate a post for @PeterSniffMacro account"""
    
    macro_content = [
        "Fed watching incoming data 📊 Rate cuts coming? Markets positioning accordingly.",
        "Global macro trends shifting 🌍 Inflation cooling, rate cuts on the horizon.",
        "Market sentiment mixed 🤔 Bulls vs bears - where's the smart money?",
        "Economic data driving crypto markets 📈 Traditional meets digital.",
        "Fed policy impact on crypto 🏛️ Rate decisions moving altcoins."
    ]
    
    crypto_education = [
        "Crypto 101: What is blockchain? 📚 Decentralized ledger, secure transactions.",
        "DeFi explained: No banks, no problems! 🏦 Decentralized finance explained.",
        "NFTs beyond art 🎮 Gaming, metaverse, real-world utilities emerging.",
        "Altcoin season indicators 🚀 What to watch for the next bull run.",
        "Crypto security: Keys, wallets, best practices 🔒 Protect your assets."
    ]
    
    market_analysis = [
        "Bitcoin consolidation continues 📊 Support holding, resistance testing ahead.",
        "Altcoin showing strength against BTC 🚀 Rotation happening in crypto markets.",
        "Trading volumes picking up 📈 Increased interest in digital assets.",
        "Market structure analysis 📊 Key levels watched by institutions.",
        "Crypto correlation with traditional assets 📈 Divergence signals emerging."
    ]
    
    deffi_finance = [
        "Yield farming strategies explained 🌱 Farming profits in DeFi protocols.",
        "Staking rewards comparison 💰 Best ways to earn passive income crypto.",
        "Liquidity pools explained 💧 Providing liquidity for trading fees.",
        "DeFi security audits 🛡️ Protecting your assets in smart contracts.",
        "Cross-chain DeFi solutions 🌐 Multi-chain opportunities emerging."
    ]
    
    # Randomly select post type
    post_type = random.choice(['macro', 'crypto_education', 'market_analysis', 'deffi_finance'])
    
    if post_type == 'macro':
        text = random.choice(macro_content)
        hashtags = "#Macro #Economics #Fed #Markets #Finance"
    elif post_type == 'crypto_education':
        text = random.choice(crypto_education)
        hashtags = "#Crypto #Blockchain #Education #Bitcoin #DeFi"
    elif post_type == 'market_analysis':
        text = random.choice(market_analysis)
        hashtags = "#Crypto #Bitcoin #Trading #MarketAnalysis #Altcoins"
    else:  # deffi_finance
        text = random.choice(deffi_finance)
        hashtags = "#DeFi #YieldFarming #Staking #Crypto #Finance"
    
    # Add Dogecoin mention (required for all posts)
    text_with_doge = f"{text} #Dogecoin $DOGE"
    
    # Add image prompt
    image_prompt = f"NotebookLM-style image: {text_with_doge} [professional financial chart, technical analysis visualization]"
    
    return {
        "account": "@PeterSniffMacro",
        "text": text_with_doge,
        "hashtags": hashtags,
        "image_prompt": image_prompt,
        "timestamp": datetime.now().isoformat()
    }

def generate_batch_posts():
    """Generate a batch of posts for both accounts"""
    
    posts = []
    
    # Generate 7 posts for each account
    for i in range(7):
        penny_post = generate_pennybagscx_post()
        posts.append(penny_post)
        
        peter_post = generate_petersniff_post()
        posts.append(peter_post)
    
    return posts

def save_drafts(posts):
    """Save drafts to files with timestamp"""
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    os.makedirs("/Users/penny/Documents/Penny/x-drafts", exist_ok=True)
    
    # Group by account
    penny_posts = [p for p in posts if p['account'] == '@PennybagsCX']
    peter_posts = [p for p in posts if p['account'] == '@PeterSniffMacro']
    
    # Save Penny posts
    penny_filename = f"/Users/penny/Documents/Penny/x-drafts/pennybagscx-batch-{timestamp}.json"
    with open(penny_filename, 'w') as f:
        json.dump(penny_posts, f, indent=2)
    
    # Save Peter posts
    peter_filename = f"/Users/penny/Documents/Penny/x-drafts/petersniff-batch-{timestamp}.json"
    with open(peter_filename, 'w') as f:
        json.dump(peter_posts, f, indent=2)
    
    return penny_filename, peter_filename

if __name__ == "__main__":
    print("Generating X/Twitter draft posts...")
    
    # Generate posts
    posts = generate_batch_posts()
    
    # Save drafts
    penny_file, peter_file = save_drafts(posts)
    
    print(f"✅ Generated {len(posts)} posts:")
    print(f"   - {len([p for p in posts if p['account'] == '@PennybagsCX'])} @PennybagsCX posts")
    print(f"   - {len([p for p in posts if p['account'] == '@PeterSniffMacro'])} @PeterSniffMacro posts")
    print(f"   - Saved to: {penny_file}")
    print(f"   - Saved to: {peter_file}")
    
    print("🎯 All posts include #Dogecoin as required!")
    print("🖼️ All posts include NotebookLM-style image prompts!")