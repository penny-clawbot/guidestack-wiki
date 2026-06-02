#!/usr/bin/env python3
"""
Content Freshness Tracker — Detects stale articles needing updates.
Part of the self-improving PSEO system.

Articles should be updated every 90 days for optimal GEO signals.
"""
import os, sys, json, re
from datetime import datetime, timedelta

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITES_DIR = os.path.join(PROJECT_DIR, 'output', 'sites')
FRESHNESS_DAYS = 90  # Articles older than this are "stale"

def get_article_date(filepath):
    """Extract date from frontmatter."""
    with open(filepath) as f:
        content = f.read(500)  # Only read first 500 chars for speed
    # Try frontmatter date
    m = re.search(r'^date:\s*["\']?(\d{4}-\d{2}-\d{2})', content, re.MULTILINE)
    if m:
        return m.group(1)
    # Try filename date
    m = re.match(r'^(\d{4}-\d{2}-\d{2})-', os.path.basename(filepath))
    if m:
        return m.group(1)
    return None

def analyze_site(site_dir):
    """Analyze content freshness for a single site."""
    articles_dir = os.path.join(site_dir, 'src', 'content', 'articles')
    if not os.path.isdir(articles_dir):
        return None
    
    site_name = os.path.basename(site_dir)
    config_path = os.path.join(site_dir, 'site-config.json')
    config = {}
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)
    
    articles = []
    now = datetime.now()
    stale_threshold = now - timedelta(days=FRESHNESS_DAYS)
    
    for fn in os.listdir(articles_dir):
        if not fn.endswith('.md'):
            continue
        
        filepath = os.path.join(articles_dir, fn)
        date_str = get_article_date(filepath)
        
        if date_str:
            try:
                art_date = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                art_date = now
        else:
            art_date = now  # Assume fresh if no date
        
        age_days = (now - art_date).days
        
        # Extract title
        with open(filepath) as f:
            content = f.read(200)
        title_match = re.search(r'^title:\s*["\'](.+?)["\']', content, re.MULTILINE)
        title = title_match.group(1) if title_match else fn.replace('.md', '')
        
        # Classify freshness
        if age_days <= 14:
            status = "fresh"
        elif age_days <= 30:
            status = "recent"
        elif age_days <= FRESHNESS_DAYS:
            status = "aging"
        else:
            status = "stale"
        
        slug = re.sub(r'^\d{4}-\d{2}-\d{2}-(ai-)?', '', fn.replace('.md', ''))
        
        articles.append({
            "title": title,
            "slug": slug,
            "date": date_str,
            "age_days": age_days,
            "status": status,
            "file": fn
        })
    
    # Stats
    fresh = [a for a in articles if a["status"] == "fresh"]
    recent = [a for a in articles if a["status"] == "recent"]
    aging = [a for a in articles if a["status"] == "aging"]
    stale = [a for a in articles if a["status"] == "stale"]
    
    return {
        "site": site_name,
        "niche": config.get("niche", ""),
        "total": len(articles),
        "fresh": len(fresh),
        "recent": len(recent),
        "aging": len(aging),
        "stale": len(stale),
        "oldest_article": max(articles, key=lambda a: a["age_days"]) if articles else None,
        "stale_articles": sorted(stale, key=lambda a: -a["age_days"])[:5]
    }

def main():
    print("📅 Content Freshness Report")
    print(f"   Threshold: {FRESHNESS_DAYS} days")
    print("")
    
    sites = [d for d in os.listdir(SITES_DIR) 
             if os.path.isdir(os.path.join(SITES_DIR, d)) and d != 'unified']
    
    all_results = []
    total_articles = 0
    total_stale = 0
    
    for site_name in sorted(sites):
        site_dir = os.path.join(SITES_DIR, site_name)
        result = analyze_site(site_dir)
        if not result:
            continue
        
        all_results.append(result)
        total_articles += result["total"]
        total_stale += result["stale"]
        
        # Site summary
        status_icons = {"fresh": "🟢", "recent": "🟡", "aging": "🟠", "stale": "🔴"}
        print(f"{'📍 ' + result['site'] + ' (' + result['niche'] + ')':<50}")
        print(f"   {result['total']} articles: 🟢{result['fresh']} 🟡{result['recent']} 🟠{result['aging']} 🔴{result['stale']}")
        
        if result["stale_articles"]:
            print(f"   Oldest stale:")
            for a in result["stale_articles"][:3]:
                print(f"     🔴 {a['age_days']}d — {a['title'][:60]}")
        print("")
    
    # Network summary
    print("═══════════════════════════════════════")
    print(f"📊 Network: {total_articles} articles across {len(all_results)} sites")
    print(f"   🔴 {total_stale} stale articles need updates ({total_stale*100//max(total_articles,1)}%)")
    print("═══════════════════════════════════════")
    
    # Save report
    report_path = os.path.join(PROJECT_DIR, 'data', 'freshness-report.json')
    with open(report_path, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "freshness_threshold_days": FRESHNESS_DAYS,
            "total_articles": total_articles,
            "total_stale": total_stale,
            "sites": all_results
        }, f, indent=2)
    print(f"\nReport: {report_path}")

if __name__ == '__main__':
    main()
