#!/usr/bin/env python3
"""Generate remaining 7 Bitcoin beginner articles for PennyPress."""
import subprocess, os, time, glob, sys

OUTDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "content", "bitcoin-beginners")
SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fast-writer.py")

topics = [
    "Bitcoin vs Ethereum: Key Differences Explained",
    "How to Accept Bitcoin Payments as a Business",
    "Bitcoin Price History: From Pennies to Thousands",
    "How to Avoid Bitcoin Scams and Fraud",
    "Bitcoin Tax Guide: What You Need to Know",
    "The Environmental Impact of Bitcoin Mining",
    "Bitcoin Forks: Hard Forks vs Soft Forks Explained",
]

os.makedirs(OUTDIR, exist_ok=True)

for i, topic in enumerate(topics):
    print(f"[{i+1}/7] {topic}...", flush=True)
    result = subprocess.run(
        [sys.executable, SCRIPT, topic, "bitcoin-beginners", OUTDIR, "2500"],
        capture_output=True, text=True, timeout=120
    )
    print(result.stdout.strip(), flush=True)
    if result.returncode != 0:
        print(f"  STDERR: {result.stderr.strip()[:300]}", flush=True)
    time.sleep(1)

files = glob.glob(os.path.join(OUTDIR, "*.md"))
total_chars = sum(os.path.getsize(f) for f in files)
print(f"\n=== DONE: {len(files)} total articles, {total_chars:,} bytes ===", flush=True)
for f in sorted(files):
    size = os.path.getsize(f)
    print(f"  {os.path.basename(f)} ({size:,} bytes)", flush=True)
