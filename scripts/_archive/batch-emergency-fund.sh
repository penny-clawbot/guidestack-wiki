#!/bin/bash
# Batch generate 20 articles for smart-emergency-fund site
set -e

SCRIPT="/Users/penny/Documents/Penny/pseo-network/scripts/fast-writer.py"
OUTDIR="/Users/penny/Documents/Penny/pseo-network/output/sites/smart-emergency-fund/src/content/articles"
NICHE="emergency fund"
WORDS=2000

TOPICS=(
  "Emergency Fund Calculator How to Determine Your Exact Savings Target"
  "Best Emergency Fund Savings Strategies That Actually Work"
  "When to Use Your Emergency Fund and When Not To"
  "How to Rebuild Your Emergency Fund After a Withdrawal"
  "Best High-Yield Savings Accounts for Emergency Funds 2025"
  "Emergency Fund vs Credit Cards Which Should You Rely On"
  "Emergency Fund Planning for Gig Economy Workers and Freelancers"
  "Medical Emergency Financial Preparation Complete Guide"
  "Natural Disaster Financial Preparedness How to Protect Your Money"
  "Job Loss Survival Guide Financial Steps to Take Immediately"
  "Side Hustles to Build Your Emergency Fund Faster"
  "Emergency Fund Myths That Are Costing You Money"
  "How Much Emergency Fund You Need by Age and Lifestyle"
  "Automating Your Emergency Fund Savings Set It and Forget It"
  "Emergency Fund Investment Options Beyond Savings Accounts"
  "Teaching Kids About Emergency Funds Age-Appropriate Money Lessons"
  "Emergency Fund Strategies for Couples Merging Finances"
  "Emergency Fund Guide for Self-Employed and Small Business Owners"
  "Renters Emergency Fund Guide What Tenants Need to Save For"
  "Emergency Fund Tips for Seasonal and Contract Workers"
)

TOTAL=${#TOPICS[@]}
SUCCESS=0
FAIL=0

for i in "${!TOPICS[@]}"; do
  TOPIC="${TOPICS[$i]}"
  NUM=$((i+1))
  echo "[$NUM/$TOTAL] Generating: $TOPIC"
  
  python3 "$SCRIPT" "$TOPIC" "$NICHE" "$OUTDIR" "$WORDS"
  RESULT=$?
  
  if [ $RESULT -eq 0 ]; then
    SUCCESS=$((SUCCESS+1))
  else
    FAIL=$((FAIL+1))
  fi
  echo ""
done

echo "================================"
echo "Done! $SUCCESS succeeded, $FAIL failed out of $TOTAL"
