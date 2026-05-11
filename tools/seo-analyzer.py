#!/usr/bin/env python3
"""
Python SEO Analyzer for PennyPress
Analyzes generated content for SEO quality metrics.
Usage: python3 seo-analyzer.py <article.md> [article2.md ...]
       python3 seo-analyzer.py --dir <content-dir>
"""

import sys
import os
import re
import glob
from pathlib import Path

def analyze_article(filepath):
    """Analyze a single article for SEO quality."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    results = {
        'file': os.path.basename(filepath),
        'word_count': len(re.findall(r'\w+', content)),
        'issues': [],
        'warnings': [],
        'score': 100
    }
    
    # Extract frontmatter
    fm_match = re.search(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    frontmatter = fm_match.group(1) if fm_match else ''
    body = re.sub(r'^---\n.*?\n---\n', '', content, count=1, flags=re.DOTALL)
    
    # 1. Meta description length (ideal: 150-160)
    desc_match = re.search(r'description:\s*["\']?([^"\'\n]+)', frontmatter)
    if desc_match:
        desc_len = len(desc_match.group(1))
        if desc_len < 120:
            results['warnings'].append(f"Meta description too short ({desc_len} chars, ideal: 150-160)")
            results['score'] -= 5
        elif desc_len > 160:
            results['issues'].append(f"Meta description too long ({desc_len} chars, ideal: 150-160)")
            results['score'] -= 10
        else:
            results['warnings'].append(f"Meta description OK ({desc_len} chars)")
    else:
        results['issues'].append("Missing meta description in frontmatter")
        results['score'] -= 15
    
    # 2. Title presence
    h1_match = re.search(r'^# (.+)', body, re.MULTILINE)
    if h1_match:
        title = h1_match.group(1).strip()
        results['title'] = title[:80]
        if len(title) < 30:
            results['issues'].append(f"Title too short ({len(title)} chars)")
            results['score'] -= 5
        elif len(title) > 70:
            results['warnings'].append(f"Title long ({len(title)} chars), may be truncated in SERP")
        else:
            results['warnings'].append(f"Title OK ({len(title)} chars)")
    else:
        results['issues'].append("Missing H1 title")
        results['score'] -= 15
    
    # 3. Heading hierarchy (H2/H3)
    h2_count = len(re.findall(r'^## ', body, re.MULTILINE))
    h3_count = len(re.findall(r'^### ', body, re.MULTILINE))
    results['h2_count'] = h2_count
    results['h3_count'] = h3_count
    if h2_count < 3:
        results['warnings'].append(f"Few H2 sections ({h2_count}, ideal: 4-8)")
        results['score'] -= 5
    if h3_count < 1:
        results['warnings'].append("No H3 subsections (consider adding for depth)")
        results['score'] -= 3
    
    # 4. Internal link placeholders
    link_count = len(re.findall(r'\[LINK:', body))
    results['internal_links'] = link_count
    if link_count < 2:
        results['warnings'].append(f"Few internal links ({link_count}, ideal: 3-5)")
        results['score'] -= 5
    
    # 5. FAQ section
    faq_match = re.search(r'## .*FAQ', body, re.IGNORECASE)
    q_count = len(re.findall(r'^###? .*\?', body, re.MULTILINE))
    results['faq_count'] = q_count
    if q_count < 5:
        results['warnings'].append(f"FAQ section weak ({q_count} questions, ideal: 5-10)")
        results['score'] -= 5
    if not faq_match and q_count < 3:
        results['warnings'].append("No FAQ section detected")
        results['score'] -= 5
    
    # 6. Word count
    if results['word_count'] < 800:
        results['issues'].append(f"Word count very low ({results['word_count']}, ideal: 1500+)")
        results['score'] -= 20
    elif results['word_count'] < 1500:
        results['warnings'].append(f"Word count low ({results['word_count']}, ideal: 1500+)")
        results['score'] -= 5
    else:
        pass  # OK
    
    # 7. Reading level estimate (simple Flesch-based heuristic)
    sentences = len(re.findall(r'[.!?]+', body))
    if sentences > 0:
        avg_sentence_len = results['word_count'] / sentences
        if avg_sentence_len > 30:
            results['warnings'].append(f"Sentences very long (avg {avg_sentence_len:.0f} words), hard to read")
            results['score'] -= 3
    
    # 8. Bold/key term usage
    bold_count = len(re.findall(r'\*\*[^*]+\*\*', body))
    if bold_count < 3:
        results['warnings'].append(f"Few bold key terms ({bold_count}, consider adding more for scannability)")
        results['score'] -= 2
    
    # 9. List usage
    list_items = len(re.findall(r'^\s*[-*+]\s', body, re.MULTILINE))
    if list_items < 3:
        results['warnings'].append(f"Few bullet lists ({list_items}), consider adding for scannability)")
        results['score'] -= 2
    
    # 10. Table presence
    table_count = len(re.findall(r'\|.*\|', body))
    if table_count > 0:
        results['warnings'].append(f"Tables found ({table_count}), good for comparisons")
    else:
        results['warnings'].append("No tables found (add comparison tables for better engagement)")
        results['score'] -= 2
    
    results['score'] = max(0, results['score'])
    return results

def print_report(results):
    score = results['score']
    score_bar = '█' * (score // 10) + '░' * (10 - score // 10)
    print(f"\n{'='*60}")
    print(f"📄 {results['file']}")
    print(f"{'='*60}")
    print(f"  Score: {score}/100 {score_bar}")
    print(f"  Words: {results['word_count']:,} | H2: {results.get('h2_count',0)} | H3: {results.get('h3_count',0)} | Links: {results.get('internal_links',0)} | FAQs: {results.get('faq_count',0)}")
    if 'title' in results:
        print(f"  Title: {results['title']}")
    if results['issues']:
        print(f"\n  ❌ ISSUES:")
        for issue in results['issues']:
            print(f"     • {issue}")
    if results['warnings']:
        print(f"\n  ⚠️ WARNINGS:")
        for warn in results['warnings']:
            print(f"     • {warn}")
    if not results['issues'] and not results['warnings']:
        print(f"\n  ✅ All checks passed!")

def main():
    files = []
    
    if '--dir' in sys.argv:
        idx = sys.argv.index('--dir')
        dir_path = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else '.'
        files = glob.glob(f"{dir_path}/*.md")
    else:
        files = [f for f in sys.argv[1:] if os.path.exists(f)]
    
    if not files:
        print(__doc__)
        sys.exit(1)
    
    print(f"Analyzing {len(files)} article(s)...")
    
    total_score = 0
    for filepath in sorted(files):
        results = analyze_article(filepath)
        print_report(results)
        total_score += results['score']
    
    avg_score = total_score / len(files)
    print(f"\n{'='*60}")
    print(f"📊 OVERALL SEO SCORE: {avg_score:.1f}/100 ({len(files)} articles)")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
