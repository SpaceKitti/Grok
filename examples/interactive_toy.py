"""Viz smoke entry point (alias of examples/smoke_plot.py).

Replaces the previous empty placeholder. Runs a short NS (or --mhd) case and
writes smoke_monitors.csv + smoke_monitors.png.

    python examples/interactive_toy.py
    python examples/interactive_toy.py --mhd
"""

from __future__ import annotations

import runpy
from pathlib import Path

if __name__ == "__main__":
    target = Path(__file__).resolve().parent / "smoke_plot.py"
    runpy.run_path(str(target), run_name="__main__")
