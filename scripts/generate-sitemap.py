#!/usr/bin/env python3
"""Generate sitemap.xml from articles in the content directory."""
import os, sys, json, re
from datetime import datetime

site_dir = sys.argv[1] if len(sys.argv) > 1 else '/Users/penny/Documents/Penny/pseo-network/output/sites/budget-travel-tips'
content_dir = os.path.join(site_dir, 'src/content/articles')
config_path = os.path.join(site_dir, 'site-config.json')
output_path = os.path.join(site_dir, 'dist/sitemap.xml')

with open(config_path) as f:
    config = json.load(f)
domain = config.get('domain', 'example.com')
site_url = f'https://{domain}'

categories = set()
articles = []
if os.path.exists(content_dir):
    for file in sorted(os.listdir(content_dir)):
        if not file.endswith('.md'): continue
        content = open(os.path.join(content_dir, file)).read()
        dm = re.search(r'date:\s*["\'](.+?)["\']', content)
        cm = re.search(r'category:\s*["\'](.+?)["\']', content)
        slug = re.sub(r'^\d{4}-\d{2}-\d{2}-(ai-)?', '', file.replace('.md', ''))
        date = dm.group(1) if dm else datetime.now().strftime('%Y-%m-%d')
        if cm: categories.add(cm.group(1))
        articles.append({'slug': slug, 'date': date})

xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
xml += f'  <url><loc>{site_url}</loc><changefreq>daily</changefreq><priority>1.0</priority></url>\n'
for page in ['about', 'privacy-policy', 'terms', 'contact']:
    xml += f'  <url><loc>{site_url}/{page}</loc><changefreq>monthly</changefreq><priority>0.5</priority></url>\n'
for cat in sorted(categories):
    xml += f'  <url><loc>{site_url}/category/{cat}</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>\n'
for a in articles:
    xml += f'  <url><loc>{site_url}/{a["slug"]}</loc><lastmod>{a["date"]}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>\n'
xml += '</urlset>'

os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w') as f:
    f.write(xml)
total = len(articles) + 1 + 4 + len(categories)
print(f'Generated sitemap with {total} URLs -> {output_path}')
