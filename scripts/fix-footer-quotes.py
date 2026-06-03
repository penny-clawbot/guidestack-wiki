#!/usr/bin/env python3
"""Fix broken footer nav block (escaped single quotes from Python f-string)."""
import re
from pathlib import Path

NETWORK = Path("/Users/penny/Documents/Penny/pseo-network")
SITES = [
    "budget-travel-tips", "bitcoin-beginners", "crypto-investing-guide",
    "crypto-trading-strategies", "defi-yield-guide", "personal-finance-tips",
    "ai-tools-hub", "smart-emergency-fund",
]

# The broken pattern uses \\' \\' (which was Python \' \' escaping in the original f-string)
# Replace it with proper double quotes
for site in SITES:
    f = NETWORK / "output" / "sites" / site / "src" / "layouts" / "BaseLayout.astro"
    if not f.exists():
        continue
    content = f.read_text()
    original = content
    
    # Replace the broken footer nav block (with \\' \\' pattern)
    # Use raw string with double backslash
    broken = "{navItems.slice(0, 6).map(cat => {\n            const words = cat.replace(/-/g, \\' \\').split(\' \\');\n            const display = words.length > 2 ? words.slice(0, 2).join(\' \\') : cat.replace(/-/g, \\' \\');\n            return (\n              <li><a href={`/category/${cat}`} class=\"text-[var(--color-text-muted)] hover:text-[var(--color-primary)] transition-colors truncate inline-block max-w-[180px]\" title={cat.replace(/-/g, \\' \\')}>{display.replace(/\\b\\w/g, (l: string) => l.toUpperCase())}</a></li>\n            );\n          })}"
    fixed = "{navItems.slice(0, 6).map(cat => {\n            const words = cat.replace(/-/g, \" \").split(\" \");\n            const display = words.length > 2 ? words.slice(0, 2).join(\" \") : cat.replace(/-/g, \" \");\n            return (\n              <li><a href={`/category/${cat}`} class=\"text-[var(--color-text-muted)] hover:text-[var(--color-primary)] transition-colors truncate inline-block max-w-[180px]\" title={cat.replace(/-/g, \" \")}>{display.replace(/\\b\\w/g, (l: string) => l.toUpperCase())}</a></li>\n            );\n          })}"
    
    if broken in content:
        content = content.replace(broken, fixed)
        f.write_text(content)
        print(f"✅ {site}: footer nav quotes fixed")
    else:
        # Try simpler approach: just replace \\' with " globally in the file
        if "\\'" in content:
            content = content.replace("\\'", '"')
            f.write_text(content)
            print(f"✅ {site}: replaced \\' with \" (simple fix)")
        else:
            print(f"⏭ {site}: no broken quotes found")
