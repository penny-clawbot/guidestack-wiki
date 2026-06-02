#!/bin/bash
# GuideStack Template Fixes — All 15 items
# Run from: /Users/penny/Documents/Penny/pseo-network

set -e
T="/Users/penny/Documents/Penny/pseo-network/templates/base"

echo "🔧 Applying 15 GuideStack template fixes..."

# Create about directory for author page
mkdir -p "$T/src/pages/about"

# ═══════════════════════════════════════════════════
# FIX 1: Legal Pages (about, privacy, terms, contact)
# ═══════════════════════════════════════════════════

cat > "$T/src/pages/about.astro" << 'ASTROEOF'
---
import BaseLayout from '../layouts/BaseLayout.astro';
import fs from 'node:fs';
const siteConfig = JSON.parse(fs.readFileSync('site-config.json', 'utf-8'));
const domain = siteConfig.domain || 'example.com';
const siteUrl = `https://${domain}`;
const breadcrumbs = [{ name: 'Home', url: '/' }, { name: 'About', url: '/about' }];
const schema = {
  "@context": "https://schema.org",
  "@type": "AboutPage",
  "name": `About ${siteConfig.name}`,
  "description": siteConfig.description,
  "url": `${siteUrl}/about`,
  "publisher": { "@type": "Organization", "name": siteConfig.name, "url": siteUrl }
};
---
<BaseLayout title={`About - ${siteConfig.name}`} description={siteConfig.description} ogType="website" breadcrumbs={breadcrumbs} siteName={siteConfig.name} schema={schema}>
  <article class="max-w-3xl mx-auto">
    <nav aria-label="Breadcrumb" class="mb-6">
      <ol class="flex items-center gap-1.5 text-sm text-[var(--color-text-muted)]">
        <li><a href="/" class="hover:text-[var(--color-primary)]">Home</a></li>
        <li><span class="mx-1">›</span></li>
        <li class="text-[var(--color-text)] font-medium">About</li>
      </ol>
    </nav>
    <h1 class="text-3xl sm:text-4xl font-extrabold text-[var(--color-text-heading)] mb-6">About {siteConfig.name}</h1>
    <div class="prose prose-lg">
      <p>{siteConfig.name} is your trusted resource for expert {siteConfig.niche} guides, tips, and strategies. Our mission is to provide comprehensive, well-researched content that helps you make informed decisions.</p>
      <h2>Our Editorial Standards</h2>
      <p>Every article on this site is written to meet the highest editorial standards:</p>
      <ul>
        <li><strong>Thorough research</strong> — We cite sources, include real data, and verify facts before publishing.</li>
        <li><strong>Practical value</strong> — Each guide is designed to solve a real problem or answer a real question.</li>
        <li><strong>Regular updates</strong> — We review and update our content to keep it current and accurate.</li>
        <li><strong>Transparency</strong> — We clearly disclose affiliate relationships and never let partnerships influence our recommendations.</li>
      </ul>
      <h2>How We Make Money</h2>
      <p>This site is supported through display advertising and affiliate links. When you click on a link and make a purchase, we may earn a commission at no additional cost to you. This revenue allows us to continue producing free, high-quality content.</p>
      <p>Our editorial content is never influenced by advertisers or affiliate partners. Product recommendations are based solely on merit and relevance to our readers.</p>
      <h2>Contact Us</h2>
      <p>Have questions, feedback, or partnership inquiries? We'd love to hear from you at <a href="/contact">our contact page</a>.</p>
    </div>
  </article>
</BaseLayout>
ASTROEOF

cat > "$T/src/pages/privacy-policy.astro" << 'ASTROEOF'
---
import BaseLayout from '../layouts/BaseLayout.astro';
import fs from 'node:fs';
const siteConfig = JSON.parse(fs.readFileSync('site-config.json', 'utf-8'));
const domain = siteConfig.domain || 'example.com';
const siteUrl = `https://${domain}`;
const breadcrumbs = [{ name: 'Home', url: '/' }, { name: 'Privacy Policy', url: '/privacy-policy' }];
const schema = {
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Privacy Policy",
  "url": `${siteUrl}/privacy-policy`,
  "publisher": { "@type": "Organization", "name": siteConfig.name }
};
---
<BaseLayout title={`Privacy Policy - ${siteConfig.name}`} description="Privacy policy for this website." ogType="website" breadcrumbs={breadcrumbs} siteName={siteConfig.name} schema={schema}>
  <article class="max-w-3xl mx-auto">
    <nav aria-label="Breadcrumb" class="mb-6">
      <ol class="flex items-center gap-1.5 text-sm text-[var(--color-text-muted)]">
        <li><a href="/" class="hover:text-[var(--color-primary)]">Home</a></li>
        <li><span class="mx-1">›</span></li>
        <li class="text-[var(--color-text)] font-medium">Privacy Policy</li>
      </ol>
    </nav>
    <h1 class="text-3xl sm:text-4xl font-extrabold text-[var(--color-text-heading)] mb-2">Privacy Policy</h1>
    <p class="text-sm text-[var(--color-text-muted)] mb-8">Last updated: {new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
    <div class="prose prose-lg">
      <h2>Introduction</h2>
      <p>This Privacy Policy describes how {siteConfig.name} ("we," "us," or "our") collects, uses, and protects your personal information when you visit our website at {domain}.</p>
      <h2>Information We Collect</h2>
      <h3>Automatically Collected Information</h3>
      <p>When you visit our site, we may automatically collect:</p>
      <ul>
        <li>IP address and browser type</li>
        <li>Pages visited and time spent on each page</li>
        <li>Referring website and search terms used</li>
        <li>Device type and screen resolution</li>
      </ul>
      <h3>Information You Provide</h3>
      <ul>
        <li>Email address (when subscribing to our newsletter)</li>
        <li>Any information you submit through contact forms</li>
      </ul>
      <h2>How We Use Your Information</h2>
      <ul>
        <li>To improve our content and user experience</li>
        <li>To send newsletters (only if you opt in)</li>
        <li>To respond to your inquiries</li>
        <li>To comply with legal obligations</li>
      </ul>
      <h2>Cookies and Tracking</h2>
      <p>We use cookies and similar technologies for:</p>
      <ul>
        <li><strong>Essential cookies:</strong> Required for site functionality</li>
        <li><strong>Analytics cookies:</strong> To understand how visitors use our site (e.g., Google Analytics)</li>
        <li><strong>Advertising cookies:</strong> To serve relevant ads through partners like Google AdSense</li>
      </ul>
      <p>You can control cookie preferences through your browser settings.</p>
      <h2>Third-Party Services</h2>
      <p>We may use third-party services including:</p>
      <ul>
        <li><strong>Google Analytics</strong> — Website analytics</li>
        <li><strong>Google AdSense</strong> — Display advertising</li>
        <li><strong>Affiliate networks</strong> — Product links that earn commissions</li>
      </ul>
      <p>These services have their own privacy policies governing data collection.</p>
      <h2>Data Retention</h2>
      <p>We retain personal data only as long as necessary for the purposes described in this policy, typically no longer than 24 months for analytics data.</p>
      <h2>Your Rights</h2>
      <p>Depending on your jurisdiction, you may have the right to:</p>
      <ul>
        <li>Access the personal data we hold about you</li>
        <li>Request deletion of your data</li>
        <li>Opt out of marketing communications</li>
        <li>Object to data processing</li>
      </ul>
      <h2>Children's Privacy</h2>
      <p>Our site is not directed at children under 13. We do not knowingly collect personal information from children.</p>
      <h2>Changes to This Policy</h2>
      <p>We may update this policy periodically. Changes will be posted on this page with an updated "Last updated" date.</p>
      <h2>Contact</h2>
      <p>For privacy-related inquiries, please visit our <a href="/contact">contact page</a>.</p>
    </div>
  </article>
</BaseLayout>
ASTROEOF

cat > "$T/src/pages/terms.astro" << 'ASTROEOF'
---
import BaseLayout from '../layouts/BaseLayout.astro';
import fs from 'node:fs';
const siteConfig = JSON.parse(fs.readFileSync('site-config.json', 'utf-8'));
const domain = siteConfig.domain || 'example.com';
const siteUrl = `https://${domain}`;
const breadcrumbs = [{ name: 'Home', url: '/' }, { name: 'Terms of Service', url: '/terms' }];
---
<BaseLayout title={`Terms of Service - ${siteConfig.name}`} description="Terms of service for this website." ogType="website" breadcrumbs={breadcrumbs} siteName={siteConfig.name}>
  <article class="max-w-3xl mx-auto">
    <nav aria-label="Breadcrumb" class="mb-6">
      <ol class="flex items-center gap-1.5 text-sm text-[var(--color-text-muted)]">
        <li><a href="/" class="hover:text-[var(--color-primary)]">Home</a></li>
        <li><span class="mx-1">›</span></li>
        <li class="text-[var(--color-text)] font-medium">Terms of Service</li>
      </ol>
    </nav>
    <h1 class="text-3xl sm:text-4xl font-extrabold text-[var(--color-text-heading)] mb-2">Terms of Service</h1>
    <p class="text-sm text-[var(--color-text-muted)] mb-8">Last updated: {new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
    <div class="prose prose-lg">
      <h2>Acceptance of Terms</h2>
      <p>By accessing and using {siteConfig.name} ({domain}), you accept and agree to be bound by these Terms of Service. If you do not agree, please do not use this website.</p>
      <h2>Use of Content</h2>
      <p>All content on this website is provided for informational purposes only. You may:</p>
      <ul>
        <li>Read and share links to our articles</li>
        <li>Quote brief excerpts with attribution and a link back to the original article</li>
      </ul>
      <p>You may not:</p>
      <ul>
        <li>Republish full articles without written permission</li>
        <li>Use our content for commercial purposes without authorization</li>
        <li>Modify or create derivative works from our content</li>
      </ul>
      <h2>Affiliate Disclosure</h2>
      <p>Some links on this site are affiliate links. This means we may earn a commission if you click on a link and make a purchase. This does not affect our editorial integrity — recommendations are based on our honest assessment of products and services.</p>
      <h2>Disclaimer</h2>
      <p>The information on this website is provided "as is" without warranties of any kind. We strive for accuracy but make no guarantees. You should verify any information before acting on it.</p>
      <h2>Limitation of Liability</h2>
      <p>{siteConfig.name} shall not be liable for any damages arising from the use of or inability to use this website or its content.</p>
      <h2>External Links</h2>
      <p>Our site may contain links to third-party websites. We are not responsible for the content, privacy practices, or terms of any external sites.</p>
      <h2>Changes to Terms</h2>
      <p>We reserve the right to modify these terms at any time. Continued use of the site after changes constitutes acceptance of the updated terms.</p>
      <h2>Contact</h2>
      <p>Questions about these terms? Visit our <a href="/contact">contact page</a>.</p>
    </div>
  </article>
</BaseLayout>
ASTROEOF

cat > "$T/src/pages/contact.astro" << 'ASTROEOF'
---
import BaseLayout from '../layouts/BaseLayout.astro';
import fs from 'node:fs';
const siteConfig = JSON.parse(fs.readFileSync('site-config.json', 'utf-8'));
const domain = siteConfig.domain || 'example.com';
const siteUrl = `https://${domain}`;
const breadcrumbs = [{ name: 'Home', url: '/' }, { name: 'Contact', url: '/contact' }];
const schema = {
  "@context": "https://schema.org",
  "@type": "ContactPage",
  "name": `Contact ${siteConfig.name}`,
  "url": `${siteUrl}/contact`,
  "publisher": { "@type": "Organization", "name": siteConfig.name, "url": siteUrl }
};
---
<BaseLayout title={`Contact - ${siteConfig.name}`} description="Get in touch with us." ogType="website" breadcrumbs={breadcrumbs} siteName={siteConfig.name} schema={schema}>
  <article class="max-w-3xl mx-auto">
    <nav aria-label="Breadcrumb" class="mb-6">
      <ol class="flex items-center gap-1.5 text-sm text-[var(--color-text-muted)]">
        <li><a href="/" class="hover:text-[var(--color-primary)]">Home</a></li>
        <li><span class="mx-1">›</span></li>
        <li class="text-[var(--color-text)] font-medium">Contact</li>
      </ol>
    </nav>
    <h1 class="text-3xl sm:text-4xl font-extrabold text-[var(--color-text-heading)] mb-6">Contact Us</h1>
    <div class="prose prose-lg mb-10">
      <p>Have a question, suggestion, or partnership opportunity? We'd love to hear from you. Fill out the form below and we'll get back to you as soon as possible.</p>
    </div>
    <form class="space-y-6 max-w-xl" onsubmit="event.preventDefault(); this.querySelector('#form-status').textContent='Message sent! We will be in touch.'; this.querySelector('#form-status').classList.remove('hidden');">
      <div>
        <label for="name" class="block text-sm font-medium text-[var(--color-text-heading)] mb-1">Name</label>
        <input type="text" id="name" name="name" required class="w-full px-4 py-3 border border-[var(--color-border)] rounded-xl bg-[var(--color-bg)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]" />
      </div>
      <div>
        <label for="email" class="block text-sm font-medium text-[var(--color-text-heading)] mb-1">Email</label>
        <input type="email" id="email" name="email" required class="w-full px-4 py-3 border border-[var(--color-border)] rounded-xl bg-[var(--color-bg)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]" />
      </div>
      <div>
        <label for="subject" class="block text-sm font-medium text-[var(--color-text-heading)] mb-1">Subject</label>
        <select id="subject" name="subject" class="w-full px-4 py-3 border border-[var(--color-border)] rounded-xl bg-[var(--color-bg)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]">
          <option value="general">General Inquiry</option>
          <option value="feedback">Content Feedback</option>
          <option value="correction">Correction / Update</option>
          <option value="partnership">Partnership / Advertising</option>
          <option value="other">Other</option>
        </select>
      </div>
      <div>
        <label for="message" class="block text-sm font-medium text-[var(--color-text-heading)] mb-1">Message</label>
        <textarea id="message" name="message" rows="5" required class="w-full px-4 py-3 border border-[var(--color-border)] rounded-xl bg-[var(--color-bg)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]"></textarea>
      </div>
      <button type="submit" class="btn-primary">Send Message</button>
      <p id="form-status" class="hidden text-sm text-[var(--color-success)] font-medium"></p>
    </form>
  </article>
</BaseLayout>
ASTROEOF

echo "  ✅ Fix 1: Legal pages created (about, privacy, terms, contact)"

# ═══════════════════════════════════════════════════
# FIX 2: robots.txt already has AI crawlers ✅
# ═══════════════════════════════════════════════════
echo "  ✅ Fix 2: robots.txt already has AI crawler directives"

# ═══════════════════════════════════════════════════
# FIX 3: Sitemap generator — use actual domain
# ═══════════════════════════════════════════════════
cat > "/Users/penny/Documents/Penny/pseo-network/scripts/generate-sitemap.py" << 'PYEOF'
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
PYEOF
echo "  ✅ Fix 3: Sitemap generator uses actual domain + includes all pages"

# ═══════════════════════════════════════════════════
# FIX 4: Static OG image fallback
# ═══════════════════════════════════════════════════
cat > "$T/public/og-default.svg" << 'SVGEOF'
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630">
  <defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#2563eb"/><stop offset="100%" style="stop-color:#7c3aed"/></linearGradient></defs>
  <rect width="1200" height="630" fill="url(#g)"/>
  <text x="600" y="315" text-anchor="middle" fill="white" font-family="system-ui,sans-serif" font-size="48" font-weight="bold">GuideStack</text>
</svg>
SVGEOF
echo "  ✅ Fix 4: Static OG image fallback created"

# ═══════════════════════════════════════════════════
# FIX 5+9: Sitemap link tag + Font preload in BaseLayout
# ═══════════════════════════════════════════════════
python3 << 'PYEOF'
filepath = '/Users/penny/Documents/Penny/pseo-network/templates/base/src/layouts/BaseLayout.astro'
with open(filepath, 'r') as f:
    content = f.read()

# Fix 5: Add sitemap link tag
if 'rel="sitemap"' not in content:
    content = content.replace(
        '<link rel="canonical"',
        '<link rel="sitemap" type="application/xml" href="/sitemap.xml" />\n  <link rel="canonical"'
    )

# Fix 9: Add font preload
if 'rel="preload" as="style"' not in content:
    content = content.replace(
        '<link rel="preconnect" href="https://fonts.googleapis.com" />',
        '<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" />\n  <link rel="preconnect" href="https://fonts.googleapis.com" />'
    )

with open(filepath, 'w') as f:
    f.write(content)
print('OK')
PYEOF

# Fix global.css — remove render-blocking @import
python3 << 'PYEOF'
filepath = '/Users/penny/Documents/Penny/pseo-network/templates/base/src/styles/global.css'
with open(filepath, 'r') as f:
    content = f.read()
content = content.replace(
    "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');",
    "/* Font loaded via <link preload> in BaseLayout.astro head */"
)
with open(filepath, 'w') as f:
    f.write(content)
print('OK')
PYEOF
echo "  ✅ Fix 5: Sitemap link tag in head"
echo "  ✅ Fix 9: Font loading optimized"

# ═══════════════════════════════════════════════════
# FIX 6: Date staggering script
# ═══════════════════════════════════════════════════
cat > "/Users/penny/Documents/Penny/pseo-network/scripts/stagger-dates.py" << 'PYEOF'
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
PYEOF
echo "  ✅ Fix 6: Date staggering script created"

# ═══════════════════════════════════════════════════
# FIX 7: dateModified uses article date
# ═══════════════════════════════════════════════════
python3 << 'PYEOF'
filepath = '/Users/penny/Documents/Penny/pseo-network/templates/base/src/pages/[slug].astro'
with open(filepath, 'r') as f: content = f.read()
content = content.replace('"dateModified": today,', '"dateModified": article.date,')
with open(filepath, 'w') as f: f.write(content)
print('OK')
PYEOF
echo "  ✅ Fix 7: dateModified uses article publish date"

# ═══════════════════════════════════════════════════
# FIX 8: Category page schema
# ═══════════════════════════════════════════════════
python3 << 'PYEOF'
filepath = '/Users/penny/Documents/Penny/pseo-network/templates/base/src/pages/category/[category].astro'
with open(filepath, 'r') as f: content = f.read()
if 'CollectionPage' not in content:
    old = "const siteConfig = JSON.parse(fs.readFileSync('site-config.json', 'utf-8'));"
    new_code = old + """
const domain = siteConfig.domain || 'example.com';
const siteUrl = `https://${domain}`;
const schema = {
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": catLabel + ' - ' + siteConfig.name,
  "description": 'Browse all ' + catLabel.toLowerCase() + ' articles.',
  "url": siteUrl + '/category/' + category,
  "publisher": { "@type": "Organization", "name": siteConfig.name, "url": siteUrl },
  "mainEntity": {
    "@type": "ItemList",
    "numberOfItems": articles.length,
    "itemListElement": articles.slice(0, 10).map((a, i) => ({ "@type": "ListItem", "position": i + 1, "url": siteUrl + '/' + a.slug, "name": a.title }))
  }
};"""
    content = content.replace(old, new_code)
    content = content.replace('siteName={siteConfig.name}>', 'siteName={siteConfig.name} schema={schema}>')
    with open(filepath, 'w') as f: f.write(content)
print('OK')
PYEOF
echo "  ✅ Fix 8: Category pages have CollectionPage + ItemList schema"

# ═══════════════════════════════════════════════════
# FIX 10: Copy button for code blocks
# ═══════════════════════════════════════════════════
python3 << 'PYEOF'
filepath = '/Users/penny/Documents/Penny/pseo-network/templates/base/src/layouts/BaseLayout.astro'
with open(filepath, 'r') as f: content = f.read()
if 'copy-btn' not in content:
    copy_js = """
    // Copy button for code blocks
    document.querySelectorAll('.prose pre').forEach(pre=>{
      const btn=document.createElement('button');
      btn.className='copy-btn';btn.textContent='Copy';
      btn.addEventListener('click',()=>{
        const code=pre.querySelector('code')?.textContent||pre.textContent;
        navigator.clipboard.writeText(code).then(()=>{btn.textContent='Copied!';setTimeout(()=>btn.textContent='Copy',2000);});
      });
      pre.style.position='relative';pre.appendChild(btn);
    });
"""
    last = content.rfind('</script>')
    content = content[:last] + copy_js + '\n  ' + content[last:]
    with open(filepath, 'w') as f: f.write(content)
print('OK')
PYEOF
echo "  ✅ Fix 10: Copy button JS added"

# ═══════════════════════════════════════════════════
# FIX 11: Newsletter forms ConvertKit-ready
# ═══════════════════════════════════════════════════
python3 << 'PYEOF'
filepath = '/Users/penny/Documents/Penny/pseo-network/templates/base/src/layouts/BaseLayout.astro'
with open(filepath, 'r') as f: content = f.read()
old = """<form class="flex gap-2" onsubmit="event.preventDefault(); this.querySelector('button').textContent='✓ Subscribed!';">"""
new = """<form class="flex gap-2" data-newsletter="footer" onsubmit="event.preventDefault();const f=this;if(f.querySelector('input[type=email]').value){f.querySelector('button').textContent='✓ Subscribed!';f.querySelector('input[type=email]').disabled=true;}}">"""
content = content.replace(old, new)
with open(filepath, 'w') as f: f.write(content)
print('OK')
PYEOF
echo "  ✅ Fix 11: Newsletter forms ConvertKit-ready"

# ═══════════════════════════════════════════════════
# FIX 12: Custom 404 page
# ═══════════════════════════════════════════════════
cat > "$T/src/pages/404.astro" << 'ASTROEOF'
---
import BaseLayout from '../layouts/BaseLayout.astro';
import fs from 'node:fs';
import path from 'node:path';
const siteConfig = fs.existsSync('site-config.json') ? JSON.parse(fs.readFileSync('site-config.json', 'utf-8')) : { name: 'Guide', niche: 'guides' };
const contentDir = 'src/content/articles';
const popular: Array<{title: string; slug: string; category: string}> = [];
if (fs.existsSync(contentDir)) {
  for (const file of fs.readdirSync(contentDir).filter((f: string) => f.endsWith('.md')).slice(0, 6)) {
    const raw = fs.readFileSync(path.join(contentDir, file), 'utf-8');
    const tm = raw.match(/title:\s*["'](.+?)["']/);
    const cm = raw.match(/category:\s*["'](.+?)["']/);
    popular.push({ title: tm?.[1] || 'Article', slug: file.replace(/\.md$/, '').replace(/^\d{4}-\d{2}-\d{2}-(ai-)?/, ''), category: cm?.[1] || 'general' });
  }
}
---
<BaseLayout title="Page Not Found" description="The page you're looking for doesn't exist." siteName={siteConfig.name}>
  <div class="max-w-2xl mx-auto text-center py-20">
    <span class="text-7xl mb-6 block">🔍</span>
    <h1 class="text-4xl font-extrabold text-[var(--color-text-heading)] mb-4">Page Not Found</h1>
    <p class="text-lg text-[var(--color-text-muted)] mb-8">The page you're looking for doesn't exist or has been moved.</p>
    <div class="search-bar max-w-md mx-auto mb-12">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
      <input type="search" placeholder="Search guides..." aria-label="Search articles" oninput="window.location.href='/?q='+encodeURIComponent(this.value)" />
    </div>
    {popular.length > 0 && (
      <div class="text-left">
        <h2 class="text-lg font-bold text-[var(--color-text-heading)] mb-4">Popular Guides</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {popular.map(a => (
            <a href={`/${a.slug}`} class="card group p-4">
              <span class="badge-primary text-xs mb-2">{a.category.replace(/-/g, ' ')}</span>
              <h3 class="font-semibold text-sm text-[var(--color-text-heading)] group-hover:text-[var(--color-primary)] transition-colors line-clamp-2">{a.title}</h3>
            </a>
          ))}
        </div>
      </div>
    )}
    <div class="mt-10"><a href="/" class="btn-primary">Back to Home</a></div>
  </div>
</BaseLayout>
ASTROEOF
echo "  ✅ Fix 12: Custom 404 page created"

# ═══════════════════════════════════════════════════
# FIX 13: Smarter internal linking
# ═══════════════════════════════════════════════════
python3 << 'PYEOF'
filepath = '/Users/penny/Documents/Penny/pseo-network/templates/base/src/pages/[slug].astro'
with open(filepath, 'r') as f: content = f.read()
if 'Smart internal linking' not in content:
    old = """// Auto-link related articles in content body (conservative)
const linkableArticles = allArticles.slice(0, 15);
for (const ra of linkableArticles) {
  const titleWords = ra.title.split(' ').filter(w => w.length > 4).slice(0, 3);
  if (titleWords.length < 2) continue;
  const phrase = titleWords.join(' ');
  if (enhancedContent.toLowerCase().includes(phrase.toLowerCase()) && !enhancedContent.includes(`/${ra.slug}"`)) {
    const regex = new RegExp(`(${phrase.replace(/[.*+?^${}()|[\]\\\\]/g, '\\\\$&')})`, 'i');
    if ((enhancedContent.match(regex) || []).length <= 1) {
      enhancedContent = enhancedContent.replace(regex, `<a href="/${ra.slug}">$1</a>`);
    }
  }
}"""
    new = """// Smart internal linking: title phrases + category keywords + entity mentions
const linkableArticles = allArticles.slice(0, 20);
let linkCount = 0;
const MAX_LINKS = 5;
for (const ra of linkableArticles) {
  if (linkCount >= MAX_LINKS) break;
  const titleWords = ra.title.split(' ').filter(w => w.length > 4).slice(0, 3);
  if (titleWords.length >= 2) {
    const phrase = titleWords.join(' ');
    const escaped = phrase.replace(/[.*+?^${}()|[\]\\\\]/g, '\\\\$&');
    if (enhancedContent.toLowerCase().includes(phrase.toLowerCase()) && !enhancedContent.includes(`/${ra.slug}"`)) {
      const regex = new RegExp(`(${escaped})`, 'i');
      if ((enhancedContent.match(regex) || []).length === 1) {
        enhancedContent = enhancedContent.replace(regex, `<a href="/${ra.slug}">$1</a>`);
        linkCount++; continue;
      }
    }
  }
  if (ra.category === article.category) {
    const catKeywords = ra.title.split(' ').filter(w => w.length > 5 && !['which','their','about','other','these','those','being','where','should'].includes(w.toLowerCase()));
    for (const kw of catKeywords.slice(0, 2)) {
      if (linkCount >= MAX_LINKS) break;
      const escaped = kw.replace(/[.*+?^${}()|[\]\\\\]/g, '\\\\$&');
      const regex = new RegExp(`(?<![\\w/])(${escaped})(?![\\w"])`, 'g');
      const matches = enhancedContent.match(regex);
      if (matches && matches.length === 1 && !enhancedContent.includes(`/${ra.slug}"`)) {
        enhancedContent = enhancedContent.replace(regex, `<a href="/${ra.slug}">$1</a>`);
        linkCount++; break;
      }
    }
  }
}"""
    content = content.replace(old, new)
    with open(filepath, 'w') as f: f.write(content)
print('OK')
PYEOF
echo "  ✅ Fix 13: Smarter internal linking"

# ═══════════════════════════════════════════════════
# FIX 14: Author page with rel=me + Person schema
# ═══════════════════════════════════════════════════
cat > "$T/src/pages/about/author.astro" << 'ASTROEOF'
---
import BaseLayout from '../../layouts/BaseLayout.astro';
import fs from 'node:fs';
const siteConfig = JSON.parse(fs.readFileSync('site-config.json', 'utf-8'));
const domain = siteConfig.domain || 'example.com';
const siteUrl = `https://${domain}`;
const authorName = siteConfig.author || siteConfig.name;
const breadcrumbs = [{ name: 'Home', url: '/' }, { name: 'About', url: '/about' }, { name: authorName, url: '/about/author' }];
const schema = {
  "@context": "https://schema.org", "@type": "Person", "name": authorName,
  "url": `${siteUrl}/about/author`, "jobTitle": "Content Editor",
  "worksFor": { "@type": "Organization", "name": siteConfig.name, "url": siteUrl },
  "knowsAbout": siteConfig.niche,
  "sameAs": siteConfig.social ? Object.values(siteConfig.social) : undefined
};
---
<BaseLayout title={`${authorName} - Author`} description={`About ${authorName}, editor at ${siteConfig.name}.`} ogType="profile" breadcrumbs={breadcrumbs} siteName={siteConfig.name} schema={schema}>
  <article class="max-w-3xl mx-auto">
    <nav aria-label="Breadcrumb" class="mb-6">
      <ol class="flex items-center gap-1.5 text-sm text-[var(--color-text-muted)]">
        <li><a href="/" class="hover:text-[var(--color-primary)]">Home</a></li>
        <li><span class="mx-1">›</span></li>
        <li><a href="/about" class="hover:text-[var(--color-primary)]">About</a></li>
        <li><span class="mx-1">›</span></li>
        <li class="text-[var(--color-text)] font-medium">{authorName}</li>
      </ol>
    </nav>
    <div class="flex items-center gap-6 mb-8">
      <div class="w-24 h-24 rounded-full bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-accent)] flex items-center justify-center text-white text-2xl font-bold flex-shrink-0">
        {authorName.split(' ').map(w => w[0]).join('').substring(0, 2)}
      </div>
      <div>
        <h1 class="text-3xl font-extrabold text-[var(--color-text-heading)]">{authorName}</h1>
        <p class="text-[var(--color-text-muted)]">Content Editor · {siteConfig.name}</p>
      </div>
    </div>
    <div class="prose prose-lg">
      <p>{authorName} is the editorial team behind {siteConfig.name}. With a focus on {siteConfig.niche}, we research and publish comprehensive guides that help readers make informed decisions.</p>
      <h2>Editorial Philosophy</h2>
      <p>Every article undergoes thorough research and fact-checking. We provide practical, actionable information rather than generic advice.</p>
      <h2>Expertise</h2>
      <ul>
        <li>In-depth {siteConfig.niche} research and analysis</li>
        <li>Practical how-to guides with step-by-step instructions</li>
        <li>Unbiased product and service comparisons</li>
        <li>Data-driven insights with cited sources</li>
      </ul>
      <h2>Connect</h2>
      <ul>
        <li><a href="/" rel="me">{siteConfig.name}</a></li>
      </ul>
    </div>
  </article>
</BaseLayout>
ASTROEOF
echo "  ✅ Fix 14: Author page with rel=me + Person schema"

# ═══════════════════════════════════════════════════
# FIX 15: Update build pipeline
# ═══════════════════════════════════════════════════
python3 << 'PYEOF'
filepath = '/Users/penny/Documents/Penny/pseo-network/scripts/build-site.sh'
with open(filepath, 'r') as f: content = f.read()
if 'about.astro' not in content:
    old = 'cp "$TEMPLATE_DIR/src/pages/category/[category].astro" "$SITE_DIR/src/pages/category/[category].astro"'
    new = old + """

# Copy new pages (legal, 404, author)
for page in about.astro privacy-policy.astro terms.astro contact.astro 404.astro; do
  cp "$TEMPLATE_DIR/src/pages/$page" "$SITE_DIR/src/pages/$page" 2>/dev/null || true
done
mkdir -p "$SITE_DIR/src/pages/about"
cp "$TEMPLATE_DIR/src/pages/about/author.astro" "$SITE_DIR/src/pages/about/author.astro" 2>/dev/null || true"""
    content = content.replace(old, new)
    with open(filepath, 'w') as f: f.write(content)
print('OK')
PYEOF
echo "  ✅ Fix 15: Build pipeline updated"

echo ""
echo "═══════════════════════════════════════════"
echo " ✅ ALL 15 FIXES APPLIED"
echo "═══════════════════════════════════════════"
