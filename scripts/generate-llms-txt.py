#!/usr/bin/env python3
"""
Generate llms.txt for each site with real data.
Part of the GEO (Generative Engine Optimization) strategy.
"""
import json
import sys
import os

def generate_llms_txt(site_dir: str):
    config_path = os.path.join(site_dir, 'site-config.json')
    with open(config_path) as f:
        config = json.load(f)
    
    site_name = config.get('name', 'PennyPress')
    site_desc = config.get('description', '')
    niche = config.get('niche', '')
    domain = config.get('domain', 'example.com')
    site_url = f"https://{domain}"
    
    # Count articles and categories from data/content/<site>/ (network structure)
    site_basename = os.path.basename(site_dir)
    articles_dir = os.path.join(site_dir, 'data', 'content', site_basename)
    if not os.path.isdir(articles_dir):
        abs_site = os.path.abspath(site_dir)
        abs_root = os.path.dirname(os.path.dirname(os.path.dirname(abs_site)))
        articles_dir = os.path.join(abs_root, 'data', 'content', site_basename)
    
    article_count = 0
    categories = set()
    if os.path.isdir(articles_dir):
        for fn in os.listdir(articles_dir):
            if fn.endswith('.md'):
                article_count += 1
                with open(os.path.join(articles_dir, fn)) as f:
                    for line in f:
                        if line.startswith('category:'):
                            cat = line.split(':', 1)[1].strip().strip('"\'')
                            categories.add(cat)
                            break
    
    # Build llms.txt
    content = f"""# {site_name}
> {site_desc}

## About
{site_name} is a comprehensive {niche} resource with {article_count} expert guides, comparisons, and actionable tips. All content is fact-checked and regularly updated.

## Crawl Policy
- Access: allow
- Citation: required with source URL
- Preferred format: title + URL + author attribution

## Sitemap & Feeds
- {site_url}/sitemap.xml
- {site_url}/feed.xml

## Categories
"""
    for cat in sorted(categories):
        cat_slug = cat.lower().replace(' ', '-')
        content += f"- {site_url}/category/{cat_slug}/ — {cat.title()}\n"
    
    content += f"""
## Content Types
- {site_url}/ — All articles and guides
- {site_url}/best/ — Best-of roundups ranked by quality and depth
- {site_url}/compare/ — Side-by-side product/service comparisons

## Company
- {site_url}/about — About {site_name}
- {site_url}/about/author — Author profile and expertise
- {site_url}/contact — Get in touch

## Legal
- {site_url}/privacy-policy
- {site_url}/terms

## Technical Notes
- All pages include JSON-LD structured data (Article, FAQPage, Organization, BreadcrumbList)
- FAQ sections with FAQPage schema on most articles
- Semantic HTML5 with proper heading hierarchy
- RSS feed with 50 most recent articles
- Content updated weekly with freshness signals (dateModified)

## Crawl Guidelines
- Crawl-delay: 2 seconds
- Rate-limit: 1 request per 2 seconds
- Content language: {config.get('language', 'en')}
"""
    
    output_path = os.path.join(site_dir, 'dist', 'llms.txt')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(content)
    
    # Also write to public dir for dev
    public_path = os.path.join(site_dir, 'public', 'llms.txt')
    os.makedirs(os.path.dirname(public_path), exist_ok=True)
    with open(public_path, 'w') as f:
        f.write(content)
    
    print(f"  llms.txt generated ({len(content)} bytes, {article_count} articles, {len(categories)} categories)")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 generate-llms-txt.py <site-dir>")
        sys.exit(1)
    generate_llms_txt(sys.argv[1])