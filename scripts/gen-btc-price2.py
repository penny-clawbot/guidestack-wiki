#!/usr/bin/env python3
import json, os, sys, urllib.request
from datetime import datetime

API_KEY = ""
with open(os.path.expanduser("~/.zshrc")) as f:
    for line in f:
        if "MINIMAX_API_KEY" in line and "export" in line:
            API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
            break

BASE_URL = "https://api.minimax.io/anthropic/v1/messages"
MODEL = "MiniMax-M2.7"
OUTPUT_DIR = "/Users/penny/Documents/Penny/pseo-network/data/content/bitcoin-beginners"

topic = "Bitcoin Price History: The Complete Story From $0.003 to $100,000+"
slug = "bitcoin-price-history-from-pennies-to-thousands"

prompt = f"""Write a detailed SEO article: {topic}

Write 2500+ words. Cover Bitcoin's price journey through every major cycle: 2009 creation, 2011 bubble, 2013 double peak, 2014 bear, 2017 to $20K, 2018 winter, 2020 COVID crash, 2021 to $69K, 2022 bear, 2023-2024 ETF recovery, and 2025-2026 outlook. Include specific prices, dates, events. FAQ with 6 questions. Beginner-friendly tone.

Output markdown starting with # Title only."""

body = json.dumps({
    "model": MODEL,
    "max_tokens": 8000,
    "messages": [{"role": "user", "content": prompt}],
    "stream": False
}).encode()

req = urllib.request.Request(BASE_URL, data=body, headers={
    "x-api-key": API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
})

try:
    with urllib.request.urlopen(req, timeout=180) as resp:
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
            print("FAIL: no content", flush=True)
except Exception as e:
    print(f"ERROR: {e}", flush=True)
