#!/usr/bin/env python3
import sys, os, re, time
from datetime import datetime

sys.path.insert(0, '/Users/penny/Documents/Penny/pseo-network')
sys.path.insert(0, '/Users/penny/Documents/Penny/pseo-network/src/agents')

from src.agents.writer import (
    generate_pillar_article, generate_standard_article,
    generate_faq_article, generate_howto_article,
    generate_listicle_article, generate_comparison_article
)

OUTPUT_DIR = '/Users/penny/Documents/Penny/pseo-network/data/content/crypto-investing-guide'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def save_article(topic, content, article_type, niche):
    slug = slugify(topic)
    date = datetime.now().strftime('%Y-%m-%d')
    filename = f'{OUTPUT_DIR}/{date}-ai-{slug}.md'
    if os.path.exists(filename):
        print(f'SKIP: {topic[:50]}')
        return False
    content = re.sub(r'^---\n.*?\n---\n', '', content, count=1, flags=re.DOTALL)
    words = len(content.split())
    frontmatter = f'''---
title: "{topic}"
description: "Expert guide covering {topic.lower()}. Learn strategies, tips, and analysis for smart crypto investing."
date: "{date}"
category: "crypto"
tags:
  - crypto
  - {slug}
draft: false
readingTime: "{max(1, words // 200)} min"
---

'''
    with open(filename, 'w') as f:
        f.write(frontmatter + content)
    print(f'DONE: {words} words: {topic[:55]}')
    return True

ARTICLES = [
    ("How to Stake Ethereum: Complete Beginner's Guide", "howto", generate_howto_article, 2000),
    ("DeFi Yield Farming Risks and Rewards Explained", "standard", generate_standard_article, 2000),
    ("Bitcoin Halving 2028: The Complete Investor's Guide", "pillar", generate_pillar_article, 3000),
    ("Bitcoin ETF Explained: How to Invest Without Buying BTC Directly", "faq", generate_faq_article, 1500),
    ("Bitcoin Lightning Network: Fast, Cheap Payments Explained", "standard", generate_standard_article, 1800),
    ("Bitcoin Hardware Wallet Comparison 2026", "comparison", generate_comparison_article, 2000),
    ("Crypto Tax Loss Harvesting: The Ultimate Guide", "howto", generate_howto_article, 2000),
    ("Crypto Security Best Practices: Protect Your Assets", "pillar", generate_pillar_article, 2500),
]

for i, (topic, atype, gen_func, target_words) in enumerate(ARTICLES, 1):
    print(f'[{i}/{len(ARTICLES)}] {atype}: {topic[:50]}', flush=True)
    start = time.time()
    try:
        content = gen_func(topic, target_words, 'crypto investing')
        elapsed = time.time() - start
        if save_article(topic, content, atype, 'crypto'):
            print(f'  Saved in {elapsed:.1f}s')
    except Exception as e:
        print(f'ERROR: {e}', flush=True)
    time.sleep(3)
