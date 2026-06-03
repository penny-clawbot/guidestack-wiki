#!/usr/bin/env python3
"""
Content-level fixes for PSEO articles:
1. Date references (2024 → 2026) in body, keep slug intact
2. Fabricated statistics — replace with generic language
3. Truncation artifacts — detect and append closing paragraph
4. Add real images via Picsum (free, no API key, deterministic by seed)
5. Remove unprocessed [LINK: ...] template markers

Usage: python3 fix-content-issues.py [--dry-run] [--site SITE]
"""
import os
import re
import sys
import glob
import argparse
from pathlib import Path

CONTENT_DIR = Path("/Users/penny/Documents/Penny/pseo-network/data/content")
SITES = [
    "budget-travel-tips", "bitcoin-beginners", "crypto-investing-guide",
    "crypto-trading-strategies", "defi-yield-guide", "personal-finance-tips",
    "ai-tools-hub", "smart-emergency-fund",
]

# ============ 1. DATE FIXES ============
def fix_dates(content: str, slug: str) -> tuple[str, int]:
    """Update 2024 references in body to 2026, leave slug intact. Preserves case."""
    fixes = 0
    
    # Use re.sub with case-preserving replacement
    def replace_year(m):
        # Keep any trailing text in its original case
        return "2026" + m.group(1)
    
    # Pattern: \b2024(\s+...). The (.*?) captures the rest of the line
    # We capture space + following word to preserve case
    patterns_with_case = [
        # Format: (pattern, replacement_callback)
        # Specific phrases that need exact replacement
        (r'\bComplete 2024 Guide\b', 'Complete 2026 Guide'),
        (r'\bComplete 2024 guide\b', 'Complete 2026 guide'),
        (r'\bComprehensive 2024 Guide\b', 'Comprehensive 2026 Guide'),
        (r'\bComprehensive 2024 guide\b', 'Comprehensive 2026 guide'),
        (r'\bUltimate 2024 Guide\b', 'Ultimate 2026 Guide'),
        (r'\bUltimate 2024 guide\b', 'Ultimate 2026 guide'),
        (r'\b2024 and beyond\b', '2026 and beyond'),
        (r'\b2024 edition\b', '2026 edition'),
        (r'\bedition of 2024\b', 'edition of 2026'),
        # Year with following word - preserve the following word's case
        (r'\b2024\s+([A-Z][a-z]+)\b', lambda m: f'2026 {m.group(1)}'),  # 2024 Guide -> 2026 Guide
        (r'\b2024\s+([a-z]+)\b', lambda m: f'2026 {m.group(1)}'),  # 2024 guide -> 2026 guide
        # Common phrases
        (r'\bin 2024\b', 'in 2026'),
        (r'\bfor 2024\b', 'for 2026'),
        (r'\bof 2024\b', 'of 2026'),
        (r'\bduring 2024\b', 'during 2026'),
        (r'\bsince 2024\b', 'since 2026'),
    ]
    
    for pat, repl in patterns_with_case:
        before_matches = re.findall(pat, content)
        before_count = len(before_matches)
        if before_count > 0:
            content = re.sub(pat, repl, content)
            after_count = len(re.findall(pat, content))
            fixes += (before_count - after_count)
    
    return content, fixes

# ============ 2. FABRICATED STATS FIX ============
def fix_fabricated_stats(content: str) -> tuple[str, int]:
    """Replace hallucinated statistics with generic language."""
    fixes = 0
    
    patterns = [
        # "According to a YYYY [X] survey, N%..."
        (r'According to a 202[0-9] [A-Za-z ]+(?:survey|report|study|analysis|review),\s*\d+%\s*of\s+[A-Za-z\s-]+reported\s+[A-Za-z\s.,]+',
         'Most people who plan carefully find this approach delivers strong results'),
        # "a 2025 travel survey, 78% of budget-conscious travelers reported"
        (r'According to a \d{4} [A-Za-z ]+,\s*\d+%\s*of\s+[A-Za-z\s-]+(reported|said|experienced|felt)\s+[A-Za-z\s.,]+',
         'Most people who plan carefully find this approach delivers strong results'),
        # "A 2024 study found that..."  → "Research suggests..."
        (r'A 20\d{2} study (found|showed|revealed|indicated) that\s+',
         'Research suggests that '),
        # "In a 2024 survey of 1,000..." → remove the survey claim, keep actionable
        (r'In a 20\d{2} survey of [\d,]+\s+[A-Za-z\s]+,\s*', ''),
        # "Studies show that..." → "Evidence suggests..."
        (r'\bStudies show that\s+', 'Evidence suggests that '),
        # "Research indicates that..." with specific percentages — keep generic
        (r'Research (?:indicates|shows) that approximately \d+%\s+', 'Most people find that '),
        # "X% of [Y] reported/claimed..." with no source
        (r'\b\d{1,3}% of [A-Za-z\s-]+(reported|claimed|said)\s+that\s+[A-Za-z\s.,]+',
         'Many people in this category find this to be true in practice'),
    ]
    for pat, repl in patterns:
        new_content = re.sub(pat, repl, content, flags=re.IGNORECASE)
        n = len(re.findall(pat, content, re.IGNORECASE)) - len(re.findall(pat, new_content, re.IGNORECASE))
        if n > 0:
            fixes += n
            content = new_content
    
    return content, fixes

# ============ 3. TRUNCATION FIX ============
def fix_truncation(content: str, title: str) -> tuple[str, int]:
    """Detect truncation artifacts and append proper closing."""
    fixes = 0
    
    # Strip frontmatter
    body_match = re.match(r'^(---\n[\s\S]*?\n---\n)([\s\S]*)$', content)
    if not body_match:
        return content, 0
    frontmatter, body = body_match.groups()
    
    body = body.rstrip()
    
    # Detect truncation patterns
    truncated = False
    truncation_reason = None
    
    # Pattern 1: ends with unclosed bold **word (no closing **)
    if re.search(r'\*\*[A-Za-z][^*]*$', body):
        truncated = True
        truncation_reason = "unclosed_bold"
        # Close the bold
        body = re.sub(r'\*\*[A-Za-z][^*]*$', '', body).rstrip()
    
    # Pattern 2: ends with unclosed heading (## word)
    if re.search(r'#{1,6}\s+[A-Za-z][^#\n]*$', body) and not re.search(r'#{1,6}\s+[A-Za-z][^#\n]*\n\n*$', body):
        truncated = True
        truncation_reason = "unclosed_heading"
        body = re.sub(r'\n*#{1,6}\s+[A-Za-z][^#\n]*$', '', body).rstrip()
    
    # Pattern 3: ends mid-list (- word or * word with no period)
    if re.search(r'[-*]\s+\*\*[^*]+$', body):
        truncated = True
        truncation_reason = "unclosed_list"
        body = re.sub(r'\n*[-*]\s+\*\*[^*]+$', '', body).rstrip()
    
    # Pattern 4: ends mid-sentence (no terminal punctuation, last 50 chars)
    if not truncated and len(body) > 100:
        last_50 = body[-50:].strip()
        if last_50 and not re.search(r'[.!?\)\]"\'*]$', last_50):
            # Check if it looks like a complete thought that just lacks period
            if ' ' in last_50 and not last_50.endswith(' '):
                # Add period if missing
                body = body.rstrip() + '.'
                fixes += 1  # we added a period
    
    if truncated:
        # Add a proper closing paragraph
        closing = f"\n\n---\n\n*This guide is part of our comprehensive coverage of {title.lower()}. For more in-depth analysis, explore our related articles or subscribe for updates.*\n"
        body = body.rstrip() + closing
        fixes += 1
    
    content = frontmatter + body
    return content, fixes

# ============ 4. UNPROCESSED LINK MARKERS ============
def fix_link_markers(content: str) -> tuple[str, int]:
    """Remove [LINK: ...] template markers that are leaking into output."""
    fixes = 0
    # Remove [LINK: anything] markers
    new_content, n = re.subn(r'\s*\[LINK:\s*[^\]]+\]', '', content)
    if n > 0:
        fixes += n
        content = new_content
    return content, fixes

# ============ 5. ADD IMAGES ============
def add_images(content: str, slug: str) -> tuple[str, int]:
    """Insert 2 Picsum images with descriptive alt text if not already present.
    Uses deterministic seeds based on slug for consistency."""
    fixes = 0
    
    # Check if article already has images
    if re.search(r'!\[[^\]]*\]\([^)]+\)', content):
        return content, 0  # Already has images
    
    # Strip frontmatter
    body_match = re.match(r'^(---\n[\s\S]*?\n---\n)([\s\S]*)$', content)
    if not body_match:
        return content, 0
    frontmatter, body = body_match.groups()
    
    # Find first H2 to insert image after intro
    h2_match = re.search(r'\n(##\s+[^\n]+)\n', body)
    
    # Build image markdown - 2 images, hero + middle
    # Use slug-based seed for deterministic Picsum image
    slug_text = slug.replace("-", " ")
    hero_alt = "Hero image for " + slug_text
    mid_alt = "Illustration for " + slug_text
    hero_img = f"\n\n![{hero_alt}](https://picsum.photos/seed/{slug}-hero/1200/630)\n\n"
    mid_img = f"\n\n![{mid_alt}](https://picsum.photos/seed/{slug}-mid/1200/630)\n\n"
    
    if h2_match:
        # Insert hero after first H2
        insertion_point = h2_match.end()
        body = body[:insertion_point] + hero_img + body[insertion_point:]
        # Find second H2 for mid image
        h2_matches = list(re.finditer(r'\n(##\s+[^\n]+)\n', body))
        if len(h2_matches) >= 3:
            mid_point = h2_matches[2].end()
            body = body[:mid_point] + mid_img + body[mid_point:]
        fixes = 1 if hero_img else 0
        if len(h2_matches) >= 3:
            fixes = 2
    else:
        # No H2s, insert at start
        body = hero_img + body
    
    content = frontmatter + body
    return content, fixes

# ============ MAIN ============
def process_article(filepath: Path, dry_run: bool = False) -> dict:
    """Process a single article. Returns stats dict."""
    stats = {"dates": 0, "stats": 0, "truncation": 0, "links": 0, "images": 0}
    content = filepath.read_text()
    original = content
    
    # Extract title from frontmatter
    title_match = re.search(r'title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else filepath.stem
    
    # Extract slug
    slug = filepath.stem
    # Remove date prefix like 2026-05-10-ai- and trailing extensions
    slug = re.sub(r'^\d{4}-\d{2}-\d{2}-ai-?', '', slug)
    
    # Apply fixes in order
    content, stats["dates"] = fix_dates(content, slug)
    content, stats["stats"] = fix_fabricated_stats(content)
    content, stats["truncation"] = fix_truncation(content, title)
    content, stats["links"] = fix_link_markers(content)
    content, stats["images"] = add_images(content, slug)
    
    if content != original and not dry_run:
        filepath.write_text(content)
    
    return stats

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--site", help="Process only this site")
    args = parser.parse_args()
    
    sites = [args.site] if args.site else SITES
    
    grand_totals = {"dates": 0, "stats": 0, "truncation": 0, "links": 0, "images": 0, "articles": 0}
    
    for site in sites:
        site_dir = CONTENT_DIR / site
        if not site_dir.exists():
            print(f"❌ {site}: directory not found")
            continue
        
        articles = sorted(site_dir.glob("*.md"))
        print(f"\n--- {site} ({len(articles)} articles) ---")
        
        site_totals = {"dates": 0, "stats": 0, "truncation": 0, "links": 0, "images": 0}
        
        for f in articles:
            stats = process_article(f, dry_run=args.dry_run)
            for k in ["dates", "stats", "truncation", "links", "images"]:
                site_totals[k] += stats[k]
            site_totals["articles"] = site_totals.get("articles", 0) + 1
        
        print(f"  Dates fixed:       {site_totals['dates']}")
        print(f"  Stats removed:     {site_totals['stats']}")
        print(f"  Truncation fixed:  {site_totals['truncation']}")
        print(f"  Link markers:      {site_totals['links']}")
        print(f"  Images added:      {site_totals['images']}")
        
        for k in grand_totals:
            grand_totals[k] += site_totals[k]
    
    print("\n" + "=" * 60)
    print(f"GRAND TOTAL ({grand_totals['articles']} articles)")
    print(f"  Dates fixed:       {grand_totals['dates']}")
    print(f"  Fabricated stats:  {grand_totals['stats']}")
    print(f"  Truncation fixed:  {grand_totals['truncation']}")
    print(f"  Link markers:      {grand_totals['links']}")
    print(f"  Images added:      {grand_totals['images']}")
    print("=" * 60)
    if args.dry_run:
        print("(DRY RUN — no files modified)")

if __name__ == "__main__":
    main()
