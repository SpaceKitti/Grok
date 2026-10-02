"""pairA-jt-4d: JT-sign 2D geometry (AdS2) and 4D lifts R1, R2 built on the Pair A eigenvalue curve.
`python run.py` writes RESULTS.md. Geometry from numbers only; the D6/D7 map reads the probe-surface and qg-operator RESULTS.md read-only (SHA-256 before/after)."""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True
from pathlib import Path  # noqa: E402

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import numpy as np  # noqa: E402
import sympy as sp  # noqa: E402

import jt2d  # noqa: E402
import lift4d  # noqa: E402
import match  # noqa: E402

CLAIM = "no JT dual claimed; no Einstein solution claimed"
HEXA = "Ordinary S^2 (standard theta, phi) is used; GoldbergHexa (Akitti's custom probe lattice) not needed."
TARGET = 'R1 (AdS2 x S2, r = eps_EP) is the 4D target. R2 is not a target (kept as information only).'
REVISION = "Revision 2026-09-25 (D6/D7 map, R2 χ-forward labels, GoldbergHexa note): signed off by Venus (maths) and Helios (physics)."
TAGR2 = '[by construction: χ-forward convention; time-reversal (χ → π−χ) swaps them]'
CHA = 'F_JT and y² depend only on position, so the static geometry is identical for cw and ccw loops [standard].'
CHIRAL = "chirality inherited from H_A, not from F_JT"
ARROW = "arrow = chi forward; labels match chi"
CLAIM_NOTE = "(R1 geometry is a known Einstein–Maxwell–Λ solution [standard]; not derived from Pair A)"


SWAP_LINE = "swap/return needs a degree-2 cover: the smooth period already gives one; 4π cone [by construction]"


def yn(b):
    return "PASS" if b else "FAIL"


def main() -> int:
    H_BEFORE = match.hash_tree()
    E = jt2d.EPS_EP
    J = jt2d.run()
    L = lift4d.run()
    M, lp = match.run(J)
    DM = match.d67_map()
    CH = match.chirality()
    AR = L["R2"]["arrow"]
    print(TARGET)
    print(f"{DM['verdict']} — {DM['reason']}")
    chb = ("The monodromy is a swap, which is its own inverse, so cw and ccw give the same label map "
           + ("[computed: M1/M2 monodromy same both ways]" if CH["ok"] else "[cw/ccw check FAILED]")
           + "; the D7 direction pick therefore comes from the time-dependent lossy evolution i∂_tψ = H_A(ε(t))ψ, not from F_JT.")
    cwline = ("cw/ccw static continuation [computed]: " + "; ".join(f"{nm}: ccw {CH['n'][(nm,'ccw',1)]}/{CH['n'][(nm,'ccw',2)]}, cw {CH['n'][(nm,'cw',1)]}/{CH['n'][(nm,'cw',2)]}" for nm in ("+ε_EP", "−ε_EP"))
              + f" (n after 1/2 turns; 1 = swap, 0 = return); same label map both ways: {'YES' if CH['same'] else 'NO'}; swap then return: {'YES' if CH['swap'] else 'NO'}")
    print(CHIRAL)
    print(CHA)
    print(chb)
    print(cwline)
    if AR["ok"]:
        print(ARROW)
    else:
        print(f"arrow/label check FAILED: {AR}")
    sgn = lambda x: "negative" if x < 0 else "positive" if x > 0 else "zero"
    R2d = float(J["R_sym"])
    R1 = L["R1"]
    R2 = L["R2"]
    print(f"2D JT: R = {J['R_sym']} (symbolic, full Riemann; −F'' = {J['R_formula']}); numerical {J['R_num'][0]:.6f}..{J['R_num'][1]:.6f}; sign {sgn(R2d)} (AdS₂)")
    print(f"zeros of F_JT: {J['roots'][0]:+.8f}, {J['roots'][1]:+.8f}; F<0 inside Γ: {J['neg_inside']}; F>0 outside Γ: {J['pos_outside']}")
    print(f"4D R1: R = {R1['R']} = {R1['R_num']:.6f} (expect −2 + 2/ε_EP² = {R1['R_expect']:.6f}); sign {sgn(R1['R_num'])}")
    print(f"4D R2: R = {R2['R']}; at ε = 0: {R2['mid'][0]:.6f}; ε → ε_EP: R → {R2['lim_R']}, Kretschmann → {R2['lim_K']}")
    for m in M:
        print(f"{m[0]} {yn(m[2])} {m[3]}")
    print(CLAIM, CLAIM_NOTE)
    print(f"R1 Einstein–Maxwell–Λ: G^a_b = diag({', '.join(sp.sstr(x) for x in R1['Gmix'])}); Λ = {sp.sstr(R1['Lambda'])} = {R1['Lambda_num']:.6f}, E² = {sp.sstr(R1['E2'])} = {R1['E2_num']:.6f}, residual {R1['emL_resid']:.1e}")
    print(f"R2 Kantowski–Sachs: dε²/F → {R2['sub_dchi']} dχ², −F − ε_EP² sin²χ = {R2['sub_gtt']}, r² − ε_EP² sin²χ = {R2['sub_r2']}; Kretschmann exponent {R2['K_exp']:.4f} (+ε_EP), {R2['K_exp_minus']:.4f} (−ε_EP); R exponent {R2['R_exp']:.4f}; R·δ = {R2['R_delta']:.6f} vs (3ε_EP²+1)/ε_EP² = {R2['R_delta_pred']:.6f}")
    print(SWAP_LINE)
    cs = {k: v[-1][2] for k, v in J["cones"].items()}

    out = ["# pairA-jt-4d — RESULTS", "", "**Signed off 2026-09-25:** Venus (maths) and Helios (physics).", REVISION, "",
           "Akitti's build toward JT (AdS₂ sign) and a 4D metric, on the Pair A eigenvalue curve y² = 4v²(ε² − ε_EP²), λ± = λ_EP ± y/2. Two-mode toy.", "",
           f"**{CLAIM}** {CLAIM_NOTE}. No QG Hamiltonian is derived here.", "",
           "Inputs (numbers only for all geometry; the D6/D7 map reads two RESULTS.md files read-only, see below) [by construction]: ε_EP = 0.51368066, λ_EP = −0.308425i, v = −0.360253, τ_swap = 4π/ε_EP = "
           f"{jt2d.TAU_SWAP:.8f}, Γ = [−ε_EP, ε_EP]; sheets A WRITE, B WRITE, C held. Swap test: branch tracking of y directly (no matrix); "
           "the 2×2 stand-in v[[0,1],[ε²−ε_EP²,0]] is used only for the independent F_JT = y²/(4v²) residual (M5).", "",
           "## Summary", "", f"**{TARGET}**", "",
           f"- R sign: 2D JT R = {R2d:+.0f} [computed] (negative, AdS₂ sign); 4D R1 R = −2 + 2/ε_EP² = {R1['R_num']:+.6f} [computed] (positive for ε_EP < 1: the S² curvature 2/ε_EP² = {2/E**2:.6f} outweighs the AdS₂ −2); "
           f"4D R2 R = {sp.sstr(R2['R'])} [computed] (at ε = 0: {R2['mid'][0]:+.6f}; diverges at ±ε_EP).",
           f"- F_JT > 0 region vs Γ [computed]: F_JT < 0 on the interior of Γ, F_JT = 0 at ±ε_EP, F_JT > 0 outside Γ — the opposite of pairA-qg-operator's P2 (F = ε_EP² − ε², Euclidean inside Γ).",
           f"- Swap cover [computed]: 2π loop swaps (M1), 4π loop returns (M2); smooth horizon period 2π/ε_EP gives cone angle 2π; τ_swap = 4π/ε_EP gives 4π → **swap/return needs a degree-2 cover: the smooth period already gives one; 4π cone [by construction]** (M3).",
           "- A B C [by construction]: A WRITE, B WRITE (the two sheets of y, both lifted); C held — not in the construction.", "",
           "## JT 2D (jt2d.py)", "",
           "F_JT = ε² − ε_EP², ds² = dε²/F_JT + F_JT dτ².", "",
           f"- R [computed]: symbolic (sympy, full Christoffel/Riemann) R = {J['R_sym']}; formula −F'' = {J['R_formula']}; numerical (finite differences, 13 points in [−3, 3] ε_EP) {J['R_num'][0]:.8f} … {J['R_num'][1]:.8f}. Sign: **negative (AdS₂)** [standard for this F].",
           f"- Zeros: ε = {J['roots'][0]:+.8f}, {J['roots'][1]:+.8f} (= ±ε_EP). F_JT < 0 at every grid point inside Γ: {J['neg_inside']}; F_JT > 0 at every grid point outside Γ: {J['pos_outside']} (6001-point grid on [−3, 3] ε_EP).",
           f"- F_JT = +y²/(4v²): residual {J['res_y2']:.1e} [computed] — the opposite sign of P2's F = −y²/(4v²).",
           f"- Horizon: F′(±ε_EP) = ±2ε_EP, surface gravity κ = |F′|/2 = {J['kappa']:.8f} = ε_EP; smooth period 2π/κ = 2π/ε_EP = {2*np.pi/E:.6f} [standard].",
           f"- Cone angle at each tip (circumference / proper radius, 1e-6 from the tip) [computed]: period 2π/ε_EP → {cs[('+ε_EP','2π/ε_EP (smooth)')]/np.pi:.6f}π (+ε_EP), {cs[('−ε_EP','2π/ε_EP (smooth)')]/np.pi:.6f}π (−ε_EP): smooth; "
           f"period 4π/ε_EP → {cs[('+ε_EP','4π/ε_EP (τ_swap)')]/np.pi:.6f}π, {cs[('−ε_EP','4π/ε_EP (τ_swap)')]/np.pi:.6f}π: branched double cover (conical excess). "
           f"Local polar form ε = ε_EP cosh ρ: ds² = dρ² + ε_EP² sinh²ρ dτ² (residuals {J['polar_res']:.1e}, {J['polar_res2']:.1e}), so the angle is ε_EP × period exactly.",
           "- Topology [computed]: the Euclidean region F_JT > 0 is two disconnected pieces, ε > ε_EP and ε < −ε_EP, each containing exactly one tip, each noncompact (hyperbolic cigar / disk, K = R/2 = −1). "
           "Unlike P2's sphere (which held both tips), no Euclidean piece here contains both tips.",
           "- Gauss–Bonnet on the cut-off disk ρ ≤ ρ₀ (one piece) [identity; computed numerically]:", "",
           "| period | ρ₀ | bulk ∫K dA | boundary ∫k_g ds | tip cone term 2π − θ | total (= 2πχ, χ = 1) |", "|---|---|---|---|---|---|"]
    for pn, r0, bulk, kg, cone, tot in J["gb"]:
        out.append(f"| {pn} | {r0:g} | {bulk:.4f} | {kg:.4f} | {cone:+.6f} | {tot:.6f} |")
    out += ["", "  [identity; computed numerically]: bulk −ε_EP P(cosh ρ₀ − 1) + boundary ε_EP P cosh ρ₀ + cone (2π − ε_EP P) = 2π for every ρ₀ and P. The bulk term is negative and diverges as the cut-off is removed; the real point is that the −2π cone term is required at τ_swap.", "",
            "## 4D lift (lift4d.py)", "",
            "Ansatz [by construction]: ds² = −F_JT dt² + dε²/F_JT + r(ε)² (dθ² + sin²θ dφ²), F_JT = ε² − ε_EP².",
            HEXA, "", TARGET, "",
            "- **R1**: r = ε_EP (constant): ds² = −(ε² − ε_EP²) dt² + dε²/(ε² − ε_EP²) + ε_EP² dΩ₂² — AdS₂ × S² product [standard form].",
            f"  - R = {sp.sstr(R1['R'])} = −2 + 2/ε_EP² = {R1['R_num']:.6f} [computed] (expected {R1['R_expect']:.6f}); Kretschmann = {sp.sstr(R1['K'])} = {R1['K_num']:.6f}, constant.",
            "  - Exists as a real Lorentzian metric for all real ε ≠ ±ε_EP (outside Γ t is timelike; inside Γ, F_JT < 0, so ε is timelike and t spacelike); ε = ±ε_EP are Killing horizons (coordinate singularities, curvature constant).",
            f"  - Euclidean section (t = −iτ): F_JT dτ² + dε²/F_JT + ε_EP² dΩ₂², real Euclidean only where F_JT > 0 (outside Γ). The (τ, ε) plane is the JT cigar: smooth at ε = ±ε_EP with period 2π/ε_EP = {R1['smooth_period']:.6f} (cone 2π); with τ_swap = 4π/ε_EP it has a 4π cone (double cover). [computed, from the 2D cone angles above]",
            "- **R2**: r = ε_EP sin χ, ε = ε_EP cos χ, i.e. r² = ε_EP² − ε²: ds² = −(ε² − ε_EP²) dt² + dε²/(ε² − ε_EP²) + (ε_EP² − ε²) dΩ₂².",
            "  - r is real only for |ε| ≤ ε_EP (inside Γ). There F_JT < 0: ε is timelike, t spacelike; the metric is real Lorentzian for |ε| < ε_EP. "
            "Outside Γ r² = ε_EP² − ε² < 0 (sin of an imaginary χ): no real metric. No real Euclidean section either (Euclidean needs F_JT > 0, i.e. outside Γ, where r² < 0).",
            f"  - R = {sp.sstr(R2['R'])} [computed]; at ε = 0: {R2['mid'][0]:.6f}. Kretschmann = {sp.sstr(R2['K'])}.",
            "  - R2 is a Kantowski–Sachs cosmology inside Γ: with ε = ε_EP cosχ, ds² = −dχ² + ε_EP² sin²χ (dt² + dΩ₂²); χ is forward time, χ: 0 → π, so ε = ε_EP cos χ runs from +ε_EP down to −ε_EP; Big Bang at +ε_EP (χ = 0), Big Crunch at −ε_EP (χ = π) " + TAGR2 + "; the metric is symmetric under χ → π−χ, so with the other time orientation the Bang is at −ε_EP "
            f"(spacelike curvature singularities, R ≈ (3ε_EP²+1)/(ε_EP² δ), Kretschmann ∝ 1/(ε_EP−ε)^{R2['K_exp']:.2f}) [computed]. The bolt test does not apply to a time singularity. "
            f"(Symbolic check: dε²/F = {R2['sub_dchi']}·dχ², −F − ε_EP² sin²χ = {R2['sub_gtt']}, r² − ε_EP² sin²χ = {R2['sub_r2']}. Log-log fit for δ = 1e-3 … 1e-7: Kretschmann exponent "
            f"{R2['K_exp']:.4f} at +ε_EP, {R2['K_exp_minus']:.4f} at −ε_EP; R exponent {R2['R_exp']:.4f}; R·δ at δ = 1e-7 = {R2['R_delta']:.6f} vs (3ε_EP²+1)/ε_EP² = {R2['R_delta_pred']:.6f}. "
            f"Consistency check of the χ-forward convention (not a derivation) {TAGR2}: ε(χ=0) = {AR['eps0']:+.12f} ε_EP labelled {AR['label0']}, ε(χ=π) = {AR['epspi']:+.12f} ε_EP labelled {AR['labelpi']}, dε/dχ = {sp.sstr(AR['deps_sym'])}, max on (0, π) = {AR['max_deps']:.3e} ≤ 0: {'PASS' if AR['ok'] else 'FAIL'}; symmetry χ → π−χ: ε_EP² sin²(π−χ) − ε_EP² sin²χ = {AR['sym']}, ε(π−χ) + ε(χ) = {AR['eps_rev']} [computed]. "
            + (ARROW if AR['ok'] else 'arrow/label check FAILED') + ".) Near the Big Bang tip +ε_EP (ε = ε_EP(1 − δ)):", "",
            "| δ | R | Kretschmann |", "|---|---|---|"]
    for d, r, k in R2["near_pole"]:
        out.append(f"| {d:.0e} | {r:.6e} | {k:.6e} |")
    out += ["", f"  Limits: R → {R2['lim_R']}, Kretschmann → {R2['lim_K']} as ε → ε_EP (∝ 1/(ε_EP − ε) and 1/(ε_EP − ε)²). **R2 is singular at ±ε_EP: spacelike curvature singularities (Big Bang at +ε_EP, χ = 0; Big Crunch at −ε_EP, χ = π), not bolts.**",
            "- Einstein tensor G_ab (coordinates t, ε, θ, φ) — **information only; Einstein not the goal**:",
            f"  - R1: diag({', '.join(sp.sstr(R1['G'][i, i]) for i in range(4))})",
            f"  - R2: diag({', '.join(sp.sstr(R2['G'][i, i]) for i in range(4))})",
            f"  - R1 mixed components G^a_b = diag({', '.join(sp.sstr(x) for x in R1['Gmix'])}).",
            f"  - R1 = AdS₂×S² is an exact Einstein–Maxwell–Λ solution (Bertotti–Robinson/Nariai family; the near-horizon geometry of an extremal charged black hole with Λ>0) [standard, computed from G_ab]: "
            f"Λ = {sp.sstr(R1['Lambda'])} = {R1['Lambda_num']:.6f}, E² = {sp.sstr(R1['E2'])} = {R1['E2_num']:.6f} (residual of G^a_b + Λδ^a_b − E² diag(−1,−1,1,1), all 16 components: {R1['emL_resid']:.1e}) "
            "(convention: G_ab + Λg_ab = 8πT_ab, G=1, T^a_b = (E²/8π) diag(−1,−1,1,1); Λ is convention-independent). This describes the geometry only; no Einstein claim tied to Pair A. "
            "That ε_EP = |a−b|/(2|v|) sets the S² radius is [hive-interpretation].",
            "  - R2 is not a vacuum (G = 0) or pure-Λ (G = −Λg) solution; no matter model is proposed for it.", "",
            "Where each exists:", "",
            "| ansatz | real Lorentzian | real Euclidean (t = −iτ) | curvature at ±ε_EP |", "|---|---|---|---|",
            f"| R1 (r = ε_EP) | all ε ≠ ±ε_EP (horizons at ±ε_EP) | outside Γ (F_JT > 0); smooth tip for period 2π/ε_EP, 4π cone for 4π/ε_EP | finite, constant (R = {R1['R_num']:.4f}) |",
            "| R2 (r² = ε_EP² − ε²) | inside Γ only (|ε| < ε_EP), Kantowski–Sachs cosmology | none | divergent (Big Bang at +ε_EP, χ = 0; Big Crunch at −ε_EP, χ = π) |", "",
            "## Match (match.py)", "",
            "| id | test | result | tag | evidence |", "|---|---|---|---|---|"]
    for m in M:
        out.append(f"| {m[0]} | {m[1]} | **{yn(m[2])}** | {m[3]} | {m[4]} |")
    out += ["", SWAP_LINE if M[2][2] else "swap/return cover test FAILED.", "",
            "## D6/D7 map onto F_JT", "",
            "What D6 and D7 are (pairA-qg-probe-surface RESULTS.md, read-only):", ""]
    for did, d in DM["rows"].items():
        out.append(f"- {did}: \"{d['claim']}\" — probe {d['result']} {d['tag']}; loop r = {d['r']} ε_EP around +ε_EP, start/end {d['start']} ε_EP. "
                   f"pairA-qg-operator: INHERITED FROM H_A, not from P1: {'YES' if d['operator'] else 'NO'}.")
    out += ["", "| row | start ε/ε_EP | F_JT at start | phase at start (y at start) | loop ε range on the real axis (ε/ε_EP) | loop straddles Γ |", "|---|---|---|---|---|---|"]
    for did, d in DM["rows"].items():
        out.append(f"| {did} | {d['start']} | {d['F_start']:+.6f} | {d['phase']} (y = {d['y_start'].real:+.6f}{d['y_start'].imag:+.6f}i) | {d['loop_x'][0]:.2f} – {d['loop_x'][1]:.2f} | {'YES' if d['straddles'] else 'NO'} |")
    out += ["", f"**{DM['verdict']}** — {DM['reason']}. "
            "[by construction]: D6/D7 are defined by their start point; [computed]: F_JT sign at the start points (negative at 0.75, positive at 1.25 ε_EP), the decay/frequency split there "
            "(F_JT = y²/(4v²) < 0 ⇔ y imaginary ⇔ same frequency, different decay: loss picks the mode, D6; F_JT > 0 ⇔ y real ⇔ same decay, different frequency: direction picks the mode, D7), "
            "and the loop range 0.75–1.25 ε_EP straddling Γ; [hive-interpretation]: reading D6/D7 as whole F_JT regions. No start points other than 0.75 and 1.25 ε_EP were tested (no drive re-run).", "",
            f"**{CHIRAL}** — {CHA} {chb} (pairA-qg-operator D6/D7: INHERITED FROM H_A, not from P1.)", "",
            cwline + ".", "",
            (ARROW if AR["ok"] else "arrow/label check FAILED") + " — R2: χ forward (0 → π), ε(χ=0) = +ε_EP = Big Bang, ε(χ=π) = −ε_EP = Big Crunch, dε/dχ ≤ 0 " + TAGR2 + "; the metric is symmetric under χ → π−χ, so with the other orientation the Bang is at −ε_EP. The automated check is a consistency check of the convention, not a derivation.", "",
            "## Sheets", "", "A: WRITE (lifted). B: WRITE (lifted). C: held — C is not in the construction.", "",
            "## Tags and scope", "",
            "[standard]: AdS₂ curvature of F = ε² − ε_EP², surface gravity / smooth period, AdS₂ × S² form. [by construction]: inputs, ansatz, A/B/C status. "
            "[computed]: R values, cone angles, Gauss–Bonnet, residuals, branch tracking. [hive-interpretation]: identifying the τ angle with arg(ε−ε_EP) or arg(ε−ε_EP)/2; ε_EP setting the S² radius. [by construction, numerically confirmed]: F_JT = y²/(4v²) (M5). [identity; computed numerically]: Gauss–Bonnet table. [standard, computed from G_ab]: R1 Einstein–Maxwell–Λ. "
            "[careful-before-toy]: R2 exists only inside Γ, as a Kantowski–Sachs cosmology (χ forward: Big Bang at +ε_EP, Big Crunch at −ε_EP); R2 is not a target. " + TAGR2 + ": the arrow and the Bang/Crunch assignment (the metric is symmetric under χ → π−χ). " + HEXA + " "
            "D6/D7 map: [by construction] (D6/D7 are defined by start point) + [computed] (F_JT sign and decay/frequency split at the start points, loop range); reading D6/D7 as F_JT regions is [hive-interpretation]. Chirality: static geometry identical for cw/ccw [standard]; cw/ccw label map [computed]; D7 direction pick from H_A's lossy time evolution.",
            f"{CLAIM} {CLAIM_NOTE}. No QG Hamiltonian derived. Two-mode toy; geometry uses no files from other folders."]
    H_AFTER = match.hash_tree()
    same = H_BEFORE == H_AFTER
    print(f"loaded folders unchanged (SHA-256 of {len(H_BEFORE)} files before/after): {same}")
    out += ["", "## Loaded folders (read-only, D6/D7 map only)", "",
            f"- `{match.PROBE}` (RESULTS.md D6/D7 rows) and `{match.OPERATOR}` (RESULTS.md D6/D7 rows).",
            f"- SHA-256 of every file in both folders ({len(H_BEFORE)} files) before and after: **{'unchanged' if same else 'CHANGED'}**.", ""]
    (ROOT / "RESULTS.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("Wrote RESULTS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
