#!/usr/bin/env python3
"""Single article regeneration - Bitcoin Price History."""
import json, os, sys, urllib.request
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

topic = "The Complete History of Bitcoin Prices: From $0.003 to $100,000+ — Every Major Bull and Bear Market Explained"
slug = "bitcoin-price-history-from-pennies-to-thousands"

prompt = f"""Write an extremely detailed, comprehensive article about: {topic}

CRITICAL: This article MUST be at least 3,000 words minimum. I need every paragraph to be thorough and detailed. Do NOT summarize or skip sections.

Cover ALL of these topics in detail:
1. Bitcoin's creation in 2009 and the first real price discovery
2. The 2011 bubble and crash (Mt. Gox era)
3. The 2013 double bubble ($266 then $1,100)
4. The 2014-2015 bear market and Mt. Gox collapse
5. The 2017 bull run to $20,000 and ICO craze
6. The 2018 crypto winter
7. The 2020 COVID crash and recovery
8. The 2021 bull market to $69,000 (institutions, Tesla, El Salvador)
9. The 2022 bear market (Luna, FTX, Celsius)
10. The 2023-2024 recovery and spot ETF approval
11. The 2025-2026 cycle and current state
12. Key drivers of Bitcoin price (halving, adoption, macro, regulation)
13. Price prediction frameworks and what to watch
14. FAQ section with 8 questions

Use real price data, dates, and events. Include specific numbers and percentages.
Write in an engaging, beginner-friendly style.

Output ONLY markdown starting with # Title. No preamble."""

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
        article = ""
        for block in data.get("content", []):
            if block.get("type") == "text" and block.get("text", "").strip().startswith("#"):
                article = block["text"]
                break
        if not article:
            for block in data.get("content", []):
                if block.get("type") == "text" and len(block["text"]) > 500:
                    article = block["text"]
                    break
        
        if article:
            wc = len(article.split())
            title = article.split("\n")[0].lstrip("# ").strip()
            lines = article.split("\n\n")
            desc = ""
            for line in lines[1:]:
                clean = line.strip().replace("#", "").replace("*", "").replace('"', "'")
                if len(clean) > 50:
                    desc = clean[:160]
                    break
            if not desc: desc = title[:160]
            
            frontmatter = f"""---
title: "{title.replace('"', '\\"')}"
slug: "{slug}"
date: "{datetime.now().strftime('%Y-%m-%d')}"
description: "{desc.replace('"', '\\"')}"
category: "bitcoin-beginners"
tags: ["bitcoin", "price", "history", "beginners"]
---

{article}"""
            
            filename = f"{datetime.now().strftime('%Y-%m-%d')}-{slug}.md"
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, "w") as f:
                f.write(frontmatter)
            print(f"OK {wc} words -> {filename}", flush=True)
        else:
            print("FAIL: no article content", flush=True)
except Exception as e:
    print(f"ERROR: {e}", flush=True)
