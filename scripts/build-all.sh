#!/usr/bin/env bash
# build-all.sh — Rebuild entire PennyPress network
# Usage: bash scripts/build-all.sh [--parallel N]
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PARALLEL=1
REPORT_FILE="$PROJECT_DIR/data/build-report.json"

# Parse args
while [[ $# -gt 0 ]]; do
  case $1 in
    --parallel) PARALLEL="${2:-2}"; shift 2 ;;
    --report) REPORT_FILE="$2"; shift 2 ;;
    *) shift ;;
  esac
done

echo "═══════════════════════════════════════"
echo " 🏗️  PennyPress Network Rebuild"
echo "═══════════════════════════════════════"
echo ""

# Get all active sites
SITE_DIRS=($(ls -d "$PROJECT_DIR/output/sites"/*/ 2>/dev/null | sed 's/\/$//'))
TOTAL=${#SITE_DIRS[@]}

if [ $TOTAL -eq 0 ]; then
  echo "❌ No sites found in output/sites/"
  exit 1
fi

echo "Found $TOTAL sites to rebuild"
echo ""

SUCCESS=()
FAILED=()
declare -A RESULTS

for site_dir in "${SITE_DIRS[@]}"; do
  SITE_NAME=$(basename "$site_dir")
  CONFIG="$site_dir/site-config.json"
  
  if [ ! -f "$CONFIG" ]; then
    echo "⚠️  Skipping $SITE_NAME — no site-config.json"
    FAILED+=("$SITE_NAME")
    continue
  fi
  
  NICHE=$(python3 -c "import json; print(json.load(open('$CONFIG')).get('niche',''))" 2>/dev/null || echo "")
  
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "📦 Building: $SITE_NAME ($NICHE)"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  
  START=$(date +%s)
  
  if bash "$PROJECT_DIR/scripts/build-site.sh" "$SITE_NAME" "$NICHE" 2>&1; then
    END=$(date +%s)
    DURATION=$((END - START))
    SUCCESS+=("$SITE_NAME")
    RESULTS[$SITE_NAME]="success:${DURATION}s"
    echo "✅ $SITE_NAME built in ${DURATION}s"
  else
    END=$(date +%s)
    DURATION=$((END - START))
    FAILED+=("$SITE_NAME")
    RESULTS[$SITE_NAME]="failed:${DURATION}s"
    echo "❌ $SITE_NAME failed after ${DURATION}s"
  fi
  echo ""
done

# Generate report
echo "═══════════════════════════════════════"
echo " 📊 Build Report"
echo "═══════════════════════════════════════"
echo "Total: $TOTAL | ✅ Success: ${#SUCCESS[@]} | ❌ Failed: ${#FAILED[@]}"
echo ""

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Write JSON report
python3 << PYEOF
import json, os

report = {
  "timestamp": "$TIMESTAMP",
  "total": $TOTAL,
  "success": ${#SUCCESS[@]},
  "failed": ${#FAILED[@]},
  "sites": {}
}

for name, status in {
$(for s in "${SUCCESS[@]}"; do echo "  \"$s\": \"${RESULTS[$s]}\","; done)
$(for s in "${FAILED[@]}"; do echo "  \"$s\": \"${RESULTS[$s]}\","; done)
}.items():
    report["sites"][name] = status

os.makedirs(os.path.dirname("$REPORT_FILE"), exist_ok=True)
with open("$REPORT_FILE", 'w') as f:
    json.dump(report, f, indent=2)
PYEOF

echo "Report saved to: $REPORT_FILE"
echo ""

# List failures
if [ ${#FAILED[@]} -gt 0 ]; then
  echo "⚠️  Failed sites:"
  for s in "${FAILED[@]}"; do
    echo "  - $s"
  done
  exit 1
fi

echo "🎉 All sites built successfully!"
