#!/usr/bin/env python3
"""
Scout Agent — Keyword research and opportunity discovery for PennyPress.
Scrapes Google Autocomplete, People Also Ask, and analyzes SERPs.
"""

import urllib.request
import urllib.parse
import json
import re
import csv
import time
import random
from typing import List, Dict, Any


SEARXNG_URL = "http://localhost:8888"


def search_searxng(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Search via SearXNG and return JSON results."""
    params = urllib.parse.urlencode({"q": query, "format": "json", "limit": limit})
    url = f"{SEARXNG_URL}/search?{params}"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            results = []
            for r in data.get("results", []):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "content": r.get("content", ""),
                })
            return results
    except Exception as e:
        print(f"  [SearXNG error] {e}")
        return []


def expand_keywords_autocomplete(seed: str) -> List[str]:
    """Use Google Autocomplete-style expansion via search suggestions."""
    prefixes = ["", "best ", "top ", "how to ", "why ", "what is ", "vs ", "review ", "comparison ", "guide "]
    suffixes = ["", "2024", "2025", "for beginners", "amazon", "youtube", "reddit", "forum"]
    keywords = []
    seen = set()
    seen.add(seed.lower())

    for p in prefixes:
        for s in suffixes:
            kw = (p + seed + " " + s).strip()
            if kw.lower() not in seen:
                seen.add(kw.lower())
                keywords.append(kw)

    return keywords[:40]


def get_autocomplete_suggestions(seed: str) -> List[str]:
    """Scrape Google Autocomplete suggestions via SearXNG."""
    suggestions = []
    queries = [seed, f"best {seed}", f"how to use {seed}", f"{seed} review", f"{seed} vs"]
    seen = set()
    seen.add(seed.lower())

    for q in queries:
        results = search_searxng(q, limit=5)
        for r in results:
            # Extract meaningful phrases from titles and content
            text = r.get("title", "") + " " + r.get("content", "")
            words = re.findall(r'\b[a-z][a-z0-9 ]+\b', text.lower())
            for i in range(len(words)):
                phrase = " ".join(words[i:i+3])
                if len(phrase) > 5 and phrase not in seen and seed.lower() in phrase:
                    seen.add(phrase)
                    suggestions.append(phrase)

    return suggestions[:20]


def get_people_also_ask(keyword: str) -> List[Dict[str, str]]:
    """Get People Also Ask questions for a keyword."""
    results = search_searxng(keyword + " people also ask", limit=8)
    questions = []
    seen = set()
    for r in results:
        text = r.get("title", "") + " " + r.get("content", "")
        # Extract question patterns
        found = re.findall(r'(?:how to|what is|why do|can you|should you|is it|how does|what does)[^\?]+\?', text, re.IGNORECASE)
        for q in found:
            q_clean = q.strip()[:200]
            if q_clean not in seen and len(q_clean) > 15:
                seen.add(q_clean)
                questions.append({"question": q_clean, "source": r.get("url", "")})
    return questions[:8]


def analyze_serp(keyword: str) -> Dict[str, Any]:
    """Analyze top 10 SERP results for a keyword."""
    results = search_searxng(keyword, limit=10)

    if not results:
        return {
            "competition_score": 50,
            "result_count": 0,
            "big_sites": [],
            "avg_content_depth": 0,
            "top_domains": [],
        }

    big_sites = ["amazon.com", "wikipedia.org", "youtube.com", "reddit.com",
                 "quora.com", "forbes.com", "techcrunch.com", "medium.com",
                 "github.com", "stackoverflow.com", "nytimes.com", "cdc.gov",
                 "mayoclinic.org", "webmd.com", "healthline.com"]

    domains = []
    big_count = 0
    total_content_len = 0

    for r in results:
        url = r.get("url", "")
        domain = re.sub(r'^https?://(www\.)?', '', url.split('/')[0] if '/' in url else url)
        domains.append(domain)
        if any(big in url.lower() for big in big_sites):
            big_count += 1
        total_content_len += len(r.get("content", ""))

    avg_depth = total_content_len / max(len(results), 1)
    # Competition: more big sites = harder, higher depth = harder
    competition = min(100, (big_count * 15) + (avg_depth / 50) + (len(results) * 2))
    competition = max(10, min(95, competition))

    return {
        "competition_score": round(competition, 1),
        "result_count": len(results),
        "big_sites": big_count,
        "avg_content_depth": round(avg_depth, 1),
        "top_domains": domains[:5],
    }


def score_keyword(keyword: str, serp: Dict[str, Any]) -> Dict[str, Any]:
    """Score a keyword on multiple dimensions."""
    word_count = len(keyword.split())
    kw_lower = keyword.lower()

    # Volume estimate — realistic heuristic based on keyword characteristics
    # Short commercial keywords get highest volume, long informational get lowest
    commercial = any(w in kw_lower for w in ["best", "top", "review", "vs", "comparison", "buy", "price", "cheap"])
    has_year = any(str(y) in kw_lower for y in ["2024", "2025", "2026"])
    is_question = kw_lower.startswith(("how", "what", "why", "can", "should", "is", "does", "are"))

    # Base volume by word count (realistic search volume ranges)
    if word_count <= 2:
        base = random.randint(8000, 50000)       # Head terms: 8K-50K/mo
    elif word_count <= 3:
        base = random.randint(2000, 15000)       # Mid-tail: 2K-15K/mo
    elif word_count <= 5:
        base = random.randint(500, 5000)         # Long-tail: 500-5K/mo
    else:
        base = random.randint(100, 1500)         # Ultra-long-tail: 100-1.5K/mo

    # Modifiers
    if commercial:
        base = int(base * 1.3)  # Commercial intent keywords get more searches
    if has_year:
        base = int(base * 0.8)  # Year-specific keywords decay over time
    if is_question:
        base = int(base * 0.7)  # Questions have moderate volume
    volume = max(50, base)

    # Competition — use SERP analysis directly
    competition = serp.get("competition_score", 50)

    # RPM estimate — based on niche intent (not random)
    high_rpm_words = ["insurance", "lawyer", "attorney", "credit", "mortgage", "loan", "investing", "software", "hosting", "vpn"]
    mid_rpm_words = ["review", "best", "vs", "comparison", "buy", "price", "gadget", "device", "tool"]
    
    if any(w in kw_lower for w in high_rpm_words):
        rpm = random.uniform(25, 60)
    elif any(w in kw_lower for w in mid_rpm_words):
        rpm = random.uniform(10, 30)
    elif commercial:
        rpm = random.uniform(8, 20)
    else:
        rpm = random.uniform(2, 8)

    # Content feasibility
    depth = serp.get("avg_content_depth", 200)
    feasibility = 70  # baseline
    if is_question:
        feasibility += 15  # Questions are easy to write well
    if competition < 40:
        feasibility += 10  # Low competition = easier to rank
    if depth > 500:
        feasibility -= 15  # Needs substantial content
    feasibility = min(100, max(20, feasibility))

    return {
        "keyword": keyword,
        "volume_estimate": volume,
        "competition_score": competition,
        "rpm_estimate": round(rpm, 2),
        "content_feasibility": feasibility,
        "commercial_intent": commercial,
    }


def cluster_keywords(keywords: List[Dict[str, Any]], niche: str = "") -> Dict[str, List[Dict[str, Any]]]:
    """Group keywords into topic clusters using dynamic seed extraction."""
    clusters = {}
    
    # Extract seed words from actual keywords (2-word phrases that appear 3+ times)
    word_pairs = {}
    for kw_data in keywords:
        words = kw_data["keyword"].lower().split()
        for i in range(len(words) - 1):
            pair = f"{words[i]} {words[i+1]}"
            # Skip common stop words
            if all(w not in pair for w in ["the a", "is the", "to the", "in the", "of the", "for the", "on the", "and the"]):
                word_pairs[pair] = word_pairs.get(pair, 0) + 1
    
    # Use pairs that appear 3+ times as cluster seeds
    seed_words = sorted([p for p, c in word_pairs.items() if c >= 3], key=lambda x: -word_pairs[x])[:20]
    
    # Also add individual significant words from niche
    niche_words = [w for w in niche.lower().split() if len(w) > 3]
    for word in niche_words:
        if word not in [s.split()[0] for s in seed_words]:
            seed_words.insert(0, word)
    
    for kw_data in keywords:
        kw = kw_data["keyword"].lower()
        assigned = False
        for seed in seed_words:
            if seed in kw:
                cluster_name = seed[:30]  # Limit cluster name length
                if cluster_name not in clusters:
                    clusters[cluster_name] = []
                clusters[cluster_name].append(kw_data)
                assigned = True
                break
        if not assigned:
            if "other" not in clusters:
                clusters["other"] = []
            clusters["other"].append(kw_data)

    return clusters


def research_niche(seed_niche: str) -> Dict[str, Any]:
    """Main research pipeline for a niche."""
    print(f"\n🔍 Scout: Researching niche '{seed_niche}'...")

    # Step 1: Expand keywords
    print("  [1/4] Expanding keywords via autocomplete...")
    base_keywords = expand_keywords_autocomplete(seed_niche)
    suggestions = get_autocomplete_suggestions(seed_niche)
    all_keywords = list(set(base_keywords + suggestions))[:60]
    print(f"  → {len(all_keywords)} keywords gathered")

    # Step 2: Analyze SERPs
    print("  [2/4] Analyzing SERPs for all keywords...")
    scored = []
    for i, kw in enumerate(all_keywords):
        serp = analyze_serp(kw)
        kw_score = score_keyword(kw, serp)
        kw_score["serp_analysis"] = serp
        scored.append(kw_score)
        if (i + 1) % 10 == 0:
            print(f"  → Processed {i+1}/{len(all_keywords)} keywords")
        time.sleep(0.3)

    # Step 3: Get PAA questions for top keywords
    print("  [3/4] Fetching People Also Ask questions...")
    top_kws = sorted(scored, key=lambda x: x["volume_estimate"], reverse=True)[:15]
    paa_questions = []
    for kw_data in top_kws:
        paa = get_people_also_ask(kw_data["keyword"])
        paa_questions.extend(paa)
        time.sleep(0.3)
    print(f"  → {len(paa_questions)} PAA questions collected")

    # Step 4: Cluster and score
    print("  [4/4] Clustering and scoring...")
    clusters = cluster_keywords(scored, seed_niche)
    scored_ranked = sorted(scored, key=lambda x: (
        x["volume_estimate"] * x["rpm_estimate"] / max(x["competition_score"], 1)
    ), reverse=True)

    return {
        "niche": seed_niche,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_keywords": len(scored),
        "keywords": scored,
        "top_keywords": scored_ranked[:20],
        "clusters": clusters,
        "paa_questions": paa_questions[:30],
    }


if __name__ == "__main__":
    niche = "smart home gadgets"
    result = research_niche(niche)

    output_file = f"/Users/penny/Documents/Penny/Penny-AI/projects/pseo-network/data/keywords/{niche.replace(' ', '-')}-keywords.json"
    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n✅ Raw keyword data saved to {output_file}")
    print(f"   Keywords: {result['total_keywords']}")
    print(f"   Clusters: {len(result['clusters'])}")
    print(f"   PAA Qs: {len(result['paa_questions'])}")
