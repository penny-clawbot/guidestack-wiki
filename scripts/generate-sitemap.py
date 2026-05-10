#!/usr/bin/env python3
"""Generate sitemap.xml from articles in the content directory."""
import os, sys, json, re
from datetime import datetime

site_dir = sys.argv[1] if len(sys.argv) > 1 else '/Users/penny/Documents/Penny/pseo-network/output/sites/budget-travel-tips'
content_dir = os.path.join(site_dir, 'src/content/articles')
config_path = os.path.join(site_dir, 'site-config.json')
output_path = os.path.join(site_dir, 'dist/sitemap.xml')

site_url = 'https://example.com'  # Replace when domain is set

with open(config_path) as f:
    config = json.load(f)

articles = []
if os.path.exists(content_dir):
    for file in sorted(os.listdir(content_dir)):
        if not file.endswith('.md'): continue
        content = open(os.path.join(content_dir, file)).read()
        dm = re.search(r'date:\s*["\'](.+?)["\']', content)
        slug = re.sub(r'^\d{4}-\d{2}-\d{2}-(ai-)?', '', file.replace('.md', ''))
        articles.append({'slug': slug, 'date': dm.group(1) if dm else datetime.now().strftime('%Y-%m-%d')})

xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
xml += f'  <url><loc>{site_url}</loc><changefreq>daily</changefreq><priority>1.0</priority></url>\n'
for a in articles:
    xml += f'  <url><loc>{site_url}/{a["slug"]}</loc><lastmod>{a["date"]}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>\n'
xml += '</urlset>'

os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w') as f:
    f.write(xml)
print(f'Generated sitemap with {len(articles) + 1} URLs → {output_path}')
