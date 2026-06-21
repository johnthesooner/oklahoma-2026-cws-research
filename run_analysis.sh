#!/usr/bin/env bash
#
# run_analysis.sh — one-command reproduction of the analysis assets.
# Equivalent to `make all`, for environments without GNU make.
#
set -euo pipefail

PYTHON="${PYTHON:-python3}"
cd "$(dirname "$0")"

echo "==> Using interpreter: $($PYTHON --version 2>&1)"
echo "==> Step 1/2: validate datasets"
"$PYTHON" scripts/validate_data.py

echo "==> Step 2/2: build report assets (charts + manifest)"
"$PYTHON" scripts/build_report_assets.py

echo "==> Done. See charts/*.png, build_manifest.json, and report/."
