#!/usr/bin/env python3
"""Cross-device visual QA — capture screenshots of all 8 sites at 7 viewports.
Output: /Users/penny/Documents/Penny/Penny-AI/projects/guidestack-pseo/qa-screenshots/
"""
import os
import sys
import subprocess
from pathlib import Path
import asyncio
import http.server
import socketserver
import threading
import time
from playwright.async_api import async_playwright

# Try to use playwright python
try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Installing playwright...")
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
    from playwright.async_api import async_playwright

NETWORK = Path("/Users/penny/Documents/Penny/pseo-network")
SITES = [
    "budget-travel-tips", "bitcoin-beginners", "crypto-investing-guide",
    "crypto-trading-strategies", "defi-yield-guide", "personal-finance-tips",
    "ai-tools-hub", "smart-emergency-fund",
]

# Viewports covering mobile, tablet, laptop, desktop, 4K
VIEWPORTS = [
    {"name": "iphone-se",      "width": 375,  "height": 667},
    {"name": "iphone-15-pro",  "width": 393,  "height": 852},
    {"name": "android-pixel",  "width": 412,  "height": 915},
    {"name": "ipad-mini",      "width": 768,  "height": 1024},
    {"name": "ipad-pro",       "width": 1024, "height": 1366},
    {"name": "laptop-1280",    "width": 1280, "height": 800},
    {"name": "desktop-1920",   "width": 1920, "height": 1080},
]

# Path-prefix routing (used by unified site but each site has its own)
SITE_BASE = {
    "budget-travel-tips": "/",
    "bitcoin-beginners": "/",
    "crypto-investing-guide": "/",
    "crypto-trading-strategies": "/",
    "defi-yield-guide": "/",
    "personal-finance-tips": "/",
    "ai-tools-hub": "/",
    "smart-emergency-fund": "/",
}

# Each site has its own dist
OUTPUT_DIR = NETWORK / "Penny-AI" / "projects" / "guidestack-pseo" / "qa-screenshots"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Find one good article per site (the first article, skip non-content pages)
def find_test_article(site: str) -> str:
    d = NETWORK / "output" / "sites" / site / "dist"
    # Find a non-category, non-best, non-special page
    for f in d.glob("*/index.html"):
        if f.parent.name not in ("category", "best", "404", "contact", "about", "privacy-policy", "terms", "_astro", "compare"):
            # Skip paths with /compare/ or /category/
            if "/compare/" not in str(f) and "/category/" not in str(f) and "/best/" not in str(f):
                return f"/{f.parent.name}/"
    return "/"

# Start a static file server for the dist folders
def start_server(site: str, port: int):
    d = NETWORK / "output" / "sites" / site / "dist"
    os.chdir(d)
    handler = http.server.SimpleHTTPRequestHandler
    handler.directory = str(d)
    httpd = socketserver.TCPServer(("", port), handler)
    httpd_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    httpd_thread.start()
    return httpd

async def capture():
    print("=" * 60)
    print("Cross-Device Visual QA")
    print("=" * 60)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        
        for site in SITES:
            port = 9000 + SITES.index(site)
            print(f"\n--- {site} (port {port}) ---")
            httpd = start_server(site, port)
            time.sleep(0.5)  # Let server start

            article_path = find_test_article(site)
            url = f"http://localhost:{port}{article_path}"
            print(f"  URL: {url}")

            for vp in VIEWPORTS:
                ctx = await browser.new_context(
                    viewport={"width": vp["width"], "height": vp["height"]},
                    device_scale_factor=2 if vp["name"] in ("iphone-15-pro", "android-pixel") else 1,
                    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36" if vp["name"].startswith(("laptop", "desktop", "ipad")) else None
                )
                page = await ctx.new_page()
                try:
                    await page.goto(url, wait_until="networkidle", timeout=15000)
                    # Screenshot full page
                    out = OUTPUT_DIR / f"{site}_{vp['name']}.png"
                    await page.screenshot(path=str(out), full_page=False)  # Viewport only for size
                    print(f"    ✅ {vp['name']} ({vp['width']}x{vp['height']}): {out.name}")
                except Exception as e:
                    print(f"    ❌ {vp['name']}: {e}")
                await ctx.close()

            httpd.shutdown()

        await browser.close()

    print(f"\n📸 Screenshots saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    asyncio.run(capture())
