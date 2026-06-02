#!/usr/bin/env python3
"""
Template Parity Checker — Verifies all sites have identical template files.
Run after build-site.sh to detect drift between template and built sites.

Usage: python3 scripts/check-template-parity.py [--fix]
"""
import os, sys, filecmp, json, shutil

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'templates', 'base')
SITES_DIR = os.path.join(PROJECT_DIR, 'output', 'sites')

# Files that should be identical across all sites
TEMPLATE_FILES = [
    'src/layouts/BaseLayout.astro',
    'src/components/CrossSiteLinks.astro',
    'src/components/MidArticleCTA.astro',
    'src/components/NewsletterCTA.astro',
    'src/components/ReadingProgress.astro',
    'src/components/RelatedGuides.astro',
    'src/components/Sidebar.astro',
    'src/components/TOC.astro',
    'src/components/Breadcrumbs.astro',
    'src/components/ArticleCard.astro',
    'src/pages/404.astro',
    'src/pages/about.astro',
    'src/pages/about/author.astro',
    'src/pages/contact.astro',
    'src/pages/privacy-policy.astro',
    'src/pages/terms.astro',
    'src/pages/index.astro',
    'src/pages/feed.xml.ts',
    'src/pages/compare/[...slug].astro',
    'src/pages/best/[category].astro',
    'src/utils/marked-config.ts',
    'src/styles/global.css',
    'src/data/affiliates.json',
    'public/robots.txt',
    'public/og-default.svg',
    'public/llms.txt',
    'astro.config.mjs',
]

# Files that are site-specific (generated per site)
SITE_SPECIFIC = [
    'site-config.json',
    'src/pages/[slug].astro',
    'src/pages/category/[category].astro',
]

def check_parity(fix=False):
    sites = [d for d in os.listdir(SITES_DIR) if os.path.isdir(os.path.join(SITES_DIR, d)) and d != 'unified']
    
    print(f"🔍 Template Parity Check")
    print(f"   Template: {TEMPLATE_DIR}")
    print(f"   Sites: {len(sites)}")
    print("")
    
    results = {"matching": 0, "missing": 0, "drifted": 0, "fixed": 0}
    issues = []
    
    for site in sorted(sites):
        site_dir = os.path.join(SITES_DIR, site)
        site_issues = []
        
        for tf in TEMPLATE_FILES:
            template_file = os.path.join(TEMPLATE_DIR, tf)
            site_file = os.path.join(site_dir, tf)
            
            # Check if template file exists
            if not os.path.exists(template_file):
                continue
            
            # Check if site file exists
            if not os.path.exists(site_file):
                site_issues.append(f"MISSING: {tf}")
                results["missing"] += 1
                if fix:
                    os.makedirs(os.path.dirname(site_file), exist_ok=True)
                    shutil.copy2(template_file, site_file)
                    site_issues[-1] += " → FIXED"
                    results["fixed"] += 1
                continue
            
            # Compare content
            if not filecmp.cmp(template_file, site_file, shallow=False):
                site_issues.append(f"DRIFTED: {tf}")
                results["drifted"] += 1
                if fix:
                    shutil.copy2(template_file, site_file)
                    site_issues[-1] += " → FIXED"
                    results["fixed"] += 1
            else:
                results["matching"] += 1
        
        if site_issues:
            issues.append((site, site_issues))
    
    # Report
    print(f"📊 Results: {results['matching']} matching, {results['missing']} missing, {results['drifted']} drifted")
    if fix:
        print(f"🔧 Fixed: {results['fixed']} files synced")
    print("")
    
    if issues:
        for site, site_issues in issues:
            print(f"⚠️  {site} ({len(site_issues)} issues):")
            for issue in site_issues:
                print(f"    {issue}")
            print("")
    else:
        print("✅ All sites in perfect parity with template!")
    
    # Save report
    report_path = os.path.join(PROJECT_DIR, 'data', 'parity-report.json')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w') as f:
        json.dump({
            "timestamp": __import__('datetime').datetime.now().isoformat(),
            "results": results,
            "issues": {s: iss for s, iss in issues}
        }, f, indent=2)
    print(f"Report: {report_path}")
    
    return len(issues) == 0

if __name__ == '__main__':
    fix = '--fix' in sys.argv
    ok = check_parity(fix=fix)
    sys.exit(0 if ok else 1)
