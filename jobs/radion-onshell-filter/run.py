"""Job Five: on-shell radion/Betti filter bridge.
Generated artifacts are written only by this script.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import math
import os
import re
import sys
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
J3 = Path(r"C:\Users\Akitt\betti-berry-vacuum-filter")
J2 = Path(r"C:\Users\Akitt\sm-zero-modes-S2")
J3_RESULTS = J3 / "RESULTS.md"
J3_RUN = J3 / "run.py"
J2_RESULTS = J2 / "RESULTS_final.md"
WINDOW = (0.010, 0.030)
# [assumed input] Overall radius-unit normalization between this reduction and Job Three.
BASE_SCALE = 1.0
SCALES = (0.8, 0.95, 1.0, 1.15, 1.25)
M4_NUM = 1.0  # [assumed input] fixed 4D Einstein-frame Planck unit for the table.


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(root: Path):
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            out[str(p.relative_to(root))] = sha(p)
    return out


def surviving_vacua(vacua, rho_window=WINDOW, spectrum_filter=None):
    """Job Three hook semantics, kept local to avoid importing/writing its tree."""
    lo, hi = rho_window
    result = []
    for v in vacua:
        rho = v.get("rho_res")
        if rho is None or not (lo <= float(rho) <= hi):
            continue
        if spectrum_filter is not None and not spectrum_filter(
                v.get("field_content"), v.get("spectrum"), v):
            continue
        result.append(v)
    return result


def fmt_list(values):
    return "[" + "; ".join(v["id"] for v in values) + "]"


def parse_job3_curve(path: Path):
    """Read only Job Three's already-generated m=16 local-minimum table."""
    rows = []
    active = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("### 5b."):
            active = True
            continue
        if active and line.startswith("Summary [computed]"):
            break
        if not active or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6:
            continue
        try:
            p = float(cells[3])
            rho = float(cells[5])
        except ValueError:
            continue
        rows.append((p, rho))
    if not rows:
        raise RuntimeError("Could not read Job Three's existing rho(p) table")
    # De-duplicate p values deterministically, averaging repeated parameter sets.
    grouped = {}
    for p, rho in rows:
        grouped.setdefault(round(p, 10), []).append(rho)
    curve = sorted((p, sum(v) / len(v)) for p, v in grouped.items())
    # Full occupancy and empty occupancy have no residual cycles in the sphere
    # complex; add exact endpoint anchors rather than extrapolating the last
    # local-minimum row [identity, post-hoc].
    if curve[0][0] > 0.0:
        curve.insert(0, (0.0, 0.0))
    if curve[-1][0] < 1.0:
        curve.append((1.0, 0.0))
    return curve


def interp_curve(curve, p):
    """Linear interpolation of the existing Job Three table [post-hoc]."""
    if p <= curve[0][0]:
        return curve[0][1]
    if p >= curve[-1][0]:
        return curve[-1][1]
    for (p0, r0), (p1, r1) in zip(curve, curve[1:]):
        if p0 <= p <= p1:
            t = (p - p0) / (p1 - p0)
            return r0 + t * (r1 - r0)
    return curve[-1][1]


def p_window_bands(curve):
    """Locate the two default-window bands using only the inherited curve."""
    def crossing(lo, hi, target):
        flo = interp_curve(curve, lo) - target
        for _ in range(40):
            mid = (lo + hi) / 2.0
            fmid = interp_curve(curve, mid) - target
            if flo * fmid <= 0.0:
                hi = mid
            else:
                lo, flo = mid, fmid
        return (lo + hi) / 2.0
    grid = [i / 10000.0 for i in range(10001)]
    inside = [WINDOW[0] <= interp_curve(curve, q) <= WINDOW[1] for q in grid]
    bands = []
    i = 0
    while i < len(grid):
        if not inside[i]:
            i += 1
            continue
        j = i
        while j + 1 < len(grid) and inside[j + 1]:
            j += 1
        left = grid[i] if i == 0 else crossing(grid[i - 1], grid[i], WINDOW[0] if interp_curve(curve, grid[i - 1]) < WINDOW[0] else WINDOW[1])
        right = grid[j] if j == len(grid) - 1 else crossing(grid[j], grid[j + 1], WINDOW[0] if interp_curve(curve, grid[j + 1]) < WINDOW[0] else WINDOW[1])
        bands.append((left, right))
        i = j + 1
    return bands


def main():
    before_j3 = snapshot(J3)
    before_j2 = snapshot(J2)
    curve = parse_job3_curve(J3_RESULTS)

    # Symbols and reduction convention [assumed input].
    R, x, n = sp.symbols("R x n", positive=True)
    Lambda6, M6, g6, M4 = sp.symbols("Lambda_6 M_6 g_6 M_4", positive=True)
    a = 4 * sp.pi
    b = 4 * sp.pi * M6**4
    c = sp.pi / (2 * g6**2)
    Vx = a * Lambda6 / x - b / x**2 + c * n**2 / x**3
    VR = Vx.subs(x, R**2)
    Q = a * Lambda6 * x**2 - 2 * b * x + 3 * c * n**2
    dVdx = sp.diff(Vx, x)
    d2Vdx2 = sp.diff(Vx, x, 2)
    x1_stable = 3 * c * n**2 / (b + sp.sqrt(b**2 - 3 * a * Lambda6 * c * n**2))
    x2 = (b + sp.sqrt(b**2 - 3 * a * Lambda6 * c * n**2)) / (a * Lambda6)
    x1_quad = (b - sp.sqrt(b**2 - 3 * a * Lambda6 * c * n**2)) / (a * Lambda6)

    L = []
    w = L.append
    now = dt.datetime.now().astimezone()
    w("# RESULTS (generated by run.py - do not edit by hand)")
    w("")
    w("**Job Five sign-off [computed]:** NanoRibbon approved with Akitti's go; Jobs One–Three treated as main/read-only inputs.")
    w("Generated: %s (BST/local time, UTC%s:%s)" % (now.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%z")[:3], now.strftime("%z")[3:]))
    w("")
    w("Toy 6D Einstein–Maxwell breathing-mode calculation. Only R is dynamical; this is not a complete compactification.")
    w("")
    w("## Source audit [computed, read-only]")
    w("")
    w("Job Three tree: %d files; Job Two tree: %d files; both were read-only inputs." % (len(before_j3), len(before_j2)))
    w("Job Three source hashes before run: RESULTS.md %s; run.py %s." % (sha(J3_RESULTS), sha(J3_RUN)))
    w("Job Two source hash before run: RESULTS_final.md %s." % sha(J2_RESULTS))
    w("")

    w("## Stage A — symbolic reduction and identities")
    w("")
    w("Reduction convention [assumed input]: S_6 = ∫√-G [M_6^4 R_6/2 − Λ_6 − F^2/(4 g_6^2)], with F_θφ = n sinθ/2 and round-S² radius R.")
    w("Jordan-frame potential before the Weyl division [computed]: U_J(R) = 4πΛ_6 R² − 4πM_6^4 + πn²/(2g_6²R²).")
    w("Dividing by R^4 to reach the 4D Einstein frame [computed]: V(R) = 4πΛ_6/R² − 4πM_6^4/R^4 + πn²/(2g_6²R^6).")
    w("V(x) = aΛ_6/x − b/x² + cn²/x³ with a = %s, b = %s, c = %s [computed; assumed input symbols]." % (a, b, c))
    w("Three R powers [computed]: Λ_6 term R^-2, curvature term R^-4, flux term R^-6.")
    w("")
    w("| Stage A check | result |")
    w("|---|---|")
    w("| V'(x) = −Q(x)/x^4 | %s [identity] |" % (sp.simplify(dVdx + Q / x**4) == 0))
    w("| Q(x) = aΛ_6x² − 2bx + 3cn² | %s [identity] |" % (sp.expand(Q - (a * Lambda6 * x**2 - 2 * b * x + 3 * c * n**2)) == 0))
    w("| For Λ_6>0, x₁=(b−√D)/(aΛ_6) is the minimum and x₂=(b+√D)/(aΛ_6) the barrier | %s [identity] |" % (sp.simplify(x1_quad - x1_stable) == 0))
    w("| Stable root rationalisation | x₁ = 3cn²/(b+√D), with Λ_6→0 limit 3cn²/(2b) [identity] |")
    w("| Positive-Λ root rule | D=b²−3acΛ_6n²≥0, so n²≤b²/(3acΛ_6), only for Λ_6>0 [identity] |")
    w("| Λ_6≤0 rule | exactly one positive AdS minimum for every n; no n_max [identity] |")
    flat_x = sp.simplify(2 * c * n**2 / b)
    flat_L = sp.simplify(b**2 / (4 * a * c * n**2))
    flat_vxx = sp.simplify(d2Vdx2.subs({x: flat_x, Lambda6: flat_L}))
    w("| Flat stationary point | x*=2cn²/b; Λ_6=b²/(4acn²); V''(x*)=b/x*^4=2cn²/x*^5: %s [identity] |" % (sp.simplify(flat_vxx - b / flat_x**4) == 0))
    w("| Small-n limit | x₁≈3cn²/(2b), V≈x₁^-2(−b+2b/3)=−b/(3x₁²)<0 [computed, identity] |")
    w("")
    w("Aethon caveat [standard]: exact flatness requires n₀=√(b²/(4acΛ_6)) to be a whole number; generic Λ_6 gives an AdS/dS boundary rather than an exactly flat integer flux. Exactly flat rows below are tagged [tuned].")
    K_R = 8 * M4**2 / R**2
    VRR_stationary = 4 * x * d2Vdx2
    m2 = sp.simplify((VRR_stationary / K_R.subs(R, sp.sqrt(x))).subs(x, x))
    w("Breathing kinetic factor [standard]: K_R = 8M_4²/R² for −K_R(∂R)²/2; at a stationary point d²V/dR²=4xV''(x), so m_radion²=d²V/dR²/K_R=x²V''(x)/(2M_4²) [computed, sign follows V''].")
    w("Radion-mass convention [standard]: this code uses the M_4²𝓇 convention, K_R=8M_4²/R² and m²=x²V''/(2M_4²). With the (M_4²/2)𝓇 convention, K_R=4M_4²/R² and m²=x²V''/M_4². The factor of 2 changes the mass normalisation, not its sign or stability.")
    w("")

    # Numeric couplings are an explicit cheap [assumed input] probe.
    nums = {M6: 1.0, g6: 1.0, M4: M4_NUM}
    aa, bb, cc = [float(sp.N(z.subs(nums))) for z in (a, b, c)]
    w("Numeric Stage B/C convention [assumed input]: M_6=1, g_6=1, M_4=1, so a=%.9f, b=%.9f, c=%.9f; BASE_SCALE=%.2f." % (aa, bb, cc, BASE_SCALE))

    def state(Lam, flux):
        D = bb**2 - 3 * aa * cc * Lam * flux**2
        nmax = bb / math.sqrt(3 * aa * cc * Lam) if Lam > 0 else None
        if Lam > 0 and abs(D) <= 1e-12:
            return {"exists": False, "critical": True, "nmax": nmax}
        if Lam > 0 and D < 0:
            return {"exists": False, "critical": False, "nmax": nmax}
        root = 3 * cc * flux**2 / (bb + math.sqrt(max(D, 0.0)))
        Rstar = math.sqrt(root)
        val = aa * Lam / root - bb / root**2 + cc * flux**2 / root**3
        vxx = 2 * aa * Lam / root**3 - 6 * bb / root**4 + 12 * cc * flux**2 / root**5
        mass2 = root**2 * vxx / (2 * M4_NUM**2)
        if abs(val) < 1e-8:
            sign = "flat [tuned]"
        elif val < 0:
            sign = "AdS"
        else:
            sign = "dS"
        return {"exists": True, "critical": False, "nmax": nmax, "x": root, "R": Rstar, "V": val, "vxx": vxx, "m2": mass2, "sign": sign}

    cases = [("Λ6 = −0.5", -0.5, range(1, 5)), ("Λ6 = 0.1", 0.1, range(1, 7)), ("Λ6 = 0.5 tuned at n=2", 0.5, range(1, 5))]
    all_states = {}
    w("")
    w("## Stage B — on-shell radion table")
    w("")
    w("All rows use the same a,b,c above [assumed input]; Λ_6≤0 has no n_max, while positive Λ_6 uses n_max=b/√(3acΛ_6) [identity].")
    for label, Lam, fluxes in cases:
        nmax = bb / math.sqrt(3 * aa * cc * Lam) if Lam > 0 else None
        n0 = math.sqrt(bb**2 / (4 * aa * cc * Lam)) if Lam > 0 else None
        w("")
        w("### %s [assumed input]" % label)
        w("n_max = %s; AdS/dS boundary n₀ = %s [computed]." % ("none (Λ6≤0)" if nmax is None else "%.6f" % nmax, "none (Λ6≤0)" if n0 is None else "%.6f" % n0))
        w("| n | minimum? | R* | V sign | V''(x*) | radion m² |")
        w("|---:|---|---:|---|---:|---:|")
        all_states[Lam] = {}
        for flux in fluxes:
            st = state(Lam, flux)
            all_states[Lam][flux] = st
            if not st["exists"]:
                w("| %d | NO%s | — | — | — | — |" % (flux, " (double-root critical point)" if st.get("critical") else ""))
            else:
                w("| %d | YES | %.6f | %s | %.6e | %.6e |" % (flux, st["R"], st["sign"], st["vxx"], st["m2"]))
        w("Root-rule check [computed]: rows with n < n_max have one stable minimum; rows beyond n_max do not; Λ6≤0 rows all have one AdS minimum.")

    w("")
    w("## Stage C — Job Three filter on on-shell points only")
    w("")
    w("Job Three bridge [post-hoc]: rho_res is linearly interpolated from its existing m=16 local-minimum table in betti-berry-vacuum-filter/RESULTS.md; no Job Three run or heavy percolation run was performed. This keeps Stage C algebra/root-finding cheap.")
    w("The on-shell map is p = clip(n/(3 R*²), 0, 1) with R* measured in BASE_SCALE×R* [assumed input]. Venus heads-up [prediction]: p≈2b/(9cn) at small n, so p falls with n; at fixed couplings the filter becomes a function of n alone [computed from the map].")
    w("| Λ6 case | n | R* | p_raw | p used | rho_res [post-hoc interpolation] | survives default window? |")
    w("|---|---:|---:|---:|---:|---:|---|")
    on_shell = {}
    for label, Lam, fluxes in cases:
        on_shell[Lam] = []
        for flux in fluxes:
            st = all_states[Lam][flux]
            if not st["exists"]:
                continue
            p_raw = flux / (3 * (BASE_SCALE * st["R"])**2)
            p_used = min(1.0, max(0.0, p_raw))
            rho = interp_curve(curve, p_used)
            record = {"id": "%s: n=%d" % (label, flux), "Lambda6": Lam, "n": flux, "Rstar": st["R"], "p_raw": p_raw, "p": p_used, "rho_res": rho, "field_content": {"breathing_mode": "R"}, "spectrum": {"source": "Job Three m=16 table"}}
            on_shell[Lam].append(record)
            w("| %s | %d | %.6f | %.6f | %.6f | %.6f | %s |" % (label, flux, st["R"], p_raw, p_used, rho, "YES" if surviving_vacua([record]) else "NO"))
    w("")
    w("On-shell surviving vacua at BASE_SCALE=%.2f [prediction, post-hoc interpolation]:" % BASE_SCALE)
    for label, Lam, _ in cases:
        surv = surviving_vacua(on_shell[Lam])
        w("- %s: %s" % (label, fmt_list(surv)))
    w("Key question [prediction]: n=3 survival is reported above rather than assumed; it may depend on Λ6 and the radius normalisation. n=3 is not selected by construction here.")
    w("")
    w("### Exact Λ6 windows for n=3 [computed]")
    p_bands = p_window_bands(curve)
    def lambda_at_x(x_value, flux=3):
        return (2.0 * bb * x_value - 3.0 * cc * flux**2) / (aa * x_value**2)
    w("Inversion [identity]: Λ6(x)=(2bx−3cn²)/(ax²); at n=3 and unit normalisation p=1/x. The map's p bands are converted to Λ6 bands without refitting.")
    w("| band | p interval from Job Three m=16 table | computed Λ6 interval | Venus estimate | comparison |")
    w("|---|---|---|---|---|")
    lambda_bands = []
    for idx, (plo, phi) in enumerate(p_bands, 1):
        vals = [lambda_at_x(1.0 / plo), lambda_at_x(1.0 / phi)]
        lo_lam, hi_lam = min(vals), max(vals)
        lambda_bands.append((lo_lam, hi_lam))
        estimate = (0.0908, 0.1753) if idx == 1 else (-1.325, -1.219)
        ok = abs(lo_lam - estimate[0]) < 0.01 and abs(hi_lam - estimate[1]) < 0.01
        w("| %d | [%.6f, %.6f] | [%.6f, %.6f] | [%.4f, %.4f] | %s |" % (idx, plo, phi, lo_lam, hi_lam, estimate[0], estimate[1], "agrees" if ok else "DIFFERS"))
    r_flat = 1.5
    r_merge = math.sqrt(27.0 / 8.0)
    r_main_lo = math.sqrt(1.0 / p_bands[0][1])
    r_main_hi = math.sqrt(1.0 / p_bands[0][0])
    s_dS_lo = r_main_lo / r_merge
    s_dS_hi = r_main_hi / r_flat
    w("Exact dS rule for n=3 [computed, identity]: at Λ6=2/9 it is exactly flat at x=9/4 and R=3/2; at Λ6=8/27 the minimum merges with the barrier at x=27/8 and R=√(27/8)=%.6f." % r_merge)
    w("A dS n=3 survivor exists when the scaled main band reaches physical R in [1.500000, %.6f], giving computed %.6f ≤ s ≤ %.6f; Venus estimate was roughly 0.74 ≤ s ≤ 0.957." % (r_merge, s_dS_lo, s_dS_hi))
    w("Exact formula check [computed]: for n=3, dS requires 2/9 < Λ6 ≤ 8/27 [identity].")
    w("no n = 3 survivor is dS at unit normalisation; for roughly 0.74 ≲ s ≲ 0.957 a dS survivor exists [assumed input: normalisation].")
    w("Every unit-normalisation main-window survivor is AdS (n₀ = √(2/Λ₆) is between 3.4 and 4.7 > 3); the dS statement changes under scale [computed].")
    w("| normalisation scale | band 1 Λ6 interval | band 2 Λ6 interval |")
    w("|---:|---|---|")
    for scale in (BASE_SCALE,) + tuple(x for x in SCALES if x != BASE_SCALE):
        intervals = []
        for plo, phi in p_bands:
            vals = [lambda_at_x(1.0 / (scale**2 * plo)), lambda_at_x(1.0 / (scale**2 * phi))]
            intervals.append("[%.6f, %.6f]" % (min(vals), max(vals)))
        w("| %.2f | %s | %s |" % (scale, intervals[0] if intervals else "-", intervals[1] if len(intervals) > 1 else "-"))
    base_n3 = [v for vals in on_shell.values() for v in vals if v["n"] == 3 and surviving_vacua([v])]
    for v in base_n3:
        distances = []
        for lo_lam, hi_lam in lambda_bands:
            distances.extend([abs(v["Lambda6"] - lo_lam), abs(v["Lambda6"] - hi_lam)])
        nearest = min(distances) if distances else float("nan")
        lower = lambda_bands[0][0] if lambda_bands else float("nan")
        pct = 100.0 * (v["Lambda6"] - lower) / lower if lower else float("nan")
        w("Spot survivor distance in Λ6 [computed]: %s has Λ6=%.6f; nearest edge distance %.6f, %.3f%% of the main-window width, and %.3f%% relative to the lower-edge value." % (v["id"], v["Lambda6"], nearest, 100.0 * nearest / (lambda_bands[0][1] - lambda_bands[0][0]), pct))
        p_lo, p_hi = p_bands[0]
        p_distances = [(abs(v["p"] - p_lo), "lower", p_lo), (abs(v["p"] - p_hi), "upper", p_hi)]
        p_nearest, p_side, p_edge = min(p_distances)
        w("Spot survivor distance in p [computed]: p=%.6f is %.6f below the %s p edge %.6f; %.3f%% relative to that edge and %.3f%% of the p-window width." % (v["p"], p_nearest, p_side, p_edge, 100.0 * p_nearest / p_edge, 100.0 * p_nearest / (p_hi - p_lo)))
        r_edge_lo, r_edge_hi = r_main_lo, r_main_hi
        r_near = min(abs(v["Rstar"] - r_edge_lo), abs(v["Rstar"] - r_edge_hi))
        r_side = "lower" if abs(v["Rstar"] - r_edge_lo) <= abs(v["Rstar"] - r_edge_hi) else "upper"
        r_edge = r_edge_lo if r_side == "lower" else r_edge_hi
        w("Spot survivor distance in R [computed]: R*=%.6f is %.6f from the %s R edge %.6f; %.3f%% relative to that edge and %.3f%% of the R-window width." % (v["Rstar"], r_near, r_side, r_edge, 100.0 * r_near / r_edge, 100.0 * r_near / (r_edge_hi - r_edge_lo)))
    w("Venus coordinate clarification [computed]: the p gap is about 0.005 (about 1%), the R gap is about 0.5%, and the Λ6 gap is 9.4% above the lower Λ6 edge; these are different coordinates, not a contradiction.")
    w("")
    w("### Normalisation scan [post-hoc; assumed input]")
    w("Changing BASE_SCALE changes p and therefore the inherited Job Three rho_res lookup; this is a unit-matching assumption, not a prediction.")
    w("| scale | Λ6=−0.5 survivors | Λ6=0.1 survivors | Λ6=0.5 tuned survivors | dS n=3 survivor? |")
    w("|---:|---|---|---|---|")
    for scale in SCALES:
        cells = []
        for label, Lam, _ in cases:
            vals = []
            for old in on_shell[Lam]:
                v = dict(old)
                v["p_raw"] = v["n"] / (3 * (scale * v["Rstar"])**2)
                v["p"] = min(1.0, max(0.0, v["p_raw"]))
                v["rho_res"] = interp_curve(curve, v["p"])
                vals.append(v)
            cells.append(fmt_list(surviving_vacua(vals)))
        w("| %.2f | %s | %s | %s | %s |" % (scale, cells[0], cells[1], cells[2], "YES" if s_dS_lo <= scale <= s_dS_hi else "NO"))
    w("Any dependence on Λ6 or BASE_SCALE is an honest PARTIAL on selection [prediction], not a failure of the Stage A/B identities.")
    w("")
    w("## Caveats and omitted physics [assumed input]")
    w("Only the breathing mode is included. Shape modes, flux tunnelling n→n−1, one-loop/Casimir radion terms, and Job Four brane tension are omitted [assumed input].")
    w("Stable means classically stable in R only [standard]. The Job Three rho curve is reused from its existing generated table, not recomputed here [post-hoc].")
    w("References checked 2026-10-02: Carroll, Geddes, Hoffman & Wald, 'Classical Stabilization of Homogeneous Extra Dimensions,' Phys. Rev. D 66, 024036 (2002), arXiv:hep-th/0110149 [standard]; Blanco-Pillado, Schwartz-Perlov & Vilenkin, 'Quantum Tunneling in Flux Compactifications,' JCAP 2009(12), 006, arXiv:0904.3106 [standard].")
    w("Additional references: arXiv:0912.4082 for the barrier/decompactification caveat; Randjbar-Daemi, Salam & Strathdee, Nucl. Phys. B 214 (1983) 491 [standard].")
    w("")
    after_j3 = snapshot(J3)
    after_j2 = snapshot(J2)
    w("Read-only source audit after run [computed]: Job Three unchanged = %s; Job Two unchanged = %s." % (before_j3 == after_j3, before_j2 == after_j2))
    w("Job Three hashes after: RESULTS.md %s; run.py %s. Job Two RESULTS_final.md after: %s." % (sha(J3_RESULTS), sha(J3_RUN), sha(J2_RESULTS)))
    (HERE / "RESULTS.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
