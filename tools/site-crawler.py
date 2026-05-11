#!/usr/bin/env python3
"""
Site Crawler — Scrapy-based crawler for PennyPress SEO auditing.
Usage:
    python3 tools/site-crawler.py <site-dir> [--max-pages 100]
"""

import sys
import os
import re
import glob
from pathlib import Path
import urllib.parse

def crawl_local_site(site_dir, max_pages=100):
    """Crawl built site HTML files and extract SEO signals."""
    dist_dir = Path(site_dir) / 'dist'
    if not dist_dir.exists():
        print(f"❌ No dist/ directory found in {site_dir}")
        print(f"   Run: bash scripts/build-site.sh <site-name> <niche>")
        return
    
    html_files = list(dist_dir.rglob('*.html'))[:max_pages]
    
    results = []
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title
        title_match = re.search(r'<title>([^<]+)</title>', content)
        title = title_match.group(1) if title_match else 'MISSING'
        
        # Extract meta description
        desc_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', content, re.I)
        if not desc_match:
            desc_match = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']description["\']', content, re.I)
        description = desc_match.group(1) if desc_match else 'MISSING'
        if description != 'MISSING':
            description = description[:157] + '...' if len(description) > 157 else description
        
        # Extract H1
        h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content, re.I)
        h1 = h1_match.group(1).strip() if h1_match else 'MISSING'
        
        # Count internal links
        links = re.findall(r'href=["\']([^"\']+)["\']', content)
        internal = sum(1 for l in links if not l.startswith(('http://', 'https://', '//', 'mailto:', 'tel:')))
        
        # Count external links
        external = sum(1 for l in links if l.startswith(('http://', 'https://')))
        
        # Extract meta robots
        robots_match = re.search(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)["\']', content, re.I)
        robots = robots_match.group(1) if robots_match else 'INDEX,FOLLOW'
        
        # Check for canonical URL
        canonical_match = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', content, re.I)
        if not canonical_match:
            canonical_match = re.search(r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']', content, re.I)
        canonical = canonical_match.group(1) if canonical_match else 'MISSING'
        
        # Check for Open Graph tags
        og_title = bool(re.search(r'property=["\']og:title["\']', content, re.I))
        og_desc = bool(re.search(r'property=["\']og:description["\']', content, re.I))
        og_image = bool(re.search(r'property=["\']og:image["\']', content, re.I))
        og_complete = og_title and og_desc and og_image
        
        # Check for structured data (JSON-LD)
        schema_match = re.findall(r'<script[^>]+type=["\']application/ld\+json["\']', content, re.I)
        schema_count = len(schema_match)
        
        # Check for sitemap reference in robots.txt
        has_robots = bool((dist_dir / 'robots.txt').exists())
        
        # Check for alt text on images
        imgs = re.findall(r'<img[^>]+>', content, re.I)
        imgs_no_alt = [i for i in imgs if 'alt=' not in i.lower()]
        
        # Extract body text for reading level estimation
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.I)
        body_text = re.sub(r'<[^>]+>', ' ', body_match.group(1)) if body_match else ''
        body_text = re.sub(r'\s+', ' ', body_text).strip()
        words = body_text.split()
        word_count = len(words)
        sentences = len(re.findall(r'[.!?]+', body_text))
        avg_sentence_len = word_count / max(sentences, 1)
        
        # Simple readability score (Flesch-Kincaid approximation)
        syllable_count = sum(
            max(1, len(re.findall(r'[aeiouy]+', w.lower()))) for w in words
        )
        if word_count > 0 and sentences > 0:
            fk_grade = 0.39 * (word_count / sentences) + 11.8 * (syllable_count / word_count) - 15.59
        else:
            fk_grade = 0
        
        results.append({
            'file': str(html_file.relative_to(dist_dir)),
            'title': title[:80],
            'title_len': len(title),
            'description': description,
            'desc_len': len(description) if description != 'MISSING' else 0,
            'h1': h1[:60],
            'internal_links': internal,
            'external_links': external,
            'robots': robots,
            'canonical': canonical,
            'og_complete': og_complete,
            'schema_count': schema_count,
            'imgs_no_alt': len(imgs_no_alt),
            'img_total': len(imgs),
            'word_count': word_count,
            'fk_grade': round(fk_grade, 1),
            'avg_sentence_len': round(avg_sentence_len, 1)
        })
    
    return results

def print_crawl_report(results, site_name):
    print(f"\n{'='*70}")
    print(f"🔍 SEO Crawl Report: {site_name} ({len(results)} pages)")
    print(f"{'='*70}")
    
    missing_title = [r for r in results if 'MISSING' in r['title']]
    missing_desc = [r for r in results if 'MISSING' in r['description']]
    missing_h1 = [r for r in results if 'MISSING' in r['h1']]
    noindex = [r for r in results if 'noindex' in r['robots'].lower()]
    missing_canonical = [r for r in results if 'MISSING' in r.get('canonical', '')]
    no_schema = [r for r in results if r.get('schema_count', 0) == 0]
    no_og = [r for r in results if not r.get('og_complete', False)]
    bad_titles = [r for r in results if r.get('title_len', 0) > 60 or r.get('title_len', 0) < 30]
    bad_descs = [r for r in results if r.get('desc_len', 0) > 160 or r.get('desc_len', 0) < 120]
    bad_readability = [r for r in results if r.get('fk_grade', 0) > 12]
    imgs_no_alt_total = sum(r.get('imgs_no_alt', 0) for r in results)
    
    print(f"\n  📄 Pages crawled:        {len(results)}")
    print(f"  ❌ Missing <title>:      {len(missing_title)}")
    print(f"  ❌ Missing meta desc:    {len(missing_desc)}")
    print(f"  ❌ Missing <h1>:         {len(missing_h1)}")
    print(f"  ❌ Missing canonical:    {len(missing_canonical)}")
    print(f"  ❌ Missing schema:       {len(no_schema)}")
    print(f"  ❌ Missing OG tags:      {len(no_og)}")
    print(f"  ⚠️ Title len issues:     {len(bad_titles)} (ideal 30-60 chars)")
    print(f"  ⚠️ Desc len issues:      {len(bad_descs)} (ideal 120-160 chars)")
    print(f"  ⚠️ Reading level >12:    {len(bad_readability)} (ideal 8th-10th grade)")
    print(f"  ⚠️ Images missing alt:   {imgs_no_alt_total}")
    print(f"  🚫 Noindex pages:       {len(noindex)}")
    
    # Internal link stats
    if results:
        avg_links = sum(r.get('internal_links', 0) for r in results) / len(results)
        avg_ext = sum(r.get('external_links', 0) for r in results) / len(results)
        avg_words = sum(r.get('word_count', 0) for r in results) / len(results)
        avg_fk = sum(r.get('fk_grade', 0) for r in results) / len(results)
        print(f"\n  📊 Averages per page:")
        print(f"     Internal links: {avg_links:.1f} | External links: {avg_ext:.1f}")
        print(f"     Word count: {avg_words:.0f} | Reading level: {avg_fk:.1st} grade")
    
    # Show worst pages
    print(f"\n  🔻 Pages needing attention:")
    attention = [r for r in results if (
        'MISSING' in r['title'] or 'MISSING' in r['description'] or 
        'MISSING' in r['h1'] or r.get('schema_count', 0) == 0
    )]
    for r in attention[:10]:
        issues = []
        if 'MISSING' in r['title']: issues.append('NO_TITLE')
        if 'MISSING' in r['description']: issues.append('NO_DESC')
        if 'MISSING' in r['h1']: issues.append('NO_H1')
        if r.get('schema_count', 0) == 0: issues.append('NO_SCHEMA')
        if not r.get('og_complete', False): issues.append('NO_OG')
        print(f"     [{', '.join(issues)}] {r['file']}")
    
    if not attention:
        print(f"     ✅ All pages pass basic SEO checks!")
    
    # Score
    score = 100
    score -= len(missing_title) * 10
    score -= len(missing_desc) * 5
    score -= len(noindex) * 10
    score -= len(missing_canonical) * 3
    score -= len(no_schema) * 3
    score -= len(no_og) * 2
    score -= len(bad_titles) * 2
    score -= len(bad_descs) * 2
    score -= min(imgs_no_alt_total, 10)
    print(f"\n  📊 Crawl SEO Score: {max(0,score)}/100")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    site_dir = sys.argv[1]
    max_pages = 100
    if '--max-pages' in sys.argv:
        idx = sys.argv.index('--max-pages')
        max_pages = int(sys.argv[idx + 1]) if idx + 1 < len(sys.argv) else 100
    
    site_name = os.path.basename(site_dir)
    results = crawl_local_site(site_dir, max_pages)
    if results:
        print_crawl_report(results, site_name)

if __name__ == '__main__':
    main()
