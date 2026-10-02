"""Diagnostic (post hoc, not used in the verdict): dt convergence for the interior starts at gamma T = 40.
Refines dt by factor 1, 2, 4, 8 relative to drive-return's dt rule and prints the 4pi weight of sheet B."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import sweep as SW


def conv_table(fracs=(0.25, 0.50, 0.75), tips=(+1, -1), gT=40.0, factors=(1, 2, 4, 8)):
    out = []
    for sgn in tips:
        tip = sgn * SW.E
        for f in fracs:
            SW.set_loop(sgn * f * SW.E, tip)
            for dn, s in SW.DIRS.items():
                for st in (0, 1):
                    ws = [float(SW.D.run_drive(s, gT, st, factor=k)["marks"][2]["w"][1]) for k in factors]
                    out.append({"tip": sgn, "frac": f, "dir": dn, "start": "AB"[st], "wB": ws})
    return factors, out


if __name__ == "__main__":
    import json
    fac, rows = conv_table()
    (Path(__file__).resolve().parent / "outputs").mkdir(exist_ok=True)
    (Path(__file__).resolve().parent / "outputs" / "diag_dt.json").write_text(json.dumps({"factors": list(fac), "rows": rows}, indent=1), encoding="utf-8")
    for r in rows:
        print(r["tip"], r["frac"], r["dir"], r["start"], " ".join(f"{w:.5f}" for w in r["wB"]))
