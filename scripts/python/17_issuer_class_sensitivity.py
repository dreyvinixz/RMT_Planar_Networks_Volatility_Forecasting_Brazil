from __future__ import annotations

"""Compatibility entry point for the same-date, liquidity-tiebroken analysis."""

from pathlib import Path
import runpy


def main() -> None:
    corrected = Path(__file__).with_name("23_issuer_panel_same_dates.py")
    runpy.run_path(str(corrected), run_name="__main__")


if __name__ == "__main__":
    main()
