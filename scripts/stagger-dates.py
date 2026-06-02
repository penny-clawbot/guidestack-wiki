#!/usr/bin/env python3
"""Stagger article dates for SEO freshness signals."""
import os, sys, re, argparse
from datetime import datetime, timedelta
parser = argparse.ArgumentParser()
parser.add_argument('site_dir')
parser.add_argument('--start', default='2026-01-15')
parser.add_argument('--interval', type=int, default=3)
args = parser.parse_args()
content_dir = os.path.join(args.site_dir, 'src/content/articles')
if not os.path.exists(content_dir):
    print(f'No content dir: {content_dir}'); sys.exit(1)
files = sorted([f for f in os.listdir(content_dir) if f.endswith('.md')])
start_date = datetime.strptime(args.start, '%Y-%m-%d')
updated = 0
for i, file in enumerate(files):
    filepath = os.path.join(content_dir, file)
    with open(filepath, 'r') as f: content = f.read()
    new_date = (start_date + timedelta(days=i * args.interval)).strftime('%Y-%m-%d')
    new_content = re.sub(r'date:\s*["\']\d{4}-\d{2}-\d{2}["\']', f'date: "{new_date}"', content)
    if new_content != content:
        with open(filepath, 'w') as f: f.write(new_content)
        updated += 1
print(f'Staggered {updated}/{len(files)} dates from {args.start} (every {args.interval} days)')
