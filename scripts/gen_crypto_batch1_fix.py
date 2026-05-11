#!/usr/bin/env python3
import sys, os, re, time
from datetime import datetime

sys.path.insert(0, '/Users/penny/Documents/Penny/pseo-network')
sys.path.insert(0, '/Users/penny/Documents/Penny/pseo-network/src/agents')

from src.agents.writer import generate_standard_article, generate_faq_article, generate_howto_article

OUTPUT_DIR = '/Users/penny/Documents/Penny/pseo-network/data/content/crypto-investing-guide'

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def save_article(topic, content, niche):
    slug = slugify(topic)
    date = datetime.now().strftime('%Y-%m-%d')
    filename = f'{OUTPUT_DIR}/{date}-ai-{slug}.md'
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
    return words

# Articles under 2000 words - regenerate with higher target
ARTICLES = [
    ("DeFi Yield Farming Risks and Rewards Explained", generate_standard_article, 2500),
    ("Bitcoin ETF Explained: How to Invest Without Buying BTC Directly", generate_faq_article, 2500),
    ("Bitcoin Lightning Network: Fast, Cheap Payments Explained", generate_standard_article, 2500),
    ("Crypto Tax Loss Harvesting: The Ultimate Guide", generate_howto_article, 2500),
]

for i, (topic, gen_func, target_words) in enumerate(ARTICLES, 1):
    print(f'[{i}/{len(ARTICLES)}] {topic[:50]}', flush=True)
    start = time.time()
    try:
        content = gen_func(topic, target_words, 'crypto investing')
        elapsed = time.time() - start
        words = save_article(topic, content, 'crypto')
        if words < 2000:
            print(f'  ⚠️ Still under 2000 ({words}), retrying with 3000 target...')
            content = gen_func(topic, 3000, 'crypto investing')
            words = save_article(topic, content, 'crypto')
            print(f'  Retry: {words} words in {time.time()-start:.1f}s total')
        else:
            print(f'  Saved in {elapsed:.1f}s')
    except Exception as e:
        print(f'ERROR: {e}', flush=True)
    time.sleep(3)
