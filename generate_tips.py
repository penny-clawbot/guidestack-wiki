import sys, os, json, re, time
from datetime import datetime
sys.path.insert(0, '/Users/penny/Documents/Penny/pseo-network')
from writer import generate_article

articles = [
    ("Cheap Flights Hacks That Actually Work in 2026", "standard", 1500),
    ("How to Find Budget Accommodation Anywhere", "howto", 1500),
    ("Best Travel Rewards Credit Cards for Beginners", "comparison", 1500),
    ("How to Travel Europe on $50 a Day", "pillar", 3000),
    ("Top 10 Budget Destinations for 2026", "listicle", 2000),
    ("Travel Insurance: Is It Worth the Money?", "faq", 1200),
    ("How to Save Money on Food While Traveling", "standard", 1500),
    ("Best Budget Travel Gear Under $50", "listicle", 2000),
    ("How to Plan a Budget Trip Step by Step", "howto", 1500),
    ("Solo Budget Travel: Complete Safety Guide", "pillar", 3000),
    ("Budget Travel Mistakes That Cost You Money", "standard", 1500),
    ("How to Use Points and Miles for Free Travel", "standard", 1500),
    ("Best Apps for Budget Travelers", "listicle", 1500),
    ("How to Travel with Only a Carry-On", "howto", 1200),
    ("Budget Travel FAQ: 20 Common Questions Answered", "faq", 2000),
]

output_dir = '/Users/penny/Documents/Penny/pseo-network/data/content/budget-travel-tips'
os.makedirs(output_dir, exist_ok=True)

for i, (topic, article_type, target_words) in enumerate(articles):
    slug = re.sub(r'[^a-z0-9]+', '-', topic.lower()).strip('-')
    date = datetime.now().strftime('%Y-%m-%d')
    filename = f'{output_dir}/{date}-ai-{slug}.md'
    
    if os.path.exists(filename):
        print(f'[{i+1}/{len(articles)}] SKIP: {topic[:40]}')
        continue
    
    print(f'[{i+1}/{len(articles)}] {article_type}: {topic[:40]}')
    start = time.time()
    try:
        content = generate_article(topic, article_type, target_words, 'budget travel')
        elapsed = time.time() - start
        words = len(content.split())
        
        # Strip any frontmatter from content
        content = re.sub(r'^---\n.*?\n---\n', '', content, count=1, flags=re.DOTALL)
        
        descriptions = {
            'pillar': f'Comprehensive guide to {topic.lower()}',
            'standard': f'Everything you need to know about {topic.lower()}',
            'faq': f'Answers to common questions about {topic.lower()}',
            'howto': f'Step-by-step guide: {topic.lower()}',
            'listicle': f'Discover the best options for {topic.lower()}',
            'comparison': f'Compare your options for {topic.lower()}',
        }
        
        frontmatter = f'''---
title: "{topic}"
description: "{descriptions.get(article_type, topic.lower())}"
date: "{date}"
category: "budget-travel"
tags:
  - budget-travel
  - {slug}
draft: false
readingTime: "{max(1, words // 200)} min"
---

'''
        
        with open(filename, 'w') as f:
            f.write(frontmatter + content)
        
        print(f'  ✅ {words} words in {elapsed:.1f}s -> {slug}')
    except Exception as e:
        print(f'  ❌ ERROR: {e}')

print(f'\nDone!')