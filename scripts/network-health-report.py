#!/usr/bin/env python3
"""
Network Health Report — Comprehensive weekly health check for PennyPress PSEO network.
Covers: template parity, content freshness, build status, quality scores, GEO compliance.

Usage: python3 scripts/network-health-report.py
Cron: Weekly (Monday 9 AM)
"""
import os, sys, json, subprocess
from datetime import datetime

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITES_DIR = os.path.join(PROJECT_DIR, 'output', 'sites')
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
REPORT_DIR = os.path.join(PROJECT_DIR, 'docs', 'reports')

def run_cmd(cmd):
    """Run a command and return output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

def get_site_stats(site_dir):
    """Get stats for a single site."""
    site_name = os.path.basename(site_dir)
    config_path = os.path.join(site_dir, 'site-config.json')
    config = {}
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)
    
    # Article count
    articles_dir = os.path.join(site_dir, 'src', 'content', 'articles')
    articles = [f for f in os.listdir(articles_dir) if f.endswith('.md')] if os.path.isdir(articles_dir) else []
    
    # Build output
    dist_dir = os.path.join(site_dir, 'dist')
    html_files = []
    total_size = 0
    has_llms = False
    has_sitemap = False
    has_feed = False
    
    if os.path.isdir(dist_dir):
        for root, dirs, files in os.walk(dist_dir):
            for f in files:
                fp = os.path.join(root, f)
                total_size += os.path.getsize(fp)
                if f.endswith('.html'):
                    html_files.append(f)
                if f == 'llms.txt':
                    has_llms = True
                if f == 'sitemap.xml':
                    has_sitemap = True
                if f == 'feed.xml':
                    has_feed = True
    
    # Schema check (sample one article)
    schema_types = set()
    if html_files:
        import re
        sample_html = os.path.join(dist_dir, html_files[0])
        if os.path.exists(sample_html):
            with open(sample_html) as f:
                content = f.read()
            for m in re.finditer(r'"@type"\s*:\s*"([^"]+)"', content):
                schema_types.add(m.group(1))
    
    return {
        "name": site_name,
        "niche": config.get("niche", ""),
        "domain": config.get("domain", ""),
        "articles": len(articles),
        "pages": len(html_files),
        "size_mb": round(total_size / 1024 / 1024, 1),
        "has_llms_txt": has_llms,
        "has_sitemap": has_sitemap,
        "has_rss_feed": has_feed,
        "schema_types": sorted(list(schema_types)),
        "dist_exists": os.path.isdir(dist_dir)
    }

def main():
    print("🏥 PennyPress Network Health Report")
    print(f"   Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("")
    
    sites = sorted([d for d in os.listdir(SITES_DIR) 
                   if os.path.isdir(os.path.join(SITES_DIR, d)) and d != 'unified'])
    
    all_stats = []
    total_articles = 0
    total_pages = 0
    
    for site_name in sites:
        site_dir = os.path.join(SITES_DIR, site_name)
        stats = get_site_stats(site_dir)
        all_stats.append(stats)
        total_articles += stats["articles"]
        total_pages += stats["pages"]
        
        # Health indicators
        health = []
        if not stats["dist_exists"]:
            health.append("❌ No build")
        if not stats["has_llms_txt"]:
            health.append("⚠️ No llms.txt")
        if not stats["has_sitemap"]:
            health.append("⚠️ No sitemap")
        if not stats["has_rss_feed"]:
            health.append("⚠️ No RSS feed")
        if stats["articles"] < 40:
            health.append(f"⚠️ Low content ({stats['articles']})")
        
        status_line = "✅" if not health else " ".join(health)
        print(f"📍 {site_name:<30} {stats['articles']:>3} articles → {stats['pages']:>3} pages ({stats['size_mb']}MB) {status_line}")
    
    print("")
    print("═══════════════════════════════════════")
    print(f"📊 Network Totals:")
    print(f"   Sites: {len(all_stats)}")
    print(f"   Articles: {total_articles}")
    print(f"   Pages: {total_pages}")
    print(f"   Avg pages/site: {total_pages // max(len(all_stats), 1)}")
    
    # GEO compliance
    geo_ok = sum(1 for s in all_stats if s["has_llms_txt"] and s["has_sitemap"] and s["has_rss_feed"])
    print(f"   GEO-compliant sites: {geo_ok}/{len(all_stats)}")
    print("═══════════════════════════════════════")
    
    # Run parity check
    print("")
    print("🔍 Template Parity:")
    parity_output = run_cmd(f"python3 {PROJECT_DIR}/scripts/check-template-parity.py")
    parity_ok = "perfect parity" in parity_output.lower()
    if parity_ok:
        print("   ✅ All sites in perfect parity")
    else:
        drifted = parity_output.count("DRIFTED")
        missing = parity_output.count("MISSING")
        print(f"   ⚠️ {drifted} drifted, {missing} missing files")
    
    # Run freshness check
    print("")
    print("📅 Content Freshness:")
    freshness_output = run_cmd(f"python3 {PROJECT_DIR}/scripts/check-freshness.py")
    if "0 stale" in freshness_output:
        print("   ✅ All articles fresh")
    else:
        stale_count = freshness_output.count("🔴 stale")
        print(f"   ⚠️ Some articles approaching stale threshold")
    
    # Save report
    os.makedirs(REPORT_DIR, exist_ok=True)
    report_path = os.path.join(REPORT_DIR, f"health-{datetime.now().strftime('%Y-%m-%d')}.md")
    
    with open(report_path, 'w') as f:
        f.write(f"# Network Health Report — {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write(f"## Summary\n")
        f.write(f"- Sites: {len(all_stats)}\n")
        f.write(f"- Articles: {total_articles}\n")
        f.write(f"- Pages: {total_pages}\n")
        f.write(f"- GEO-compliant: {geo_ok}/{len(all_stats)}\n")
        f.write(f"- Template parity: {'✅' if parity_ok else '⚠️'}\n\n")
        
        f.write(f"## Per-Site Details\n\n")
        f.write(f"| Site | Articles | Pages | Size | llms.txt | Sitemap | RSS | Status |\n")
        f.write(f"|------|----------|-------|------|----------|---------|-----|--------|\n")
        for s in all_stats:
            status = "✅" if (s["has_llms_txt"] and s["has_sitemap"] and s["has_rss_feed"]) else "⚠️"
            f.write(f"| {s['name']} | {s['articles']} | {s['pages']} | {s['size_mb']}MB | {'✅' if s['has_llms_txt'] else '❌'} | {'✅' if s['has_sitemap'] else '❌'} | {'✅' if s['has_rss_feed'] else '❌'} | {status} |\n")
    
    print(f"\n📄 Report saved: {report_path}")
    
    # Update latest report symlink
    latest_path = os.path.join(REPORT_DIR, 'latest.md')
    with open(latest_path, 'w') as f:
        f.write(open(report_path).read())
    
    return all_stats

if __name__ == '__main__':
    main()
