#!/usr/bin/env python3
"""Add @astrojs/sitemap integration to all sites."""
import re
from pathlib import Path

NETWORK = Path("/Users/penny/Documents/Penny/pseo-network")
SITES = [
    "budget-travel-tips", "bitcoin-beginners", "crypto-investing-guide",
    "crypto-trading-strategies", "defi-yield-guide", "personal-finance-tips",
    "ai-tools-hub", "smart-emergency-fund",
]

for site in SITES:
    f = NETWORK / "output" / "sites" / site / "astro.config.mjs"
    if not f.exists():
        continue
    content = f.read_text()
    if 'sitemap' in content:
        continue
    original = content
    # Add sitemap import and integration
    new = '''import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://example.com',
  integrations: [
    tailwind(),
    sitemap({
      changefreq: 'weekly',
      priority: 0.7,
    })
  ],
  output: 'static',
  build: {
    inlineStylesheets: 'auto',
  },
  vite: {
    build: {
      cssMinify: true,
    },
  },
});'''
    f.write_text(new)
    print(f"✅ {site}: sitemap integration added")
