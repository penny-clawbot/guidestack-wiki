#!/usr/bin/env python3
"""
PennyPress Rank Monitor
Tracks keyword rankings over time using SearXNG
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

SEARXNG_URL = "http://localhost:8888"
DATA_DIR = Path(__file__).parent.parent / "data" / "analytics"


def search_searxng(query, limit=20):
    """Search using SearXNG and return results."""
    params = {
        "q": query,
        "format": "json",
        "engines": "google,bing,duckduckgo",
        "limit": limit
    }
    url = f"{SEARXNG_URL}/search?{urllib.parse.urlencode(params)}"
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Search error for '{query}': {e}", file=sys.stderr)
        return {"results": []}


def extract_domain(url):
    """Extract domain from URL."""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc.lower().replace("www.", "")
    except:
        return ""


def find_domain_position(results, target_domain):
    """Find position of target domain in search results. Returns position or None."""
    target = target_domain.lower().replace("www.", "")
    for i, result in enumerate(results, 1):
        result_domain = extract_domain(result.get("url", ""))
        if target in result_domain or result_domain in target:
            return i
    return None


def load_rankings(domain):
    """Load existing rankings file or create new structure."""
    filepath = DATA_DIR / f"{domain}-rankings.json"
    if filepath.exists():
        with open(filepath, "r") as f:
            return json.load(f)
    return {
        "domain": domain,
        "last_checked": None,
        "keywords": {}
    }


def save_rankings(data, domain):
    """Save rankings to JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    filepath = DATA_DIR / f"{domain}-rankings.json"
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def check_keyword(keyword, domain, existing_data):
    """Check ranking for a single keyword."""
    print(f"  Checking: '{keyword}'...")
    
    results_data = search_searxng(keyword)
    results = results_data.get("results", [])
    
    position = find_domain_position(results, domain)
    today = datetime.now().strftime("%Y-%m-%d")
    
    keyword_data = existing_data.get("keywords", {}).get(keyword, {})
    positions = keyword_data.get("positions", [])
    
    if position:
        positions.append({"date": today, "position": position})
        print(f"    Found at position {position}")
    else:
        positions.append({"date": today, "position": None})
        print(f"    Not found in top results")
    
    # Keep last 90 days of history
    positions = positions[-90:]
    
    # Calculate change
    current = position
    change = 0
    if len(positions) >= 2:
        prev = positions[-2].get("position")
        if prev and current:
            change = prev - current  # positive = improvement
    
    return {
        "positions": positions,
        "current": current,
        "change": change
    }


def flag_significant_changes(old_data, new_data):
    """Flag significant rank changes (±5 positions)."""
    flags = []
    for keyword, new_kw in new_data.get("keywords", {}).items():
        old_kw = old_data.get("keywords", {}).get(keyword, {})
        old_pos = old_kw.get("current")
        new_pos = new_kw.get("current")
        
        if old_pos and new_pos:
            diff = old_pos - new_pos
            if abs(diff) >= 5:
                direction = "↑" if diff > 0 else "↓"
                flags.append(f"{keyword}: {direction} {abs(diff)} positions (now #{new_pos})")
    
    return flags


def main():
    parser = argparse.ArgumentParser(description="Track keyword rankings")
    parser.add_argument("--keywords", required=True, help="JSON file with keywords and domain")
    parser.add_argument("--domain", help="Target domain (overrides file)")
    args = parser.parse_args()
    
    # Load input file
    with open(args.keywords, "r") as f:
        input_data = json.load(f)
    
    domain = args.domain or input_data.get("domain")
    keywords = input_data.get("keywords", [])
    
    if not domain or not keywords:
        print("Error: Must provide domain and keywords", file=sys.stderr)
        sys.exit(1)
    
    print(f"Monitoring rankings for: {domain}")
    print(f"Keywords: {len(keywords)}")
    print()
    
    # Load existing data
    existing = load_rankings(domain)
    
    # Check each keyword
    new_keywords = {}
    for keyword in keywords:
        kw_result = check_keyword(keyword, domain, existing)
        new_keywords[keyword] = kw_result
    
    # Build updated data
    updated = {
        "domain": domain,
        "last_checked": datetime.now().isoformat(),
        "keywords": new_keywords
    }
    
    # Check for significant changes
    flags = flag_significant_changes(existing, updated)
    
    # Save results
    save_rankings(updated, domain)
    
    print()
    print(f"Last checked: {updated['last_checked']}")
    print(f"Results saved to: {DATA_DIR}/{domain}-rankings.json")
    
    if flags:
        print()
        print("⚠️  Significant changes detected:")
        for flag in flags:
            print(f"  • {flag}")
    
    # Summary stats
    tracked = len(new_keywords)
    found = sum(1 for kw in new_keywords.values() if kw["current"] is not None)
    avg_pos = sum(kw["current"] for kw in new_keywords.values() if kw["current"]) / found if found > 0 else 0
    
    print()
    print(f"Summary: {found}/{tracked} keywords found, avg position: {avg_pos:.1f}")


if __name__ == "__main__":
    main()