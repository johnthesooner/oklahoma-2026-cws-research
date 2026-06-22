#!/usr/bin/env python3
"""
build_report_assets.py — one-command, deterministic rebuild of all analysis assets.

Pipeline:
  1. Validate every dataset (scripts/validate_data.py). Abort the build on failure.
  2. Regenerate the full chart suite (charts/make_charts.py).
  3. Write a deterministic build manifest (build_manifest.json): dataset row counts,
     chart inventory, and SHA-256 checksums of every data + chart file.

Deterministic by design: no timestamps or RNG are embedded, so identical inputs
produce an identical manifest (good for `make all` and CI diffing).
No network access; no data is fabricated or modified.
"""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CHARTS = ROOT / "charts"
SCRIPTS = ROOT / "scripts"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def run(label: str, args: list[str]) -> None:
    print(f"\n>>> {label}: {' '.join(args)}")
    res = subprocess.run(args, cwd=ROOT)
    if res.returncode != 0:
        print(f"!!! {label} FAILED (exit {res.returncode}). Aborting build.")
        sys.exit(res.returncode)


def main() -> int:
    print("=" * 70)
    print("BUILD REPORT ASSETS — 2026 Oklahoma Sooners CWS research package")
    print("=" * 70)

    # 1. Validate (hard gate)
    run("Validate datasets", [sys.executable, str(SCRIPTS / "validate_data.py")])

    # 2. Charts
    run("Generate charts", [sys.executable, str(CHARTS / "make_charts.py")])

    # 2b. Phase 11 championship comparison (charts 11-15 + results md)
    run("Championship analysis (Phase 11)", [sys.executable, str(SCRIPTS / "championship_analysis.py")])

    # 2c. P0 audit additions: game log, luck tests, ratings, market (charts 16-18 + results md)
    run("Game-log / market analysis", [sys.executable, str(SCRIPTS / "gamelog_market_analysis.py")])

    # 2d. Phase 13 (P1): survivorship-corrected modeling (charts 19-22 + results md)
    run("Championship model (Phase 13)", [sys.executable, str(SCRIPTS / "championship_model.py")])

    # 3. Deterministic manifest (sorted for stable output)
    import csv
    datasets = {}
    for p in sorted(DATA.glob("*.csv")):
        with p.open() as fh:
            rows = sum(1 for _ in fh) - 1  # minus header
        datasets[p.name] = {"data_rows": rows, "sha256": sha256(p)}

    charts = {p.name: {"sha256": sha256(p)} for p in sorted(CHARTS.glob("*.png"))}

    manifest = {
        "project": "oklahoma-2026-cws-research",
        "note": "Deterministic build manifest. No timestamps embedded by design.",
        "datasets": datasets,
        "charts": charts,
        "dataset_count": len(datasets),
        "chart_count": len(charts),
    }
    out = ROOT / "build_manifest.json"
    out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    print("\n" + "=" * 70)
    print(f"BUILD OK — {len(datasets)} datasets, {len(charts)} charts")
    print(f"Manifest: {out.relative_to(ROOT)}")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
