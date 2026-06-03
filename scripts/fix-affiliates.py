#!/usr/bin/env python3
"""Move _warning out of links array (caused build error) and into a separate field."""
import re
from pathlib import Path

NETWORK = Path("/Users/penny/Documents/Penny/pseo-network")
SITES = [
    "budget-travel-tips", "bitcoin-beginners", "crypto-investing-guide",
    "crypto-trading-strategies", "defi-yield-guide", "personal-finance-tips",
    "ai-tools-hub", "smart-emergency-fund",
]

for site in SITES:
    f = NETWORK / "output" / "sites" / site / "src" / "data" / "affiliates.json"
    if not f.exists():
        continue
    content = f.read_text()
    # Remove the warning object from inside links array
    content = re.sub(
        r'\{\s*"_warning":[^}]+\},?\s*\n\s*',
        '',
        content
    )
    # Add as a top-level field after _note (or after the _note line)
    if '"_warning"' not in content:
        # Insert before the closing }
        content = re.sub(
            r'(\s*"_note":\s*"[^"]*"\s*\n)(}\s*)$',
            r'\1  "_warning": "REPLACE_REF / REPLACE_AID / REPLACE_TAG / REPLACE_AFF must be replaced with real affiliate IDs before deploy or affiliate clicks will not earn commission.",\n\2',
            content
        )
    f.write_text(content)
    print(f"✅ {site}: affiliates.json fixed")
