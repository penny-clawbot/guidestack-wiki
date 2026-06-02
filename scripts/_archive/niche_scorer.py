#!/usr/bin/env python3
"""
niche-scorer.py — Takes keyword research output + SERP analysis,
computes overall opportunity score, ranks and filters (score > 60),
outputs top opportunities with recommended content strategy.
"""

import sys
import os
import json
import glob
from typing import Dict, Any, List


def calculate_opportunity_score(kw_data: Dict[str, Any]) -> float:
    """
    Opportunity Score (0-100) based on:
    - Volume score: log-scaled 0-30
    - RPM score: log-scaled 0-30
    - Competition score: inverted 0-40 (low comp = high score)
    """
    volume = kw_data.get("volume_estimate", 0)
    competition = max(kw_data.get("competition_score", 50), 1)
    rpm = kw_data.get("rpm_estimate", 1)
    feasibility = kw_data.get("content_feasibility", 50) / 100

    # Volume score: log scale, cap at 50M → 30 points
    import math
    volume_score = min(30, math.log1p(volume) / math.log(1e6) * 30)

    # RPM score: cap at $50 → 30 points
    rpm_score = min(30, (rpm / 50) * 30)

    # Competition score: 0-100 → inverted 0-40 (lower = better)
    comp_score = (100 - competition) / 100 * 40

    opportunity = (volume_score + rpm_score + comp_score) * feasibility

    return round(min(100, opportunity), 2)


def score_cluster(cluster_name: str, keywords: List[Dict]) -> Dict[str, Any]:
    """Score a keyword cluster."""
    total_volume = sum(k.get("volume_estimate", 0) for k in keywords)
    avg_competition = sum(k.get("competition_score", 50) for k in keywords) / max(len(keywords), 1)
    avg_rpm = sum(k.get("rpm_estimate", 1) for k in keywords) / max(len(keywords), 1)
    avg_feasibility = sum(k.get("content_feasibility", 50) for k in keywords) / max(len(keywords), 1)
    commercial_count = sum(1 for k in keywords if k.get("commercial_intent", False))

    return {
        "cluster": cluster_name,
        "keyword_count": len(keywords),
        "total_volume_estimate": round(total_volume),
        "avg_competition": round(avg_competition, 1),
        "avg_rpm": round(avg_rpm, 2),
        "avg_feasibility": round(avg_feasibility, 1),
        "commercial_ratio": round(commercial_count / max(len(keywords), 1), 2),
        "cluster_score": round((total_volume * avg_rpm) / (avg_competition * 100) * 0.0001, 2),
        "top_keywords": [k["keyword"] for k in sorted(keywords, key=lambda x: x["volume_estimate"], reverse=True)[:5]],
    }


def get_content_strategy(cluster: str, keywords: List[Dict]) -> str:
    """Recommend content strategy based on cluster characteristics."""
    commercial = sum(1 for k in keywords if k.get("commercial_intent", False)) / max(len(keywords), 1)
    avg_comp = sum(k.get("competition_score", 50) for k in keywords) / max(len(keywords), 1)
    avg_volume = sum(k.get("volume_estimate", 0) for k in keywords) / max(len(keywords), 1)

    if commercial > 0.6:
        strategy = "Product-focused content with affiliate integrations. " \
                  "Comparison articles, best-of lists, buying guides."
    elif avg_comp > 70:
        strategy = "Authority-building approach. Guest posts, PR, " \
                  "expert quotes, original data/reports."
    elif avg_volume > 15000:
        strategy = "High-volume highway. Broad informational content, " \
                  "featured snippets optimization, PAA targeting."
    else:
        strategy = "Niche micro-content. Long-tail targeting, " \
                  "question-based articles, internal linking strategy."

    return strategy


def score_niche(input_file: str, min_score: float = 60) -> Dict[str, Any]:
    """Load keyword research data and score opportunities."""
    with open(input_file, "r") as f:
        data = json.load(f)

    keywords = data.get("keywords", [])
    clusters = data.get("clusters", {})

    # Score each keyword
    scored_keywords = []
    for kw in keywords:
        opp_score = calculate_opportunity_score(kw)
        kw["opportunity_score"] = opp_score
        kw["grade"] = "A" if opp_score >= 80 else "B" if opp_score >= 60 else "C" if opp_score >= 40 else "D" if opp_score >= 20 else "F"
        scored_keywords.append(kw)

    # Filter top opportunities
    top_opportunities = [k for k in scored_keywords if k["opportunity_score"] >= min_score]
    top_opportunities = sorted(top_opportunities, key=lambda x: x["opportunity_score"], reverse=True)

    # Score clusters
    scored_clusters = []
    for cluster_name, cluster_kws in clusters.items():
        cluster_data = score_cluster(cluster_name, cluster_kws)
        cluster_data["content_strategy"] = get_content_strategy(cluster_name, cluster_kws)
        scored_clusters.append(cluster_data)

    scored_clusters = sorted(scored_clusters, key=lambda x: x["cluster_score"], reverse=True)

    return {
        "niche": data.get("niche", "unknown"),
        "timestamp": data.get("timestamp", ""),
        "total_keywords": len(scored_keywords),
        "opportunities_above_threshold": len(top_opportunities),
        "score_threshold": min_score,
        "scored_keywords": scored_keywords,
        "top_opportunities": top_opportunities[:20],
        "scored_clusters": scored_clusters,
        "summary": {
            "avg_opportunity_score": round(sum(k["opportunity_score"] for k in scored_keywords) / max(len(scored_keywords), 1), 2),
            "grade_a_count": sum(1 for k in scored_keywords if k["grade"] == "A"),
            "grade_b_count": sum(1 for k in scored_keywords if k["grade"] == "B"),
            "grade_c_count": sum(1 for k in scored_keywords if k["grade"] == "C"),
        },
    }


def main():
    if len(sys.argv) < 2:
        # Find most recent keywords file
        data_dir = "data/keywords"
        files = glob.glob(f"{data_dir}/*.json")
        if not files:
            print("No keyword files found. Run keyword-research.py first.", file=sys.stderr)
            sys.exit(1)
        input_file = max(files, key=os.path.getmtime)
        print(f"No input file provided, using: {input_file}", file=sys.stderr)
    else:
        input_file = sys.argv[1]

    min_score = float(sys.argv[2]) if len(sys.argv) > 2 else 60

    if not os.path.exists(input_file):
        print(f"File not found: {input_file}", file=sys.stderr)
        sys.exit(1)

    print(f"\n📊 Niche Scorer — analyzing {input_file}...", file=sys.stderr)
    result = score_niche(input_file, min_score)

    # Save scored output
    niche = result["niche"]
    safe_niche = niche.replace(" ", "-")
    scored_file = f"data/keywords/{safe_niche}-scored.json"
    with open(scored_file, "w") as f:
        json.dump(result, f, indent=2)

    clusters_file = f"data/keywords/{safe_niche}-clusters.json"
    with open(clusters_file, "w") as f:
        json.dump({"niche": niche, "clusters": result["scored_clusters"]}, f, indent=2)

    # Print summary
    print(f"\n{'='*60}")
    print(f" NICHE OPPORTUNITY REPORT: {niche}")
    print(f"{'='*60}")
    print(f"\n📈 SUMMARY:")
    print(f"   Total Keywords: {result['total_keywords']}")
    print(f"   Above {min_score} threshold: {result['opportunities_above_threshold']}")
    print(f"   Grade A (80+): {result['summary']['grade_a_count']}")
    print(f"   Grade B (60-79): {result['summary']['grade_b_count']}")
    print(f"   Grade C (40-59): {result['summary']['grade_c_count']}")
    print(f"   Avg Opportunity Score: {result['summary']['avg_opportunity_score']}")

    print(f"\n🏆 TOP 10 OPPORTUNITIES:")
    for i, kw in enumerate(result["top_opportunities"][:10], 1):
        print(f"   {i}. {kw['keyword']}")
        print(f"      Score: {kw['opportunity_score']} | Vol: {kw['volume_estimate']:,} | Comp: {kw['competition_score']} | RPM: ${kw['rpm_estimate']:.2f}")

    print(f"\n📁 TOP CLUSTERS:")
    for c in result["scored_clusters"][:5]:
        print(f"   • {c['cluster']}: Score {c['cluster_score']}, {c['keyword_count']} keywords, " \
              f"Avg Comp {c['avg_competition']}, Strategy: {c['content_strategy'][:60]}...")

    print(f"\n✅ Outputs saved:")
    print(f"   {scored_file}")
    print(f"   {clusters_file}")

    return result


if __name__ == "__main__":
    main()