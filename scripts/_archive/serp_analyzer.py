#!/usr/bin/env python3
"""
serp-analyzer.py — Analyzes SERP competition for a keyword.
Returns competition score 0-100 based on:
- Number of results
- Presence of big sites (authority sites)
- Content depth indicators
- Domain diversity
"""

import sys
import os
import json
import urllib.request
import urllib.parse
import re
from typing import Dict, Any

SEARXNG_URL = "http://localhost:8888"

# High-authority sites that make competition harder
BIG_SITES = {
    "amazon.com": 15, "wikipedia.org": 12, "youtube.com": 10,
    "reddit.com": 10, "quora.com": 8, "forbes.com": 10,
    "techcrunch.com": 10, "medium.com": 7, "github.com": 8,
    "stackoverflow.com": 8, "nytimes.com": 10, "cdc.gov": 8,
    "mayoclinic.org": 8, "webmd.com": 8, "healthline.com": 8,
    "wikihow.com": 6, "imdb.com": 5, "zillow.com": 6,
    "yelp.com": 5, "glassdoor.com": 5, "Indeed": 5,
    "microsoft.com": 7, "apple.com": 7, "google.com": 5,
    "bing.com": 5, "epa.gov": 6, "nih.gov": 7,
    "www.amazon.co.uk": 15, "www.amazon.de": 15,
    "quora.com": 8, "reddit.com": 10,
}

# Content depth indicators
DEPTH_SIGNALS = ["guide", "tutorial", "review", "complete", "ultimate",
                 "comprehensive", "everything you need", "step by step"]
SHALLOW_SIGNALS = ["quick", "simple", "basic", "intro", "beginner"]


def search_serxng(query: str, limit: int = 10) -> list:
    """Search via SearXNG."""
    params = urllib.parse.urlencode({"q": query, "format": "json", "limit": limit})
    url = f"{SEARXNG_URL}/search?{params}"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data.get("results", [])
    except Exception as e:
        print(f"  [SearXNG error] {e}", file=sys.stderr)
        return []


def extract_domain(url: str) -> str:
    """Extract clean domain from URL."""
    domain = re.sub(r'^https?://(www\.)?', '', url)
    domain = domain.split('/')[0] if '/' in domain else domain
    return domain.lower()


def analyze_serp(keyword: str, limit: int = 10) -> Dict[str, Any]:
    """Full SERP analysis for a keyword."""
    print(f"Analyzing SERP for: '{keyword}'", file=sys.stderr)

    results = search_serxng(keyword, limit=limit)

    if not results:
        return {
            "keyword": keyword,
            "competition_score": 50,
            "grade": "C",
            "result_count": 0,
            "big_site_count": 0,
            "big_sites": [],
            "avg_content_length": 0,
            "content_depth_score": 50,
            "domain_diversity": 0,
            "top_domains": [],
            "recommendation": "No data available. Assume medium competition.",
            "results": [],
        }

    domains = []
    big_site_count = 0
    big_sites = []
    total_content_len = 0
    domain_set = set()

    for r in results:
        url = r.get("url", "")
        domain = extract_domain(url)
        domains.append(domain)
        domain_set.add(domain)

        content = r.get("content", "")
        title = r.get("title", "")
        combined = (title + " " + content).lower()
        total_content_len += len(content)

        # Check for big sites
        for big, weight in BIG_SITES.items():
            if big in url.lower():
                big_site_count += 1
                big_sites.append({"domain": big, "weight": weight, "title": title})
                break

    # Calculate scores
    avg_len = total_content_len / max(len(results), 1)
    domain_diversity = len(domain_set) / max(len(results), 1)

    # Content depth score (0-100)
    depth_score = 0
    for r in results:
        combined = (r.get("title", "") + " " + r.get("content", "")).lower()
        if any(s in combined for s in DEPTH_SIGNALS):
            depth_score += 15
        if any(s in combined for s in SHALLOW_SIGNALS):
            depth_score -= 5
    depth_score = max(0, min(100, depth_score))

    # Competition score formula
    competition = 0
    competition += big_site_count * 12
    competition += (avg_len / 30) * 5
    competition += (1 - domain_diversity) * 15
    competition += depth_score * 0.15
    competition += len(results) * 1.5
    competition = max(5, min(98, competition))

    # Grade
    if competition < 25:
        grade = "A"
        rec = "Low competition. Fast entry opportunity."
    elif competition < 45:
        grade = "B"
        rec = "Medium-low competition. Good opportunity with quality content."
    elif competition < 65:
        grade = "C"
        rec = "Medium competition. Need strong differentiation."
    elif competition < 80:
        grade = "D"
        rec = "High competition. Challenging to rank without authority."
    else:
        grade = "F"
        rec = "Very high competition. Not recommended without existing authority."

    return {
        "keyword": keyword,
        "competition_score": round(competition, 1),
        "grade": grade,
        "result_count": len(results),
        "big_site_count": big_site_count,
        "big_sites": big_sites[:5],
        "avg_content_length": round(avg_len, 1),
        "content_depth_score": round(depth_score, 1),
        "domain_diversity": round(domain_diversity, 2),
        "top_domains": list(domain_set)[:5],
        "recommendation": rec,
        "results": [
            {"title": r.get("title", ""), "url": r.get("url", ""), "content": r.get("content", "")[:200]}
            for r in results
        ],
    }


def main():
    if len(sys.argv) < 2:
        keyword = "smart home gadgets"
        print(f"No keyword provided, using default: '{keyword}'", file=sys.stderr)
    else:
        keyword = sys.argv[1]

    result = analyze_serp(keyword)

    # Output
    if len(sys.argv) > 2 and sys.argv[2] == "--json":
        print(json.dumps(result, indent=2))
    else:
        print(f"\n📊 SERP Analysis: {keyword}")
        print(f"   Competition Score: {result['competition_score']}/100 (Grade: {result['grade']})")
        print(f"   Results Found: {result['result_count']}")
        print(f"   Big Sites: {result['big_site_count']}")
        print(f"   Avg Content Length: {result['avg_content_length']} chars")
        print(f"   Content Depth Score: {result['content_depth_score']}/100")
        print(f"   Domain Diversity: {result['domain_diversity']}")
        print(f"   Top Domains: {', '.join(result['top_domains'])}")
        print(f"\n💡 {result['recommendation']}")

    return result


if __name__ == "__main__":
    main()