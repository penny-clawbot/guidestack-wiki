#!/usr/bin/env python3
"""
PennyPress Performance Report Generator
Aggregates ranking data into weekly/monthly performance summaries
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
ANALYTICS_DIR = DATA_DIR / "analytics"
SITES_DIR = DATA_DIR / "sites"


def load_site_registry():
    """Load site registry."""
    registry_path = SITES_DIR / "registry.json"
    if registry_path.exists():
        with open(registry_path, "r") as f:
            return json.load(f)
    return {"sites": []}


def load_rankings(domain):
    """Load rankings for a domain."""
    filepath = ANALYTICS_DIR / f"{domain}-rankings.json"
    if filepath.exists():
        with open(filepath, "r") as f:
            return json.load(f)
    return None


def load_all_rankings():
    """Load all ranking files."""
    rankings = {}
    if ANALYTICS_DIR.exists():
        for f in ANALYTICS_DIR.glob("*-rankings.json"):
            domain = f.stem.replace("-rankings", "")
            data = load_rankings(domain)
            if data:
                rankings[domain] = data
    return rankings


def calculate_trend(positions, days=7):
    """Calculate position trend over last N days."""
    cutoff = datetime.now() - timedelta(days=days)
    recent = [p for p in positions if datetime.strptime(p["date"], "%Y-%m-%d") >= cutoff]
    
    if len(recent) < 2:
        return 0
    
    # Compare first and last position in window
    first_pos = recent[0].get("position")
    last_pos = recent[-1].get("position")
    
    if first_pos and last_pos:
        return first_pos - last_pos  # positive = improvement
    return 0


def generate_weekly_report():
    """Generate weekly performance summary."""
    rankings = load_all_rankings()
    registry = load_site_registry()
    
    total_sites = len(rankings)
    total_keywords = 0
    total_found = 0
    all_positions = []
    improvements = []
    
    site_stats = []
    
    for domain, data in rankings.items():
        keywords = data.get("keywords", {})
        site_kw_count = len(keywords)
        site_found = sum(1 for kw in keywords.values() if kw.get("current") is not None)
        site_positions = [kw["current"] for kw in keywords.values() if kw.get("current")]
        
        total_keywords += site_kw_count
        total_found += site_found
        all_positions.extend(site_positions)
        
        # Calculate site improvement
        site_improvement = 0
        for kw_name, kw_data in keywords.items():
            trend = calculate_trend(kw_data.get("positions", []), days=7)
            site_improvement += trend
        
        avg_pos = sum(site_positions) / len(site_positions) if site_positions else 0
        
        site_stats.append({
            "domain": domain,
            "keywords_tracked": site_kw_count,
            "keywords_found": site_found,
            "avg_position": round(avg_pos, 1),
            "improvement": round(site_improvement, 1)
        })
        
        improvements.append(site_improvement)
    
    # Aggregate stats
    avg_all_pos = sum(all_positions) / len(all_positions) if all_positions else 0
    total_improvement = sum(improvements)
    
    # Find top movers
    site_stats.sort(key=lambda x: x["improvement"], reverse=True)
    top_movers = site_stats[:3]
    
    report = {
        "period": "weekly",
        "generated": datetime.now().isoformat(),
        "summary": {
            "total_sites": total_sites,
            "total_keywords": total_keywords,
            "keywords_found": total_found,
            "average_position": round(avg_all_pos, 1),
            "total_improvement": round(total_improvement, 1),
            "found_rate": round((total_found / total_keywords * 100) if total_keywords > 0 else 0, 1)
        },
        "sites": site_stats,
        "top_movers": top_movers
    }
    
    return report


def generate_monthly_report():
    """Generate monthly performance summary."""
    rankings = load_all_rankings()
    
    total_keywords = 0
    all_positions = []
    position_history = {}
    
    for domain, data in rankings.items():
        for kw_name, kw_data in data.get("keywords", {}).items():
            positions = kw_data.get("positions", [])
            if positions:
                total_keywords += 1
                current = kw_data.get("current")
                if current:
                    all_positions.append(current)
                
                # Track monthly history
                for p in positions:
                    month = p["date"][:7]  # YYYY-MM
                    if month not in position_history:
                        position_history[month] = []
                    if p["position"]:
                        position_history[month].append(p["position"])
    
    # Calculate month-over-month
    months = sorted(position_history.keys())
    monthly_avgs = {}
    for month in months:
        avg = sum(position_history[month]) / len(position_history[month])
        monthly_avgs[month] = round(avg, 1)
    
    current_avg = sum(all_positions) / len(all_positions) if all_positions else 0
    
    report = {
        "period": "monthly",
        "generated": datetime.now().isoformat(),
        "summary": {
            "total_keywords": total_keywords,
            "current_avg_position": round(current_avg, 1),
            "months_tracked": len(months)
        },
        "monthly_averages": monthly_avgs
    }
    
    return report


def format_text_report(report):
    """Format report as plain text."""
    lines = []
    lines.append("=" * 50)
    lines.append("PENNYPRESS PERFORMANCE REPORT")
    lines.append("=" * 50)
    lines.append(f"Period: {report['period'].upper()}")
    lines.append(f"Generated: {report['generated']}")
    lines.append()
    
    summary = report["summary"]
    lines.append("SUMMARY")
    lines.append("-" * 30)
    lines.append(f"  Sites tracked:    {summary.get('total_sites', 0)}")
    lines.append(f"  Keywords tracked: {summary.get('total_keywords', 0)}")
    lines.append(f"  Keywords found:   {summary.get('keywords_found', 0)}")
    lines.append(f"  Average position: {summary.get('average_position', 'N/A')}")
    lines.append(f"  Found rate:       {summary.get('found_rate', 'N/A')}%")
    
    if "total_improvement" in summary:
        imp = summary["total_improvement"]
        direction = "↑" if imp > 0 else "↓" if imp < 0 else "→"
        lines.append(f"  Total movement:   {direction} {abs(imp)} positions")
    
    lines.append()
    
    if "sites" in report and report["sites"]:
        lines.append("PER-SITE BREAKDOWN")
        lines.append("-" * 30)
        for site in report["sites"][:10]:  # Top 10
            lines.append(f"  {site['domain']}")
            lines.append(f"    Keywords: {site['keywords_found']}/{site['keywords_tracked']}, "
                        f"Avg: #{site['avg_position']}, "
                        f"Change: {'+' if site['improvement'] > 0 else ''}{site['improvement']}")
        lines.append()
    
    if "top_movers" in report and report["top_movers"]:
        lines.append("TOP MOVERS")
        lines.append("-" * 30)
        for i, site in enumerate(report["top_movers"], 1):
            imp = site["improvement"]
            direction = "↑" if imp > 0 else "↓" if imp < 0 else "→"
            lines.append(f"  {i}. {site['domain']} ({direction} {abs(imp)} positions)")
        lines.append()
    
    if "monthly_averages" in report:
        lines.append("MONTHLY AVERAGE POSITIONS")
        lines.append("-" * 30)
        for month, avg in sorted(report["monthly_averages"].items()):
            lines.append(f"  {month}: #{avg}")
        lines.append()
    
    lines.append("=" * 50)
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate performance reports")
    parser.add_argument("--period", choices=["weekly", "monthly"], default="weekly",
                       help="Report period")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of text")
    parser.add_argument("--output", help="Save to file")
    args = parser.parse_args()
    
    if args.period == "weekly":
        report = generate_weekly_report()
    else:
        report = generate_monthly_report()
    
    if args.json:
        output = json.dumps(report, indent=2)
    else:
        output = format_text_report(report)
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Report saved to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()