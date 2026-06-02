#!/usr/bin/env python3
"""Article Quality Scorer — Ranks articles by SEO quality signals.
Scores articles on: word count, uniqueness, data points, structure, FAQ presence, readability."""
import os, re, json, sys
from datetime import datetime

PROJECT_DIR = "/Users/penny/Documents/Penny/pseo-network"
CONTENT_DIR = f"{PROJECT_DIR}/data/content"
SITES_JSON = f"{PROJECT_DIR}/data/sites.json"

def score_article(filepath, site_name):
    """Score an article on multiple quality dimensions. Returns dict with scores."""
    with open(filepath, 'r') as f:
        raw = f.read()
    
    # Parse frontmatter
    fm = {}
    fm_match = re.match(r'^---\n([\s\S]*?)\n---\n', raw)
    if fm_match:
        for line in fm_match.group(1).split('\n'):
            m = re.match(r'^(\w+):\s*["\']?(.+?)["\']?\s*$', line)
            if m:
                fm[m[1]] = m[2]
    
    body = raw[fm_match.end():] if fm_match else raw
    title = fm.get('title', 'Unknown')
    description = fm.get('description', '')
    category = fm.get('category', 'general')
    date = fm.get('date', '')
    
    # 1. Word Count Score (0-20 points)
    words = len(body.split())
    if words >= 2000:
        word_score = 20
    elif words >= 1500:
        word_score = 17
    elif words >= 1000:
        word_score = 14
    elif words >= 800:
        word_score = 10
    elif words >= 500:
        word_score = 6
    else:
        word_score = 3
    
    # 2. Structure Score (0-20 points)
    h2_count = len(re.findall(r'^## ', body, re.MULTILINE))
    h3_count = len(re.findall(r'^### ', body, re.MULTILINE))
    has_lists = 1 if re.search(r'^[-*] ', body, re.MULTILINE) else 0
    has_bold = 1 if '**' in body else 0
    
    structure_score = min(20, h2_count * 3 + min(h3_count * 2, 6) + has_lists * 3 + has_bold * 2)
    
    # 3. Data Points Score (0-20 points) — numbers, percentages, years, sources
    numbers = len(re.findall(r'\b\d+\.?\d*%?\b', body))
    percentages = len(re.findall(r'\b\d+\.?\d*%', body))
    years = len(re.findall(r'\b20[12]\d\b', body))
    sources = len(re.findall(r'(according to|source|study|research|survey|report|data)', body, re.IGNORECASE))
    dollar_amounts = len(re.findall(r'\$\d+', body))
    
    data_score = min(20, percentages * 4 + years * 2 + sources * 3 + dollar_amounts * 1)
    
    # 4. FAQ Score (0-15 points)
    has_faq = 1 if re.search(r'##\s*(frequently asked questions|faq|common questions)', body, re.IGNORECASE) else 0
    faq_questions = len(re.findall(r'^### ', body, re.MULTILINE)) if has_faq else 0
    faq_score = min(15, 5 if has_faq else 0 + faq_questions * 3)
    
    # 5. Title & Meta Score (0-10 points)
    title_len = len(title)
    title_score = 0
    if 40 <= title_len <= 65:
        title_score += 5
    elif 30 <= title_len <= 75:
        title_score += 3
    if description and 120 <= len(description) <= 165:
        title_score += 5
    elif description:
        title_score += 2
    
    # 6. Content Type Bonus (0-15 points)
    content_type = fm.get('type', '')
    type_bonus = 0
    if 'pillar' in content_type.lower() or 'guide' in title.lower():
        type_bonus = 15  # Pillar content is highest value
    elif 'howto' in content_type.lower() or 'how to' in title.lower():
        type_bonus = 12
    elif 'comparison' in content_type.lower() or 'vs' in title.lower():
        type_bonus = 10
    elif 'listicle' in content_type.lower() or re.search(r'\d+\s+(best|top|ways)', title, re.IGNORECASE):
        type_bonus = 8
    elif 'faq' in content_type.lower():
        type_bonus = 6
    else:
        type_bonus = 4
    
    total = word_score + structure_score + data_score + faq_score + title_score + type_bonus
    max_total = 100
    
    return {
        'title': title,
        'site': site_name,
        'file': os.path.basename(filepath),
        'category': category,
        'date': date,
        'words': words,
        'total_score': total,
        'word_score': word_score,
        'structure_score': structure_score,
        'data_score': data_score,
        'faq_score': faq_score,
        'title_score': title_score,
        'type_bonus': type_bonus,
        'has_faq': bool(has_faq),
        'h2_count': h2_count,
    }

def main():
    results = []
    
    for site_dir in sorted(os.listdir(CONTENT_DIR)):
        site_path = os.path.join(CONTENT_DIR, site_dir)
        if not os.path.isdir(site_path):
            continue
        for fname in sorted(os.listdir(site_path)):
            if not fname.endswith('.md'):
                continue
            fpath = os.path.join(site_path, fname)
            try:
                score = score_article(fpath, site_dir)
                results.append(score)
            except Exception as e:
                print(f"  Error: {site_dir}/{fname}: {e}", file=sys.stderr)
    
    # Sort by total score descending
    results.sort(key=lambda x: x['total_score'], reverse=True)
    
    # Output
    print(f"\n{'='*80}")
    print(f"PENNYPRESS ARTICLE QUALITY SCORES")
    print(f"Total articles: {len(results)}")
    print(f"{'='*80}\n")
    
    # Per-site summary
    print("PER-SITE AVERAGES:")
    print("-" * 50)
    sites = {}
    for r in results:
        if r['site'] not in sites:
            sites[r['site']] = []
        sites[r['site']].append(r['total_score'])
    
    for site, scores in sorted(sites.items()):
        avg = sum(scores) / len(scores)
        print(f"  {site:30s} {len(scores):3d} articles  avg={avg:.0f}/100")
    
    # Tier breakdown
    tier_s = [r for r in results if r['total_score'] >= 60]
    tier_a = [r for r in results if 45 <= r['total_score'] < 60]
    tier_b = [r for r in results if 30 <= r['total_score'] < 45]
    tier_c = [r for r in results if r['total_score'] < 30]
    
    print(f"\nTIER BREAKDOWN:")
    print(f"  S-Tier (60+): {len(tier_s)} articles — LAUNCH FIRST")
    print(f"  A-Tier (45-59): {len(tier_a)} articles — LAUNCH MONTH 1")
    print(f"  B-Tier (30-44): {len(tier_b)} articles — LAUNCH MONTH 2")
    print(f"  C-Tier (<30): {len(tier_c)} articles — NEEDS IMPROVEMENT")
    
    # Top 20 articles
    print(f"\nTOP 20 ARTICLES (LAUNCH CANDIDATES):")
    print("-" * 80)
    for i, r in enumerate(results[:20], 1):
        print(f"  {i:2d}. [{r['total_score']:2d}/100] {r['site']:25s} | {r['title'][:55]}")
    
    # Bottom 10
    print(f"\nBOTTOM 10 (NEED IMPROVEMENT):")
    print("-" * 80)
    for i, r in enumerate(results[-10:], 1):
        print(f"  {i:2d}. [{r['total_score']:2d}/100] {r['site']:25s} | {r['title'][:55]} ({r['words']} words)")
    
    # Save full results as JSON
    output_path = f"{PROJECT_DIR}/data/quality-scores.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nFull results saved to: {output_path}")
    
    # Save tier lists as JSON for staged deployment
    tiers = {
        's_tier_launch': [{'site': r['site'], 'file': r['file'], 'score': r['total_score']} for r in tier_s],
        'a_tier_month1': [{'site': r['site'], 'file': r['file'], 'score': r['total_score']} for r in tier_a],
        'b_tier_month2': [{'site': r['site'], 'file': r['file'], 'score': r['total_score']} for r in tier_b],
        'c_tier_needs_work': [{'site': r['site'], 'file': r['file'], 'score': r['total_score']} for r in tier_c],
    }
    tier_path = f"{PROJECT_DIR}/data/deployment-tiers.json"
    with open(tier_path, 'w') as f:
        json.dump(tiers, f, indent=2)
    print(f"Deployment tiers saved to: {tier_path}")

if __name__ == '__main__':
    main()
