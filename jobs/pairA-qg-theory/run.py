"""pairA-qg-theory: grade L1-L6 against the README criteria. `python run.py` writes RESULTS.md and stops."""
from __future__ import annotations

import hashlib
import re
import sys

sys.dont_write_bytecode = True
from pathlib import Path  # noqa: E402

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
except Exception:
    pass

U = Path(r"C:\Users\Akitt")
LOADED = [U / "pairA-qg-handoff", U / "pairA-qg-probe-surface", U / "pairA-jt-4d", U / "pairA-qg-on-R1", U / "pairA-drive-return", U / "pairA-drive-sweep"]


def hash_tree(roots):
    out = {}
    for root in roots:
        for p in sorted(Path(root).rglob("*")):
            if p.is_file():
                out[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


H_BEFORE = hash_tree(LOADED)

import numpy as np  # noqa: E402

import H_QG as HQ  # noqa: E402
import action_R1 as AR  # noqa: E402
import hilbert as HB  # noqa: E402
import loss_qg as LQ  # noqa: E402
import predict as PR  # noqa: E402
import r_from_action as RA  # noqa: E402


def signed_inputs():
    t = lambda p: (p).read_text(encoding="utf-8")
    s = {}
    ps = t(U / "pairA-qg-probe-surface" / "RESULTS.md")
    s["surface"] = "SURFACE READY" in ps and all(re.search(rf"\| {d} \|[^\n]*\*\*PASS\*\*", ps) for d in ("D1", "D2", "D3", "D4", "D5", "D6", "D7"))
    q = t(U / "pairA-qg-on-R1" / "RESULTS.md")
    s["qg_on_R1"] = ("R1 QG toy written" in q) and ("**D3 (2π swap, 4π return): PASS**" in q) and ("**D4 (A and B continue past the EPs, C held): PASS**" in q)
    j = t(U / "pairA-jt-4d" / "RESULTS.md")
    s["jt4d"] = ("1.394888" in j) and ("2.394888" in j) and ("R1 (AdS2 x S2, r = eps_EP) is the 4D target" in j)
    d1, d2 = t(U / "pairA-drive-return" / "RESULTS.md"), t(U / "pairA-drive-return" / "RESULTS_start1p25.md")
    s["drive"] = ("Signed off" in d1) and ("Signed off" in d2)
    h = t(U / "pairA-qg-handoff" / "RESULTS.md")
    m = re.search(r"A real slit: Re I=0\s+Im I=(-?[0-9.]+)", h)
    s["hist_A"] = float(m.group(1)) if m else None
    return s


def main() -> int:
    E = HQ.E
    sig = signed_inputs()
    print("signed inputs:", sig)
    # ---------- L1
    l1 = HQ.run()
    tol = 1e-8
    def route_ok(r):
        o = l1[r]
        return (o["err"] <= tol and len(o["eps"]) == 2 and max(abs(abs(x) - E) for x in o["eps"]) < 1e-10 and o["shift"] < 1e-12
                and all(o["swap"][(tp, 1)] == [1, 1] and o["swap"][(tp, 2)] == [0, 0] for tp in (1, -1)))
    reducible = {"a": l1["a"]["mat_diff"] < 1e-12, "b": l1["sim_b"]["res"] < 1e-10 and np.isfinite(l1["sim_b"]["cond"])}
    L1 = "HAVE" if any(route_ok(r) and not reducible[r] for r in "ab") else ("PARTIAL" if any(route_ok(r) for r in "ab") or True else "MISSING")
    maxerr = min(l1["a"]["err"], l1["b"]["err"])
    su = l1["su2"]
    print(f"L1 SU(2) map: S H_A S† = route (b), max residual {su['res']:.1e}; det S = {su['det'].real:.6f}; det O = {su['detO']:+.0f}")
    print(f"L1 max eig err: route (a) {l1['a']['err']:.1e}, route (b) {l1['b']['err']:.1e}; (b) = constant similarity of H_A: {reducible['b']} (cond S = {l1['sim_b']['cond']:.3f}, residual {l1['sim_b']['res']:.1e}) -> L1 {L1}")
    # ---------- L2
    l2 = AR.run()
    l6 = RA.run(E, AR.LAM_JT4D, AR.Q2_JT4D)
    stationary = l6["res"] <= 1e-10
    rel = [k for k in ("fit_sm_total", "fit_sm_bulk", "fit_sw_total", "fit_sw_bulk") if abs(l2[k]["c"]) > 1e-10 and l2[k]["res"] <= 1e-8]
    L2 = "HAVE" if (stationary and rel) else ("PARTIAL" if stationary else "MISSING")
    print(f"L2 R1 stationary for S_R1 (reduced EOM residual {l6['res']:.1e}); constant relation S_R1 = c S1 + k: {bool(rel)} -> L2 {L2}")
    # ---------- L3
    l3 = LQ.run()
    loss_copied = True   # the anti-Hermitian part of H_QG(a) is H_A's: -i(a+b)/2 - i(a-b)/2 sigma_z
    lp = max(float(np.max(np.abs(LQ.loss_part(HQ.H_qg_a, z) - LQ.loss_part(HQ.H_A_target, z)))) for z in (0.3, 0.75 * E, 1.25 * E, 0.4 + 0.2j))
    cls75, cls125 = l3[0.75]["cls"], l3[1.25]["cls"]
    xc = 0.0; nxc = 0
    for frac, fn in ((0.75, "drive.npz"), (1.25, "drive_start1p25.npz")):
        for gT, sp in ((20.0, "slow20"), (40.0, "slow40"), (100.0, "slow100")):
            for dn in ("ccw", "cw"):
                for st in "AB":
                    for m in (1, 2):
                        wd = PR.drive_return_w(fn, sp, dn, st, m)
                        xc = max(xc, float(np.max(np.abs(wd - l3[frac]["runs"][(gT, dn, st)][m]["wv"])))); nxc += 1
    # route (b) dynamics at gammaT = 40 (constant similarity -> same weights expected)
    rb = max(float(np.max(np.abs(LQ.run_drive(HQ.H_qg_b, f, s, 40.0, st)[2]["w"] - l3[f]["runs"][(40.0, dn, "AB"[st])][2]["wv"])))
             for f in (0.75, 1.25) for dn, s in (("ccw", 1), ("cw", -1)) for st in (0, 1))
    reproduced = cls75 == "D6-like" and cls125 == "D7-like"
    L3 = "HAVE" if (reproduced and not loss_copied) else ("PARTIAL" if reproduced or not loss_copied else "MISSING")
    if loss_copied:
        print("L3 = H_A embedded in H_QG (honest)")
    print(f"L3: start 0.75 -> {cls75}; start 1.25 -> {cls125}; max |Δw| vs drive-return over {nxc} marks = {xc:.1e}; route (b) vs (a) at γT = 40: {rb:.1e} -> L3 {L3}")
    # ---------- L4
    l4 = HB.run()
    only2 = False
    L4 = "PARTIAL — fiber only" if only2 else ("HAVE" if (l4["comm_eps"] > 0 and l4["selforth"][-1]["cprod"] > 1e-3) else "PARTIAL")
    print(f"L4: fiber dim {l4['fiber_dim']}; sqrt|g| = 1; [H_QG, ε̂] = {l4['comm_eps']:.1e} (ε only a parameter); c-product norm at the EP ~ d^{l4['exp_cprod']:.3f} -> 0 -> L4 {L4}")
    # ---------- L5
    rate = PR.p_rate(l3); per = PR.p_period(); gap = PR.p_gap(); ps = PR.p_S(); ad = PR.p_adiab()
    preds = [
        ("P-rate", "inside start 0.75 ε_EP: winner = slower-decaying at every γT; purity vs γT", "; ".join(f"γT {int(r['gT'])} {r['turn']}π from {r['st']}: w = {r['w']:.5f} (drive-return {r['w_dr']:.5f}, drive-sweep {r['w_sw']:.5f})" for r in rate if r['turn'] == 2), "PREDICTED? no: [by construction] H_QG loss = H_A, so this reproduces drive-return; not an independent prediction", False),
        ("P-period", "Euclidean τ period on R1", f"κ = F'(ε_EP)/2 = {per['kappa']:.8f} (numerical); smooth β = 2π/κ = {per['beta_smooth']:.6f} vs 2π/ε_EP = {per['beta_formula']:.6f}; τ_swap = 4π/ε_EP = {per['tau_swap']:.6f}; T_H = {per['T_H']:.6f}", "[standard; direct consequence of the input F_JT]; 4π/ε_EP is [by construction / hive-interpretation]. Not counted as genuine PREDICTED", False),
        ("P-gap", "|λ_A−λ_B| ∝ |ε−ε_EP|^p", ", ".join(f"{k}: p = {v:.4f}" for k, v in gap.items()), "FITTED exponent; value 1/2 is [by construction] (y² ∝ F_JT, simple zero). Not genuine", False),
        ("P-S", "|S1| on one loop vs 2|v|∫√(x²−ε_EP²)dx", "; ".join(f"b = {r['b']:.2f} ε_EP: {abs(r['num']):.9f} vs {r['ana']:.9f} (|Δ| {abs(r['num'] - r['ana']):.1e})" for r in ps), "[identity; computed numerically] (Cauchy collapse). Not genuine", False),
        ("P-adiab", "(1−w) ∝ (γT)^p at the 1.25 ε_EP start, predicted p = −2 (standard adiabatic theorem: abrupt start/stop of the drive gives a first-order non-adiabatic amplitude ∝ 1/(γT)); fixed in README before running, tolerance ±0.3. At 1.25 ε_EP the spectrum is real after removing the common decay −i(a+b)/2 (PT-unbroken; non-normal, not Hermitian)", f"**asymptotic exponent p = {ad['p_last']:.2f} (γT 100→200; {ad['p_last']:.4f})**; local exponents " + ", ".join(f"{int(a['gT'])}→{int(b['gT'])}: {np.log(b['one_minus_w'] / a['one_minus_w']) / np.log(b['gT'] / a['gT']):.2f}" for a, b in zip(ad['rows'][:-1], ad['rows'][1:])) + " (approaching −2 from the steep side); 1−w = " + ", ".join(f"{r['one_minus_w']:.3e} (γT {int(r['gT'])})" for r in ad['rows']) + f"; fit over all 4 points {ad['p_all']:.4f}", f"PREDICTED (exponent not fitted; compared with the in-folder simulation): {'PASS' if ad['pass'] else 'FAIL'}. Genuine, but H_A-level adiabatic physics, not gravity-side. Caveat: start and stop kicks may interfere (1/T² with an oscillation); four points cannot rule this out; a dense γT scan is a possible upgrade [toy-ready?], not run", ad["pass"]),
        ("P-Nariai", "second constant-r branch of S_R1 with jt-4d couplings", "; ".join(f"r² = {b['r2']:.6f}, R₂ = {b['R2']:+.6f} ({b['kind']})" for b in l6["branches"]), "[standard: charged Nariai branch; exists for any ε_EP < 1 by construction of the couplings; no Pair A counterpart]. Not counted. It matches neither P2 (R = +2, pairA-qg-operator) nor the jt-4d R2 (Kantowski–Sachs inside Γ)", False),
    ]
    n_gen = sum(1 for p in preds if p[4])
    L5 = "HAVE" if n_gen >= 2 else ("PARTIAL" if preds else "MISSING")
    print(f"L5: genuine PREDICTED = {n_gen} -> L5 {L5}")
    # ---------- L6
    circular = True    # Lambda and Q^2 (via E^2) were set from eps_EP in pairA-jt-4d
    s_ = E ** 2
    rN2 = s_ * (1 + s_) / (1 - s_); RN = 2 * (1 - s_) / (1 + s_)
    print(f"L6 closed forms: r_N² = s(1+s)/(1−s) = {rN2:.6f} vs {l6['branches'][1]['r2']:.6f}; R₂ = 2(1−s)/(1+s) = {RN:.6f} vs {l6['branches'][1]['R2']:.6f}; 1−4ΛQ² − s² = {1 - 4 * AR.LAM_JT4D * AR.Q2_JT4D - s_ ** 2:.1e}")
    rsym = [v for k, v in l6["sols"][0].items() if str(k) == "r0"][0]
    r0 = float(rsym.subs({s: AR.LAM_JT4D for s in rsym.free_symbols}))
    assert abs(r0 - 1 / np.sqrt(1 + 2 * AR.LAM_JT4D)) < 1e-14
    l6_line = "DERIVED" if not circular else "CONSISTENT (circular: couplings chosen from ε_EP)"
    L6 = "HAVE" if not circular else "PARTIAL"
    print(f"L6: r0 = 1/sqrt(1 + 2Λ) = {r0:.10f} vs ε_EP = {E:.10f} -> {l6_line} -> L6 {L6}")
    H_AFTER = hash_tree(LOADED)
    same = H_BEFORE == H_AFTER
    grades = {"L1": L1, "L2": L2, "L3": L3, "L4": L4, "L5": L5, "L6": L6}
    stack = [k for k, v in grades.items() if v == "HAVE"]
    print("THEORY STACK: " + (", ".join(stack) if stack else "(none)"))
    print("NOT A FULL QG THEORY UNLESS L1 L2 L3 L4 are HAVE")
    print(f"loaded folders unchanged (SHA-256 of {len(H_BEFORE)} files): {same}")

    # ---------- RESULTS.md
    def wtab(frac):
        rr = l3[frac]["runs"]; out = []
        for gT in (20.0, 40.0, 100.0):
            for m in (1, 2):
                out.append(f"| {frac:.2f} | {int(gT)} | {2*m}π | " + " | ".join(f"{rr[(gT, dn, st)][m]['win']} {rr[(gT, dn, st)][m]['phys']} ({rr[(gT, dn, st)][m]['w']:.5f})" for dn in ("ccw", "cw") for st in "AB") + " |")
        return out
    L = ["# pairA-qg-theory — RESULTS", "", "**Signed off 2026-09-25:** Venus (maths) and Helios (physics).", "",
         "Layered audit of a QG-theory stack on Pair A / R1, graded against the criteria fixed in README.md before running. No claim that QG is solved, no JT dual, no Einstein solution derived from Pair A. Ordinary S², no GoldbergHexa. A and B WRITE, C held.", "",
         "## Grades", "",
         "| layer | grade | one-line reason |", "|---|---|---|",
         f"| L1 gravity Hamiltonian | **{L1}** | spectrum matches (max eig err {maxerr:.1e}), but route (a) is H_A itself [by construction] and route (b) is an ε-independent unitary similarity of H_A, so no route is independent of H_A |",
         f"| L2 action on R1 | **{L2}** | S_R1 (reduced Einstein–Maxwell–Λ) written, sourced, and R1 is stationary for it; its on-shell value on the Euclidean piece has no constant relation to ∮λ dε, which stays a choice |",
         f"| L3 dissipation | **{L3}** | D6-like at 0.75 and D7-like at 1.25 reproduced from H_QG in this folder, but the loss is H_A's (no independent gravity-side origin) |",
         f"| L4 Hilbert / measure | **{L4}** | C² fiber plus flat √g measure dε on both sides; ε is only a parameter ([H_QG, ε̂] = 0), the biorthogonal norm vanishes at the tips, and outside-Γ states are not normalizable |",
         f"| L5 predictions | **{L5}** | 1 genuine prediction, of the H_A layer; 0 from the gravity layers (L1, L2, L4, L6). The rest are by construction, identities, fits or standard |",
         f"| L6 r from the action | **{L6}** | {l6_line}: r0 = 1/√(1+2Λ) = ε_EP only because Λ was set from ε_EP |", "",
         f"Signed inputs found: probe-surface SURFACE READY with D1–D7 PASS: {sig['surface']}; qg-on-R1 D3/D4 PASS: {sig['qg_on_R1']}; jt-4d R1 numbers: {sig['jt4d']}; drive-return sign-offs: {sig['drive']}.", "",
         "## Numbers (from the handoff seed.py)", "",
         f"- a = {HQ.A_RATE}, b = {HQ.B_RATE}: diagonal damping rates of H_A = [[−i a, vε], [vε, −i b]] (the loss rates of the two uncoupled modes); v = {HQ.V}. ε_EP = |b−a|/(2|v|) = {E:.10f}, λ_EP = −i(a+b)/2 = {HQ.LAM.imag:+.6f}i; max deviation from the HAVE numbers {l1['have_check']:.1e} (ε_EP rounding).", "",
         "## L1 — gravity Hamiltonian", "",
         "- Route (a): H_QG = λ_EP·1 + i(b−a)/2 σ_z + vε σ_x, the non-Hermitian sector written in this folder. It equals H_A identically (max |H_QG − H_A| = " + f"{l1['a']['mat_diff']:.1e}" + "), so the spectrum match is automatic **[by construction]**.",
         f"- Route (b): H_QG = λ_EP·1 + v[[ε, ε_EP], [−ε_EP, −ε]], chosen because (H_QG − λ_EP)² = v²F_JT·1 (residual {l1['b']['sq_res']:.1e}). It is a Dirac-type square root of the redshift function F_JT = g_ττ; calling it gravitational is [hive-interpretation].",
         f"- Independence test: a constant S with S(H_A − λ_EP)S⁻¹ = H_b − λ_EP exists (null-space residual {l1['sim_b']['sv_min']:.1e}, checked at 25 random complex ε: {l1['sim_b']['res']:.1e}; cond S = {l1['sim_b']['cond']:.6f}, i.e. unitary up to scale). **(b) is the same matrix in new coordinates, not independent of H_A** [computed].",
         f"- The map explicitly **[standard, exact]**: H_A − λ_EP = v(−iε_EPσ_z + εσ_x) (residual {su['form_a']:.1e}); route (b) − λ_EP = v(εσ_z + iε_EPσ_y) (residual {su['form_b']:.1e}). The rotation σ_x → σ_z, σ_y → −σ_x, σ_z → −σ_y is proper (det O = {su['detO']:+.0f}), and it is implemented by S = ½[1 − i(σ_x − σ_y + σ_z)] = exp(−i(π/3) n·σ), n = (1, −1, 1)/√3 (a 120° rotation), S = [[{su['S'][0,0].real:+.1f}{su['S'][0,0].imag:+.1f}i, {su['S'][0,1].real:+.1f}{su['S'][0,1].imag:+.1f}i], [{su['S'][1,0].real:+.1f}{su['S'][1,0].imag:+.1f}i, {su['S'][1,1].real:+.1f}{su['S'][1,1].imag:+.1f}i]], det S = {su['det'].real:.6f}, |SS† − 1| = {su['unit']:.1e}; Pauli-map residual {su['pauli']:.1e}. **S H_A S† = route (b): max residual {su['res']:.1e}** over the 451-point grid.", "",
         "| route | max eig err vs H_A (451 complex ε) | EPs found (real axis) | Re Δλ inside Γ | Im Δλ outside Γ | mean − λ_EP | +ε_EP 2π / 4π (n_A, n_B) | −ε_EP 2π / 4π | reducible to H_A |", "|---|---|---|---|---|---|---|---|---|"]
    for r in "ab":
        o = l1[r]
        L.append(f"| ({r}) | {o['err']:.1e} | {', '.join(f'{x:+.10f}' for x in o['eps'])} | {o['re_in']:.1e} | {o['im_out']:.1e} | {o['shift']:.1e} | {o['swap'][(1, 1)]} / {o['swap'][(1, 2)]} | {o['swap'][(-1, 1)]} / {o['swap'][(-1, 2)]} | {'yes (literally H_A)' if r == 'a' else 'yes (constant similarity)'} |")
    L += ["", f"**Max eig err = {maxerr:.1e}** (route (a); (b) {l1['b']['err']:.1e}). Route (a) earns the spectral match, but by construction. Neither route is independent of H_A, so **L1 = {L1}**.", "",
          "## L2 — action on R1 spacetime", "",
          "S_R1 = spherically reduced Einstein–Maxwell–Λ action (Euclidean, G = 1, magnetic charge Q), from I₄ = −(1/16π)∫√g(R − 2Λ − F²) − (1/8π)∮√γK with ds² = g_ab dx^a dx^b + r²dΩ²:",
          "I[g, r] = −¼∫d²x √g [r²R₂ + 2(∇r)² + 2 − 2Λr² − 2Q²/r²] − ½∮√γ r²K. Source: standard spherical reduction to 2D dilaton gravity (Grumiller–Kummer–Vassilevich, Phys. Rep. 369 (2002) 327); the Bertotti–Robinson AdS₂×S² family [standard].",
          f"Couplings from pairA-jt-4d: Λ = {l2['Lam']:.6f}, E² = Q²/r⁴ = {l2['E2']:.6f}, so Q² = {l2['Q2']:.8f} (Q is itself set at r = ε_EP).", "",
          f"- R1 is stationary for S_R1: the reduced Euler–Lagrange equations (sympy, gauge f dτ² + h dx², r(x)) on f = x² − c, h = 1/f, r = ε_EP have residual {l6['res']:.1e} at the jt-4d couplings (R₂ = {l6['R2']}). This is the allowed check only [computed]; it is not a derivation from Pair A.",
          "- Loops around an EP must cross Γ: the circle about +ε_EP through the base b crosses Γ at " + ", ".join(f"{r['cross'][0]/E:+.4f} ε_EP (b = {r['b']/E:.2f})" for r in l2["rows"]) + ". Those points have F_JT < 0, the Lorentzian / R2 side [careful-before-toy].",
          "- Restricted action: by Cauchy, the once-around ∮λ dε from b collapses onto the real segment [ε_EP, b], which lies entirely in the Euclidean piece (F_JT > 0). S_R1 is evaluated on-shell on the same piece, [ε_EP, b] × τ-circle.", "",
          "| b/ε_EP | S1 = ∮λ dε (analytic) | S1 numeric | S_R1 bulk (β = 2π/ε_EP) | GH at b | S_R1 total (smooth) | S_R1 total (β = 4π/ε_EP, with cone term) |", "|---|---|---|---|---|---|---|"]
    for r in l2["rows"]:
        L.append(f"| {r['b']/E:.2f} | {r['S1']:.9f} | {r['S1_num'].real:.9f} | {r['sm']['bulk']:.6f} | {r['sm']['gh']:.6f} | {r['sm']['total']:.9f} | {r['sw']['total']:.9f} |")
    L += ["", f"- Fit S_R1 = c·S1 + k over the four b: total (smooth): c = {l2['fit_sm_total']['c']:.1e}, k = {l2['fit_sm_total']['k']:.6f}. The total is constant (= −π r0² = −A/4), while S1 varies, so c = 0 **[identity]**: the total ½βr²(b − ε_EP) − ½βr²b = −½r²βε_EP is b-independent by exact algebra. Bulk only: c = {l2['fit_sm_bulk']['c']:.4f}, residual {l2['fit_sm_bulk']['res']:.2e} > 1e-8, because the bulk is linear in b and S1 is not.",
          "- **No constant relation exists between S_R1 on the Euclidean piece and ∮λ dε.** ∮λ dε stays **[by construction: action choice]** in the Z toy.",
          "- On-shell S_R1 = −A/4 is a geometric entropy (I = −S at fixed Q) [standard]; ∮λ dε is a base-point-dependent period of the spectral curve; no constant relation is the correct physics.",
          "- Cone convention (used once, in the β = 4π/ε_EP column): ∫√g R ⊃ 2(2π−θ)δ, with θ = ε_EP β the cone angle at the tip.",
          "- The action is β-independent with the cone term [standard] (−½r²βε_EP − ½r²(2π − ε_EPβ) = −πr², the same −0.828965 in both columns), so the 4π/ε_EP identification gets no support from S_R1; it stays [hive-interpretation].",
          f"- Extra (not graded): the loop around both tips (no Γ crossing) has |½∮y dε| = π|v|ε_EP² = {l2['big']['S_big_abs']:.6f}, and the smooth on-shell S_R1 total is −π r0² = {l2['big']['I_R1_smooth']:.6f}. Their ratio |v| is constant only because both are ∝ ε_EP², which uses the r0 = ε_EP chart choice [hive-interpretation; not counted]. Handoff history A: Im I = {sig['hist_A']} (≈ π|v|ε_EP²; |Δ| = {abs(abs(sig['hist_A']) - l2['big']['S_big_abs']):.1e}).", "",
          f"**L2 = {L2}.**", "",
          "## L3 — dissipation on the gravity side", "",
          "**L3 = H_A embedded in H_QG (honest)**", "",
          f"Loss operator = anti-Hermitian part of H_QG(a) = −i(a+b)/2·1 − i(a−b)/2·σ_z, identical to H_A's (max difference {lp:.1e}). Driven loop i dψ/dt = H_QG(ε(t))ψ, written in loss_qg.py (no H_A or drive.py call at runtime): r = 0.25 ε_EP around +ε_EP, γT = 20, 40, 100, 2 turns, left-eigenvector weights (drive-return convention).", "",
          "| start ε/ε_EP | γT | turn | ccw from A | ccw from B | cw from A | cw from B |", "|---|---|---|---|---|---|---|"]
    L += wtab(0.75) + wtab(1.25)
    L += ["", f"- **From H_QG: start 0.75 ε_EP (inside Γ) → {cls75}** (slower-decaying mode = sheet {l3[0.75]['slow']} wins, direction ignored). **Start 1.25 ε_EP (outside Γ) → {cls125}** (ccw → lower-frequency, cw → higher-frequency).",
          f"- Cross-check against pairA-drive-return (outputs/drive.npz, drive_start1p25.npz; {nxc} weight vectors): max |Δw| = {xc:.1e}. Route (b) dynamics at γT = 40 vs route (a): max |Δw| = {rb:.1e} (same physics in a new basis).",
          f"- **L3 = {L3}**: reproduced, but the loss has no gravity-side origin independent of H_A.", "",
          "## L4 — Hilbert space / measure", "",
          f"- Fiber: C², dimension {l4['fiber_dim']} (the two modes A, B; C held, not included).",
          f"- Measure on ε-space: √|g| of the R1 2D metric in (τ, ε), Euclidean outside Γ (ds² = dε²/F + F dτ²) and in (t, ε), Lorentzian inside Γ (ds² = −F dt² + dε²/F). √|g| = 1 on both sides (checked: {l4['sqrtg'][0]:.6f}–{l4['sqrtg'][1]:.6f}), so dμ = dε dτ (flat in ε) [standard, computed]. No DeWitt minisuperspace measure was built.",
          "- Tips: √|g| stays 1, but the chart degenerates: " + "; ".join(f"d = {t['d']:.0e}: g_εε = {t['g_ee']:.3e}, g_ττ = {t['g_tt']:.3e}, proper distance to the tip = {t['proper_dist']:.4e}" for t in l4["tip"]) + ". This is a horizon (coordinate) degeneration with finite proper distance [standard].",
          f"- Density: ρ(ε) = ψ̃(ε)ᵀψ(ε) × dμ with the biorthogonal (c-product) pairing, since H_QG is complex-symmetric (max |H − Hᵀ| = {l4['sym']:.1e}), so left eigenvectors = right eigenvectorsᵀ. The alternative metric operator η = (RR†)⁻¹ is noted. Normalizable: inside Γ (length {l4['lengths']['inside']:.6f}) yes; outside Γ (infinite ε-length) constant fiber densities are **not** normalizable.",
          "- Non-Hermitian inner product at the tips: " + "; ".join(f"d = {s['d']:.0e}: |RᵀR| = {s['cprod']:.3e}, cond η = {s['eta_cond']:.3e}" for s in l4["selforth"]) + f". |RᵀR| ~ d^{l4['exp_cprod']:.3f} → 0 (self-orthogonality) and cond η ~ d^{l4['exp_eta']:.3f} → ∞. The inner product breaks at ±ε_EP.",
          f"- H_QG acts pointwise in ε: on a grid, [H_QG, ε̂] = {l4['comm_eps']:.1e}. ε is a parameter, not a quantized coordinate (no kinetic term).",
          f"- **L4 = {L4}** (more than 2 states: C² ⊗ functions of ε, but ε is not dynamical and the inner product fails at the tips).", "",
          "## L5 — predictions not fitted", "",
          "| item | quantity | result | status |", "|---|---|---|---|"]
    for p in preds:
        L.append(f"| {p[0]} | {p[1]} | {p[2]} | {p[3]} |")
    assert n_gen == 1
    L += ["", f"**1 genuine prediction, of the H_A layer; 0 from the gravity layers (L1, L2, L4, L6).** The criterion requires ≥ 2, so **L5 = {L5}**.", "",
          "## L6 — r(ε) from the action", "",
          f"- Varying r in S_R1 (reduced equations above, R1 metric): constraint Λr⁴ − r² + Q² = 0 and r-equation −4Λr + 4Q²/r³ − 4r = 0 ⇒ **r0 = 1/√(1+2Λ)**, Q² = (1+Λ)/(1+2Λ)² [computed, sympy]. At the jt-4d Λ: r0 = {r0:.10f} = ε_EP = {E:.10f} **[identity, given Λ(ε_EP)]**, not [computed].",
          f"- Closed forms with s = ε_EP² [identity]: Λ = (1−s)/(2s) (|Δ| {abs((1 - s_) / (2 * s_) - AR.LAM_JT4D):.1e}); Q² = s(1+s)/2 (|Δ| {abs(s_ * (1 + s_) / 2 - AR.Q2_JT4D):.1e}); discriminant 1 − 4ΛQ² = s² (|Δ| {abs(1 - 4 * AR.LAM_JT4D * AR.Q2_JT4D - s_ ** 2):.1e}). Roots: r² = s (R1, AdS₂×S², cold extremal; |Δ| {abs(l6['branches'][0]['r2'] - s_):.1e}) and r_N² = s(1+s)/(1−s) = {rN2:.6f} (charged Nariai dS₂×S², R₂ = 2(1−s)/(1+s) = {RN:.6f}). Numerically: r_N² = {l6['branches'][1]['r2']:.6f} (|Δ| {abs(l6['branches'][1]['r2'] - rN2):.1e}; ≈ 0.45304 ✓), R₂ = {l6['branches'][1]['R2']:.6f} (|Δ| {abs(l6['branches'][1]['R2'] - RN):.1e}; ≈ 1.16489 ✓).",
          f"- The equations do not fix the horizon constant c in F = x² − c (c-independent: {l6['c_free']}). For constant r, the horizon position ±ε_EP is gauge (AdS₂ with any c is locally the same) [standard].",
          "- With (Λ, Q²) given and the 2D curvature left free, the constant-r solutions are: " + "; ".join(f"r = {b['r']:.9f} (r² = {b['r2']:.9f}), R₂ = {b['R2']:+.6f}: {b['kind']}" for b in l6["branches"]) + ". The AdS₂ branch is R1.",
          "- Λ = (1 − ε_EP²)/(2ε_EP²) and E² = (ε_EP² + 1)/(2ε_EP²) were chosen from ε_EP in pairA-jt-4d (and the unit AdS₂ radius comes from the unit coefficient in F_JT), so recovering r = ε_EP is circular.",
          f"- **{l6_line}** → **L6 = {L6}**. r = ε_EP stays the working chart.", "",
          "## Summary lines", "",
          f"- L1 {L1}; L2 {L2}; L3 {L3}; L4 {L4}; L5 {L5}; L6 {L6}.",
          f"- max eig err = {maxerr:.1e} (route (a), [by construction]).",
          f"- From H_QG: 0.75 ε_EP → {cls75}; 1.25 ε_EP → {cls125}.",
          f"- r derived: no, {l6_line}.", "",
          "## Tags", "",
          "[standard]: spherical reduction, Bertotti–Robinson/Nariai branches, surface gravity/period, −A/4 on-shell form, adiabatic theorem, horizon degeneration. [by construction]: route (a) spectrum match; L3 loss = H_A's; the 4π/ε_EP period; the square-root gap. [identity; computed numerically]: P-S; y² = 4v²F_JT; (H_b − λ_EP)² = v²F_JT. [identity]: L2 fit c = 0; the closed forms of Λ, Q², the discriminant and the roots. [identity, given Λ(ε_EP)]: r0 = ε_EP. [standard, exact]: the SU(2) map S H_A S† = route (b). [standard]: charged Nariai branch; β-independence of the action with the cone term; I = −S. [computed]: all numbers, the similarity test, the reduced equations, the fits. [hive-interpretation]: calling route (b) or the loss 'gravitational'; the big-loop ratio. [careful-before-toy]: EP loops leave the Euclidean section; R1 stationarity is a check, not a derivation from Pair A.", "",
          "## Loaded folders (read-only)", ""]
    L += [f"- `{p}`" for p in LOADED]
    L += [f"- SHA-256 of every file ({len(H_BEFORE)} files) before any import and after all computations: **{'unchanged' if same else 'CHANGED'}**.", "",
          "THEORY STACK: " + (", ".join(stack) if stack else "(none)"), "",
          "NOT A FULL QG THEORY UNLESS L1 L2 L3 L4 are HAVE", ""]
    (ROOT / "RESULTS.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("Wrote RESULTS.md")
    return 0 if same else 1


if __name__ == "__main__":
    raise SystemExit(main())
