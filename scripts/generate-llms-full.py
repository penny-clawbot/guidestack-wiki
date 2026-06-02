#!/usr/bin/env python3
"""
Generate llms-full.txt — concatenates all article content into a single
machine-readable file for LLM crawlers. Part of the llms.txt convention.

This gives AI engines a complete, structured view of all site content
in one request, maximizing citation probability.
"""
import json
import sys
import os
import re

def extract_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter from markdown."""
    fm = {}
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if m:
        for line in m.group(1).split('\n'):
            if ':' in line:
                k, v = line.split(':', 1)
                fm[k.strip()] = v.strip().strip('"\'')
    return fm

def strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter."""
    return re.sub(r'^---\s*\n.*?\n---\s*\n', '', text, flags=re.DOTALL)

def generate_llms_full(site_dir: str):
    config_path = os.path.join(site_dir, 'site-config.json')
    with open(config_path) as f:
        config = json.load(f)
    
    site_name = config.get('name', 'PennyPress')
    site_desc = config.get('description', '')
    domain = config.get('domain', 'example.com')
    site_url = f"https://{domain}"
    niche = config.get('niche', '')
    
    # Try data/content/<site>/ first (network structure)
    articles_dir = os.path.join(site_dir, 'data', 'content', os.path.basename(site_dir))
    if not os.path.isdir(articles_dir):
        # Fallback: derive pseo-network root from site_dir (output/sites/<site>)
        # site_dir -> output/sites/<site> -> output/sites -> output -> pseo-network root
        abs_site = os.path.abspath(site_dir)
        abs_root = os.path.dirname(os.path.dirname(os.path.dirname(abs_site)))
        articles_dir = os.path.join(abs_root, 'data', 'content', os.path.basename(site_dir))
        if not os.path.isdir(articles_dir):
            print(f"  No articles dir found for {site_dir}, skipping llms-full.txt")
            return
    
    output = f"""# {site_name} — Complete Content
# {site_desc}
# URL: {site_url}
# Niche: {niche}
# This file contains the full text of all articles for AI/LLM consumption.
# Format: Markdown with metadata headers.
# Last updated: {__import__('datetime').date.today().isoformat()}

"""
    
    # Get all markdown files sorted by date
    files = sorted([f for f in os.listdir(articles_dir) if f.endswith('.md')])
    
    for fn in files:
        filepath = os.path.join(articles_dir, fn)
        with open(filepath) as f:
            content = f.read()
        
        fm = extract_frontmatter(content)
        body = strip_frontmatter(content).strip()
        slug = fn.replace('.md', '').replace(re.match(r'^\d{4}-\d{2}-\d{2}-(ai-)?', fn).group(), '') if re.match(r'^\d{4}-\d{2}-\d{2}-(ai-)?', fn) else fn.replace('.md', '')
        
        title = fm.get('title', slug.replace('-', ' ').title())
        desc = fm.get('description', '')
        date = fm.get('date', '')
        category = fm.get('category', '')
        
        output += f"""---
title: {title}
url: {site_url}/{slug}
date: {date}
category: {category}
description: {desc}
---

# {title}

{body}

---

"""
    
    output_path = os.path.join(site_dir, 'dist', 'llms-full.txt')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(output)
    
    size_kb = len(output.encode('utf-8')) / 1024
    print(f"  llms-full.txt generated ({len(files)} articles, {size_kb:.0f}KB)")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 generate-llms-full.py <site-dir>")
        sys.exit(1)
    generate_llms_full(sys.argv[1])