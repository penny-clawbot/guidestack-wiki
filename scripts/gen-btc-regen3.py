#!/usr/bin/env python3
"""Regenerate final batch of short bitcoin articles."""
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
    ("Bitcoin Price History: From Pennies to Thousands — The Complete Story of BTC", "bitcoin-price-history-from-pennies-to-thousands"),
    ("Bitcoin Wallets Explained: Hardware, Software, and Paper Wallets — Complete Guide", "bitcoin-wallets-explained-hardware-software-and-paper-wallets"),
    ("How to Avoid Bitcoin Scams and Fraud: Essential Security Guide for 2026", "how-to-avoid-bitcoin-scams-and-fraud"),
    ("Bitcoin Forks Explained: Hard Forks vs Soft Forks — What Every Beginner Must Know", "bitcoin-forks-hard-forks-vs-soft-forks-explained"),
]

def generate_article(topic: str) -> str:
    prompt = f"""Write a comprehensive SEO article about: {topic}

MUST be at least 2,500 words. Be thorough.

Niche: bitcoin-beginners
Structure: H1 title, 3-4 para intro, 7-9 H2 sections with H3, bullet lists, FAQ (6 questions), conclusion.
Beginner-friendly tone. Use examples and data.
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
    if not desc: desc = title[:160]
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
        else:
            print(f"  FAIL: {article[:100]}", flush=True)
        if i < len(REGEN) - 1: time.sleep(2)
    
    # Count qualifying
    qualifying = 0
    for f in os.listdir(OUTPUT_DIR):
        if f.endswith('.md'):
            with open(os.path.join(OUTPUT_DIR, f)) as fh:
                wc = len(fh.read().split())
                if wc >= 2500: qualifying += 1
    print(f"\nQualifying (2500+ words): {qualifying}/{len(os.listdir(OUTPUT_DIR))}")

if __name__ == "__main__":
    main()
