#!/usr/bin/env python3
"""
PennyPress Site Registry Manager
Manages the site registry for tracking all PennyPress sites
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

REGISTRY_PATH = Path(__file__).parent.parent / "data" / "sites" / "registry.json"


def load_registry():
    """Load existing registry or create new."""
    if REGISTRY_PATH.exists():
        with open(REGISTRY_PATH, "r") as f:
            return json.load(f)
    return {"sites": []}


def save_registry(data):
    """Save registry to file."""
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REGISTRY_PATH, "w") as f:
        json.dump(data, f, indent=2)


def cmd_register(args):
    """Register a new site."""
    registry = load_registry()
    
    # Check if domain already exists
    for site in registry["sites"]:
        if site["domain"] == args.domain:
            print(f"Error: Site '{args.domain}' already registered")
            sys.exit(1)
    
    site = {
        "name": args.name,
        "niche": args.niche,
        "domain": args.domain,
        "status": args.status or "building",
        "created": datetime.now().strftime("%Y-%m-%d"),
        "keywords_tracked": 0,
        "pages_published": 0,
        "github_repo": args.repo or "",
        "cloudflare_url": args.cloudflare or ""
    }
    
    registry["sites"].append(site)
    save_registry(registry)
    
    print(f"✓ Registered: {site['name']} ({site['domain']})")
    print(f"  Status: {site['status']}")
    print(f"  Niche: {site['niche']}")


def cmd_list(args):
    """List all registered sites."""
    registry = load_registry()
    sites = registry.get("sites", [])
    
    if not sites:
        print("No sites registered. Run: site-registry.py register ...")
        return
    
    print(f"Registered Sites: {len(sites)}")
    print("=" * 70)
    
    for i, site in enumerate(sites, 1):
        status_icon = {
            "building": "🔨",
            "live": "✅",
            "paused": "⏸️",
            "archived": "📁"
        }.get(site.get("status", "building"), "❓")
        
        print(f"{i}. {status_icon} {site['name']}")
        print(f"   Domain: {site['domain']}")
        print(f"   Niche: {site['niche']}")
        print(f"   Status: {site['status']}")
        print(f"   Keywords: {site.get('keywords_tracked', 0)} | Pages: {site.get('pages_published', 0)}")
        if site.get("github_repo"):
            print(f"   Repo: {site['github_repo']}")
        if site.get("cloudflare_url"):
            print(f"   URL: {site['cloudflare_url']}")
        print()


def cmd_update(args):
    """Update site status or metadata."""
    registry = load_registry()
    
    # Find site by domain or name
    target = None
    for site in registry["sites"]:
        if site["domain"] == args.domain or site["name"] == args.domain:
            target = site
            break
    
    if not target:
        print(f"Error: Site '{args.domain}' not found")
        sys.exit(1)
    
    if args.status:
        old_status = target["status"]
        target["status"] = args.status
        print(f"✓ Updated {target['name']}: {old_status} → {args.status}")
    
    if args.keywords is not None:
        target["keywords_tracked"] = args.keywords
        print(f"✓ Updated keywords_tracked: {args.keywords}")
    
    if args.pages is not None:
        target["pages_published"] = args.pages
        print(f"✓ Updated pages_published: {args.pages}")
    
    if args.cloudflare:
        target["cloudflare_url"] = args.cloudflare
        print(f"✓ Updated cloudflare_url")
    
    save_registry(registry)


def cmd_stats(args):
    """Show registry statistics."""
    registry = load_registry()
    sites = registry.get("sites", [])
    
    total = len(sites)
    by_status = {}
    total_keywords = 0
    total_pages = 0
    
    for site in sites:
        status = site.get("status", "unknown")
        by_status[status] = by_status.get(status, 0) + 1
        total_keywords += site.get("keywords_tracked", 0)
        total_pages += site.get("pages_published", 0)
    
    print("SITE REGISTRY STATISTICS")
    print("=" * 40)
    print(f"Total sites: {total}")
    print(f"Total keywords tracked: {total_keywords}")
    print(f"Total pages published: {total_pages}")
    print()
    print("By status:")
    for status, count in sorted(by_status.items()):
        icon = {"building": "🔨", "live": "✅", "paused": "⏸️", "archived": "📁"}.get(status, "❓")
        print(f"  {icon} {status}: {count}")
    
    if total > 0:
        print()
        print(f"Avg keywords/site: {total_keywords / total:.1f}")
        print(f"Avg pages/site: {total_pages / total:.1f}")


def main():
    parser = argparse.ArgumentParser(
        description="PennyPress Site Registry Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  register   Add a new site
  list       List all sites
  update     Update site status/metadata
  stats      Show registry statistics

Examples:
  # Register a new site
  python site-registry.py register \\
    --name "SmartHome Hub" \\
    --niche "smart home gadgets" \\
    --domain "smarthomehub.com"

  # List all sites
  python site-registry.py list

  # Update site status
  python site-registry.py update example.com --status live

  # Show stats
  python site-registry.py stats
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Register command
    reg_parser = subparsers.add_parser("register", help="Register a new site")
    reg_parser.add_argument("--name", required=True, help="Site name")
    reg_parser.add_argument("--niche", required=True, help="Site niche/topic")
    reg_parser.add_argument("--domain", required=True, help="Domain (e.g., example.com)")
    reg_parser.add_argument("--status", choices=["building", "live", "paused", "archived"],
                           default="building", help="Initial status")
    reg_parser.add_argument("--repo", help="GitHub repository URL")
    reg_parser.add_argument("--cloudflare", help="Cloudflare Pages URL")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all sites")
    
    # Update command
    upd_parser = subparsers.add_parser("update", help="Update site")
    upd_parser.add_argument("domain", help="Domain or name of site to update")
    upd_parser.add_argument("--status", choices=["building", "live", "paused", "archived"],
                           help="New status")
    upd_parser.add_argument("--keywords", type=int, help="Update keyword count")
    upd_parser.add_argument("--pages", type=int, help="Update pages published count")
    upd_parser.add_argument("--cloudflare", help="Update Cloudflare URL")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show statistics")
    
    args = parser.parse_args()
    
    if args.command == "register":
        cmd_register(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "update":
        cmd_update(args)
    elif args.command == "stats":
        cmd_stats(args)


if __name__ == "__main__":
    main()