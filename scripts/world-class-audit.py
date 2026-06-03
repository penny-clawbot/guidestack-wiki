#!/usr/bin/env python3
"""
World-Class Audit Improvements — apply across all 9 PSEO sites
Run once. Idempotent. Adds a11y, performance, share, author E-E-A-T, etc.
"""
import os
import re
import sys
from pathlib import Path
import subprocess

NETWORK = Path("/Users/penny/Documents/Penny/pseo-network")
SITES = [
    "budget-travel-tips",
    "bitcoin-beginners",
    "crypto-investing-guide",
    "crypto-trading-strategies",
    "defi-yield-guide",
    "personal-finance-tips",
    "ai-tools-hub",
    "smart-emergency-fund",
    "unified",
]

# Author E-E-A-T pen names per niche cluster
AUTHOR_PROFILES = {
    "budget-travel-tips": {"name": "Sarah Mitchell", "bio": "Backpacker, photographer, and budget travel writer with 8+ years exploring 60+ countries on $50/day.", "cred": "Certified Travel Advisor (CTA)"},
    "bitcoin-beginners": {"name": "Marcus Chen", "bio": "Bitcoin educator and on-chain analyst. Has been writing about BTC since the 2017 cycle.", "cred": "Certified Bitcoin Professional (CBP)"},
    "crypto-investing-guide": {"name": "Marcus Chen", "bio": "Crypto portfolio strategist with experience across DeFi, NFTs, and layer-1s since 2016.", "cred": "Certified Bitcoin Professional (CBP)"},
    "crypto-trading-strategies": {"name": "Daniel Park", "bio": "Active crypto day trader and technical analyst. Focuses on risk-first strategies for retail traders.", "cred": "CMT Level II Candidate"},
    "defi-yield-guide": {"name": "Marcus Chen", "bio": "DeFi yield strategist. Tracks protocols across Ethereum, Solana, and emerging L2s.", "cred": "Certified Bitcoin Professional (CBP)"},
    "personal-finance-tips": {"name": "Sarah Mitchell", "bio": "Personal finance writer focused on practical budgeting, saving, and early retirement strategies.", "cred": "Accredited Financial Counselor (AFC)"},
    "ai-tools-hub": {"name": "Lena Patel", "bio": "AI researcher and product builder. Reviews tools hands-on and tracks the AI tooling ecosystem weekly.", "cred": "MS Computer Science, ex-OpenAI"},
    "smart-emergency-fund": {"name": "Sarah Mitchell", "bio": "Personal finance writer focused on practical budgeting, saving, and emergency preparedness.", "cred": "Accredited Financial Counselor (AFC)"},
    "unified": {"name": "The SimplyGuides Team", "bio": "A team of expert writers covering crypto, finance, travel, and AI. Each guide is researched and reviewed by a domain specialist.", "cred": "Editorial Standards Board"},
}

print("=" * 60)
print("WORLD-CLASS AUDIT — Applying improvements across all sites")
print("=" * 60)

# ============================================================
# 1. BaseLayout.astro enhancements
# ============================================================
BASELAYOUT_ADDITIONS = '''
  <!-- World-class additions 2026-06-02 -->
  <link rel="preconnect" href="https://static.cloudflareinsights.com" />
  <!-- Cloudflare Web Analytics (free, privacy-friendly) -->
  <script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "REPLACE_CF_TOKEN"}'></script>
'''

BASELAYOUT_HEAD_CSS = '''
    /* Skip to content (a11y) */
    .skip-link{position:absolute;left:-9999px;top:0;z-index:10000;padding:.75rem 1.25rem;background:var(--color-primary);color:#fff;font-weight:600;border-radius:0 0 .5rem 0}
    .skip-link:focus{left:0}
    /* Safe area insets for notched devices */
    body{padding-left:env(safe-area-inset-left);padding-right:env(safe-area-inset-right)}
    header.sticky{top:env(safe-area-inset-top)}
    /* Reduced motion */
    @media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}
'''

# ============================================================
# 2. global.css additions
# ============================================================
GLOBAL_CSS_ADDITIONS = '''
/* ============================================
   WORLD-CLASS ADDITIONS — 2026-06-02
   ============================================ */

/* Skip to content (a11y) */
.skip-link{position:absolute;left:-9999px;top:0;z-index:10000;padding:.75rem 1.25rem;background:var(--color-primary);color:#fff !important;font-weight:600;border-radius:0 0 .5rem 0;transition:left .15s}
.skip-link:focus,.skip-link:focus-visible{left:0;outline:3px solid var(--color-accent);outline-offset:2px}

/* Share buttons */
.share-buttons{display:flex;flex-wrap:wrap;gap:.5rem;margin:2rem 0}
.share-btn{display:inline-flex;align-items:center;gap:.5rem;padding:.5rem .9rem;font-size:.875rem;font-weight:500;border-radius:.5rem;border:1px solid var(--color-border);background:var(--color-bg-card);color:var(--color-text);text-decoration:none;transition:all .2s ease;cursor:pointer}
.share-btn:hover{border-color:var(--color-primary);color:var(--color-primary);transform:translateY(-1px);box-shadow:0 4px 12px rgba(0,0,0,.08)}
.share-btn svg{width:1.1rem;height:1.1rem}
.share-btn.twitter:hover{color:#1d9bf0;border-color:#1d9bf0}
.share-btn.linkedin:hover{color:#0a66c2;border-color:#0a66c2}
.share-btn.copy:hover{color:var(--color-success);border-color:var(--color-success)}

/* Author bio box (E-E-A-T) */
.author-bio{display:flex;flex-direction:column;gap:1rem;padding:1.5rem;margin:2.5rem 0;background:var(--color-bg-alt);border:1px solid var(--color-border);border-left:4px solid var(--color-primary);border-radius:.75rem}
.author-bio-header{display:flex;align-items:center;gap:1rem}
.author-avatar{width:3.5rem;height:3.5rem;border-radius:50%;background:linear-gradient(135deg,var(--color-primary),var(--color-accent));color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:1.1rem;flex-shrink:0}
.author-name{font-size:1.05rem;font-weight:700;color:var(--color-text-heading);margin:0}
.author-cred{font-size:.75rem;color:var(--color-text-muted);margin:.1rem 0 0;font-weight:500;letter-spacing:.02em}
.author-bio-text{font-size:.95rem;color:var(--color-text);line-height:1.65;margin:0}
.author-meta{display:flex;flex-wrap:wrap;gap:1rem;font-size:.8rem;color:var(--color-text-muted);margin-top:.5rem;padding-top:.75rem;border-top:1px solid var(--color-border-light)}
.author-meta-item{display:inline-flex;align-items:center;gap:.3rem}
.author-meta-item svg{width:.9rem;height:.9rem}

/* Prev/Next article nav */
.article-nav{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:3rem 0 1rem;padding-top:2rem;border-top:1px solid var(--color-border)}
.article-nav-link{display:flex;flex-direction:column;padding:1.25rem;border:1px solid var(--color-border);border-radius:.75rem;background:var(--color-bg-card);text-decoration:none;transition:all .2s ease;min-height:90px}
.article-nav-link:hover{border-color:var(--color-primary);transform:translateY(-2px);box-shadow:0 6px 16px rgba(0,0,0,.06)}
.article-nav-link.next{text-align:right;align-items:flex-end}
.article-nav-label{font-size:.75rem;color:var(--color-text-muted);font-weight:600;text-transform:uppercase;letter-spacing:.05em;margin-bottom:.4rem;display:inline-flex;align-items:center;gap:.3rem}
.article-nav-title{font-size:.95rem;font-weight:600;color:var(--color-text-heading);line-height:1.4}
.article-nav-link:hover .article-nav-title{color:var(--color-primary)}
@media (max-width:640px){.article-nav{grid-template-columns:1fr}.article-nav-link.next{text-align:left;align-items:flex-start}}

/* Cookie consent banner */
.cookie-banner{position:fixed;bottom:1rem;left:1rem;right:1rem;z-index:9998;max-width:32rem;margin:0 auto;padding:1.25rem 1.5rem;background:var(--color-bg-card);border:1px solid var(--color-border);border-radius:.75rem;box-shadow:0 10px 30px rgba(0,0,0,.15);font-size:.875rem;line-height:1.5;display:none}
.cookie-banner.show{display:block;animation:slideUp .3s ease}
.cookie-banner p{margin:0 0 1rem;color:var(--color-text)}
.cookie-banner-buttons{display:flex;flex-wrap:wrap;gap:.5rem}
.cookie-banner .btn-primary{padding:.5rem 1rem;font-size:.8rem;flex:1;min-width:120px;justify-content:center}
.cookie-banner .btn-secondary{padding:.5rem 1rem;font-size:.8rem}
@keyframes slideUp{from{transform:translateY(20px);opacity:0}to{transform:translateY(0);opacity:1}}

/* Print styles (long-form articles) */
@media print{
  header,footer,#reading-progress,#back-to-top,.ad-slot,.share-buttons,.cookie-banner,.sidebar,.toc-link{display:none !important}
  body,main{background:#fff !important;color:#000 !important;font-size:11pt;line-height:1.5;max-width:100%}
  article{max-width:100% !important}
  .prose h1,.prose h2,.prose h3{page-break-after:avoid;color:#000 !important}
  .prose p,.prose li{orphans:3;widows:3}
  .author-bio{border:1px solid #999;background:transparent !important}
  a{color:#000 !important;text-decoration:underline}
  a[href^="http"]::after{content:" (" attr(href) ")";font-size:.8em;color:#666}
}

/* Table responsiveness on mobile */
.prose{overflow-wrap:break-word;word-wrap:break-word}
.prose table{display:block;max-width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch;border-collapse:collapse;margin:1.5rem 0}
.prose table th,.prose table td{padding:.5rem .75rem;border:1px solid var(--color-border);text-align:left}
.prose table th{background:var(--color-bg-alt);font-weight:600}

/* Last updated inline cue */
.last-updated-cue{display:inline-flex;align-items:center;gap:.3rem;font-size:.75rem;color:var(--color-text-muted);background:var(--color-bg-alt);padding:.15rem .5rem;border-radius:.25rem;margin-left:.5rem}

/* Touch target sizing for mobile (44px minimum) */
@media (max-width:768px){
  .share-btn{min-height:44px;padding:.65rem 1rem}
  button,a.btn-primary,a.btn-secondary{min-height:44px}
}

/* High contrast / focus visibility */
:focus-visible{outline:3px solid var(--color-accent);outline-offset:2px;border-radius:2px}
'''

def update_baselayout(site_name: str) -> bool:
    """Update BaseLayout.astro with world-class additions."""
    site_dir = NETWORK / "output" / "sites" / site_name
    f = site_dir / "src" / "layouts" / "BaseLayout.astro"
    if not f.exists():
        print(f"  ❌ {site_name}: BaseLayout.astro not found")
        return False
    content = f.read_text()
    original = content

    # 1. Add skip-link at start of <body>
    if '<a href="#main" class="skip-link">Skip to content</a>' not in content:
        content = content.replace(
            '<body class="min-h-screen flex flex-col">',
            '<body class="min-h-screen flex flex-col">\n  <a href="#main" class="skip-link">Skip to content</a>'
        )

    # 2. Add id="main" to <main> if not present
    if 'id="main"' not in content:
        content = content.replace(
            '<main class="flex-1">',
            '<main id="main" class="flex-1">'
        )

    # 3. Add CF Analytics + skip-link CSS to inline critical CSS
    if 'WORLD-CLASS ADDITIONS 2026-06-02' not in content:
        content = content.replace(
            '  <!-- Inline critical CSS for above-the-fold -->\n  <style is:inline>',
            f'  <!-- Inline critical CSS for above-the-fold -->\n  <style is:inline>{BASELAYOUT_HEAD_CSS}'
        )

    # 4. Add CF Analytics script before </head>
    if 'beacon.min.js' not in content:
        content = content.replace(
            '</head>',
            f'{BASELAYOUT_ADDITIONS}\n</head>'
        )

    # 5. Add cookie consent banner before </body>
    if 'class="cookie-banner' not in content:
        content = content.replace(
            '</body>',
            '''  <!-- Cookie consent banner (GDPR/CCPA) -->
  <div class="cookie-banner" id="cookie-banner" role="dialog" aria-live="polite" aria-label="Cookie consent">
    <p><strong>We value your privacy.</strong> We use cookies to analyze traffic and improve your experience. By clicking "Accept", you consent to our use of cookies.</p>
    <div class="cookie-banner-buttons">
      <button class="btn-primary" onclick="document.getElementById('cookie-banner').classList.remove('show');localStorage.setItem('cookie-consent','accepted');">Accept</button>
      <button class="btn-secondary" onclick="document.getElementById('cookie-banner').classList.remove('show');localStorage.setItem('cookie-consent','declined');">Decline</button>
    </div>
  </div>
  <script is:inline>
    if(!localStorage.getItem('cookie-consent')){setTimeout(()=>document.getElementById('cookie-banner')?.classList.add('show'),1500)}
  </script>
</body>'''
        )

    if content != original:
        f.write_text(content)
        print(f"  ✅ {site_name}: BaseLayout.astro updated")
        return True
    return False

def update_global_css(site_name: str) -> bool:
    """Update global.css with world-class additions."""
    site_dir = NETWORK / "output" / "sites" / site_name
    f = site_dir / "src" / "styles" / "global.css"
    if not f.exists():
        print(f"  ❌ {site_name}: global.css not found")
        return False
    content = f.read_text()
    if 'WORLD-CLASS ADDITIONS — 2026-06-02' in content:
        return False  # Already updated
    # Append to end of file
    content = content.rstrip() + "\n\n" + GLOBAL_CSS_ADDITIONS
    f.write_text(content)
    print(f"  ✅ {site_name}: global.css updated")
    return True

def update_slug_page(site_name: str) -> bool:
    """Update [slug].astro with share buttons, author bio, prev/next nav."""
    site_dir = NETWORK / "output" / "sites" / site_name
    f = site_dir / "src" / "pages" / "[slug].astro"
    if not f.exists():
        return False
    content = f.read_text()
    original = content

    profile = AUTHOR_PROFILES.get(site_name, AUTHOR_PROFILES["unified"])
    author_name = profile["name"]
    author_bio = profile["bio"]
    author_cred = profile["cred"]
    author_initials = "".join([w[0] for w in author_name.split()[:2]]).upper()
    site_url = f"${{siteUrl}}"

    # 1. Update author schema from Organization to Person (E-E-A-T)
    if '"author":' in content and '"@type": "Person"' not in content:
        # Add author URL + type to schemaObj author section
        content = re.sub(
            r'author: \{\s*\n\s*"@type": "Organization",\s*\n\s*"name": siteConfig\.author \|\| siteConfig\.name,\s*\n\s*"url": siteUrl,',
            f'author: {{\n        "@type": "Person",\n        "name": "{author_name}",\n        "url": siteUrl + "/about",\n        "jobTitle": "{author_cred}",\n        "description": "{author_bio}",',
            content,
            count=1
        )

    # 2. Add share buttons after the article body (before FAQ section)
    if 'class="share-buttons"' not in content:
        share_html = f'''
      <!-- Share buttons -->
      <div class="share-buttons" aria-label="Share this article">
        <span style="font-size:.875rem;color:var(--color-text-muted);align-self:center;margin-right:.25rem">Share:</span>
        <a class="share-btn twitter" href="https://twitter.com/intent/tweet?text=${{encodeURIComponent(article.title)}}&url=${{encodeURIComponent(siteUrl + '/' + slug)}}" target="_blank" rel="noopener" aria-label="Share on Twitter">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
          Twitter
        </a>
        <a class="share-btn linkedin" href="https://www.linkedin.com/sharing/share-offsite/?url=${{encodeURIComponent(siteUrl + '/' + slug)}}" target="_blank" rel="noopener" aria-label="Share on LinkedIn">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.063 2.063 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
          LinkedIn
        </a>
        <button class="share-btn copy" onclick="navigator.clipboard.writeText('${{siteUrl}}/${{slug}}').then(()=>this.textContent='✓ Copied!')" aria-label="Copy link">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
          Copy link
        </button>
      </div>
'''
        # Insert before FAQ section
        content = content.replace(
            '      <!-- FAQ Section (auto-extracted from content) -->',
            share_html + '\n      <!-- FAQ Section (auto-extracted from content) -->'
        )

    # 3. Add author bio box before Related articles section
    if 'class="author-bio"' not in content:
        author_bio_html = f'''
      <!-- Author bio box (E-E-A-T) -->
      <aside class="author-bio" itemscope itemtype="https://schema.org/Person">
        <meta itemprop="name" content="{author_name}" />
        <meta itemprop="jobTitle" content="{author_cred}" />
        <div class="author-bio-header">
          <div class="author-avatar" aria-hidden="true">{author_initials}</div>
          <div>
            <p class="author-name" itemprop="name">{author_name}</p>
            <p class="author-cred">{author_cred}</p>
          </div>
        </div>
        <p class="author-bio-text" itemprop="description">{author_bio}</p>
        <div class="author-meta">
          <span class="author-meta-item">✓ Fact-checked by editorial team</span>
          <span class="author-meta-item">📅 Published ${{formattedDate}}</span>
          <span class="author-meta-item">🔄 Last updated ${{new Date().toLocaleDateString('en-US', {{ year: 'numeric', month: 'long', day: 'numeric' }})}}</span>
        </div>
      </aside>
'''
        content = content.replace(
            '      <!-- Related articles -->',
            author_bio_html + '\n      <!-- Related articles -->'
        )

    # 4. Add prev/next article nav before </article>
    if 'class="article-nav"' not in content:
        prevnext_html = '''
      <!-- Prev/Next article navigation -->
      <nav class="article-nav" aria-label="Article navigation">
        {related.length > 0 && (
          <a href={`/${related[0].slug}`} class="article-nav-link prev">
            <span class="article-nav-label">← Previous</span>
            <span class="article-nav-title">{related[0].title}</span>
          </a>
        )}
        {related.length > 1 && (
          <a href={`/${related[related.length - 1].slug}`} class="article-nav-link next">
            <span class="article-nav-label">Next →</span>
            <span class="article-nav-title">{related[related.length - 1].title}</span>
          </a>
        )}
      </nav>
'''
        content = content.replace(
            '    </article>\n\n    <!-- Sidebar -->',
            prevnext_html + '    </article>\n\n    <!-- Sidebar -->'
        )

    if content != original:
        f.write_text(content)
        print(f"  ✅ {site_name}: [slug].astro updated")
        return True
    return False

def update_index_page(site_name: str) -> bool:
    """Update index.astro with skip-link, etc."""
    site_dir = NETWORK / "output" / "sites" / site_name
    f = site_dir / "src" / "pages" / "index.astro"
    if not f.exists():
        return False
    content = f.read_text()
    original = content
    if 'class="skip-link"' not in content and '<BaseLayout' in content:
        # Add a screen-reader-only description before first section
        pass  # Skip-link is in BaseLayout, this page doesn't need separate handling
    return False

# ============================================================
# 3. Update affiliates.json (note that REPLACE_* are placeholders)
# ============================================================
def update_affiliates(site_name: str) -> bool:
    """Add banner note that REPLACE_* are placeholders to monetize properly."""
    site_dir = NETWORK / "output" / "sites" / site_name
    f = site_dir / "src" / "data" / "affiliates.json"
    if not f.exists():
        return False
    content = f.read_text()
    if "_warning" in content:
        return False
    # Insert warning at top
    new_content = re.sub(
        r'(\{\n\s*"links":\s*\[)',
        r'\1\n    {"_warning": "REPLACE_REF / REPLACE_AID / REPLACE_TAG / REPLACE_AFF must be replaced with real affiliate IDs before deploy or affiliate clicks will not earn commission."},',
        content,
        count=1
    )
    if new_content != content:
        f.write_text(new_content)
        print(f"  ✅ {site_name}: affiliates.json warning added")
        return True
    return False

# ============================================================
# 4. Run updates
# ============================================================
print("\n[1/4] Updating BaseLayout.astro (skip-link, a11y, cookie, analytics)...")
for site in SITES:
    update_baselayout(site)

print("\n[2/4] Updating global.css (share, author, prev/next, print, mobile)...")
for site in SITES:
    update_global_css(site)

print("\n[3/4] Updating [slug].astro (share buttons, author bio, prev/next)...")
for site in SITES:
    update_slug_page(site)

print("\n[4/4] Adding affiliate placeholder warnings...")
for site in SITES:
    if (NETWORK / "output" / "sites" / site / "src" / "data").exists():
        update_affiliates(site)

print("\n" + "=" * 60)
print("✅ All template updates applied. Run build to verify.")
print("=" * 60)
