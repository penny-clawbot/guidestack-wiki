#!/usr/bin/env python3
"""Validate article content quality at build time.
Usage: validate-content.py <site-dir> [--min-score 70]
Checks: alt text, word count, FAQ presence, heading structure, data points.
"""
import os, sys, re, json, argparse

parser = argparse.ArgumentParser()
parser.add_argument('site_dir')
parser.add_argument('--min-score', type=int, default=70)
parser.add_argument('--fix', action='store_true', help='Auto-fix what can be fixed')
args = parser.parse_args()

content_dir = args.site_dir
if not os.path.exists(content_dir):
    print(f'No content dir: {content_dir}'); sys.exit(1)

results = []
for file in sorted(os.listdir(content_dir)):
    if not file.endswith('.md'): continue
    filepath = os.path.join(content_dir, file)
    with open(filepath, 'r') as f:
        content = f.read()
    
    issues = []
    score = 100
    
    # Check images without alt text
    img_no_alt = re.findall(r'!\[\s*\]\([^)]+\)', content)
    if img_no_alt:
        issues.append(f'{len(img_no_alt)} image(s) missing alt text')
        score -= 5 * len(img_no_alt)
        if args.fix:
            # Can't auto-fix alt text meaningfully
            pass
    
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
    
    # Check for data points (numbers, percentages, dollar amounts)
    data_points = len(re.findall(r'\$[\d,]+|\d+\.?\d*%|\d{4,}', body))
    if data_points < 3:
        issues.append(f'Only {data_points} data points (minimum 3)')
        score -= 10
    
    # Check for images at all
    images = re.findall(r'!\[.*?\]\([^)]+\)', content)
    if len(images) == 0:
        issues.append('No images')
        score -= 5
    
    # === GEO (Generative Engine Optimization) Checks ===
    
    # Check: First 150 words should contain a direct answer (not just intro fluff)
    first_150 = ' '.join(body.split()[:150])
    has_numbers_early = bool(re.search(r'\$[\d,]+|\d+\.?\d*%|\d{4,}', first_150))
    has_definition_early = bool(re.search(r'(?:is |are |means |refers to |can be defined as )', first_150.lower()))
    if not has_numbers_early and not has_definition_early:
        issues.append('GEO: No direct answer/data in first 150 words — AI engines extract from opening paragraphs')
        score -= 5
    
    # Check: At least one table (markdown table)
    has_table = bool(re.search(r'\|.+:.+\|', body))
    if not has_table:
        issues.append('GEO: No data table — tables are the most-extracted format by AI engines')
        score -= 5
    
    # Check: Question-style H2 headings ("How to...", "What is...", "Why...")
    question_h2s = len(re.findall(r'^## (?:How|What|Why|When|Where|Can|Do|Is|Should|Which|How much|How many)', body, re.MULTILINE | re.IGNORECASE))
    if question_h2s == 0:
        issues.append('GEO: No question-style H2 headings — use "How to...", "What is..." format')
        score -= 5
    
    # Check: Numbered lists (how-to steps)
    has_numbered_list = bool(re.search(r'^1\. ', body, re.MULTILINE))
    if not has_numbered_list and words > 1500:
        issues.append('GEO: No numbered lists — step-by-step content favored by AI')
        score -= 3
    
    # Check: Cited sources (parenthetical citations, "according to", "source:")
    has_citations = bool(re.search(r'(?:according to|source:|\(source\)|\(\d{4}\)|study|research|report|survey)', body, re.IGNORECASE))
    if not has_citations:
        issues.append('GEO: No cited sources — AI prefers content with verifiable data')
        score -= 5
    
    # Check: Comparison content ("vs", "compared to", "better than")
    has_comparison = bool(re.search(r'(?: vs\.?|compared to|better than|versus|difference between)', body, re.IGNORECASE))
    if has_comparison:
        score += 3  # Bonus for comparison content
    
    score = min(100, score)
    
    score = max(0, score)
    results.append({'file': file, 'score': score, 'issues': issues, 'words': words})

# Sort by score
results.sort(key=lambda x: x['score'])

# Output
passed = sum(1 for r in results if r['score'] >= args.min_score)
failed = sum(1 for r in results if r['score'] < args.min_score)

print(f'\n📋 Content Validation: {passed} passed, {failed} failed (min score: {args.min_score})')
print(f'   Total articles: {len(results)}')

if failed > 0:
    print(f'\n⚠️  Articles below threshold:')
    for r in results:
        if r['score'] < args.min_score:
            print(f'   [{r["score"]}/100] {r["file"]}')
            for issue in r['issues']:
                print(f'      - {issue}')

print(f'\n✅ Articles passing:')
for r in results:
    if r['score'] >= args.min_score:
        print(f'   [{r["score"]}/100] {r["file"]}')

sys.exit(0 if failed == 0 else 1)
