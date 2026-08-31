"""freeze_ext gap sweep {0.10, 0.15, 0.20, 0.25}. Same NS+MHD Crow setup.

    python examples/freeze_gap_sweep.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from freeze_sweep_res import _run, _print_freeze
from chive_ns import default_scar_centres


def main():
    centres = default_scar_centres(1.0, 4, 3)
    print("N=48 t=0.36 tubes+4-scar B0=0.08 η=1e-3 b_guide=z  "
          "unmollified induction  freeze gap {0.10,0.15,0.20,0.25}",
          flush=True)
    rows = []
    for f in (0.10, 0.15, 0.20, 0.25):
        rows.append(_run(f"f={f:g}", 48, f, centres))
    _print_freeze(rows)
    return rows


if __name__ == "__main__":
    main()
