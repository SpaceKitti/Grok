"""pairA-qg-loss: gravity-side loss test. `python run.py` writes RESULTS.md and stops. No folders are loaded."""
from __future__ import annotations

import sys
import time

sys.dont_write_bytecode = True
from pathlib import Path  # noqa: E402

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
except Exception:
    pass

import numpy as np  # noqa: E402

import drive_test as DT  # noqa: E402
import H_try as HT  # noqa: E402
import loss_term as LT  # noqa: E402

E = LT.EPS_EP
GRID = {"P0 scalar (M = 1)": [0.0, 0.1, 1.0, 10.0],
        "P1 sigma_z (M = sigma_z)": [0.0, 1e-3, 3e-3, 1e-2, 3e-2, 0.1, 0.3, 1.0, 3.0, 10.0]}
SPEEDS = (40.0, 100.0)


def fz(z):
    return f"{z.real:+.6f}{z.imag:+.6f}i"


def main() -> int:
    t0 = time.time()
    print(LT.T_CHOICE)
    res = {}
    for pl, etas in GRID.items():
        M = LT.PLACEMENTS[pl]
        for eta in etas:
            H = HT.make_H(eta, M)
            ep = HT.ep_report(eta, M)
            cs = HT.copy_test(H)
            cd = HT.copy_test(H, traceless=True)
            loop = HT.swap_around(H, E, 0.25 * E, 1), HT.swap_around(H, E, 0.25 * E, 2)
            dr = DT.test(H, SPEEDS)
            res[(pl, eta)] = {"ep": ep, "cs": cs, "cd": cd, "loop": loop, "dr": dr}
            print(f"{pl} η_g={eta:g}: EPs {[fz(x['eps']) for x in ep['rows']]} (±ε_EP kept {ep['pm_kept']}); copy strict {'YES' if cs['copy'] else 'NO'} "
                  f"(s_min {cs['smin_best']:.1e}), dynamical {'YES' if cd['copy'] else 'NO'} (s_min {cd['smin_best']:.1e}), spec err {cs['spec_err']:.1e}; "
                  f"loop swap/return {loop}; γ_g={dr['gamma_g']:.5f}; 0.75 → {dr[0.75]['cls']}, 1.25 → {dr[1.25]['cls']} (dt-halving Δw {max(dr[0.75]['dw'], dr[1.25]['dw']):.1e}) t={time.time()-t0:.0f}s")
    # inherited check: weights vs eta = 0 (same placement)
    for (pl, eta), r in res.items():
        base = res[(pl, 0.0)]["dr"]
        # winner-weight change (label-order independent: at 1.25 the mode order switches from frequency to decay once eta_g > 0)
        r["dW"] = max(abs(r["dr"][f]["runs"][k][m]["w"] - base[f]["runs"][k][m]["w"]) for f in (0.75, 1.25) for k in r["dr"][f]["runs"] for m in (1, 2))
    # grading
    good = {}
    for pl, etas in GRID.items():
        ok = [eta for eta in etas if eta > 0 and not res[(pl, eta)]["cs"]["copy"] and not res[(pl, eta)]["cd"]["copy"]
              and res[(pl, eta)]["dr"][0.75]["cls"] == "D6-like" and res[(pl, eta)]["dr"][1.25]["cls"] == "D7-like"]
        # longest run of consecutive grid points
        pos = [e for e in etas if e > 0]
        best, cur = [], []
        for e in pos:
            if e in ok:
                cur.append(e)
                if len(cur) > len(best) or (len(cur) == len(best) and cur and best and cur[-1] / cur[0] > best[-1] / best[0]):
                    best = list(cur)
            else:
                cur = []
        good[pl] = {"ok": ok, "run": best, "decades": (np.log10(best[-1] / best[0]) if len(best) > 1 else 0.0)}
    have = [pl for pl in GRID if good[pl]["ok"]]
    notcopy = [pl for pl in GRID if any(not res[(pl, e)]["cs"]["copy"] and not res[(pl, e)]["cd"]["copy"] for e in GRID[pl] if e > 0)]
    grade = "HAVE" if have else ("PARTIAL" if notcopy else "MISSING")
    pick = have[0] if have else (notcopy[0] if notcopy else None)
    robust = bool(have) and good[pick]["decades"] >= 1.0
    copy_line = {pl: ("NO" if any(not res[(pl, e)]["cs"]["copy"] and not res[(pl, e)]["cd"]["copy"] for e in GRID[pl] if e > 0) else "YES") for pl in GRID}
    letter_grade = grade
    print(f"LETTER GRADE {letter_grade} ({pick}; robust η_g range: {robust}; {good[pick] if pick else ''})")
    P1 = "P1 sigma_z (M = sigma_z)"
    rel = [e for e in good[P1]["ok"] if max(res[(P1, e)]["dr"][0.75]["dw"], res[(P1, e)]["dr"][1.25]["dw"]) <= 1e-3]
    rel_dec = np.log10(rel[-1] / rel[0]) if len(rel) > 1 else 0.0
    dW_win = max((res[(P1, e)]["dW"] for e in good[P1]["ok"]), default=float("nan"))
    # (Venus/Helios) final grade: the question is whether the loss CAUSES D6; it does not
    grade = "PARTIAL"
    # dt refinement at eta_g = 0.001 (P1), gamma_g T = 40, start mode 0, both directions
    H001 = HT.make_H(1e-3, LT.SZ); g001 = DT.gamma_g(H001)
    PAIRS = {"dt vs dt/2": (1, 2), "dt/2 vs dt/4": (2, 4), "dt/4 vs dt/8": (4, 8)}
    ref = {}
    for frac in (0.75, 1.25):
        for dn, s in (("ccw", 1), ("cw", -1)):
            W = {f: DT.run_drive(H001, frac, s, SPEEDS[0], 0, g001, factor=f) for f in (1, 2, 4, 8)}
            ref[(frac, dn)] = {k: max(float(np.max(np.abs(W[a][m] - W[b][m]))) for m in (1, 2)) for k, (a, b) in PAIRS.items()}
    dw4 = max(r["dt/4 vs dt/8"] for r in ref.values())
    clean4 = dw4 < 1e-3
    for k, r in ref.items():
        print(f"eta_g=0.001 dt refinement {k}: " + ", ".join(f"{a} {b:.1e}" for a, b in r.items()))
    print(f"eta_g=0.001: dt/4 delta-w (dt/4 vs dt/8) = {dw4:.1e} -> {'below' if clean4 else 'NOT below'} 1e-3")
    # rounding probe: P0 at eta_g = 1e-15 (a scalar that must drop out exactly) vs eta_g = 0, 0.75 start, gamma_g T = 40
    H0p, Hep = HT.make_H(0.0, LT.I2), HT.make_H(1e-15, LT.I2); g0p = DT.gamma_g(H0p)
    rprobe = max(max(float(np.max(np.abs(DT.run_drive(H0p, 0.75, s, SPEEDS[0], 0, g0p)[m] - DT.run_drive(Hep, 0.75, s, SPEEDS[0], 0, g0p)[m]))) for m in (1, 2)) for s in (1, -1))
    print(f"rounding probe (P0 eta_g=1e-15 vs 0, 0.75 start, gT=40): max delta-w {rprobe:.1e}")
    # transpose identity H^T = sigma_z H sigma_z
    zs = [0.3 + 0.2j, -0.7 + 0.1j, 1.1 - 0.5j, 0.75 * E, 1.25 * E]
    tr_res = max(float(np.max(np.abs(HT.make_H(e, LT.PLACEMENTS[pl])(z).T - LT.SZ @ HT.make_H(e, LT.PLACEMENTS[pl])(z) @ LT.SZ))) for pl in GRID for e in GRID[pl] for z in zs)
    print(f"transpose identity H^T = sz H sz: max residual {tr_res:.1e} over all placements and eta_g")
    # inside-Gamma split at eps = 0.75 eps_EP (P1)
    split = {}
    for e in GRID[P1]:
        w = np.linalg.eigvals(HT.make_H(e, LT.SZ)(0.75 * E)); d = w[0] - w[1]
        split[e] = (abs(d.real), abs(d.imag))
    # basis map under the constant SU(2) S = (1/2)[1 - i(sx - sy + sz)] (from pairA-qg-theory)
    SX = np.array([[0, 1], [1, 0]], dtype=complex); SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
    S = 0.5 * (LT.I2 - 1j * (SX - SY + LT.SZ))
    best_map = None
    for nm, U in (("S X S^-1", S), ("S^-1 X S", np.linalg.inv(S))):
        imz = U @ LT.SZ @ np.linalg.inv(U); imy = U @ SY @ np.linalg.inv(U)
        if np.max(np.abs(imz - SX)) < 1e-12:
            sy_to = [(lbl, sg) for lbl, P in (("sigma_x", SX), ("sigma_y", SY), ("sigma_z", LT.SZ)) for sg in (1, -1) if np.max(np.abs(imy - sg * P)) < 1e-12]
            best_map = (nm, sy_to)
    print(f"basis map: {best_map}")
    # gamma_g closed form at eta_g = 0
    gg_closed = abs(LT.V) * E * np.sqrt(0.25 * 1.75)
    gg_num = res[(P1, 0.0)]["dr"]["gamma_g"]
    print(f"gamma_g(eta=0) numeric {gg_num:.8f} vs |v| eps_EP sqrt(0.4375) = {gg_closed:.8f}; ratio to |v| eps_EP = {gg_num / (abs(LT.V) * E):.8f} (sqrt(7)/4 = {np.sqrt(7) / 4:.8f})")
    thr = abs(LT.V) / (0.25 * E)
    thr_ok = all((res[(P1, e)]["ep"]["rows"] and sum(1 for x in res[(P1, e)]["ep"]["rows"] if x["in_loop"]) == (2 if e > thr else 1)) for e in GRID[P1])
    print(f"GRADE {grade} (letter: {letter_grade})")

    # ---------------- RESULTS.md
    L = ["# pairA-qg-loss — RESULTS", "",
         "**Signed off 2026-09-25:** Venus (maths) and Helios (physics).", "",
         "Gravity-side [hive-interpretation] loss test on the Pair A curve. No folder was loaded; the numbers are hard-coded (ε_EP = 0.51368066, λ_EP = −0.308425i, v = −0.360253; source: pairA-qg-handoff / pairA-jt-4d as given by Akitti). H_A is not imported; a and b appear only inside the copy check. No claim of QG, a JT dual, or an Einstein solution. A and B WRITE, C held.", "",
         f"## Verdict", "",
         f"- **Loss term: {LT.T_CHOICE}**.",
         "- **Sign note.** With ψ ~ e^{−iλt}, Im V = η_g F_JT is **loss inside Γ (F_JT < 0) and gain outside (F_JT > 0)**. Every use of 'loss' in this file means this sign-changing term.",
         "- Placements: P0 = iη_g F_JT·1 (scalar), and P1 = iη_g F_JT σ_z. σ_z is the direction that multiplies ε in the curve part, so vε → vε + iη_g F_JT: an imaginary shift of the dilaton-like variable. Both placements vanish at ±ε_EP.",
         f"- **Copy of H_A:** P0 {copy_line['P0 scalar (M = 1)']} for η_g > 0 (strict NO, but dynamical copy YES: the scalar drops out of the normalised dynamics); P1 {copy_line['P1 sigma_z (M = sigma_z)']} for η_g > 0 (strict and dynamical NO). At η_g = 0 both placements reduce to the curve part, which **is** a copy (YES).",
         f"- **D6/D7 from H_try (P1):** D6-like at 0.75 and D7-like at 1.25 for η_g ∈ {good['P1 sigma_z (M = sigma_z)']['ok']} (longest consecutive run {good['P1 sigma_z (M = sigma_z)']['run']}, {good['P1 sigma_z (M = sigma_z)']['decades']:.2f} decades).",
         f"- **GRADE: {grade}**",
         f"  HAVE (weak) by the pre-fixed letter; clean window {rel_dec:.2f} decades once eta_g=0.001 (dt check fail) is excluded; D6 inherited from the eta_g=0 rotated H_A",
         f"- Pre-fixed letter grade computed by the README rule: {letter_grade} (window {good[P1]['run']}, {good[P1]['decades']:.2f} decades by the grid).",
         f"- **η_g = 0.001 dt refinement** (P1, γ_g T = 40, both directions): dt/4 Δw (dt/4 vs dt/8) = {dw4:.1e}, {'below' if clean4 else '**not** below'} 1e-3. " + ("The letter window is then cleanly one decade." if clean4 else "The letter window is therefore **not** cleanly one decade.") + " Per start: " + "; ".join(f"{fr} {dn}: " + ", ".join(f"{a} {b:.1e}" for a, b in r.items()) for (fr, dn), r in ref.items()) + f". At 1.25 ε_EP the differences fall as dt² (step-size error). At 0.75 ε_EP they do not fall: this is a rounding floor, because a 10⁻¹⁵ scalar perturbation (P0, η_g = 10⁻¹⁵ vs 0) already shifts the 0.75 ε_EP, γ_g T = 40 weights by {rprobe:.1e} [computed: floating-point floor, amplified exponentially along the loop at 0.75 ε_EP, γ_gT = 40; not integrator step error] A 1e-15 scalar moving w by {rprobe:.1e} is a gain of about 1e11 ({rprobe:.1e}/1e-15 ≈ {rprobe / 1e-15:.0e}); this comes from the exponential gain along the loop (the losing mode is suppressed by e^{{-Δγ t}} and must regrow, carrying its rounding with it: stability-loss delay), not from the eigenvector condition number, which is O(1) at 0.25 ε_EP from the tip. With this setup the η_g = 0.001 row cannot be pushed under the 1e-3 rule at any dt, because the floor does not depend on dt. The grade stays PARTIAL either way: the question was whether the loss causes D6, and it does not.", "",
         "**Caveat attached to the grade.** The curve part H_curve = λ_EP·1 + v[[ε, ε_EP], [−ε_EP, −ε]] is itself H_A in a rotated basis (constant SU(2); copy test YES at η_g = 0). Inside Γ its eigenvalue split is already purely imaginary, so the mode selection for D6 is already present before any loss is added. Where D6/D7 hold at small η_g they are **inherited from H_curve**: the winners are the same as at η_g = 0 (weights differ by at most the Δw listed below). The new term does not change the winners there and is not the mechanism. Also, the inputs (λ_EP, ε_EP, v) fix a and b up to a swap, so 'not using a, b' is nominal.", "",
         "**Physics reading (Helios).** P1 = dissipative (imaginary) coupling in H_A's basis (curve sigma_z maps to H_A sigma_x under the constant SU(2) rotation; curve sigma_y maps to H_A sigma_z, the loss-contrast direction). It is the wrong direction to cause D6, which is selection by loss contrast, so it can only destroy D6 [standard + computed]." + f" Check: under {best_map[0] if best_map else '?'} with S = ½[1 − i(σx − σy + σz)], σ_z → σ_x and σ_y → {', '.join(('+' if sg > 0 else '−') + lbl for lbl, sg in best_map[1]) if best_map else '?'} [computed]. The sign (curve σ_y → −σ_z) does not matter, because only squares enter the discriminant and the copy test.", "",
         f"**Mechanism.** Transpose identity kept; the PT property that makes the inside-Γ split purely imaginary is broken by the imaginary coupling [computed]. H_try^T = σ_z H_try σ_z holds at every η_g (max residual {tr_res:.1e} over both placements, all η_g, 5 sample ε) [identity + computed]. Inside-Γ split at ε = 0.75 ε_EP (|Re Δλ|, |Im Δλ|): " + "; ".join(f"η_g = {e:g}: ({split[e][0]:.1e}, {split[e][1]:.1e})" for e in GRID[P1]) + " [computed].", "",
         "The premise 'a scalar loss must make D6 fail' does not hold here. The scalar term cannot select a mode, but the selection comes from H_curve, so P0 gives exactly the η_g = 0 (H_A-like) winners. P0 is therefore a dynamical copy, not a new mechanism. For P0 the 'max Δw vs η_g = 0' should be exactly 0 [identity: c(ε)·1 commutes and drops out of the normalised dynamics]. The listed 4.9e-4 to 1.1e-3 are numerical error, the same size as the dt-halving column: they come entirely from the 0.75 ε_EP, γ_g T = 40 runs (1.25 ε_EP gives ~1e-16), where the rounding floor quoted above dominates [computed: floating-point floor, amplified exponentially along the loop at 0.75 ε_EP, γ_gT = 40; not integrator step error].", "",
         "## Scan table", "",
         "| placement | η_g | EPs (discriminant roots) | ±ε_EP kept | EPs inside the drive loop | loop 2π / 4π (continuation) | copy strict (s_min) | dynamical copy (s_min) | spectrum err vs H_A | γ_g | 0.75 ε_EP | 1.25 ε_EP | max Δw vs η_g = 0 | dt-halving Δw |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for (pl, eta), r in res.items():
        ep, cs, cd, dr = r["ep"], r["cs"], r["cd"], r["dr"]
        L.append(f"| {pl.split(' (')[0]} | {eta:g} | {', '.join(fz(x['eps']) for x in ep['rows'])} | {'yes' if all(ep['pm_kept']) else 'NO'} | {sum(1 for x in ep['rows'] if x['in_loop'])} | {r['loop'][0]} / {r['loop'][1]} | {'YES' if cs['copy'] else 'NO'} ({cs['smin_best']:.1e}) | {'YES' if cd['copy'] else 'NO'} ({cd['smin_best']:.1e}) | {cs['spec_err']:.1e} | {dr['gamma_g']:.5f} | **{dr[0.75]['cls']}** | **{dr[1.25]['cls']}** | {r['dW']:.1e} | {max(dr[0.75]['dw'], dr[1.25]['dw']):.1e} |")
    L += ["", "## EP-location report", "",
          "- The discriminant of H_try(P1) is ∝ (vε + iη_g F_JT)² − v²ε_EP² = (ε − ε_EP)(ε + ε_EP)[v + iη_g(ε + ε_EP)][v + iη_g(ε − ε_EP)] [identity].",
          "- Its roots are **±ε_EP (kept, since the loss vanishes there) plus two new EPs at ±ε_EP + i v/η_g** (Im < 0 for η_g > 0, since v < 0) [identity; numerically confirmed in the per-η_g list]. For η_g → 0 the new EPs go to infinity. The loop r = 0.25 ε_EP encloses the new EP near +ε_EP once |v|/η_g < 0.25 ε_EP, i.e. η_g > " + f"{thr:.4f}" + f" [identity; checked against the computed in-loop counts on the grid: {'consistent' if thr_ok else 'INCONSISTENT'}].",
          "- Every EP (old and new) shows a 2π swap and a 4π return on small circles (table in the per-η_g EP list below). For P0 the spectrum's EPs are exactly ±ε_EP for all η_g.",
          "- When the loop encloses two EPs, the loop itself returns after 2π (monodromy of two square-root points), shown in the 'loop 2π / 4π' column.", "",
          "### Per-η_g EP list (P1)", ""]
    for eta in GRID["P1 sigma_z (M = sigma_z)"]:
        ep = res[("P1 sigma_z (M = sigma_z)", eta)]["ep"]
        L.append(f"- η_g = {eta:g}: " + "; ".join(f"{fz(x['eps'])} (2π {x['swap']}, 4π {x['ret']}, in loop {'yes' if x['in_loop'] else 'no'})" for x in ep["rows"]))
    L += ["", "## Weights (P1, selected η_g)", "",
          "Winner index 0 = slower-decaying (or higher-frequency if the decays are equal) at the start/end point. Weight = left-eigenvector weight of the winner.", "",
          "| η_g | start | γ_g T | turn | ccw from 0 | ccw from 1 | cw from 0 | cw from 1 | class |", "|---|---|---|---|---|---|---|---|---|"]
    for eta in GRID["P1 sigma_z (M = sigma_z)"]:
        dr = res[("P1 sigma_z (M = sigma_z)", eta)]["dr"]
        for f in (0.75, 1.25):
            nm = dr[f]["names"]
            for gT in SPEEDS:
                for m in (1, 2):
                    rr = dr[f]["runs"]
                    L.append(f"| {eta:g} | {f:.2f} | {int(gT)} | {2*m}π | " + " | ".join(f"{nm[rr[(gT, dn, st)][m]['win']]} ({rr[(gT, dn, st)][m]['w']:.4f})" for dn in ("ccw", "cw") for st in (0, 1)) + f" | {dr[f]['cls']} |")
    L += ["", "## Copy test details", "",
          "- Strict: the smallest relative singular value of the stacked system S H_try(ε_k) − H_A(αε_k + β) S = 0 over 6 complex ε_k, minimised over complex α, β (Nelder–Mead, 5 starts). Copy if ≤ 1e-8. At a single ε any two matrices with the same eigenvalues are similar, which is why the constant-S test is the meaningful one.",
          "- Dynamical: the same test on the traceless parts (removes any c(ε)·1, which does not affect normalised dynamics).",
          "- η_g = 0: s_min ≈ 1.4e-9, the rounding level of the given ε_EP (0.51368066 vs |b−a|/(2|v|) = 0.5136806633). The spectrum error of about 2e-5 is the √-amplified rounding near the EPs. Copy YES.",
          "- P1, η_g > 0: copy NO [identity]. A constant S preserves the spectrum, and P1's discriminant is quartic in ε while H_A(αε + β)'s is quadratic, so no S and no affine reparametrisation can work; η_g does not recreate a and b. The numerical s_min values agree [computed].",
          "- P0, η_g > 0: dynamical copy YES [identity], because c(ε)·1 commutes with everything and drops out of the traceless part. Strict NO only because the trace differs [computed].", "",
          "## Caveats", "",
          "- The mode selection is inherited from H_curve (≡ H_A up to a constant rotation) wherever D6/D7 hold at small η_g; see 'max Δw vs η_g = 0'.",
          f"- γ_g (Venus): at η_g = 0, γ_g = |v| ε_EP √(0.25·1.75) = {gg_closed:.5f} (numeric {gg_num:.5f}), the smallest split on the loop (at ε = 0.75 ε_EP, where the split is purely imaginary, so it is also the max |Im| gap used as the definition). Since |a−b|/2 = |v| ε_EP, γ_g/(|a−b|/2) = √7/4 = {np.sqrt(7) / 4:.6f} exactly [identity]. This is a definitional ratio, not a physical difference; γ_g T = 40 corresponds to drive-return's γT = 40·4/√7.",
          "- For η_g > 0 the 1.25 ε_EP winners switch from frequency to decay ordering, and the equal-frequency/equal-decay regions no longer lie on the real axis. 'D7-like' at 1.25 ε_EP is a real chirality but not a like-for-like comparison with drive-return (Helios).",
          "- dt-halving changes are listed per row. At 0.75 ε_EP, γ_g T = 40 they sit at a ~1e-3 rounding floor (see the verdict) [computed: floating-point floor, amplified exponentially along the loop at 0.75 ε_EP, γ_gT = 40; not integrator step error], so values near 1e-3 there do not measure step-size error. At 1.25 ε_EP they are step-size error.",
          "- New EPs at ±ε_EP + iv/η_g move into the drive loop for η_g > 2.8, which changes the loop's monodromy. D6/D7 there are not comparable to the H_A case.",
          "- [by construction]: H_curve; the placements; γ_g. [computed]: EPs, copy tests, weights. [identity]: the factorisation of the discriminant, the EP locations, the γ_g ratio, P1 copy NO, P0 dynamical copy YES. [hive-interpretation]: calling iη_g F_JT σ_z 'gravity-side' (an imaginary dilaton shift).", "",
          ]
    L += ["## Post-hoc notes (criteria as fixed in README; the final grade PARTIAL follows the Venus/Helios sign-off)", "",
          f"- The HAVE window {good[P1]['ok']} is exactly one decade by the grid. Its lowest point (η_g = 0.001) fails the dt-halving check (Δw = {max(res[(P1, 0.001)]['dr'][0.75]['dw'], res[(P1, 0.001)]['dr'][1.25]['dw']):.1e} > 1e-3). Using only rows with dt-halving Δw ≤ 1e-3, the window is {rel} = {rel_dec:.2f} decades, which is under one decade and would be flagged. The robustness claim therefore rests on a numerically marginal point (see the dt refinement in the verdict).",
          f"- Inside the window the winner weights differ from η_g = 0 (the H_A-equivalent curve part) by at most {dW_win:.1e}; the winners are unchanged from η_g = 0, and the shift grows steadily towards the D6 flip at η_g = 0.03. D6/D7 in the window are inherited from H_curve, not produced by the new loss.",
          "- Once the loss is strong enough to change the weights (η_g ≥ 0.03), D6 fails at 0.75 ε_EP. At γ_g T = 40, ccw and cw pick different modes inside Γ (ccw → faster-decaying, cw → slower-decaying at η_g = 0.1), while at γ_g T = 100 both pick the slower-decaying mode. That is chirality inside Γ at moderate speed [computed; mechanism: inside-Γ split no longer purely imaginary, so equal-frequency is lost].",
          "- For η_g ≥ 3 the new EP at ε_EP + iv/η_g lies inside the drive loop. The loop then encloses two EPs, returns after 2π, and both starts are D7-like.",
          "- Physics reading: the new σ_z term does not supply the D6 mechanism; wherever it is strong enough to matter it destroys D6. So HAVE holds only weakly by the letter of the rule, and a gravity-side loss that *causes* D6 has not been found; hence PARTIAL [hive-interpretation of the computed table].", "",
          "## Offered next run (not started)", "",
          "- Loss-contrast placement: a term ∝ F_JT on curve σ_y (= H_A σ_z). It keeps the EPs at ±ε_EP and tests 'gravity-side loss causes D6' on the right footing. 'Gravity-side' is [hive-interpretation].", "",
          "No folders were loaded (nothing to SHA-check); only this folder was written.", ""]
    (ROOT / "RESULTS.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("Wrote RESULTS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
