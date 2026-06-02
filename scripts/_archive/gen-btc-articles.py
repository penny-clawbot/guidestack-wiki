#!/usr/bin/env python3
"""Generate 15 Bitcoin beginner articles for PennyPress."""
import subprocess, os, time, glob, sys

OUTDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "content", "bitcoin-beginners")
SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fast-writer.py")

topics = [
    "What is Bitcoin: A Complete Beginners Guide",
    "How to Buy Bitcoin for the First Time",
    "Bitcoin Wallets Explained: Hardware Software and Paper Wallets",
    "How to Keep Your Bitcoin Safe and Secure",
    "What is Bitcoin Mining and How Does It Work",
    "Understanding Bitcoin Halving Cycles",
    "What is the Bitcoin Lightning Network",
    "Bitcoin vs Ethereum: Key Differences Explained",
    "How to Accept Bitcoin Payments as a Business",
    "Bitcoin Price History: From Pennies to Thousands",
    "What Are Bitcoin ETFs and Should You Invest",
    "How to Avoid Bitcoin Scams and Fraud",
    "Bitcoin Tax Guide: What You Need to Know",
    "The Environmental Impact of Bitcoin Mining",
    "Bitcoin Forks: Hard Forks vs Soft Forks Explained",
]

os.makedirs(OUTDIR, exist_ok=True)

for i, topic in enumerate(topics):
    print(f"[{i+1}/15] {topic}...")
    result = subprocess.run(
        [sys.executable, SCRIPT, topic, "bitcoin-beginners", OUTDIR, "2500"],
        capture_output=True, text=True, timeout=120
    )
    print(result.stdout.strip())
    if result.returncode != 0:
        print(f"  STDERR: {result.stderr.strip()[:300]}")
    time.sleep(1)

files = glob.glob(os.path.join(OUTDIR, "*.md"))
print(f"\n=== DONE: {len(files)} articles generated ===")
for f in sorted(files):
    size = os.path.getsize(f)
    print(f"  {os.path.basename(f)} ({size} bytes)")
