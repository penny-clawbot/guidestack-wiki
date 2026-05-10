#!/usr/bin/env python3
"""
Batch Generator - Generate multiple articles from a keyword cluster JSON
Creates internal link map between articles and generates category pages
"""

import sys
import os
import json
import re
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.content_generator import generate_article, slugify


def load_cluster(cluster_path: str) -> dict:
    """Load keyword cluster JSON from Scout agent."""
    with open(cluster_path, 'r') as f:
        return json.load(f)


def generate_cluster_articles(cluster: dict, output_dir: str, site_name: str = "default") -> dict:
    """Generate all articles for a keyword cluster."""
    articles = []
    article_paths = {}
    
    niche = cluster.get("niche", "general")
    keywords = cluster.get("keywords", [])
    
    # Ensure output dir exists
    content_dir = os.path.join(output_dir, "content", site_name)
    os.makedirs(content_dir, exist_ok=True)
    
    print(f"Generating {len(keywords)} articles for cluster: {niche}")
    
    for kw in keywords:
        article_type = kw.get("type", "standard")
        topic = kw.get("keyword", "")
        tags = kw.get("tags", [])
        
        if not topic:
            continue
        
        print(f"\n  → Generating {article_type}: {topic}")
        
        try:
            article_content = generate_article(
                topic=topic,
                article_type=article_type,
                category=niche,
                tags=tags + [niche]
            )
            
            # Save article
            slug = slugify(topic)
            date = datetime.now().strftime("%Y-%m-%d")
            filename = f"{date}-{slug}.md"
            filepath = os.path.join(content_dir, filename)
            
            with open(filepath, 'w') as f:
                f.write(article_content)
            
            article_paths[topic] = {
                "path": filepath,
                "slug": slug,
                "type": article_type
            }
            
            print(f"    Saved: {filename}")
            
        except Exception as e:
            print(f"    ERROR: {e}")
    
    return article_paths


def build_internal_link_map(articles: dict) -> dict:
    """Build internal link suggestions between articles."""
    link_map = {}
    topics = list(articles.keys())
    
    for topic in topics:
        slug = articles[topic]["slug"]
        # Find related articles (simple slug matching for now)
        related = []
        for other_topic in topics:
            if other_topic != topic:
                other_slug = articles[other_topic]["slug"]
                # Suggest links if slugs share words
                topic_words = set(slug.split('-'))
                other_words = set(other_slug.split('-'))
                if topic_words & other_words:
                    related.append({
                        "topic": other_topic,
                        "slug": other_slug,
                        "anchor": other_topic
                    })
        
        link_map[topic] = related[:5]  # Max 5 related links
    
    return link_map


def generate_category_page(niche: str, articles: dict, output_dir: str, site_name: str) -> str:
    """Generate a category index page."""
    content_dir = os.path.join(output_dir, "content", site_name)
    
    title = niche.replace("-", " ").title()
    date = datetime.now().strftime("%Y-%m-%d")
    
    # Build article list
    article_list = []
    for topic, info in articles.items():
        slug = info["slug"]
        article_list.append(f'- [{topic}]({slug}.md)')
    
    content = f'''---
title: "{title} - Complete Guide"
description: "Explore our complete collection of {title} articles, guides, and resources."
date: "{date}"
category: "{niche}"
draft: false
---

# {title}

Welcome to our comprehensive {title} resource center. Browse our articles below:

{"".join(article_list)}

## About This Category

This category covers everything related to {title.lower()}. Our articles are written by experts and regularly updated to ensure accuracy.

[Back to Home](/)
'''
    
    filepath = os.path.join(content_dir, f"category-{slugify(niche)}.md")
    with open(filepath, 'w') as f:
        f.write(content)
    
    return filepath


def save_link_map(link_map: dict, output_dir: str, site_name: str) -> None:
    """Save internal link map as JSON for reference."""
    content_dir = os.path.join(output_dir, "content", site_name)
    filepath = os.path.join(content_dir, "internal-links.json")
    
    with open(filepath, 'w') as f:
        json.dump(link_map, f, indent=2)
    
    print(f"\nLink map saved to: {filepath}")


def main():
    if len(sys.argv) < 2:
        print("Usage: batch-generator.py <cluster.json> [output_dir] [site_name]")
        print("Example: batch-generator.py cluster.json ./data smarthome")
        sys.exit(1)
    
    cluster_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./data"
    site_name = sys.argv[3] if len(sys.argv) > 3 else "default"
    
    # Load cluster
    cluster = load_cluster(cluster_path)
    print(f"Loaded cluster: {cluster.get('niche', 'unknown')}")
    
    # Generate articles
    articles = generate_cluster_articles(cluster, output_dir, site_name)
    
    # Build and save link map
    link_map = build_internal_link_map(articles)
    save_link_map(link_map, output_dir, site_name)
    
    # Generate category page
    if articles:
        niche = cluster.get("niche", "general")
        cat_path = generate_category_page(niche, articles, output_dir, site_name)
        print(f"Category page: {cat_path}")
    
    print(f"\n✓ Batch complete: {len(articles)} articles generated")


if __name__ == "__main__":
    main()