#!/usr/bin/env python3
"""
keyword-research.py — Main entry point for keyword research pipeline.
Usage: python keyword-research.py <seed_niche>
Example: python keyword-research.py "smart home gadgets"
"""

import sys
import os
import json
import time

# Add project root (parent of scripts/) to path so src/agents is importable
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src/agents"))

from scout import research_niche, SEARXNG_URL


def check_searxng():
    """Check if SearXNG is available."""
    try:
        import urllib.request
        with urllib.request.urlopen(SEARXNG_URL + "/search?q=test&format=json", timeout=5) as r:
            return r.status == 200
    except:
        return False


def main():
    if len(sys.argv) < 2:
        niche = "smart home gadgets"
        print(f"No niche provided, using default: '{niche}'")
    else:
        niche = sys.argv[1]

    print(f"\n{'='*60}")
    print(f" PENNYPRESS KEYWORD RESEARCH PIPELINE")
    print(f" Niche: {niche}")
    print(f"{'='*60}")

    if not check_searxng():
        print(f"\n❌ SearXNG not available at {SEARXNG_URL}")
        print("   Start with: docker start searxng")
        sys.exit(1)

    print("✅ SearXNG connected")

    start = time.time()
    result = research_niche(niche)
    elapsed = time.time() - start

    # Save raw keywords
    safe_niche = niche.replace(" ", "-")
    raw_file = f"data/keywords/{safe_niche}-keywords.json"
    with open(raw_file, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n⏱ Completed in {elapsed:.1f}s")
    print(f"\n📊 RESULTS:")
    print(f"   Total keywords: {result['total_keywords']}")
    print(f"   Top clusters: {', '.join(list(result['clusters'].keys())[:5])}")
    print(f"   PAA questions: {len(result['paa_questions'])}")
    print(f"\n📁 Output: {raw_file}")

    # Summary of top keywords
    print(f"\n🏆 TOP 10 KEYWORDS:")
    for i, kw in enumerate(result["top_keywords"][:10], 1):
        print(f"   {i}. {kw['keyword']}")
        print(f"      Vol: {kw['volume_estimate']:,} | Comp: {kw['competition_score']} | RPM: ${kw['rpm_estimate']:.2f}")

    return result


if __name__ == "__main__":
    main()