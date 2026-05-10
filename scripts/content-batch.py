#!/usr/bin/env python3
"""
PennyPress — Content Batch Generator
Called by pennypress.sh to generate articles via MiniMax M2.7
"""

import sys, os, json, re, time
from datetime import datetime

# Add project to path
sys.path.insert(0, '/Users/penny/Documents/Penny/pseo-network')
from writer import generate_article

def get_topic_pool(niche: str, count: int) -> list:
    """Generate diverse topic ideas based on niche and content types."""
    content_types = ["standard", "listicle", "howto", "faq", "comparison", "pillar"]
    templates = {
        "standard": [
            f"Best {niche} Strategies for 2026",
            f"Ultimate Guide to {niche}",
            f"{niche.title()} Tips That Experts Use",
            f"How to Master {niche} Without Experience",
            f"{niche.title()} Mistakes Beginners Make",
        ],
        "listicle": [
            f"Top 10 {niche} Tools and Resources",
            f"Best {niche} Apps for 2026",
            f"{niche.title()} Hacks That Save Time",
            f"Essential {niche} Resources You Need",
            f"Free {niche} Tools Worth Using",
        ],
        "howto": [
            f"How to Get Started with {niche}",
            f"Step by Step Guide to {niche}",
            f"How to Choose the Right {niche} Strategy",
            f"How to Build a {niche} Routine",
            f"How to Avoid Common {niche} Pitfalls",
        ],
        "faq": [
            f"{niche.title()} FAQ: Common Questions Answered",
            f"What Beginners Should Know About {niche}",
            f"{niche.title()} Myths vs Facts",
            f"Is {niche} Worth It? Honest Review",
            f"{niche.title()} for Beginners: What to Expect",
        ],
        "comparison": [
            f"Best {niche} Options Compared",
            f"{niche.title()} Free vs Paid: Which Is Better",
            f"Top {niche} Platforms Compared for 2026",
            f"{niche.title()} on a Budget vs Premium Approach",
        ],
        "pillar": [
            f"Complete {niche.title()} Guide for 2026",
            f"The Definitive {niche.title()} Handbook",
            f"Everything You Need to Know About {niche}",
            f"Advanced {niche.title()} Strategies and Techniques",
            f"{niche.title()} Mastery: From Beginner to Expert",
        ],
    }
    
    topics = []
    for i in range(count):
        ct = content_types[i % len(content_types)]
        pool = templates.get(ct, templates["standard"])
        topic = pool[i // len(content_types) % len(pool)]
        topics.append((topic, ct))
    
    return topics

def save_article(topic: str, content: str, article_type: str, niche: str, output_dir: str) -> str:
    """Save article with frontmatter."""
    slug = re.sub(r'[^a-z0-9]+', '-', topic.lower()).strip('-')
    date = datetime.now().strftime('%Y-%m-%d')
    filename = f'{output_dir}/{date}-ai-{slug}.md'
    
    # Strip any existing frontmatter
    content = re.sub(r'^---\n.*?\n---\n', '', content, count=1, flags=re.DOTALL)
    
    words = len(content.split())
    descriptions = {
        'pillar': f'Comprehensive guide to {topic.lower()}',
        'standard': f'Expert insights on {topic.lower()}',
        'faq': f'Answers to your questions about {topic.lower()}',
        'howto': f'Step-by-step: {topic.lower()}',
        'listicle': f'Curated picks for {topic.lower()}',
        'comparison': f'Compare your options for {topic.lower()}',
    }
    
    frontmatter = f'''---
title: "{topic}"
description: "{descriptions.get(article_type, topic.lower())}"
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
    
    return filename

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 content-batch.py <site-name> <niche> [count]")
        sys.exit(1)
    
    site_name = sys.argv[1]
    niche = sys.argv[2]
    count = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    
    output_dir = f'/Users/penny/Documents/Penny/pseo-network/data/content/{site_name}'
    os.makedirs(output_dir, exist_ok=True)
    
    # Get topic pool
    topics = get_topic_pool(niche, count)
    
    print(f"Generating {count} articles for '{site_name}' (niche: {niche})", flush=True)
    print(f"=" * 50, flush=True)
    
    total_words = 0
    total_time = 0
    failures = 0
    
    for i, (topic, article_type) in enumerate(topics):
        slug = re.sub(r'[^a-z0-9]+', '-', topic.lower()).strip('-')
        date = datetime.now().strftime('%Y-%m-%d')
        expected_file = f'{output_dir}/{date}-ai-{slug}.md'
        
        # Skip if exists
        if os.path.exists(expected_file):
            print(f"[{i+1}/{count}] SKIP (exists): {topic[:50]}", flush=True)
            continue
        
        print(f"[{i+1}/{count}] {article_type}: {topic[:50]}", flush=True)
        start = time.time()
        
        try:
            content = generate_article(topic, article_type, niche=niche)
            elapsed = time.time() - start
            words = len(content.split())
            
            filename = save_article(topic, content, article_type, niche, output_dir)
            print(f"  ✅ {words} words in {elapsed:.1f}s", flush=True)
            
            total_words += words
            total_time += elapsed
        except Exception as e:
            elapsed = time.time() - start
            print(f"  ❌ FAILED after {elapsed:.1f}s: {e}", flush=True)
            failures += 1
    
    print(f"\n{'=' * 50}", flush=True)
    print(f"Results: {count - failures}/{count} articles", flush=True)
    print(f"Total words: {total_words:,}", flush=True)
    print(f"Total time: {total_time:.0f}s", flush=True)
    if total_time > 0:
        print(f"Avg speed: {total_words / total_time:.0f} words/sec", flush=True)

if __name__ == '__main__':
    main()
