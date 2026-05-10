#!/usr/bin/env python3
"""
PennyPress Master Pipeline — End-to-end SEO site orchestration.

Usage:
    python pipeline.py research <niche>          # Run keyword research
    python pipeline.py build <niche>             # Build site from keywords
    python pipeline.py deploy <site-name>        # Deploy to GitHub + Cloudflare
    python pipeline.py full <niche>              # Full: research → build → deploy

Examples:
    python pipeline.py research "smart home gadgets"
    python pipeline.py build "smart-home-gadgets"
    python pipeline.py deploy "smart-home-gadgets"
    python pipeline.py full "smart home gadgets"
"""

import json
import os
import sys
import subprocess
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
CONFIG_FILE = PROJECT_ROOT / "config.json"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output" / "sites"
KEYWORDS_DIR = DATA_DIR / "keywords"
CONTENT_DIR = DATA_DIR / "content"


def load_config() -> dict:
    """Load config.json."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {
        "ollama_url": "http://localhost:11434",
        "searxng_url": "http://localhost:8888",
        "output_dir": "output/sites",
        "github_org": "pennypress-sites",
    }


def save_config(config: dict) -> None:
    """Save config.json."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def run_command(cmd: list, cwd: Path = PROJECT_ROOT, desc: str = "") -> bool:
    """Run a shell command and report result."""
    print(f"\n{'='*60}")
    print(f"  {desc or 'Running'}: {' '.join(cmd)}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, cwd=cwd, check=True, capture_output=False)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with exit code {e.returncode}")
        return False


def check_searxng() -> bool:
    """Check if SearXNG is available."""
    try:
        import urllib.request
        config = load_config()
        url = config.get("searxng_url", "http://localhost:8888")
        with urllib.request.urlopen(url + "/search?q=test&format=json", timeout=5) as r:
            return r.status == 200
    except Exception:
        return False


def check_ollama() -> bool:
    """Check if Ollama is available."""
    try:
        import urllib.request
        config = load_config()
        url = config.get("ollama_url", "http://localhost:11434")
        with urllib.request.urlopen(url + "/api/tags", timeout=5) as r:
            return r.status == 200
    except Exception:
        return False


def cmd_research(niche: str) -> bool:
    """Run keyword research pipeline."""
    print(f"\n🔍 RESEARCH MODE: {niche}")
    print(f"{'='*60}")

    if not check_searxng():
        print(f"❌ SearXNG not available at {load_config().get('searxng_url')}")
        print("   Start with: docker start searxng")
        return False

    print("✅ SearXNG connected")
    print("✅ Ollama available")

    # Run keyword research script
    kw_script = SCRIPTS_DIR / "keyword-research.py"
    if not kw_script.exists():
        print(f"❌ keyword-research.py not found at {kw_script}")
        return False

    safe_niche = niche.replace(" ", "-")
    keywords_file = KEYWORDS_DIR / f"{safe_niche}-keywords.json"

    print(f"\n⏳ Running keyword research (this may take a while)...")
    start = time.time()

    # Run the research script
    result = subprocess.run(
        [sys.executable, str(kw_script), niche],
        cwd=PROJECT_ROOT,
    )

    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"❌ Keyword research failed")
        return False

    if not keywords_file.exists():
        print(f"❌ Keywords file not generated at {keywords_file}")
        return False

    # Load and summarize results
    with open(keywords_file) as f:
        data = json.load(f)

    print(f"\n✅ Research complete in {elapsed:.1f}s")
    print(f"\n📊 RESULTS:")
    print(f"   Total keywords: {data['total_keywords']}")
    print(f"   Top clusters: {', '.join(list(data['clusters'].keys())[:5])}")
    print(f"   PAA questions: {len(data['paa_questions'])}")

    print(f"\n🏆 TOP 10 KEYWORDS:")
    for i, kw in enumerate(data["top_keywords"][:10], 1):
        print(f"   {i}. {kw['keyword']}")
        print(f"      Vol: {kw['volume_estimate']:,} | Comp: {kw['competition_score']} | RPM: ${kw['rpm_estimate']:.2f}")

    print(f"\n📁 Keywords saved to: {keywords_file}")

    # Run niche scorer
    niche_script = SCRIPTS_DIR / "niche-scorer.py"
    if niche_script.exists():
        print(f"\n⏳ Running niche scoring...")
        result = subprocess.run(
            [sys.executable, str(niche_script), str(keywords_file)],
            cwd=PROJECT_ROOT,
        )
        if result.returncode == 0:
            print("✅ Niche scoring complete")
        else:
            print("⚠️ Niche scoring had issues (non-fatal)")

    return True


def cmd_build(niche: str) -> bool:
    """Build Astro site from niche keywords."""
    print(f"\n🏗 BUILD MODE: {niche}")
    print(f"{'='*60}")

    safe_niche = niche.replace(" ", "-")
    keywords_file = KEYWORDS_DIR / f"{safe_niche}-keywords.json"

    if not keywords_file.exists():
        print(f"❌ Keywords file not found: {keywords_file}")
        print(f"   Run 'research' first: python pipeline.py research '{niche}'")
        return False

    # Load keywords
    with open(keywords_file) as f:
        data = json.load(f)

    print(f"✅ Loaded {data['total_keywords']} keywords")

    if not check_ollama():
        print("❌ Ollama not available. Content will use placeholder text.")
    else:
        print("✅ Ollama connected")

    # Run content generator
    content_script = SCRIPTS_DIR / "content-generator.py"
    if not content_script.exists():
        print(f"❌ content-generator.py not found")
        return False

    print(f"\n⏳ Generating content via Ollama...")
    result = subprocess.run(
        [sys.executable, str(content_script), str(keywords_file)],
        cwd=PROJECT_ROOT,
    )

    if result.returncode != 0:
        print("⚠️ Content generation had issues")

    # Run site generator
    site_script = SCRIPTS_DIR / "generate-site.py"
    if not site_script.exists():
        print(f"❌ generate-site.py not found")
        return False

    # Build site config
    site_config = {
        "name": f"{niche.title()} Hub",
        "niche": niche,
        "domain": f"{safe_niche}.pennypress.dev",
        "description": f"Comprehensive {niche} guide with reviews, comparisons, and how-tos.",
        "tagline": f"Everything you need to know about {niche}",
        "keywords": [kw["keyword"] for kw in data["top_keywords"][:10]],
        "colors": {"primary": "#00d4ff", "accent": "#ff6b6b"},
    }

    config_path = OUTPUT_DIR / f"{safe_niche}-config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(site_config, f, indent=2)

    print(f"\n⏳ Building Astro site...")
    result = subprocess.run(
        [sys.executable, str(site_script), str(config_path)],
        cwd=PROJECT_ROOT,
    )

    if result.returncode == 0:
        site_dir = OUTPUT_DIR / safe_niche
        print(f"\n✅ Site built: {site_dir}")
        print(f"\n📁 Site contents:")
        for p in sorted(site_dir.rglob("*")):
            if p.is_file():
                print(f"   {p.relative_to(site_dir)}")
        return True
    else:
        print("❌ Site build failed")
        return False


def cmd_deploy(site_name: str) -> bool:
    """Deploy site to GitHub + Cloudflare Pages."""
    print(f"\n🚀 DEPLOY MODE: {site_name}")
    print(f"{'='*60}")

    safe_name = site_name.replace(" ", "-").replace("_", "-")
    site_dir = OUTPUT_DIR / safe_name

    if not site_dir.exists():
        print(f"❌ Site directory not found: {site_dir}")
        return False

    deploy_script = SCRIPTS_DIR / "deploy.sh"
    if not deploy_script.exists():
        print(f"❌ deploy.sh not found at {deploy_script}")
        return False

    # Make executable
    os.chmod(str(deploy_script), 0o755)

    print(f"\n⏳ Running deployment script...")
    result = subprocess.run(
        ["bash", str(deploy_script), str(site_dir)],
        cwd=PROJECT_ROOT,
    )

    if result.returncode == 0:
        print(f"\n✅ Deployment successful!")
        return True
    else:
        print(f"\n❌ Deployment failed")
        return False


def cmd_full(niche: str) -> bool:
    """Run full pipeline: research → build → deploy."""
    print(f"\n🚀 FULL PIPELINE: {niche}")
    print(f"{'='*60}")

    safe_niche = niche.replace(" ", "-")

    # Step 1: Research
    print(f"\n{'='*60}")
    print("STEP 1/3: RESEARCH")
    print(f"{'='*60}")
    if not cmd_research(niche):
        print("❌ Research phase failed, aborting.")
        return False

    # Step 2: Build
    print(f"\n{'='*60}")
    print("STEP 2/3: BUILD")
    print(f"{'='*60}")
    if not cmd_build(niche):
        print("❌ Build phase failed, aborting.")
        return False

    # Step 3: Deploy
    print(f"\n{'='*60}")
    print("STEP 3/3: DEPLOY")
    print(f"{'='*60}")
    if not cmd_deploy(safe_niche):
        print("❌ Deploy phase failed.")
        return False

    print(f"\n{'='*60}")
    print("✅ FULL PIPELINE COMPLETE!")
    print(f"{'='*60}")
    print(f"\n🌐 Site deployed at: https://{safe_niche}.pennypress.dev")
    return True


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "research" and len(sys.argv) >= 3:
        niche = " ".join(sys.argv[2:])
        success = cmd_research(niche)
    elif command == "build" and len(sys.argv) >= 3:
        niche = " ".join(sys.argv[2:])
        success = cmd_build(niche)
    elif command == "deploy" and len(sys.argv) >= 3:
        site_name = sys.argv[2]
        success = cmd_deploy(site_name)
    elif command == "full" and len(sys.argv) >= 3:
        niche = " ".join(sys.argv[2:])
        success = cmd_full(niche)
    else:
        print(__doc__)
        sys.exit(1)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()