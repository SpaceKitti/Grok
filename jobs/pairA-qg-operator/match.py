"""MATCH: D1-D7 against P1 + P2 (+ curve). Each row PASS / FAIL (tested, not assumed); D6, D7 inherited from H_A."""
from __future__ import annotations

import numpy as np

INHERIT = "INHERITED FROM H_A, not from P1"


def riemann_hurwitz(S, C, P):
    """[computed] y^2 = 4v^2(eps^2 - eps_EP^2): degree-2 cover of the eps-sphere; branch points = odd-monodromy points."""
    E = S["EPS_EP"]
    inf = C["infinity"]
    mo = C["monodromy"]
    finite = [r for r in inf["roots"]]
    tips_ok = inf["roots_imag"] < 1e-12 and np.allclose(sorted(finite), [-E, E], atol=1e-12, rtol=0) and all(d > 0 for d in inf["dy2"])
    odd_finite = int(mo["+ε_EP once"]["n"] == 1) + int(mo["−ε_EP once"]["n"] == 1)
    no_inf = all(c["n_branches"] == [0, 0] for c in inf["circles"].values())
    n_branch = odd_finite + (0 if no_inf else 1)
    chi_curve = 2 * 2 - n_branch * (2 - 1)          # Riemann-Hurwitz, degree 2 over the sphere (chi = 2), ramification e = 2
    genus = (2 - chi_curve) // 2
    chi_p2 = P["p2"]["gb"] / (2 * np.pi)
    cone = P["p2"]["cone_final"]
    p2_ok = abs(chi_p2 - 2) < 1e-4 and all(abs(c / (2 * np.pi) - 2) < 1e-3 for c in cone.values())
    ok = tips_ok and no_inf and n_branch == 2 and chi_curve == 2 and genus == 0 and p2_ok
    circ = "; ".join(f"|ε| = {Rf:g} ε_EP: branches n = {c['n_branches'][0]}, {c['n_branches'][1]} (return), max ||y/(2vε)| − 1| = {c['asym']:.1e}" for Rf, c in inf["circles"].items())
    line = (f"Riemann–Hurwitz cross-check [computed]: {'PASS' if ok else 'FAIL'} — y² = 4v²(ε² − ε_EP²) is quadratic in ε; finite branch points = zeros of y² at "
            f"{inf['roots'][0]/E:+.12f}, {inf['roots'][1]/E:+.12f} ε_EP (simple zeros, one-turn monodromy n = 1 at each); no branching at infinity ({circ}); "
            f"χ = 2·2 − {n_branch} = {chi_curve}, genus {genus}: a genus-0 double cover branched only at ±ε_EP. "
            f"P2: χ = {chi_p2:.6f} (Gauss–Bonnet with cones), 4π cone points exactly at ±ε_EP — same topology and branch points.")
    return ok, line


def run(S, C, P, h_before, h_after, c_files):
    E = S["EPS_EP"]
    p2, rows = P["p2"], []
    D = {r["id"]: r for r in S["D"]}

    # D1
    ok1 = p2["chart_ok"] and p2["link"] < 1e-12
    rows.append({"id": "D1", "claim": D["D1"]["claim"], "result": "PASS" if ok1 else "FAIL", "tag": "[computed]",
                 "reason": f"F > 0 exactly on the interior of Γ ({p2['n_pos']} of {p2['n_grid']} real grid points, all with |ε| < ε_EP and every such point) and F(±ε_EP) = {p2['tipF'][0]:.1f}, {p2['tipF'][1]:.1f}: "
                           f"the Euclidean chart of P2 is Γ, the handoff's chart; F = −y²/(4v²) (residual {p2['link']:.1e}), so F > 0 ⇔ y² < 0 ⇔ λ−λ_EP imaginary (probe D1 fact)."})
    # D2
    ec, ew = C["exp_curve"], P["wkb"]["exponent"]
    eH = {nm: S["gap_fit"](S, s * E)["exponent"] for s, nm in ((+1, "+ε_EP"), (-1, "−ε_EP"))}
    ok2 = p2["tipF"] == (0.0, 0.0) and all(abs(v - 0.5) < 0.02 for v in list(ec.values()) + list(eH.values()) + [ew])
    rows.append({"id": "D2", "claim": D["D2"]["claim"], "result": "PASS" if ok2 else "FAIL", "tag": "[computed]",
                 "reason": f"F = 0 at both tips (the chart dies there); square-root gap: curve exponent {ec['+ε_EP']:.4f} / {ec['−ε_EP']:.4f}, "
                           f"H_A exponent {eH['+ε_EP']:.4f} / {eH['−ε_EP']:.4f}, P1 WKB |p+−p−| exponent {ew:.4f} (same local √ form at a turning point [standard analogy])."})
    # D3
    mo = C["monodromy"]
    cone = p2["cone_final"]
    J2, J4 = S["Jhat2"], S["Jhat4"]
    ok3 = (mo["+ε_EP once"]["n"] == 1 and mo["−ε_EP once"]["n"] == 1 and mo["+ε_EP twice"]["n"] == 0 and mo["−ε_EP twice"]["n"] == 0
           and mo["both tips once (r = 2 ε_EP)"]["n"] == 0 and all(abs(c / (2 * np.pi) - 2) < 1e-3 for c in cone.values())
           and P["wkb"]["n_once"] == 1 and P["wkb"]["n_twice"] == 0 and C["cover_all"]
           and float(np.linalg.norm(J4 - np.eye(2))) < 1e-10 and abs(J2[0, 0]) < 1e-8)
    rows.append({"id": "D3", "claim": D["D3"]["claim"], "result": "PASS" if ok3 else "FAIL", "tag": "[computed]; 4π cone ↔ Jhat4 = I [by construction, given τ_E = 4π/ε_EP from the handoff]",
                 "reason": f"curve: y → −y once around each tip (n = 1), returns after two turns (n = 0) and around both tips (n = 0); P1 WKB branches swap once / return twice [standard analogy]; "
                           f"cone angle at each tip {cone['+ε_EP']/np.pi:.6f}π / {cone['−ε_EP']/np.pi:.6f}π (double cover); handoff Jhat2 swap, ‖Jhat4−I‖ = {float(np.linalg.norm(J4 - np.eye(2))):.1e}; "
                           f"U_G = Φ(n) on all 6 probe loops: {'YES' if C['cover_all'] else 'NO'}."})
    # D4
    dt = C["detours"]
    ok4 = all(d["swapped"] and d["min_gap"] > 0 for d in dt.values())
    rows.append({"id": "D4", "claim": D["D4"]["claim"], "result": "PASS" if ok4 else "FAIL", "tag": "[computed, equivalent to 2π swap]",
                 "reason": "two sheets y = ± continue past each tip; two-detour test on the curve (±0.75 → ±1.25 ε_EP, semicircles r = 0.25 ε_EP): "
                           + "; ".join(f"{nm}: y_above = {d['y_above'].real:+.6f}{d['y_above'].imag:+.1e}i, y_below = {d['y_below'].real:+.6f}{d['y_below'].imag:+.1e}i, swapped {'YES' if d['swapped'] else 'NO'}, min |y| = {d['min_gap']:.6f}" for nm, d in dt.items())
                           + ". Not new information (same fact as the one-tip swap)."})
    # D5
    c_ok = bool(c_files) and all(h_before.get(p) == h_after.get(p) for p in c_files)
    rows.append({"id": "D5", "claim": D["D5"]["claim"], "result": "PASS" if c_ok else "FAIL", "tag": "[by construction]",
                 "reason": f"P1 + P2 involve only the two sheets y = ± (A, B); C never enters. C-related handoff files ({len(c_files)}) unchanged by SHA-256: {'YES' if c_ok else 'NO'}."})
    # D6, D7
    herm = P["dir"]["herm"]
    ev_common = (f"P1 is Hermitian (FD matrix ‖H − H†‖ = {herm:.1e}, real spectrum) and P2 is a real metric: neither is dissipative. "
                 f"H_A is non-Hermitian (‖H_A − H_A†‖ = {P['HA_nonherm']:.3f} at ε = 0.5 ε_EP). ")
    dl = S["drive_lines"]
    rows.append({"id": "D6", "claim": D["D6"]["claim"], "result": INHERIT, "tag": "[inherited: H_A loss]",
                 "reason": ev_common + f"Probe D6 {'PASS' if D['D6']['result'] else 'FAIL'}; drive-return: " + " ".join(sorted((l for l in dl if "missing mechanism:" in l or l.startswith("Signed off")), key=lambda l: "Signed off" in l)).rstrip(".") + "."})
    rows.append({"id": "D7", "claim": D["D7"]["claim"], "result": INHERIT, "tag": "[inherited: H_A loss]",
                 "reason": ev_common + f"Probe D7 {'PASS' if D['D7']['result'] else 'FAIL'}; drive-return: " + " ".join(sorted((l for l in dl if "start 1.25" in l or l.startswith("**Signed off")), key=lambda l: "Signed off" in l)).rstrip(".") + "."})
    return rows
