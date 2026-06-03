#!/usr/bin/env python3
"""Update article header in [slug].astro to use the new pen name instead of siteConfig.author."""
import re
from pathlib import Path

NETWORK = Path("/Users/penny/Documents/Penny/pseo-network")
SITES = [
    "budget-travel-tips", "bitcoin-beginners", "crypto-investing-guide",
    "crypto-trading-strategies", "defi-yield-guide", "personal-finance-tips",
    "ai-tools-hub", "smart-emergency-fund",
]

AUTHOR_PROFILES = {
    "budget-travel-tips": ("Sarah Mitchell", "Certified Travel Advisor (CTA)"),
    "bitcoin-beginners": ("Marcus Chen", "Certified Bitcoin Professional (CBP)"),
    "crypto-investing-guide": ("Marcus Chen", "Certified Bitcoin Professional (CBP)"),
    "crypto-trading-strategies": ("Daniel Park", "CMT Level II Candidate"),
    "defi-yield-guide": ("Marcus Chen", "Certified Bitcoin Professional (CBP)"),
    "personal-finance-tips": ("Sarah Mitchell", "Accredited Financial Counselor (AFC)"),
    "ai-tools-hub": ("Lena Patel", "MS Computer Science, ex-OpenAI"),
    "smart-emergency-fund": ("Sarah Mitchell", "Accredited Financial Counselor (AFC)"),
}

for site in SITES:
    f = NETWORK / "output" / "sites" / site / "src" / "pages" / "[slug].astro"
    if not f.exists():
        continue
    content = f.read_text()
    if 'siteConfig.author' not in content:
        continue
    name, cred = AUTHOR_PROFILES[site]
    # Get initials
    initials = "".join([w[0] for w in name.split()[:2]]).upper()
    original = content

    # Replace the article header author section to use hardcoded name + credential
    # The block we need to replace:
    old_block = '''        <div class="flex items-center gap-4 text-sm text-[var(--color-text-muted)]">
          <div class="flex items-center gap-2">
            <div class="w-8 h-8 rounded-full bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-accent)] flex items-center justify-center text-white text-xs font-bold">
              {(siteConfig.author || siteConfig.name).split(' ').map((w: string) => w[0]).join('').substring(0, 2)}
            </div>
            <span class="font-medium text-[var(--color-text)]">{siteConfig.author || siteConfig.name}</span>
            <span class="text-xs text-[var(--color-text-muted)] hidden sm:inline">· {siteConfig.niche ? `${siteConfig.niche.charAt(0).toUpperCase() + siteConfig.niche.slice(1)} Expert` : 'Editorial Team'}</span>
          </div>'''
    new_block = f'''        <div class="flex items-center gap-4 text-sm text-[var(--color-text-muted)]">
          <div class="flex items-center gap-2">
            <div class="w-8 h-8 rounded-full bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-accent)] flex items-center justify-center text-white text-xs font-bold">{initials}</div>
            <span class="font-medium text-[var(--color-text)]">{name}</span>
            <span class="text-xs text-[var(--color-text-muted)] hidden sm:inline">· {cred}</span>
          </div>'''
    if old_block in content:
        content = content.replace(old_block, new_block)
        f.write_text(content)
        print(f"✅ {site}: header author updated to {name}")
    else:
        print(f"⚠ {site}: pattern not found")
