#!/usr/bin/env python3
"""Fix share button Astro template-literal syntax in [slug].astro"""
import re
from pathlib import Path

NETWORK = Path("/Users/penny/Documents/Penny/pseo-network")
SITES = [
    "budget-travel-tips", "bitcoin-beginners", "crypto-investing-guide",
    "crypto-trading-strategies", "defi-yield-guide", "personal-finance-tips",
    "ai-tools-hub", "smart-emergency-fund",
]

for site in SITES:
    f = NETWORK / "output" / "sites" / site / "src" / "pages" / "[slug].astro"
    if not f.exists():
        continue
    content = f.read_text()
    original = content

    # Fix Twitter share href - wrap in Astro expression
    content = re.sub(
        r'href="https://twitter\.com/intent/tweet\?text=\$\{encodeURIComponent\(article\.title\)\}&url=\$\{encodeURIComponent\(siteUrl \+ \'/\' \+ slug\)\}"',
        'href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(article.title)}&url=${encodeURIComponent(siteUrl + \'/\') + slug}`}',
        content
    )

    # Fix LinkedIn share href
    content = re.sub(
        r'href="https://www\.linkedin\.com/sharing/share-offsite/\?url=\$\{encodeURIComponent\(siteUrl \+ \'/\' \+ slug\)\}"',
        'href={`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(siteUrl + \'/\') + slug}`}',
        content
    )

    # Fix copy button onclick
    content = re.sub(
        r"onclick=\"navigator\.clipboard\.writeText\('\$\{siteUrl\}/\$\{slug\}'\)\.then\(\(\)=>this\.textContent='✓ Copied!'\)\"",
        "onclick={`navigator.clipboard.writeText(siteUrl + '/' + slug).then(()=>this.textContent='✓ Copied!')`}",
        content
    )

    if content != original:
        f.write_text(content)
        print(f"✅ {site}: share buttons fixed")
    else:
        print(f"⏭ {site}: no changes needed")
