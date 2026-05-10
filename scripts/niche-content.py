#!/usr/bin/env python3
"""Generate targeted content for a specific niche."""
import sys, os, json, re, time
from datetime import datetime

sys.path.insert(0, '/Users/penny/Documents/Penny/pseo-network')
from writer import generate_article

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 niche-content.py <site-name> <niche> <topics-json>")
        sys.exit(1)
    
    site_name = sys.argv[1]
    niche = sys.argv[2]
    topics = json.loads(sys.argv[3])
    
    output_dir = f'/Users/penny/Documents/Penny/pseo-network/data/content/{site_name}'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Generating {len(topics)} articles for '{site_name}' ({niche})", flush=True)
    
    total_words = 0
    total_time = 0
    
    for i, item in enumerate(topics):
        topic = item[0]
        article_type = item[1]
        target_words = item[2] if len(item) > 2 else 1500
        
        slug = re.sub(r'[^a-z0-9]+', '-', topic.lower()).strip('-')
        date = datetime.now().strftime('%Y-%m-%d')
        filename = f'{output_dir}/{date}-ai-{slug}.md'
        
        if os.path.exists(filename):
            print(f"[{i+1}/{len(topics)}] SKIP: {topic[:45]}", flush=True)
            continue
        
        print(f"[{i+1}/{len(topics)}] {article_type}: {topic[:45]}", flush=True)
        start = time.time()
        
        try:
            content = generate_article(topic, article_type, target_words, niche)
            elapsed = time.time() - start
            words = len(content.split())
            
            # Strip existing frontmatter
            content = re.sub(r'^---\n.*?\n---\n', '', content, count=1, flags=re.DOTALL)
            
            frontmatter = f'''---
title: "{topic}"
description: "Expert guide to {topic.lower()}"
date: "{date}"
category: "{niche.lower().replace(' ', '-')}"
tags:
  - {niche.lower().replace(' ', '-')}
  - {slug}
draft: false
readingTime: "{max(1, words // 200)} min"
---

'''
            with open(filename, 'w') as f:
                f.write(frontmatter + content)
            
            print(f"  ✅ {words} words in {elapsed:.1f}s", flush=True)
            total_words += words
            total_time += elapsed
        except Exception as e:
            print(f"  ❌ {e}", flush=True)
    
    print(f"\nDone: {total_words:,} words in {total_time:.0f}s", flush=True)

if __name__ == '__main__':
    main()
