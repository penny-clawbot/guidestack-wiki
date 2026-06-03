#!/usr/bin/env python3
"""Add Astro View Transitions + cross-niche linking to all sites."""
import re
from pathlib import Path

NETWORK = Path("/Users/penny/Documents/Penny/pseo-network")
SITES = [
    "budget-travel-tips", "bitcoin-beginners", "crypto-investing-guide",
    "crypto-trading-strategies", "defi-yield-guide", "personal-finance-tips",
    "ai-tools-hub", "smart-emergency-fund",
]

# ============ 1. ADD VIEW TRANSITIONS ============
for site in SITES:
    f = NETWORK / "output" / "sites" / site / "src" / "layouts" / "BaseLayout.astro"
    if not f.exists():
        continue
    content = f.read_text()
    original = content

    # Add ClientRouter import (Astro's view transitions)
    if 'ClientRouter' not in content:
        content = content.replace(
            "---\nimport '../styles/global.css';",
            "---\nimport '../styles/global.css';\nimport { ClientRouter } from 'astro:transitions';"
        )

    # Add ClientRouter in <head> with transition:animate
    if '<ClientRouter' not in content:
        # Insert before </head>
        content = content.replace(
            '</head>',
            '  <ClientRouter />\n</head>'
        )

    if content != original:
        f.write_text(content)
        print(f"✅ {site}: ClientRouter (view transitions) added")

# ============ 2. ADD TRANSITION DIRECTIVES TO KEY ELEMENTS ============
# Add transition:name to h1, brand, and main content for smoother page transitions
for site in SITES:
    slug_f = NETWORK / "output" / "sites" / site / "src" / "pages" / "[slug].astro"
    if not slug_f.exists():
        continue
    content = slug_f.read_text()
    original = content

    # Add transition:name to article h1
    if 'transition:name' not in content and '<h1 class="text-3xl' in content:
        content = content.replace(
            '<h1 class="text-3xl sm:text-4xl lg:text-[2.75rem]',
            '<h1 transition:name="article-title" class="text-3xl sm:text-4xl lg:text-[2.75rem]'
        )

    # Add transition:name to the article header section
    if 'transition:name="article-header"' not in content and 'class="mb-10">\n        <div class="flex flex-wrap gap-2 mb-4">' in content:
        content = content.replace(
            '<!-- Article header -->\n      <header class="mb-10">',
            '<!-- Article header -->\n      <header transition:name="article-header" class="mb-10">'
        )

    if content != original:
        slug_f.write_text(content)
        print(f"✅ {site}: transition:animate directives added to [slug].astro")

    # Also add to BaseLayout for site-wide title transition
    bl = NETWORK / "output" / "sites" / site / "src" / "layouts" / "BaseLayout.astro"
    if bl.exists():
        c = bl.read_text()
        o = c
        # Add transition to logo brand text
        if 'transition:name="site-name"' not in c:
            c = c.replace(
                '<span class="text-lg font-bold text-[var(--color-text-heading)] group-hover:text-[var(--color-primary)] transition-colors">{displayTitle}</span>',
                '<span transition:name="site-name" class="text-lg font-bold text-[var(--color-text-heading)] group-hover:text-[var(--color-primary)] transition-colors">{displayTitle}</span>'
            )
            c = c.replace(
                '<span class="text-lg font-bold text-[var(--color-text-heading)]">{displayTitle}</span>',
                '<span transition:name="site-name" class="text-lg font-bold text-[var(--color-text-heading)]">{displayTitle}</span>'
            )
        if c != o:
            bl.write_text(c)

# ============ 3. ADD CROSS-NICHE LINKING ============
# Add a "Related from other sites" section to the unified site sidebar
# And add CrossSiteLinks component to all individual sites

# Add to each site's [slug].astro - inject a "popular across network" section
# This uses the existing CrossSiteLinks component, but we add a small footer-style network strip
NETWORK_FOOTER_HTML = '''
      <!-- Network: Other sites in the network -->
      <section class="mt-12 pt-8 border-t border-[var(--color-border)]">
        <h3 class="text-lg font-bold text-[var(--color-text-heading)] mb-4 flex items-center gap-2">
          <svg class="w-4 h-4 text-[var(--color-primary)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
          Explore more guides
        </h3>
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
{NETWORK_LINKS}
        </div>
      </section>
'''

NETWORK_SITES = [
    {"name": "AI Tools Hub", "emoji": "🤖", "path": "/ai-tools/", "desc": "Best AI tools"},
    {"name": "Bitcoin 101", "emoji": "₿", "path": "/bitcoin-beginners/", "desc": "Bitcoin basics"},
    {"name": "Crypto Investing", "emoji": "💰", "path": "/crypto-investing/", "desc": "Investment strategies"},
    {"name": "Crypto Trading", "emoji": "📊", "path": "/crypto-trading/", "desc": "Trading strategies"},
    {"name": "DeFi Yield", "emoji": "🏦", "path": "/defi-yield/", "desc": "DeFi yield farming"},
    {"name": "Personal Finance", "emoji": "💵", "path": "/personal-finance/", "desc": "Money management"},
    {"name": "Emergency Fund", "emoji": "🛡️", "path": "/emergency-fund/", "desc": "Build your safety net"},
    {"name": "Budget Travel", "emoji": "✈️", "path": "/budget-travel/", "desc": "Travel for less"},
]

# Build link cards (will appear at path-prefixed URL on unified site)
def build_links(current_site):
    cards = []
    for s in NETWORK_SITES:
        if s["path"].strip("/") in current_site or current_site in s["path"]:
            continue
        # Use site name as slug for unified site linking
        # When deployed at single domain: /ai-tools/, /crypto-investing/, etc.
        cards.append(f'          <a href="{s["path"]}" class="card group p-3 flex flex-col items-start gap-1.5 hover:border-[var(--color-primary)]">\n            <span class="text-xl" aria-hidden="true">{s["emoji"]}</span>\n            <span class="text-sm font-semibold text-[var(--color-text-heading)] group-hover:text-[var(--color-primary)]">{s["name"]}</span>\n            <span class="text-xs text-[var(--color-text-muted)]">{s["desc"]}</span>\n          </a>')
    return "\n".join(cards)

for site in SITES:
    slug_f = NETWORK / "output" / "sites" / site / "src" / "pages" / "[slug].astro"
    if not slug_f.exists():
        continue
    content = slug_f.read_text()
    if 'Explore more guides' in content:
        continue
    original = content
    cards = build_links(site)
    html = NETWORK_FOOTER_HTML.replace("{NETWORK_LINKS}", cards)
    # Insert before </article>
    content = content.replace(
        '    </article>\n\n    <!-- Sidebar -->',
        html + '\n    </article>\n\n    <!-- Sidebar -->'
    )
    if content != original:
        slug_f.write_text(content)
        print(f"✅ {site}: cross-niche 'Explore more guides' section added")
