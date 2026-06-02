#!/usr/bin/env python3
"""Regenerate remaining short bitcoin-beginners articles - batch 2."""
import json, os, sys, urllib.request, time
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

BASE_URL = "https://api.minimax.io/anthropic/v1/messages"
MODEL = "MiniMax-M2.7"
OUTPUT_DIR = "/Users/penny/Documents/Penny/pseo-network/data/content/bitcoin-beginners"

REGEN = [
    ("What Is the Bitcoin Lightning Network: Complete Beginner's Guide to Fast BTC Payments", "what-is-the-bitcoin-lightning-network"),
    ("Bitcoin vs Ethereum: Key Differences Every Beginner Should Understand in 2026", "bitcoin-vs-ethereum-key-differences-explained"),
    ("Understanding Bitcoin Halving Cycles: How They Affect Price, Supply, and Mining", "understanding-bitcoin-halving-cycles"),
    ("How to Buy Bitcoin for the First Time: Complete Step-by-Step Guide for Beginners", "how-to-buy-bitcoin-for-the-first-time"),
    ("Bitcoin Price History: From Pennies to Thousands — The Complete Story", "bitcoin-price-history-from-pennies-to-thousands"),
    ("Bitcoin Wallets Explained: Hardware, Software, and Paper Wallets Compared", "bitcoin-wallets-explained-hardware-software-and-paper-wallets"),
    ("How to Avoid Bitcoin Scams and Fraud: Essential Security Guide for Beginners", "how-to-avoid-bitcoin-scams-and-fraud"),
    ("Bitcoin Forks Explained: Hard Forks vs Soft Forks and What They Mean", "bitcoin-forks-hard-forks-vs-soft-forks-explained"),
]

def generate_article(topic: str) -> str:
    prompt = f"""Write a VERY comprehensive, SEO-optimized article about: {topic}

CRITICAL: This article MUST be at least 2,500 words. Do NOT stop early. Write thoroughly.

Niche: bitcoin-beginners
Structure:
- H1 title with primary keyword
- 3-4 paragraph intro with hook and statistics
- 7-9 H2 sections with H3 subheadings
- Bullet points, numbered lists, tables where appropriate
- FAQ section with 6 questions at end
- Conclusion with next steps

Be detailed, use examples, data, and write in beginner-friendly tone.
Output ONLY markdown starting with # Title."""

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
    generated = 0
    for i, (topic, slug) in enumerate(REGEN):
        filename = f"{datetime.now().strftime('%Y-%m-%d')}-{slug}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)
        print(f"[{i+1}/{len(REGEN)}] {topic}...", flush=True)
        article = generate_article(topic)
        if article and not article.startswith("ERROR"):
            wc = len(article.split())
            with open(filepath, "w") as f:
                f.write(add_frontmatter(article, topic, slug))
            print(f"  OK {wc} words", flush=True)
            generated += 1
        else:
            print(f"  FAIL: {article[:100]}", flush=True)
        if i < len(REGEN) - 1:
            time.sleep(2)
    print(f"\nDone: {generated}/{len(REGEN)}")
    print(f"Total files: {len(os.listdir(OUTPUT_DIR))}")

if __name__ == "__main__":
    main()
