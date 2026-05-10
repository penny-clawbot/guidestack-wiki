#!/usr/bin/env python3
"""
Content Generator - Main entry point for PennyPress article generation
Takes keyword/topic + article type and generates full SEO-optimized markdown
"""

import sys
import os
import re
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.writer import generate_pillar_article, generate_standard_article, generate_faq_article, generate_howto_article, generate_listicle_article, generate_comparison_article


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'^-|-$', '', text)
    return text


def build_frontmatter(title: str, description: str, category: str, tags: list, image: str = "") -> str:
    """Build YAML frontmatter block."""
    date = datetime.now().strftime("%Y-%m-%d")
    tags_yaml = "\n  - " + "\n  - ".join(tags) if tags else ""
    image_yaml = f'\nimage: "{image}"' if image else ""
    return f'''---
title: "{title}"
description: "{description}"
date: "{date}"
category: "{category}"{tags_yaml}{image_yaml}
draft: false
readingTime: "8 min"
---
'''


def extract_seo_metadata(content: str, topic: str) -> dict:
    """Extract and validate SEO metadata from content."""
    lines = content.strip().split('\n')
    
    # Extract title (first H1)
    title = ""
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    # Extract meta description from frontmatter or first paragraph
    desc_match = re.search(r'description:\s*["\']?([^"\'\n]+)', content)
    description = desc_match.group(1) if desc_match else ""
    
    # Estimate word count
    word_count = len(re.findall(r'\w+', content))
    
    # Calculate reading time (200 wpm average)
    reading_time = f"{max(1, word_count // 200)} min"
    
    return {
        "title": title,
        "description": description[:155] if description else "",
        "word_count": word_count,
        "reading_time": reading_time
    }


def generate_article(topic: str, article_type: str, category: str = "general", tags: list = None) -> str:
    """Main entry point: generate complete article with frontmatter."""
    
    if tags is None:
        tags = [slugify(topic), article_type, "2026"]
    
    print(f"Generating {article_type} article: {topic}")
    
    generators = {
        "pillar": (generate_pillar_article, 3500),
        "standard": (generate_standard_article, 1800),
        "faq": (generate_faq_article, 1200),
        "howto": (generate_howto_article, 1500),
        "listicle": (generate_listicle_article, 2000),
        "comparison": (generate_comparison_article, 2000),
    }
    
    if article_type not in generators:
        raise ValueError(f"Unknown article type: {article_type}")
    
    gen_func, target_words = generators[article_type]
    
    print(f"Target word count: {target_words}+")
    content = gen_func(topic, target_words)
    
    # Extract metadata
    metadata = extract_seo_metadata(content, topic)
    
    # Build frontmatter
    frontmatter = build_frontmatter(
        title=metadata["title"] or topic,
        description=metadata["description"],
        category=category,
        tags=tags
    )
    
    # Combine frontmatter + content
    # Remove any existing frontmatter from content to avoid duplication
    content = re.sub(r'^---\n.*?\n---\n', '', content, count=1, flags=re.DOTALL)
    
    final_output = frontmatter + content
    
    return final_output


def main():
    if len(sys.argv) < 3:
        print("Usage: content-generator.py <topic> <article_type> [category] [output_dir]")
        print("Article types: pillar, standard, faq, howto, listicle, comparison")
        print("Example: content-generator.py 'Smart Home Automation' pillar technology")
        sys.exit(1)
    
    topic = sys.argv[1]
    article_type = sys.argv[2]
    category = sys.argv[3] if len(sys.argv) > 3 else "general"
    output_dir = sys.argv[4] if len(sys.argv) > 4 else None
    
    # Generate article
    article = generate_article(topic, article_type, category)
    
    # Save or print
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        slug = slugify(topic)
        date = datetime.now().strftime("%Y-%m-%d")
        filename = f"{date}-{slug}.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(article)
        
        print(f"\nArticle saved to: {filepath}")
        print(f"Word count: {len(re.findall(r'\w+', article))}")
    else:
        print(article)


if __name__ == "__main__":
    main()