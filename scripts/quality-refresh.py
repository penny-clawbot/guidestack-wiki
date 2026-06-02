#!/usr/bin/env python3
"""Quality Refresh — Regenerate failing articles using current Writer template.
Reads article paths from validate-content.py output, regenerates using writer.py.
Usage: python3 quality-refresh.py <site-name> [--min-score 70] [--dry-run]
"""
import os, sys, re, glob, argparse

PROJECT_DIR = "/Users/penny/Documents/Penny/pseo-network"
CONTENT_DIR = f"{PROJECT_DIR}/data/content"
sys.path.insert(0, PROJECT_DIR)
from writer import generate_article

def score_article(filepath):
    """Replicate validate-content.py scoring logic. Returns (score, issues)."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    issues = []
    score = 100
    
    # Check images without alt text
    img_no_alt = re.findall(r'!\[\s*\]\([^)]+\)', content)
    if img_no_alt:
        issues.append(f'{len(img_no_alt)} image(s) missing alt text')
        score -= 5 * len(img_no_alt)
    
    # Check word count
    body = re.sub(r'^---[\s\S]*?---', '', content).strip()
    words = len(body.split())
    if words < 1500:
        issues.append(f'Too short ({words} words, minimum 1500)')
        score -= 15
    elif words < 2000:
        issues.append(f'Could be longer ({words} words)')
        score -= 5
    
    # Check FAQ section
    if not re.search(r'#.*(?:FAQ|Frequently Asked|Common Questions)', content, re.IGNORECASE):
        issues.append('No FAQ section')
        score -= 10
    
    # Check heading structure (should have H2s)
    h2_count = len(re.findall(r'^## ', body, re.MULTILINE))
    if h2_count < 3:
        issues.append(f'Only {h2_count} H2 sections (minimum 3)')
        score -= 10
    
    # Check for data points
    data_points = len(re.findall(r'\$[\d,]+|\d+\.?\d*%|\d{4,}', body))
    if data_points < 3:
        issues.append(f'Only {data_points} data points (minimum 3)')
        score -= 10
    
    # Check for images at all
    images = re.findall(r'!\[.*?\]\([^)]+\)', content)
    if len(images) == 0:
        issues.append('No images')
        score -= 5
    
    # GEO: First 150 words should contain direct answer
    first_150 = ' '.join(body.split()[:150])
    has_numbers_early = bool(re.search(r'\$[\d,]+|\d+\.?\d*%|\d{4,}', first_150))
    has_definition_early = bool(re.search(r'(?:is |are |means |refers to |can be defined as )', first_150.lower()))
    if not has_numbers_early and not has_definition_early:
        issues.append('GEO: No direct answer/data in first 150 words')
        score -= 5
    
    # GEO: Check for table
    if not re.search(r'\|.*\|.*\|', content):
        issues.append('GEO: No markdown table')
        score -= 5
    
    return max(0, score), issues


def extract_article_info(filepath):
    """Extract title, article_type from frontmatter."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    fm_match = re.match(r'^---\n([\s\S]*?)\n---\n', content)
    if not fm_match:
        # Try to extract title from first H1
        h1 = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = h1.group(1).strip() if h1 else os.path.basename(filepath)
        return title, "standard", content
    
    fm = fm_match.group(1)
    title_match = re.search(r'title:\s*["\']?(.+?)["\']?\s*$', fm, re.MULTILINE)
    type_match = re.search(r'type:\s*["\']?(.+?)["\']?\s*$', fm, re.MULTILINE)
    category_match = re.search(r'category:\s*["\']?(.+?)["\']?\s*$', fm, re.MULTILINE)
    
    title = title_match.group(1).strip() if title_match else "Untitled"
    article_type = type_match.group(1).strip() if type_match else "standard"
    category = category_match.group(1).strip() if category_match else ""
    
    return title, article_type, category


def refresh_article(filepath, min_score, dry_run=False):
    """Score article, regenerate if below threshold."""
    score, issues = score_article(filepath)
    
    if score >= min_score:
        return "pass", score, []
    
    title, article_type, category = extract_article_info(filepath)
    
    if dry_run:
        return "would_regenerate", score, issues
    
    print(f"  🔄 Regenerating ({score}/100): {title}")
    print(f"     Issues: {', '.join(issues[:3])}")
    
    try:
        new_content = generate_article(
            topic=title,
            article_type=article_type,
            target_words=800,
            niche=category
        )
        
        # Preserve original frontmatter
        with open(filepath, 'r') as f:
            original = f.read()
        
        fm_match = re.match(r'^---\n([\s\S]*?)\n---\n', original)
        frontmatter = fm_match.group(0) if fm_match else ""
        
        # Write back with original frontmatter + new body
        with open(filepath, 'w') as f:
            if frontmatter:
                f.write(frontmatter)
            f.write(new_content)
        
        # Re-score to verify
        new_score, new_issues = score_article(filepath)
        print(f"     ✅ New score: {new_score}/100")
        
        return "refreshed", new_score, new_issues
        
    except Exception as e:
        print(f"     ❌ Error: {e}")
        return "error", score, [str(e)]


def main():
    parser = argparse.ArgumentParser(description='Quality refresh for PSEO articles')
    parser.add_argument('site_name', help='Site name (e.g., defi-yield-guide)')
    parser.add_argument('--min-score', type=int, default=70)
    parser.add_argument('--dry-run', action='store_true', help='Show what would be regenerated without regenerating')
    parser.add_argument('--site-dir', help='Override content directory path')
    args = parser.parse_args()
    
    site_dir = args.site_dir or os.path.join(CONTENT_DIR, args.site_name)
    
    if not os.path.exists(site_dir):
        print(f"❌ Site directory not found: {site_dir}")
        sys.exit(1)
    
    articles = sorted(glob.glob(os.path.join(site_dir, "*.md")))
    if not articles:
        print(f"❌ No .md articles found in {site_dir}")
        sys.exit(1)
    
    print(f"\n🔍 Quality Refresh: {args.site_name}")
    print(f"   Min score: {args.min_score}")
    print(f"   Articles: {len(articles)}")
    print(f"   Mode: {'DRY RUN' if args.dry_run else 'LIVE'}\n")
    
    results = {"pass": 0, "refreshed": 0, "error": 0, "would_regenerate": 0}
    failed_details = []
    
    for i, filepath in enumerate(articles, 1):
        fname = os.path.basename(filepath)
        status, score, issues = refresh_article(filepath, args.min_score, args.dry_run)
        results[status] = results.get(status, 0) + 1
        
        if status in ("would_regenerate", "error"):
            failed_details.append((fname, score, issues))
        
        if i % 10 == 0:
            print(f"  ... {i}/{len(articles)} processed")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Results for {args.site_name} (min-score {args.min_score}):")
    print(f"  ✅ Pass:        {results.get('pass', 0)}")
    print(f"  🔄 Refreshed:   {results.get('refreshed', 0)}")
    print(f"  ❌ Error:       {results.get('error', 0)}")
    if args.dry_run:
        print(f"  ⚠️  Would regen: {results.get('would_regenerate', 0)}")
    
    if failed_details:
        print(f"\n⚠️  Articles needing attention:")
        for fname, score, issues in failed_details[:10]:
            print(f"  - {fname} (score: {score})")
            for issue in issues[:2]:
                print(f"      → {issue}")
    
    print(f"\n{'='*50}")
    total_good = results.get('pass', 0) + results.get('refreshed', 0)
    pct = total_good / len(articles) * 100 if articles else 0
    print(f"Quality rate: {pct:.1f}% ({total_good}/{len(articles)} passing)")


if __name__ == '__main__':
    main()