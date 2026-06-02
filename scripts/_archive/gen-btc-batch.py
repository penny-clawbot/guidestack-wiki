#!/usr/bin/env python3
"""Batch generate 13 remaining bitcoin-beginners articles (2500+ words each)."""
import json, os, sys, urllib.request, re, time
from datetime import datetime

API_KEY = os.environ.get("MINIMAX_API_KEY", "")
if not API_KEY:
    try:
        with open(os.path.expanduser("~/.zshrc")) as f:
            for line in f:
                if "MINIMAX_API_KEY" in line and "export" in line:
                    API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    except: pass

if not API_KEY:
    print("ERROR: No MINIMAX_API_KEY found")
    sys.exit(1)

BASE_URL = "https://api.minimax.io/anthropic/v1/messages"
MODEL = "MiniMax-M2.7"

TOPICS = [
    ("Bitcoin Wallet Security: How to Protect Your Crypto", "bitcoin-wallet-security"),
    ("Bitcoin Halving Cycles: What Every Beginner Needs to Know", "bitcoin-halving-cycles"),
    ("Bitcoin Mining Explained: How New Coins Are Created", "bitcoin-mining-explained"),
    ("Lightning Network: Bitcoin's Scaling Solution for Beginners", "lightning-network-bitcoin-scaling"),
    ("Bitcoin ETFs: Everything You Need to Know", "bitcoin-etfs-guide"),
    ("How to Store Bitcoin Safely: Hot vs Cold Wallets", "bitcoin-hot-cold-wallets"),
    ("Bitcoin vs Traditional Investments: Pros and Cons", "bitcoin-vs-traditional-investments"),
    ("Common Bitcoin Scams and How to Avoid Them", "common-bitcoin-scams"),
    ("Bitcoin Tax Guide: What Beginners Must Know", "bitcoin-tax-guide"),
    ("How to Send and Receive Bitcoin Step by Step", "send-receive-bitcoin-guide"),
    ("Bitcoin Price History and What Drives It", "bitcoin-price-history"),
    ("Best Bitcoin Exchanges for Beginners in 2026", "best-bitcoin-exchanges-2026"),
    ("What Is Blockchain: The Technology Behind Bitcoin", "blockchain-technology-explained"),
]

OUTPUT_DIR = "/Users/penny/Documents/Penny/pseo-network/data/content/bitcoin-beginners"

def generate_article(topic: str, niche: str = "bitcoin-beginners", words: int = 2800) -> str:
    prompt = f"""Write a comprehensive, SEO-optimized article about: {topic}

Niche: {niche} (targeting beginners)
Target length: 2500-3000 words (be thorough and detailed)

Requirements:
- Compelling H1 title with the main keyword
- Engaging introduction (2-3 paragraphs) with a strong hook
- 6-8 H2 sections with detailed subheadings
- Include H3 subheadings where appropriate for deeper coverage
- Practical tips, real-world examples, statistics, or data throughout
- Use bullet points and numbered lists for readability
- Include a FAQ section at the end with 5-6 common questions
- Conclusion with actionable next steps and call-to-action
- Natural keyword usage (primary + related keywords)
- Write in an authoritative but friendly, beginner-friendly tone
- No jargon without explanation

Output ONLY the article in markdown format starting with # Title. No preamble."""

    body = json.dumps({
        "model": MODEL,
        "max_tokens": 16000,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }).encode()

    req = urllib.request.Request(BASE_URL, data=body, headers={
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    })

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read())
            for block in data.get("content", []):
                if block.get("type") == "text" and block.get("text", "").strip().startswith("#"):
                    return block["text"]
            for block in data.get("content", []):
                if block.get("type") == "text" and len(block["text"]) > 500:
                    return block["text"]
            return ""
    except Exception as e:
        return f"ERROR: {e}"

def add_frontmatter(content: str, title: str, slug: str) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    # Extract first meaningful paragraph for description
    lines = content.split("\n\n")
    desc = ""
    for line in lines[1:]:
        clean = line.strip().replace("#", "").replace("*", "").replace('"', "'")
        if len(clean) > 50:
            desc = clean[:160]
            break
    if not desc:
        desc = title[:160]

    return f"""---
title: "{title.replace('"', '\\"')}"
slug: "{slug}"
date: "{today}"
description: "{desc.replace('"', '\\"')}"
category: "bitcoin-beginners"
tags: ["bitcoin", "beginners", "{slug.split('-')[0]}"]
---

{content}"""

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Check what already exists
    existing = set(os.listdir(OUTPUT_DIR))
    print(f"Existing articles: {len(existing)}")
    
    generated = 0
    failed = 0
    
    for i, (topic, slug) in enumerate(TOPICS):
        filename = f"{datetime.now().strftime('%Y-%m-%d')}-{slug}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # Check if already generated (any date prefix with this slug)
        already_exists = any(slug in f for f in existing)
        if already_exists:
            print(f"⏭️  [{i+1}/{len(TOPICS)}] {slug} — already exists, skipping")
            continue
        
        print(f"📝 [{i+1}/{len(TOPICS)}] Generating: {topic}...")
        article = generate_article(topic)
        
        if article and not article.startswith("ERROR"):
            word_count = len(article.split())
            final = add_frontmatter(article, topic, slug)
            with open(filepath, "w") as f:
                f.write(final)
            print(f"✅ {filename} ({word_count} words, {len(final)} chars)")
            generated += 1
            existing.add(filename)
        else:
            print(f"❌ Failed: {topic} — {article[:200]}")
            failed += 1
        
        # Small delay between API calls
        if i < len(TOPICS) - 1:
            time.sleep(2)
    
    print(f"\n{'='*50}")
    print(f"Generated: {generated} | Failed: {failed} | Total existing: {len(os.listdir(OUTPUT_DIR))}")

if __name__ == "__main__":
    main()
