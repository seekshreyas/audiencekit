"""Prepare an AudienceKit persona panel from a full GSS file.

Usage:
    uv run python scripts/extract_panel.py path/to/gss7224_r3.dta \
        --years 2022 2024 --out data/gss_panel.csv

The raw GSS cumulative file is not bundled. Download it from NORC, then use
this script to create a local weighted persona frame.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audiencekit.gss import write_gss_panel


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="Path to a GSS .dta, .csv, or .parquet file")
    parser.add_argument("--years", nargs="*", type=int, default=None, help="GSS years to keep")
    parser.add_argument("--out", default="data/gss_panel.csv", help="Output CSV path")
    args = parser.parse_args()

    out = write_gss_panel(args.source, args.out, years=args.years)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
