#!/usr/bin/env python3
"""
PennyPress Site Generator — Builds Astro SEO sites from keyword data.

Usage:
    python generate-site.py <config.json> [output-name]
    cat niche-config.json | python generate-site.py --stdin

Reads from config.json (or stdin) for site configuration, copies the base Astro
template, customizes it, and generates proper content collection format.

Config format:
{
  "name": "Smart Home Hub",
  "niche": "smart home gadgets",
  "domain": "smarthome.example.com",
  "description": "...",
  "tagline": "...",
  "keywords": ["kw1", "kw2", ...],
  "colors": {"primary": "#00d4ff", "accent": "#ff6b6b"}
}
"""

import json
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
TEMPLATE_DIR = PROJECT_ROOT / "templates" / "base"
CONFIG_FILE = PROJECT_ROOT / "config.json"
OUTPUT_DIR = PROJECT_ROOT / "output" / "sites"


def load_project_config() -> dict:
    """Load project config.json."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {"output_dir": "output/sites", "data_dir": "data"}


def load_site_config(config_path: str) -> dict:
    """Load site configuration from a JSON file or stdin."""
    if config_path == "--stdin" or config_path == "-":
        return json.load(sys.stdin)
    with open(config_path) as f:
        return json.load(f)


def slugify(text: str) -> str:
    """Convert text to URL-safe slug."""
    text = text.lower().replace(" ", "-").replace("_", "-")
    text = re.sub(r"[^a-z0-9-]", "", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def copy_template(site_dir: Path) -> None:
    """Copy base template to site directory."""
    if site_dir.exists():
        shutil.rmtree(site_dir)
    if not TEMPLATE_DIR.exists():
        raise FileNotFoundError(f"Template directory not found: {TEMPLATE_DIR}")
    shutil.copytree(TEMPLATE_DIR, site_dir)
    print(f"✓ Copied base template to {site_dir}")


def customize_template(site_dir: Path, config: dict, project_config: dict) -> None:
    """Replace template placeholders with site-specific values."""
    replacements = {
        "{{SITE_NAME}}": config.get("name", config.get("niche", "PennyPress Site")),
        "{{SITE_DESCRIPTION}}": config.get("description", ""),
        "{{SITE_TAGLINE}}": config.get("tagline", config.get("description", "")),
        "{{SITE_URL}}": f"https://{config.get('domain', config.get('niche', 'example.com').replace(' ', '-') + '.com')}",
    }

    # Custom colors
    colors = config.get("colors", {})
    if colors:
        css_file = site_dir / "src" / "styles" / "global.css"
        if css_file.exists():
            content = css_file.read_text()
            for color_name, color_value in colors.items():
                content = content.replace(
                    f"--color-{color_name}:", f"--color-{color_name}: {color_value}"
                )
            css_file.write_text(content)

    # Walk through all text files and replace placeholders
    for file_path in site_dir.rglob("*"):
        if file_path.is_file() and file_path.suffix in [
            ".astro", ".mjs", ".json", ".md", ".css", ".js", ".ts", ".txt"
        ]:
            try:
                content = file_path.read_text()
                modified = False
                for placeholder, value in replacements.items():
                    if placeholder in content:
                        content = content.replace(placeholder, value)
                        modified = True
                if modified:
                    file_path.write_text(content)
            except Exception as e:
                print(f"  ⚠ Could not process {file_path}: {e}")

    # Update astro.config.mjs with real site URL
    astro_config = site_dir / "astro.config.mjs"
    if astro_config.exists():
        content = astro_config.read_text()
        content = content.replace("{{SITE_URL}}", replacements["{{SITE_URL}}"])
        # Also update the site: line
        import re as re_module
        content = re_module.sub(
            r"site:\s*['\"][^'\"]*['\"]",
            f"site: '{replacements['{{SITE_URL}}']}'",
            content
        )
        astro_config.write_text(content)

    # Update package.json with site name
    pkg_json = site_dir / "package.json"
    if pkg_json.exists():
        pkg = json.loads(pkg_json.read_text())
        pkg["name"] = slugify(config.get("name", config.get("niche", "site")))
        pkg_json.write_text(json.dumps(pkg, indent=2))

    print(f"✓ Customized template")


def create_content_structure(site_dir: Path, config: dict) -> None:
    """Create Astro content collection directory structure."""
    content_dir = site_dir / "src" / "content"
    articles_dir = content_dir / "articles"
    articles_dir.mkdir(parents=True, exist_ok=True)

    # Create config.ts for content collections
    config_ts = content_dir / "config.ts"
    config_ts.write_text("""import { defineCollection, z } from 'astro:content';

const articles = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishedAt: z.date(),
    updatedAt: z.date().optional(),
    author: z.string().default('PennyPress'),
    category: z.string().default('general'),
    tags: z.array(z.string()).default([]),
    featured: z.boolean().default(false),
    image: z.object({
      url: z.string(),
      alt: z.string(),
    }).optional(),
  }),
});

export const collections = { articles };
""")
    print(f"  ✓ Created content config: src/content/config.ts")

    # Create sample articles from keywords if provided
    keywords = config.get("keywords", [])
    sample_articles = []

    if keywords:
        sample_articles = [
            {
                "title": f"The Complete Guide to {config.get('niche', 'Topic').title()}",
                "slug": "complete-guide",
                "category": "guides",
                "description": f"A comprehensive guide to {config.get('niche', 'the topic')} with expert tips and recommendations.",
                "content": f"""# The Complete Guide to {config.get('niche', 'Topic').title()}

Welcome to our comprehensive guide to {config.get('niche', 'this topic')}. In this article, we'll cover everything you need to know.

## Introduction

{config.get('description', 'Discover everything about ' + config.get('niche', 'this topic'))}

This guide is designed to help you make informed decisions and get the most out of your journey into {config.get('niche', 'this space')}.

## Key Topics We'll Cover

- Understanding the fundamentals
- Choosing the right products
- Common mistakes to avoid
- Expert tips and recommendations
- Frequently asked questions

## Getting Started

Before diving in, it's important to understand what you're getting into. Take your time, do your research, and don't rush any decisions.

## Expert Tips

1. **Do your research** — Spend time understanding the landscape
2. **Start small** — Don't overcommit before you understand the basics
3. **Learn from others** — Read reviews and real user experiences
4. **Stay updated** — This space evolves quickly

## Conclusion

With the right knowledge and approach, you can successfully navigate {config.get('niche', 'this topic')} and achieve your goals.

Start exploring today!
"""
            },
            {
                "title": f"Top 10 {config.get('niche', 'Topic').title()} You Need to Know About",
                "slug": "top-10-list",
                "category": "lists",
                "description": f"Our curated list of the top 10 {config.get('niche', 'topics')} you should know about.",
                "content": f"""# Top 10 {config.get('niche', 'Topic').title()} You Need to Know About

We've curated this list of the top 10 essentials for anyone interested in {config.get('niche', 'this topic')}.

## Introduction

Whether you're just starting out or looking to level up your knowledge, this list covers the essentials.

## The Top 10

### 1. Start with Basics
Understanding the fundamentals is crucial before diving deeper.

### 2. Quality Over Quantity
It's better to master a few key concepts than to skim many.

### 3. Stay Consistent
Regular engagement leads to better long-term results.

### 4. Learn from Community
The community has invaluable insights to share.

### 5. Follow Experts
Industry leaders often share tips that can accelerate your progress.

### 6. Test and Iterate
Don't be afraid to experiment and adjust based on results.

### 7. Read Reviews
Real user experiences can save you time and money.

### 8. Join Discussions
Active participation helps build knowledge.

### 9. Track Your Progress
Metrics help you understand what's working.

### 10. Never Stop Learning
The space is always evolving — stay curious!

## Conclusion

These are the foundational elements that will set you up for success. Start implementing them today!
"""
            },
            {
                "title": f"How to Choose the Right {config.get('niche', 'Topic').title()}",
                "slug": "how-to-choose",
                "category": "guides",
                "description": f"A practical guide to choosing the right {config.get('niche', 'options')} for your needs.",
                "content": f"""# How to Choose the Right {config.get('niche', 'Topic').title()}

Making the right choice can be overwhelming. This guide will help you make an informed decision.

## Introduction

With so many options available, choosing the right {config.get('niche', 'solution')} can feel daunting. This guide breaks it down step by step.

## Step 1: Define Your Needs

Before looking at options, clearly define what you're looking for. Consider:
- Your budget
- Your experience level
- Your specific goals
- Your timeline

## Step 2: Research Options

Take time to research all available options. Don't rush this step.

## Step 3: Compare Features

Create a comparison checklist to evaluate each option objectively.

## Step 4: Read Reviews

Real user experiences reveal pros and cons that specs can't.

## Step 5: Make Your Decision

Trust your research and make a confident choice.

## Conclusion

Choosing right requires patience and research, but it's worth it. Use this guide to make an informed decision that you'll be happy with.
"""
            }
        ]

    for article in sample_articles:
        article_file = articles_dir / f"{article['slug']}.md"
        article_content = f'''---
title: "{article['title']}"
description: "{article['description']}"
publishedAt: "{datetime.now().isoformat()}"
author: "PennyPress Editorial"
category: "{article['category']}"
tags: [{", ".join(f'"{config.get("niche", "general")}"')}']
featured: false
---

{article['content']}
'''
        article_file.write_text(article_content)
        print(f"  ✓ Created article: {article_file.name}")

    # Create images directory
    images_dir = site_dir / "public" / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    # Create a placeholder favicon
    favicon_svg = site_dir / "public" / "favicon.svg"
    favicon_svg.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="45" fill="#00d4ff"/>
  <text x="50" y="65" font-size="50" text-anchor="middle" fill="white">P</text>
</svg>''')

    print(f"✓ Created content structure")


def generate_site(config_path: str, output_name: str = None) -> Path:
    """Generate a complete Astro site from config."""
    project_config = load_project_config()

    try:
        config = load_site_config(config_path)
    except Exception as e:
        print(f"❌ Failed to load config: {e}")
        sys.exit(1)

    # Determine output directory
    safe_name = slugify(output_name or config.get("niche", config.get("name", "site")))
    site_dir = Path(project_config.get("output_dir", "output/sites")) / safe_name
    site_dir = PROJECT_ROOT / site_dir

    print(f"\n{'='*50}")
    print(f"Generating site: {config.get('name', safe_name)}")
    print(f"{'='*50}\n")

    print(f"📁 Output directory: {site_dir}")

    # Copy template
    copy_template(site_dir)

    # Customize
    customize_template(site_dir, config, project_config)

    # Create content
    create_content_structure(site_dir, config)

    print(f"\n{'='*50}")
    print(f"✓ Site generated successfully!")
    print(f"{'='*50}")
    print(f"\nLocation: {site_dir}")
    print(f"\nNext steps:")
    print(f"  1. cd {site_dir}")
    print(f"  2. npm install")
    print(f"  3. npm run dev")
    print(f"  4. npm run build")
    print(f"\nConfig used:")
    print(f"  - Name: {config.get('name', 'N/A')}")
    print(f"  - Niche: {config.get('niche', 'N/A')}")
    print(f"  - Domain: {config.get('domain', 'not specified')}")
    print(f"  - Keywords: {len(config.get('keywords', []))}")

    return site_dir


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    config_path = sys.argv[1]
    output_name = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        site_dir = generate_site(config_path, output_name)
        print(f"\nSite ready at: {site_dir}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()