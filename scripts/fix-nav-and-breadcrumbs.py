#!/usr/bin/env python3
"""Fix long category names in nav, breadcrumb truncation, 2024 date references."""
import re
from pathlib import Path

NETWORK = Path("/Users/penny/Documents/Penny/pseo-network")
SITES = [
    "budget-travel-tips", "bitcoin-beginners", "crypto-investing-guide",
    "crypto-trading-strategies", "defi-yield-guide", "personal-finance-tips",
    "ai-tools-hub", "smart-emergency-fund",
]

# Limit nav category names to max 2 words
NAV_TRUNC_JS = '''
          {{navItems.map(cat => {{
            const words = cat.replace(/-/g, ' ').split(' ');
            const display = words.length > 2 ? words.slice(0, 2).join(' ') : cat.replace(/-/g, ' ');
            return (
              <a href={{`/category/${{cat}}`}} class="px-3 py-2 text-sm font-medium rounded-lg hover:bg-[var(--color-bg-alt)] transition-colors truncate max-w-[140px] inline-block" title={{cat.replace(/-/g, ' ')}}>{{display.replace(/\\b\\w/g, l => l.toUpperCase())}}</a>
            );
          }})}}
'''

# 1. Update BaseLayout.astro to truncate nav categories
for site in SITES:
    f = NETWORK / "output" / "sites" / site / "src" / "layouts" / "BaseLayout.astro"
    if not f.exists():
        continue
    content = f.read_text()
    original = content

    # Update desktop nav items map to truncate
    old_desktop = '''        <div class="hidden md:flex items-center gap-1">
          <a href="/" class="px-3 py-2 text-sm font-medium rounded-lg hover:bg-[var(--color-bg-alt)] transition-colors">Home</a>
          {navItems.map(cat => (
            <a href={`/category/${cat}`} class="px-3 py-2 text-sm font-medium rounded-lg hover:bg-[var(--color-bg-alt)] transition-colors">{cat.replace(/-/g, ' ').replace(/\\b\\w/g, (l: string) => l.toUpperCase())}</a>
          ))}
        </div>'''
    new_desktop = '''        <div class="hidden md:flex items-center gap-1">
          <a href="/" class="px-3 py-2 text-sm font-medium rounded-lg hover:bg-[var(--color-bg-alt)] transition-colors">Home</a>
          {navItems.slice(0, 5).map(cat => {
            const words = cat.replace(/-/g, ' ').split(' ');
            const display = words.length > 2 ? words.slice(0, 2).join(' ') : cat.replace(/-/g, ' ');
            return (
              <a href={`/category/${cat}`} class="px-3 py-2 text-sm font-medium rounded-lg hover:bg-[var(--color-bg-alt)] transition-colors truncate max-w-[140px]" title={cat.replace(/-/g, ' ')}>{display.replace(/\\b\\w/g, (l: string) => l.toUpperCase())}</a>
            );
          })}
        </div>'''
    if old_desktop in content:
        content = content.replace(old_desktop, new_desktop)
    else:
        # Try simpler pattern
        old_simple = '{navItems.map(cat => (\n            <a href={`/category/${cat}`} class="px-3 py-2 text-sm font-medium rounded-lg hover:bg-[var(--color-bg-alt)] transition-colors">{cat.replace(/-/g, \' \').replace(/\\b\\w/g, (l: string) => l.toUpperCase())}</a>\n          ))}'
        new_simple = '''{navItems.slice(0, 5).map(cat => {
            const words = cat.replace(/-/g, ' ').split(' ');
            const display = words.length > 2 ? words.slice(0, 2).join(' ') : cat.replace(/-/g, ' ');
            return (
              <a href={`/category/${cat}`} class="px-3 py-2 text-sm font-medium rounded-lg hover:bg-[var(--color-bg-alt)] transition-colors truncate max-w-[140px]" title={cat.replace(/-/g, ' ')}>{display.replace(/\\b\\w/g, (l: string) => l.toUpperCase())}</a>
            );
          })}'''
        content = content.replace(old_simple, new_simple)

    # Also fix mobile nav same way
    if 'navItems.map(cat =>' in content and 'slice(0, 5)' not in content:
        # Mobile nav block - simpler approach
        content = re.sub(
            r'(\{)navItems\.map\(cat => \(\s*\n\s*<a href=\{`/category/\$\{cat\}`\}[^}]+\}\s*\n\s*\)\)\}',
            r'\1navItems.slice(0, 5).map(cat => {\n            const words = cat.replace(/-/g, \' \').split(\' \');\n            const display = words.length > 2 ? words.slice(0, 2).join(\' \') : cat.replace(/-/g, \' \');\n            return (\n              <a href={`/category/${cat}`} class="px-3 py-2 text-sm font-medium rounded-lg hover:bg-[var(--color-bg-alt)] transition-colors truncate" title={cat.replace(/-/g, \' \')}>{display.replace(/\\b\\w/g, (l: string) => l.toUpperCase())}</a>\n            );\n          })}',
            content
        )

    # Fix footer nav too
    if 'navItems.map(cat =>' in content:
        content = re.sub(
            r'\{navItems\.map\(cat => \(\s*\n\s*<li><a href=\{`/category/\$\{cat\}`\}[^}]+\}</a></li>\s*\n\s*\)\)\}',
            r'{navItems.slice(0, 6).map(cat => {\n            const words = cat.replace(/-/g, \' \').split(\' \');\n            const display = words.length > 2 ? words.slice(0, 2).join(\' \') : cat.replace(/-/g, \' \');\n            return (\n              <li><a href={`/category/${cat}`} class="text-[var(--color-text-muted)] hover:text-[var(--color-primary)] transition-colors truncate inline-block max-w-[180px]" title={cat.replace(/-/g, \' \')}>{display.replace(/\\b\\w/g, (l: string) => l.toUpperCase())}</a></li>\n            );\n          })}',
            content
        )

    if content != original:
        f.write_text(content)
        print(f"✅ {site}: nav truncated to first 2 words")

# 2. Fix breadcrumb truncation in [slug].astro
for site in SITES:
    f = NETWORK / "output" / "sites" / site / "src" / "pages" / "[slug].astro"
    if not f.exists():
        continue
    content = f.read_text()
    if 'truncate max-w-[140px]' in content and 'line-clamp-2' not in content:
        # Wrap last breadcrumb differently
        old = '<li class="text-[var(--color-text)] font-medium truncate max-w-[200px]">{article.title}</li>'
        new = '<li class="text-[var(--color-text)] font-medium line-clamp-1 break-words" style="max-width:60vw">{article.title}</li>'
        if old in content:
            content = content.replace(old, new)
            f.write_text(content)
            print(f"✅ {site}: breadcrumb last item fix")
