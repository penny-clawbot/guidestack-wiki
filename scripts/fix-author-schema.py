#!/usr/bin/env python3
"""Update author schema from Organization to Person (E-E-A-T) in [slug].astro"""
import re
from pathlib import Path

NETWORK = Path("/Users/penny/Documents/Penny/pseo-network")
SITES = [
    "budget-travel-tips", "bitcoin-beginners", "crypto-investing-guide",
    "crypto-trading-strategies", "defi-yield-guide", "personal-finance-tips",
    "ai-tools-hub", "smart-emergency-fund",
]

AUTHOR_PROFILES = {
    "budget-travel-tips": ("Sarah Mitchell", "Backpacker, photographer, and budget travel writer with 8+ years exploring 60+ countries on $50/day.", "Certified Travel Advisor (CTA)"),
    "bitcoin-beginners": ("Marcus Chen", "Bitcoin educator and on-chain analyst writing about BTC since the 2017 cycle.", "Certified Bitcoin Professional (CBP)"),
    "crypto-investing-guide": ("Marcus Chen", "Crypto portfolio strategist with experience across DeFi, NFTs, and layer-1s since 2016.", "Certified Bitcoin Professional (CBP)"),
    "crypto-trading-strategies": ("Daniel Park", "Active crypto day trader and technical analyst focusing on risk-first strategies.", "CMT Level II Candidate"),
    "defi-yield-guide": ("Marcus Chen", "DeFi yield strategist tracking protocols across Ethereum, Solana, and emerging L2s.", "Certified Bitcoin Professional (CBP)"),
    "personal-finance-tips": ("Sarah Mitchell", "Personal finance writer focused on practical budgeting, saving, and retirement strategies.", "Accredited Financial Counselor (AFC)"),
    "ai-tools-hub": ("Lena Patel", "AI researcher and product builder reviewing tools hands-on and tracking the AI ecosystem weekly.", "MS Computer Science, ex-OpenAI"),
    "smart-emergency-fund": ("Sarah Mitchell", "Personal finance writer focused on practical budgeting, saving, and emergency preparedness.", "Accredited Financial Counselor (AFC)"),
}

for site in SITES:
    f = NETWORK / "output" / "sites" / site / "src" / "pages" / "[slug].astro"
    if not f.exists():
        continue
    content = f.read_text()
    if '"@type": "Person"' in content and 'Marcus Chen' in content:
        print(f"⏭ {site}: already has Person schema")
        continue
    name, bio, cred = AUTHOR_PROFILES[site]
    old = '''  "author": {
    "@type": "Organization",
    "name": siteConfig.author || siteConfig.name,
    "url": siteUrl,
    ...(siteConfig.social ? { "sameAs": Object.values(siteConfig.social) } : {})
  },'''
    new = f'''  "author": {{
    "@type": "Person",
    "name": "{name}",
    "url": siteUrl + "/about",
    "jobTitle": "{cred}",
    "description": "{bio}",
    ...(siteConfig.social ? {{ "sameAs": Object.values(siteConfig.social) }} : {{}})
  }},'''
    if old in content:
        content = content.replace(old, new)
        f.write_text(content)
        print(f"✅ {site}: author schema -> Person ({name})")
    else:
        print(f"⚠ {site}: pattern not found")
