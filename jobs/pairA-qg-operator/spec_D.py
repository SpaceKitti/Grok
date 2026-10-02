r"""SPEC for pairA-qg-operator: D1-D7 loaded from the probe surface (its dictionary, cross-checked against its RESULTS.md),
handoff constants asserted against Akitti's numbers (not hard-coded as inputs), and hashing of the loaded folders.
Nothing here writes into the loaded folders (bytecode writing is disabled before any import from them)."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

PROBE = Path(r"C:\Users\Akitt\pairA-qg-probe-surface")
HANDOFF = Path(r"C:\Users\Akitt\pairA-qg-handoff")
DRIVE = Path(r"C:\Users\Akitt\pairA-drive-return")
LOADED = [PROBE, HANDOFF, DRIVE]

# Akitti's numbers: used ONLY for agreement asserts, never as model inputs.
AKITTI = {"EPS_EP": 0.51368066, "LAM_EP": -0.308425j, "V": -0.360253, "TAU": 24.46339}
TOL = {"EPS_EP": 1e-8, "LAM_EP": 1e-12, "V": 1e-12, "TAU": 1e-5}


def hash_tree(roots=LOADED) -> dict:
    out = {}
    for root in roots:
        for p in sorted(root.rglob("*")):
            if p.is_file():
                out[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def _probe_module(name):
    """Import a module from the probe-surface folder (read-only, no bytecode)."""
    if str(PROBE) not in sys.path:
        sys.path.append(str(PROBE))
    return __import__(name)


def load(h_before: dict) -> dict:
    import numpy as np

    LS = _probe_module("load_surface")        # probe surface loader (imports handoff seed/tracker/wick_lorentzian)
    S = LS.load()
    import seed                                # handoff seed.py (already on sys.path via LS.load)

    E, V, A, B = float(seed.EPS_EP), float(seed.V), float(seed.A), float(seed.B)
    formula = abs(A - B) / (2 * abs(V))
    lam_formula = -0.5j * (A + B)
    asserts = []

    def chk(name, ok, text):
        assert ok, (name, text)
        asserts.append((name, text))

    chk("eps_EP", abs(E - formula) < 1e-15 and abs(E - AKITTI["EPS_EP"]) < TOL["EPS_EP"],
        f"ε_EP = {E:.12f} = |a−b|/(2|v|) = {formula:.12f}; |ε_EP − 0.51368066| = {abs(E-AKITTI['EPS_EP']):.1e}")
    chk("lam_EP", abs(complex(seed.LAM_EP) - lam_formula) < 1e-15 and abs(complex(seed.LAM_EP) - AKITTI["LAM_EP"]) < TOL["LAM_EP"],
        f"λ_EP = {complex(seed.LAM_EP).imag:+.9f}i = −i(a+b)/2; |λ_EP − (−0.308425i)| = {abs(complex(seed.LAM_EP)-AKITTI['LAM_EP']):.1e}")
    chk("v", abs(V - AKITTI["V"]) < TOL["V"], f"v = {V} (Akitti −0.360253)")
    gam = S["GAMMA"]
    chk("Gamma", abs(gam[0] + E) < 1e-15 and abs(gam[1] - E) < 1e-15,
        f"Γ = [{gam[0]:.9f}, {gam[1]:.9f}] = [−ε_EP, ε_EP]; handoff chart support: {S['chart'].get('real_section_support', '?')}")
    J2, J4 = S["Jhat2"], S["Jhat4"]
    j2_swap = abs(J2[0, 0]) < 1e-8 and abs(J2[1, 1]) < 1e-8 and abs(abs(J2[0, 1]) - 1) < 1e-8 and abs(abs(J2[1, 0]) - 1) < 1e-8
    chk("Jhat2 swap", j2_swap, f"Jhat2 = [[{J2[0,0]:.1e}, {J2[0,1]:.6f}], [{J2[1,0]:.6f}, {J2[1,1]:.1e}]] (off-diagonal: swap)")
    chk("Jhat4 = I", float(np.linalg.norm(J4 - np.eye(2))) < 1e-10, f"‖Jhat4 − I‖ = {float(np.linalg.norm(J4 - np.eye(2))):.1e}")
    summ = json.loads((HANDOFF / "outputs" / "summary.json").read_text(encoding="utf-8"))
    tau = 4 * np.pi / E
    chk("tau", abs(tau - AKITTI["TAU"]) < TOL["TAU"] and abs(tau - summ["tau"]) < 1e-12,
        f"τ = 4π/ε_EP = {tau:.8f}; handoff summary.json tau = {summ['tau']:.8f}; |τ − 24.46339| = {abs(tau-AKITTI['TAU']):.1e}")
    hist = summ["hist"]
    probe_txt = (HANDOFF / "RESULTS_probe.md").read_text(encoding="utf-8", errors="replace")
    chk("A/B WRITE, C held", hist["A"]["score"] == "WRITE" and hist["B"]["score"] == "WRITE" and hist["C"]["score"] == "NOT-SELECTED"
        and re.search(r"^held: C\s*$", probe_txt, re.M) is not None,
        f"summary.json scores A = {hist['A']['score']}, B = {hist['B']['score']}, C = {hist['C']['score']}; RESULTS_probe.md: 'held: C'")

    # D1-D7 from the probe surface dictionary (recomputed by its own code), cross-checked against its RESULTS.md
    cover = _probe_module("cover")
    dic = _probe_module("dictionary")
    cov_rows = cover.run_cover(S)
    rows = dic.build(S, cov_rows, h_before, h_before)
    presults = (PROBE / "RESULTS.md").read_text(encoding="utf-8")
    first = presults.splitlines()[0]
    verdict_ok = "SURFACE READY — QG probe may use D1–D7" in presults
    for r in rows:
        line = next((l for l in presults.splitlines() if l.startswith(f"| {r['id']} |")), "")
        r["in_results"] = (r["claim"] in line) and (r["tag"] in line) and (("**PASS**" in line) == bool(r["result"]))
    chk("probe D1–D7", all(r["result"] and r["in_results"] for r in rows) and verdict_ok,
        f"probe surface D1–D7 all PASS (recomputed by its dictionary.py; each row's claim, tag and PASS found in its RESULTS.md); probe verdict 'SURFACE READY — QG probe may use D1–D7'; probe sign-off: {first}")

    # inside no chirality / outside chirality on slow drive (drive-return npz, probe dictionary helpers)
    W0 = dic.winners(DRIVE / "outputs" / "drive.npz")
    W1 = dic.winners(DRIVE / "outputs" / "drive_start1p25.npz")
    sp0 = sorted({k[0] for k in W0})
    inside_none = all(W0[(sp, "ccw", s)][m][0] == W0[(sp, "cw", s)][m][0] for sp in sp0 for s in "AB" for m in (1, 2))
    outside_slow = all(dic.chirality(W1, sp)[m][0] for sp in ("slow20", "slow40", "slow100") for m in (1, 2))
    outside_fast = any(dic.chirality(W1, "fast")[m][0] for m in (1, 2))
    chk("inside/outside chirality", inside_none and outside_slow,
        f"inside (drive.npz, start 0.75 ε_EP): ccw and cw pick the same mode at all speeds {sp0}: {inside_none}; outside (drive_start1p25.npz, start 1.25 ε_EP): "
        f"cw/ccw pick opposite modes at γT = 20, 40, 100: {outside_slow} (γT = 1: {outside_fast})")
    drive_lines = [l.strip() for f in ("RESULTS.md", "RESULTS_start1p25.md") for l in (DRIVE / f).read_text(encoding="utf-8").splitlines()
                   if l.startswith("**missing mechanism") or "Signed off" in l]
    S.update({"asserts": asserts, "D": rows, "cover_rows": cov_rows, "tau": tau, "summary": summ, "drive_lines": drive_lines,
              "probe_signoff": first, "W0": W0, "W1": W1, "gap_fit": dic.gap_fit})
    return S
