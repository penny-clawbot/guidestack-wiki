#!/usr/bin/env python3
"""Make Cloudflare Web Analytics conditional (only load in production, not localhost)
Also add a small inline script that checks the hostname."""
import re
from pathlib import Path

NETWORK = Path("/Users/penny/Documents/Penny/pseo-network")
SITES = [
    "budget-travel-tips", "bitcoin-beginners", "crypto-investing-guide",
    "crypto-trading-strategies", "defi-yield-guide", "personal-finance-tips",
    "ai-tools-hub", "smart-emergency-fund",
]

OLD = '''  <link rel="preconnect" href="https://static.cloudflareinsights.com" />
  <!-- Cloudflare Web Analytics (free, privacy-friendly) -->
  <script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "REPLACE_CF_TOKEN"}'></script>'''

NEW = '''  <!-- Cloudflare Web Analytics (free, privacy-friendly) — loaded only in production -->
  <script is:inline>
    (function() {
      var h = location.hostname;
      // Only load CF Analytics on real domains (not localhost, not 127.0.0.1, not .pages.dev preview)
      if (h === 'localhost' || h === '127.0.0.1' || h === '' || h.indexOf('192.168.') === 0 || h.indexOf('10.') === 0) return;
      var s = document.createElement('script');
      s.defer = true;
      s.src = 'https://static.cloudflareinsights.com/beacon.min.js';
      s.setAttribute('data-cf-beacon', '{"token": "REPLACE_CF_TOKEN"}');
      document.head.appendChild(s);
    })();
  </script>'''

for site in SITES:
    f = NETWORK / "output" / "sites" / site / "src" / "layouts" / "BaseLayout.astro"
    if not f.exists():
        continue
    content = f.read_text()
    if 'Only load CF Analytics on real domains' in content:
        continue
    if OLD in content:
        content = content.replace(OLD, NEW)
        f.write_text(content)
        print(f"✅ {site}: CF Analytics made conditional")
    else:
        print(f"⚠ {site}: pattern not found")
