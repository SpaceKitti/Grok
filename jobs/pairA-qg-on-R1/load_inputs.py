"""Read-only loaders for pairA-qg-on-R1: pairA-jt-4d (R1 data) and pairA-qg-probe-surface (D1-D7).
Bytecode writing is disabled before any import so nothing is written into the loaded folders."""
from __future__ import annotations

import hashlib
import re
import sys

sys.dont_write_bytecode = True
from pathlib import Path  # noqa: E402

JT4D = Path(r"C:\Users\Akitt\pairA-jt-4d")
SURF = Path(r"C:\Users\Akitt\pairA-qg-probe-surface")
LOADED = [JT4D, SURF]


def hash_tree(roots=LOADED) -> dict:
    out = {}
    for root in roots:
        for p in sorted(Path(root).rglob("*")):
            if p.is_file():
                out[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def load_r1():
    """R1 numbers from pairA-jt-4d/jt2d.py (import, read-only) + R1 lines quoted from its RESULTS.md."""
    for d in (JT4D, SURF):
        if str(d) not in sys.path:
            sys.path.append(str(d))
    import jt2d  # pairA-jt-4d
    txt = (JT4D / "RESULTS.md").read_text(encoding="utf-8")
    target = [ln.strip() for ln in txt.splitlines() if "R1 (AdS2 x S2, r = eps_EP) is the 4D target" in ln]
    rline = [ln.strip() for ln in txt.splitlines() if ln.strip().startswith("| R1 (r = ")]
    return {"EPS_EP": float(jt2d.EPS_EP), "LAM_EP": complex(jt2d.LAM_EP), "V": float(jt2d.V), "y2": jt2d.y2,
            "track_y": jt2d.track_y, "SHEETS": dict(jt2d.SHEETS), "TAU_SWAP": float(jt2d.TAU_SWAP),
            "target_line": target[0] if target else None, "region_row": rline[0] if rline else None}


def load_surface():
    """D1-D7 rows (verdict per row) from pairA-qg-probe-surface/RESULTS.md, and its sheet convention y_cut_gamma."""
    import load_surface as LS  # pairA-qg-probe-surface (module-level imports: hashlib, re, sys, pathlib only)
    txt = (SURF / "RESULTS.md").read_text(encoding="utf-8")
    rows = {}
    for ln in txt.splitlines():
        m = re.match(r"\|\s*(D[1-7])\s*\|\s*(.*?)\s*\|\s*\*\*(PASS|FAIL)\*\*\s*\|", ln)
        if m:
            rows[m.group(1)] = {"property": m.group(2), "result": m.group(3)}
    verdict = "SURFACE READY" in txt
    signed = txt.splitlines()[0].strip()
    return {"rows": rows, "ready": verdict, "signed": signed, "y_cut_gamma": LS.y_cut_gamma}
