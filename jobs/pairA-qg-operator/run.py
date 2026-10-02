"""pairA-qg-operator: the smallest gravity-side object whose cut, tips, monodromy and inside/outside switch are Pair A's.
`python run.py` writes RESULTS.md. No Einstein solver, no new MHD matrix."""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True
from pathlib import Path  # noqa: E402

ROOT = Path(__file__).resolve().parent
# operator.py in this folder would shadow the stdlib 'operator' module: drop the script dir from sys.path,
# import the stdlib pieces first, then load our operator.py under another name.
sys.path[:] = [p for p in sys.path if Path(p or ".").resolve() != ROOT]
import operator as _stdlib_operator  # noqa: E402,F401
import importlib.util  # noqa: E402

import numpy as np  # noqa: E402
import scipy.integrate  # noqa: E402,F401
import scipy.special  # noqa: E402,F401

sys.path.append(str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import spec_D  # noqa: E402  (no loaded-folder import at module level)

H_BEFORE = spec_D.hash_tree()   # before anything from the loaded folders is imported

import curve  # noqa: E402
import match  # noqa: E402

_spec = importlib.util.spec_from_file_location("pairA_operator", ROOT / "operator.py")
OP = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(OP)

QG_LINE = "QG Hamiltonian = P1+P2 plus H_A dissipation for D6 D7"
TAG_LINE = ("Tag: [hive-interpretation] — an operator built to match the D1–D7 spec, not derived from a gravity theory; no JT dual is claimed "
            "(P2 has the 2D dilaton-gravity metric form with the dS sign, not JT's; noted as [standard] resemblance only).")
NO4D = "no 4d Einstein metric in this folder"
DS2_LINE = 'P2 has the Euclidean dS₂ static-patch (round-sphere) form, with its period doubled [standard]. (JT would be R = −2, AdS₂, F = r² − r_h²; here F = ε_EP² − ε² gives R = +2.)'
TOY_LINE = "QG-side toy = edge operator P1 at each tip, on background geometry P2, with H_A's loss supplying D6/D7 [hive-interpretation]. (P2 is a metric, not an operator, so '+' here means 'together', not an operator sum.)"
P1_NOTE = 'P1 = −∂x² + x is Hermitian; nothing merges at its turning point, and the Ai eigenfunctions stay a regular basis. The √ exponent and the one-turn swap live in the WKB momenta ±√(E − x), which is what is measured here, not an exceptional point of P1. The true local EP normal form is the 2×2 Jordan-type matrix [[0,1],[ε−ε_EP,0]].'


def main() -> int:
    S = spec_D.load(H_BEFORE)
    E = S["EPS_EP"]
    for n, t in S["asserts"]:
        print(f"assert {n}: {t}")
    C = curve.run(S)
    P = OP.run(S)
    H_MID = spec_D.hash_tree()
    c_files = sorted({p for p, i, l in spec_D._probe_module("load_surface").grep([spec_D.HANDOFF], r"\bC imaginary|\"C\"|held|NOT-SELECTED")})
    M = match.run(S, C, P, H_BEFORE, H_MID, c_files)
    rh_ok, rh_line = match.riemann_hurwitz(S, C, P)
    print(rh_line)
    ok15 = all(r["result"] == "PASS" for r in M[:5])
    ok67 = all(r["result"] == match.INHERIT for r in M[5:])
    for r in M:
        print(f"{r['id']} {r['result']} {r['tag']}")
    qg = QG_LINE if (ok15 and ok67) else "QG Hamiltonian: NOT MATCHED — failed: " + ", ".join(r["id"] for r in M[:5] if r["result"] != "PASS")
    print(qg)
    print(TOY_LINE)
    sg = P["sig"]
    if sg["res"] < 1e-13 and sg["ok_in"] and sg["ok_out"]:
        sig_line = (f"F = −y²/(4v²) [standard, residual {sg['res']:.1e}]: P2 is Euclidean (F>0) exactly in the split-decay phase inside Γ and flips signature (F<0) exactly in the split-frequency phase outside Γ, "
                    "so P2's signature change sits on the same line as the inside/outside switch.")
        sig_line += f" (y = λA − λB from H_A eigenvalues; {sg['n_in']} real ε inside Γ, {sg['n_out']} outside, |ε| ≤ 3 ε_EP.)"
    else:
        sig_line = f"F = −y²/(4v²) check NOT PASSED (residual {sg['res']:.1e}, inside ok {sg['ok_in']}, outside ok {sg['ok_out']}) — not printed as a finding."
    print(sig_line)
    p2, v, a, w, dr = P["p2"], C["verify"], P["airy"], P["wkb"], P["dir"]
    cone = p2["cone_final"]
    print(f"cone angle +ε_EP = {cone['+ε_EP']:.8f} = {cone['+ε_EP']/np.pi:.6f}π; smooth period = {p2['tau_smooth']:.6f}; τ_E = {p2['tauE']:.6f}")
    print(f"curve residual |(λA−λB)² − y²| max = {v['res_y2']:.1e} (scale {v['scale']:.3f}); R = {p2['R'][0]:.6f}")

    L = ["# pairA-qg-operator — RESULTS", "", "**Signed off 2026-09-25:** Venus (maths) and Helios (physics).", "",
         "What it is (Akitti): the smallest gravity-side object whose cut, tips, monodromy and inside/outside switch are Pair A's. "
         "Two-mode toy; no Einstein solver, no new MHD matrix.", "",
         "## Result", "", qg, TOY_LINE, TAG_LINE, DS2_LINE, "", NO4D, "",
         "Split: **P1 = tip only** (Airy edge; link to the EP is a [standard analogy] via WKB momenta; no ε_EP, no Γ, no second tip by itself). **P2 = global cut, tips and period** (F = ε_EP² − ε², τ_E = 4π/ε_EP). "
         "**D6 and D7 need the dissipative Pair A structure** (H_A's non-Hermitian loss), not P1 or P2.", "",
         "**Regularity, stated plainly:** with τ_E = 4π/ε_EP the P2 geometry is **not** a smooth Euclidean horizon. The smooth-horizon period is 4π/|F′(±ε_EP)| = 2π/ε_EP = "
         f"{p2['tau_smooth']:.6f}; τ_E = {p2['tauE']:.6f} is twice that, so each tip is a conical point with total angle {cone['+ε_EP']/np.pi:.6f}π (+ε_EP) and {cone['−ε_EP']/np.pi:.6f}π (−ε_EP), "
         "i.e. 4π: conical excess, a double-cover branch point. [hive-interpretation]: a 4π cone is a double cover, so one smooth turn (2π) is half the geometric circle, matching the Jhat2 swap. "
         "That the 4π cone matches Jhat4 = I is [by construction, given τ_E = 4π/ε_EP from the handoff]. [computed]: this choice gives both tips the same angle "
         f"({cone['+ε_EP']/np.pi:.6f}π, {cone['−ε_EP']/np.pi:.6f}π) and a consistent χ = {p2['gb']/(2*np.pi):.6f} (see P2 (ii)).", "",
         "Topology: one sphere (chi=2) double-covering the round sphere, branched at ±ε_EP.", "", rh_line, "", sig_line, "",
         "## Spec (spec_D.py)", "",
         "Handoff and drive-return values, asserted against Akitti's numbers (not hard-coded as inputs):", ""]
    L += [f"- {n}: {t}" for n, t in S["asserts"]]
    L += ["", "D1–D7 loaded from the probe surface (its dictionary.py recomputed them this run; each row's claim, tag and PASS cross-checked against its RESULTS.md):", "",
          "| row | property | probe result | probe tag | in probe RESULTS.md |", "|---|---|---|---|---|"]
    for r in S["D"]:
        L.append(f"| {r['id']} | {r['claim']} | {'PASS' if r['result'] else 'FAIL'} | {r['tag']} | {'YES' if r['in_results'] else 'NO'} |")
    L += ["", "Probe conditions per row (verbatim from its dictionary):", ""]
    L += [f"- {r['id']}: {r['conditions']}" for r in S["D"]]
    mo, dt = C["monodromy"], C["detours"]
    L += ["", "## Curve (curve.py)", "",
          f"y² = 4v²(ε² − ε_EP²); eigenvalues of H_A = λ_EP ± y/2 with λ_EP = {E*0 + S['LAM_EP'].imag:+.6f}i kept.", "",
          f"- Grid of {v['n']} complex ε ({v['box']}): max |(λA−λB)² − y²| = {v['res_y2']:.1e} (max |y²| = {v['scale']:.3f}); max min(|λA−λB ∓ y|) = {v['res_y']:.1e} "
          f"(largest at the tips, where H_A is defective and numerical eigenvalues carry a ~√(machine ε) error); max |λA + λB − 2λ_EP| = {v['res_sum']:.1e}.",
          "- Monodromy of y (continuous branch): " + "; ".join(f"{k}: n = {d['n']}" for k, d in mo.items()) + ".",
          f"- Square-root exponent of |y| at the tips: {C['exp_curve']['+ε_EP']:.4f} (+ε_EP), {C['exp_curve']['−ε_EP']:.4f} (−ε_EP).",
          "- Two-detour test on the curve: " + "; ".join(f"{nm}: {d['start']:+.2f} → {d['end']:+.2f} ε_EP, y_above = {d['y_above'].real:+.6f}, y_below = {d['y_below'].real:+.6f}, swapped {'YES' if d['swapped'] else 'NO'}, min |y| = {d['min_gap']:.6f}" for nm, d in dt.items()) + ".",
          f"- Period τ = 4π/ε_EP = {C['tau']:.8f} (asserted ≈ 24.46339).", "",
          "Cover U_G[γ] = (−1)^{I(γ,Γ)} vs Φ(n), recomputed by the probe surface's cover.py on the same six loops:", "",
          "| loop | I | signed | U_G | n_A | n_B | Φ = U_G |", "|---|---|---|---|---|---|---|"]
    for r in C["cover"]:
        L.append(f"| {r['name']} | {r['I']} | {r['I_signed']:+d} | {r['U_G']:+d} | {r['n_A']} | {r['n_B']} | {'YES' if r['match'] else 'NO'} |")
    L += ["", "## Operator P1 — edge (operator.py)", "",
          "H_edge = −∂x² + x (Airy), local at each EP [standard analogy].", "", P1_NOTE, "",
          f"- Ai solves H_edge ψ = Eψ with ψ = Ai(x − E): finite-difference relative residual (h = {a['h']}, x ∈ [{a['x_range'][0]}, {a['x_range'][1]}]) = {a['rel_res'][0.0]:.1e} (E = 0), {a['rel_res'][1.0]:.1e} (E = 1).",
          f"- Dirichlet on (0, {dr['L']}), n = {dr['n']}: lowest eigenvalues " + ", ".join(f"{x:.5f}" for x in dr['ev']) + " vs −a_k (Airy zeros) " + ", ".join(f"{x:.5f}" for x in dr['airy'])
          + f"; max relative error {dr['rel_err']:.1e}; matrix Hermitian (max |H − H†| = {dr['herm']:.1e}).",
          f"- Square-root link [standard analogy]: WKB momenta p(x) = ±√(E − x) merge at the turning point x = E; exponent of |p+ − p−| vs |x − E| = {w['exponent']:.4f} (E = 0), {P['wkb1']['exponent']:.4f} (E = 1); "
          f"H_A gap exponent near the tips: see D2 (≈ 0.5). Same local square-root form as y ∝ √(ε ∓ ε_EP).",
          f"- Monodromy [standard analogy]: tracking ±√(E − x) once around the turning point swaps the branches (n = {w['n_once']}), twice returns them (n = {w['n_twice']}) — the same as the 2π swap / 4π return of A and B.",
          "- P1 is only the tip: it carries no ε_EP, no Γ and no second tip by itself.", "",
          "## Operator P2 — global mini-superspace (operator.py)", "",
          f"F(ε) = ε_EP² − ε², ds_E² = dε²/F + F dτ_E², τ_E period 4π/ε_EP = {p2['tauE']:.6f}.", "",
          f"- (i) Chart: F > 0 at {p2['n_pos']} of {p2['n_grid']} real grid points in [−2, 2] ε_EP, exactly those with |ε| < ε_EP; F(+ε_EP) = {p2['tipF'][0]}, F(−ε_EP) = {p2['tipF'][1]}; "
          f"F(ε_EP(1 ∓ 1e-9)) = {p2['nearF'][0]:+.1e}, {p2['nearF'][1]:+.1e}. The Euclidean (real positive) chart is Γ and dies at both tips (D1, D2). F = −y²/(4v²) (residual {p2['link']:.1e}).",
          f"- (ii) Regularity: F′(±ε_EP) = ∓2ε_EP (numerical {p2['Fp_num'][1]:+.6f}, {p2['Fp_num'][-1]:+.6f}); smooth period 4π/|F′| = 2π/ε_EP = {p2['tau_smooth']:.6f}. "
          f"With τ_E = 4π/ε_EP the cone angle (circumference / proper radius as δ → 0) is:", "",
          "| δ/1 from tip | proper radius ρ (+ε_EP) | angle (+ε_EP) / π | angle (−ε_EP) / π | angle with smooth period / π |", "|---|---|---|---|---|"]
    for (d, rho, ang, angs), (_, _, angm, _) in zip(p2["cones"]["+ε_EP"], p2["cones"]["−ε_EP"]):
        L.append(f"| {d:.0e} | {rho:.6e} | {ang/np.pi:.6f} | {angm/np.pi:.6f} | {angs/np.pi:.6f} |")
    L += ["", f"  Total cone angle 4π at each tip: conical excess (double-cover branch point), NOT smooth. With the smooth period it would be 2π. "
          f"Gauss–Bonnet check: ∫K dA = {p2['area']/np.pi:.6f}π (K = R/2 = 1, area = 2ε_EP τ_E) plus Σ(2π − θ) = {sum(2*np.pi - t for t in cone.values())/np.pi:.6f}π gives {p2['gb']/np.pi:.6f}π = 2πχ with χ = {p2['gb']/(2*np.pi):.6f} "
          "(one sphere (chi=2) double-covering the round sphere, branched at ±ε_EP). "
          "[hive-interpretation]: one smooth turn (2π) is half the geometric circle → Jhat2 swap. The 4π cone ↔ Jhat4 = I is [by construction, given τ_E = 4π/ε_EP from the handoff]; "
          "[computed]: this choice gives both tips the same angle and a consistent χ.",
          "  Explanation: with ε = ε_EP cos ρ and φ = ε_EP τ_E, the metric dε²/F + F dτ_E² = dρ² + sin²ρ dφ² is the unit sphere with φ running over 4π. "
          "The curvature integral ∫K dA = 8π (K = R/2 = 1, area 2ε_EP τ_E = 8π) alone would give χ = 4 (two separate spheres). "
          "The two cone terms 2(2π − 4π) = −4π bring it to 4π = 2πχ, so χ = 2: one connected sphere wrapping the round sphere twice, joined at the two tips. "
          "Riemann–Hurwitz independently gives χ = 2·2 − 2 = 2 (see the cross-check line above).",
          f"- (iii) λ_EP kept [by construction]: P2 carries λ_EP as an additive constant; spectrum λ_EP ± y/2 with y² = −4v²F reproduces H_A on 77 real ε in [−1.9, 1.9] ε_EP (max residual {p2['res_spec']:.1e}, largest at the tips where H_A is defective).",
          f"- (iv) Curvature R = −F″ = " + ", ".join(f"{x:.6f}" for x in p2['R'][:3]) + f" … (all 9 points in [{-0.99}, {0.99}] ε_EP: min {min(p2['R']):.6f}, max {max(p2['R']):.6f}); "
          f"cross-check −2f″/f in geodesic polar form: min {min(p2['R2']):.6f}, max {max(p2['R2']):.6f}. R = +2: constant, positive (Euclidean, sphere-like / dS₂-type patch). Nothing more is claimed.", "",
          "## Match D1–D7 against P1 + P2 (match.py)", "",
          "| row | property | result | tag | reason |", "|---|---|---|---|---|"]
    for r in M:
        L.append(f"| {r['id']} | {r['claim']} | **{r['result']}** | {r['tag']} | {r['reason']} |")
    H_AFTER = spec_D.hash_tree()
    same = H_BEFORE == H_AFTER
    changed = sorted(set(H_BEFORE) ^ set(H_AFTER) | {k for k in H_BEFORE if H_AFTER.get(k) != H_BEFORE[k]})
    print(f"loaded folders unchanged (SHA-256 of {len(H_BEFORE)} files before/after): {same}")
    L += ["", "## Loaded inputs (read-only) and unchanged check", "",
          f"- Probe surface `{spec_D.PROBE}`: load_surface.load(), dictionary.build / winners / chirality / gap_fit, cover.run_cover, RESULTS.md (D1–D7 rows, verdict, sign-off).",
          f"- Handoff `{spec_D.HANDOFF}`: seed (A, B, V, EPS_EP, LAM_EP, H_A), tracker.align_evals, wick_lorentzian.chart(), outputs/Jhat.npz, outputs/summary.json, RESULTS_probe.md.",
          f"- Drive-return `{spec_D.DRIVE}`: outputs/drive.npz, outputs/drive_start1p25.npz, RESULTS.md, RESULTS_start1p25.md. No drive was re-run.",
          f"- SHA-256 of every file in the three folders ({len(H_BEFORE)} files) before any import and after all computations: **{'unchanged' if same else 'CHANGED: ' + ', '.join(changed)}**.", "",
          "## Scope", "",
          "Two-mode toy (H_A is 2×2). P1 and P2 are built to match the D1–D7 spec [hive-interpretation]; they are not derived from a gravity theory. "
          "No JT dual is claimed. " + DS2_LINE + " C stays held. " + NO4D + ".", ""]
    (ROOT / "RESULTS.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("Wrote RESULTS.md")
    return 0 if same else 1


if __name__ == "__main__":
    raise SystemExit(main())
