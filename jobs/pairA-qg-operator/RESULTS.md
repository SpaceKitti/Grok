# pairA-qg-operator — RESULTS

**Signed off 2026-09-25:** Venus (maths) and Helios (physics).

What it is (Akitti): the smallest gravity-side object whose cut, tips, monodromy and inside/outside switch are Pair A's. Two-mode toy; no Einstein solver, no new MHD matrix.

## Result

QG Hamiltonian = P1+P2 plus H_A dissipation for D6 D7
QG-side toy = edge operator P1 at each tip, on background geometry P2, with H_A's loss supplying D6/D7 [hive-interpretation]. (P2 is a metric, not an operator, so '+' here means 'together', not an operator sum.)
Tag: [hive-interpretation] — an operator built to match the D1–D7 spec, not derived from a gravity theory; no JT dual is claimed (P2 has the 2D dilaton-gravity metric form with the dS sign, not JT's; noted as [standard] resemblance only).
P2 has the Euclidean dS₂ static-patch (round-sphere) form, with its period doubled [standard]. (JT would be R = −2, AdS₂, F = r² − r_h²; here F = ε_EP² − ε² gives R = +2.)

no 4d Einstein metric in this folder

Split: **P1 = tip only** (Airy edge; link to the EP is a [standard analogy] via WKB momenta; no ε_EP, no Γ, no second tip by itself). **P2 = global cut, tips and period** (F = ε_EP² − ε², τ_E = 4π/ε_EP). **D6 and D7 need the dissipative Pair A structure** (H_A's non-Hermitian loss), not P1 or P2.

**Regularity, stated plainly:** with τ_E = 4π/ε_EP the P2 geometry is **not** a smooth Euclidean horizon. The smooth-horizon period is 4π/|F′(±ε_EP)| = 2π/ε_EP = 12.231695; τ_E = 24.463390 is twice that, so each tip is a conical point with total angle 3.999997π (+ε_EP) and 3.999997π (−ε_EP), i.e. 4π: conical excess, a double-cover branch point. [hive-interpretation]: a 4π cone is a double cover, so one smooth turn (2π) is half the geometric circle, matching the Jhat2 swap. That the 4π cone matches Jhat4 = I is [by construction, given τ_E = 4π/ε_EP from the handoff]. [computed]: this choice gives both tips the same angle (3.999997π, 3.999997π) and a consistent χ = 2.000003 (see P2 (ii)).

Topology: one sphere (chi=2) double-covering the round sphere, branched at ±ε_EP.

Riemann–Hurwitz cross-check [computed]: PASS — y² = 4v²(ε² − ε_EP²) is quadratic in ε; finite branch points = zeros of y² at -1.000000000000, +1.000000000000 ε_EP (simple zeros, one-turn monodromy n = 1 at each); no branching at infinity (|ε| = 10 ε_EP: branches n = 0, 0 (return), max ||y/(2vε)| − 1| = 5.0e-03; |ε| = 100 ε_EP: branches n = 0, 0 (return), max ||y/(2vε)| − 1| = 5.0e-05); χ = 2·2 − 2 = 2, genus 0: a genus-0 double cover branched only at ±ε_EP. P2: χ = 2.000003 (Gauss–Bonnet with cones), 4π cone points exactly at ±ε_EP — same topology and branch points.

F = −y²/(4v²) [standard, residual 2.2e-15]: P2 is Euclidean (F>0) exactly in the split-decay phase inside Γ and flips signature (F<0) exactly in the split-frequency phase outside Γ, so P2's signature change sits on the same line as the inside/outside switch. (y = λA − λB from H_A eigenvalues; 199 real ε inside Γ, 200 outside, |ε| ≤ 3 ε_EP.)

## Spec (spec_D.py)

Handoff and drive-return values, asserted against Akitti's numbers (not hard-coded as inputs):

- eps_EP: ε_EP = 0.513680663312 = |a−b|/(2|v|) = 0.513680663312; |ε_EP − 0.51368066| = 3.3e-09
- lam_EP: λ_EP = -0.308425000i = −i(a+b)/2; |λ_EP − (−0.308425i)| = 0.0e+00
- v: v = -0.360253 (Akitti −0.360253)
- Gamma: Γ = [-0.513680663, 0.513680663] = [−ε_EP, ε_EP]; handoff chart support: Γ=[-ε_EP, ε_EP]
- Jhat2 swap: Jhat2 = [[0.0e+00-3.7e-17j, -0.000000-1.000000j], [-0.000000+1.000000j, 3.8e-16-1.5e-16j]] (off-diagonal: swap)
- Jhat4 = I: ‖Jhat4 − I‖ = 9.8e-16
- tau: τ = 4π/ε_EP = 24.46339041; handoff summary.json tau = 24.46339041; |τ − 24.46339| = 4.1e-07
- A/B WRITE, C held: summary.json scores A = WRITE, B = WRITE, C = NOT-SELECTED; RESULTS_probe.md: 'held: C'
- probe D1–D7: probe surface D1–D7 all PASS (recomputed by its dictionary.py; each row's claim, tag and PASS found in its RESULTS.md); probe verdict 'SURFACE READY — QG probe may use D1–D7'; probe sign-off: **Signed off 2026-09-25:** Venus (maths) and Helios (physics) on D1–D7 and cover.
- inside/outside chirality: inside (drive.npz, start 0.75 ε_EP): ccw and cw pick the same mode at all speeds ['fast', 'slow100', 'slow20', 'slow40']: True; outside (drive_start1p25.npz, start 1.25 ε_EP): cw/ccw pick opposite modes at γT = 20, 40, 100: True (γT = 1: False)

D1–D7 loaded from the probe surface (its dictionary.py recomputed them this run; each row's claim, tag and PASS cross-checked against its RESULTS.md):

| row | property | probe result | probe tag | in probe RESULTS.md |
|---|---|---|---|---|
| D1 | real chart only on Γ | PASS | [by definition] | YES |
| D2 | dies at both EPs | PASS | [computed] | YES |
| D3 | 4π return of labels | PASS | [computed, known] | YES |
| D4 | A and B allowed past the stall (stall = both EPs ±ε_EP, Akitti 2026-09-25) | PASS | [computed, equivalent to 2π swap] (definition supplied by Akitti) | YES |
| D5 | C held | PASS | [by construction] | YES |
| D6 | loop starting inside Γ at 0.75ε_EP: the direction of travel is ignored (loss picks the mode) | PASS | [computed] | YES |
| D7 | loop starting outside Γ at 1.25ε_EP, slow drive (γT≳20): the direction picks the mode (cw and ccw pick opposite modes) | PASS | [computed] | YES |

Probe conditions per row (verbatim from its dictionary):

- D1: 'real chart' = the handoff's chart, which the handoff places on Γ = [−ε_EP, ε_EP]
- D2: circles r = 0.25, 0.1, 0.03, 0.01 ε_EP around each EP; gap = mean |λ+−λ−| on the circle; overlap = normalised |<v+|v−>|
- D3: continuous eigenvalue tracking on circles r = 0.25 ε_EP around each EP (this run); handoff Jhat from outputs/Jhat.npz
- D4: at each tip: (a) Helios two-detour test, semicircles r = 0.25 ε_EP just above / just below the tip from ±0.75 to ±1.25 ε_EP, continuous tracking (handoff align_evals, 8000 steps), PASS only if the pairings are swapped; (b) 2π swap / 4π return from the cover loops and handoff Jhat; (c) only A and B continue, C files unchanged (SHA-256); (d) probe.py:44 allowed_past_Wick [A, B] cited as the same fact
- D5: this probe never writes C or any handoff file; checked by SHA-256 before/after
- D6: loop r = 0.25 ε_EP around +ε_EP, start/end 0.75 ε_EP (inside Γ), γT = 1, 20, 40, 100; left-eigenvector weights. The loop straddles the tip (it also passes 1.25 ε_EP outside Γ); no driven loop lies entirely inside or outside Γ
- D7: r = 0.25 ε_EP, start/end 1.25 ε_EP (outside Γ), slow drive: the direction picks the mode cleanly from about γT ≈ 20 (w = 0.99699 at γT = 20, 0.99937 at 40, 0.99991 at 100), only partially at γT = 5 (a lean of about 91/9), and not at γT = 1. The loop straddles the tip (it crosses Γ at 0.75 ε_EP); no driven loop lies entirely inside or outside Γ

## Curve (curve.py)

y² = 4v²(ε² − ε_EP²); eigenvalues of H_A = λ_EP ± y/2 with λ_EP = -0.308425i kept.

- Grid of 3721 complex ε (Re ε ∈ [−2, 2] ε_EP, Im ε ∈ [−1, 1] ε_EP): max |(λA−λB)² − y²| = 5.4e-16 (max |y²| = 0.613); max min(|λA−λB ∓ y|) = 6.8e-09 (largest at the tips, where H_A is defective and numerical eigenvalues carry a ~√(machine ε) error); max |λA + λB − 2λ_EP| = 5.8e-16.
- Monodromy of y (continuous branch): +ε_EP once: n = 1; +ε_EP twice: n = 0; −ε_EP once: n = 1; −ε_EP twice: n = 0; both tips once (r = 2 ε_EP): n = 0.
- Square-root exponent of |y| at the tips: 0.5003 (+ε_EP), 0.5003 (−ε_EP).
- Two-detour test on the curve: +ε_EP: +0.75 → +1.25 ε_EP, y_above = +0.277583, y_below = -0.277583, swapped YES, min |y| = 0.244805; −ε_EP: -0.75 → -1.25 ε_EP, y_above = +0.277583, y_below = -0.277583, swapped YES, min |y| = 0.244805.
- Period τ = 4π/ε_EP = 24.46339041 (asserted ≈ 24.46339).

Cover U_G[γ] = (−1)^{I(γ,Γ)} vs Φ(n), recomputed by the probe surface's cover.py on the same six loops:

| loop | I | signed | U_G | n_A | n_B | Φ = U_G |
|---|---|---|---|---|---|---|
| +EP once (circle r=0.25 eps_EP, start 1.25 eps_EP, ccw) | 1 | -1 | -1 | 1 | 1 | YES |
| -EP once (circle r=0.25 eps_EP, start -1.25 eps_EP, ccw) | 1 | +1 | -1 | 1 | 1 | YES |
| +EP twice (same circle, 4pi) | 2 | -2 | +1 | 0 | 0 | YES |
| -EP twice (same circle, 4pi) | 2 | +2 | +1 | 0 | 0 | YES |
| figure-eight (lemniscate, foci +-eps_EP, lobes opposite senses, start sqrt2 eps_EP) | 2 | -2 | +1 | 0 | 0 | YES |
| big loop around both (circle r=2 eps_EP, start 2 eps_EP) | 0 | +0 | +1 | 0 | 0 | YES |

## Operator P1 — edge (operator.py)

H_edge = −∂x² + x (Airy), local at each EP [standard analogy].

P1 = −∂x² + x is Hermitian; nothing merges at its turning point, and the Ai eigenfunctions stay a regular basis. The √ exponent and the one-turn swap live in the WKB momenta ±√(E − x), which is what is measured here, not an exceptional point of P1. The true local EP normal form is the 2×2 Jordan-type matrix [[0,1],[ε−ε_EP,0]].

- Ai solves H_edge ψ = Eψ with ψ = Ai(x − E): finite-difference relative residual (h = 0.001, x ∈ [-10.0, 5.0]) = 8.0e-07 (E = 0), 9.8e-07 (E = 1).
- Dirichlet on (0, 20.0), n = 4000: lowest eigenvalues 2.33811, 4.08794, 5.52055, 6.78669, 7.94411 vs −a_k (Airy zeros) 2.33811, 4.08795, 5.52056, 6.78671, 7.94413; max relative error 3.3e-06; matrix Hermitian (max |H − H†| = 0.0e+00).
- Square-root link [standard analogy]: WKB momenta p(x) = ±√(E − x) merge at the turning point x = E; exponent of |p+ − p−| vs |x − E| = 0.5000 (E = 0), 0.5000 (E = 1); H_A gap exponent near the tips: see D2 (≈ 0.5). Same local square-root form as y ∝ √(ε ∓ ε_EP).
- Monodromy [standard analogy]: tracking ±√(E − x) once around the turning point swaps the branches (n = 1), twice returns them (n = 0) — the same as the 2π swap / 4π return of A and B.
- P1 is only the tip: it carries no ε_EP, no Γ and no second tip by itself.

## Operator P2 — global mini-superspace (operator.py)

F(ε) = ε_EP² − ε², ds_E² = dε²/F + F dτ_E², τ_E period 4π/ε_EP = 24.463390.

- (i) Chart: F > 0 at 1999 of 4001 real grid points in [−2, 2] ε_EP, exactly those with |ε| < ε_EP; F(+ε_EP) = 0.0, F(−ε_EP) = 0.0; F(ε_EP(1 ∓ 1e-9)) = +5.3e-10, -5.3e-10. The Euclidean (real positive) chart is Γ and dies at both tips (D1, D2). F = −y²/(4v²) (residual 5.6e-17).
- (ii) Regularity: F′(±ε_EP) = ∓2ε_EP (numerical -1.027361, +1.027361); smooth period 4π/|F′| = 2π/ε_EP = 12.231695. With τ_E = 4π/ε_EP the cone angle (circumference / proper radius as δ → 0) is:

| δ/1 from tip | proper radius ρ (+ε_EP) | angle (+ε_EP) / π | angle (−ε_EP) / π | angle with smooth period / π |
|---|---|---|---|---|
| 1e-02 | 1.976403e-01 | 3.974010 | 3.974010 | 1.987005 |
| 1e-03 | 6.240780e-02 | 3.997404 | 3.997404 | 1.998702 |
| 1e-04 | 1.973220e-02 | 3.999740 | 3.999740 | 1.999870 |
| 1e-05 | 6.239777e-03 | 3.999974 | 3.999974 | 1.999987 |
| 1e-06 | 1.973188e-03 | 3.999997 | 3.999997 | 1.999999 |

  Total cone angle 4π at each tip: conical excess (double-cover branch point), NOT smooth. With the smooth period it would be 2π. Gauss–Bonnet check: ∫K dA = 8.000000π (K = R/2 = 1, area = 2ε_EP τ_E) plus Σ(2π − θ) = -3.999995π gives 4.000005π = 2πχ with χ = 2.000003 (one sphere (chi=2) double-covering the round sphere, branched at ±ε_EP). [hive-interpretation]: one smooth turn (2π) is half the geometric circle → Jhat2 swap. The 4π cone ↔ Jhat4 = I is [by construction, given τ_E = 4π/ε_EP from the handoff]; [computed]: this choice gives both tips the same angle and a consistent χ.
  Explanation: with ε = ε_EP cos ρ and φ = ε_EP τ_E, the metric dε²/F + F dτ_E² = dρ² + sin²ρ dφ² is the unit sphere with φ running over 4π. The curvature integral ∫K dA = 8π (K = R/2 = 1, area 2ε_EP τ_E = 8π) alone would give χ = 4 (two separate spheres). The two cone terms 2(2π − 4π) = −4π bring it to 4π = 2πχ, so χ = 2: one connected sphere wrapping the round sphere twice, joined at the two tips. Riemann–Hurwitz independently gives χ = 2·2 − 2 = 2 (see the cross-check line above).
- (iii) λ_EP kept [by construction]: P2 carries λ_EP as an additive constant; spectrum λ_EP ± y/2 with y² = −4v²F reproduces H_A on 77 real ε in [−1.9, 1.9] ε_EP (max residual 3.4e-09, largest at the tips where H_A is defective).
- (iv) Curvature R = −F″ = 2.000000, 2.000000, 2.000000 … (all 9 points in [-0.99, 0.99] ε_EP: min 2.000000, max 2.000000); cross-check −2f″/f in geodesic polar form: min 2.000000, max 2.000001. R = +2: constant, positive (Euclidean, sphere-like / dS₂-type patch). Nothing more is claimed.

## Match D1–D7 against P1 + P2 (match.py)

| row | property | result | tag | reason |
|---|---|---|---|---|
| D1 | real chart only on Γ | **PASS** | [computed] | F > 0 exactly on the interior of Γ (1999 of 4001 real grid points, all with |ε| < ε_EP and every such point) and F(±ε_EP) = 0.0, 0.0: the Euclidean chart of P2 is Γ, the handoff's chart; F = −y²/(4v²) (residual 5.6e-17), so F > 0 ⇔ y² < 0 ⇔ λ−λ_EP imaginary (probe D1 fact). |
| D2 | dies at both EPs | **PASS** | [computed] | F = 0 at both tips (the chart dies there); square-root gap: curve exponent 0.5003 / 0.5003, H_A exponent 0.5003 / 0.5003, P1 WKB |p+−p−| exponent 0.5000 (same local √ form at a turning point [standard analogy]). |
| D3 | 4π return of labels | **PASS** | [computed]; 4π cone ↔ Jhat4 = I [by construction, given τ_E = 4π/ε_EP from the handoff] | curve: y → −y once around each tip (n = 1), returns after two turns (n = 0) and around both tips (n = 0); P1 WKB branches swap once / return twice [standard analogy]; cone angle at each tip 3.999997π / 3.999997π (double cover); handoff Jhat2 swap, ‖Jhat4−I‖ = 9.8e-16; U_G = Φ(n) on all 6 probe loops: YES. |
| D4 | A and B allowed past the stall (stall = both EPs ±ε_EP, Akitti 2026-09-25) | **PASS** | [computed, equivalent to 2π swap] | two sheets y = ± continue past each tip; two-detour test on the curve (±0.75 → ±1.25 ε_EP, semicircles r = 0.25 ε_EP): +ε_EP: y_above = +0.277583+0.0e+00i, y_below = -0.277583+3.8e-17i, swapped YES, min |y| = 0.244805; −ε_EP: y_above = +0.277583-1.9e-17i, y_below = -0.277583-1.9e-17i, swapped YES, min |y| = 0.244805. Not new information (same fact as the one-tip swap). |
| D5 | C held | **PASS** | [by construction] | P1 + P2 involve only the two sheets y = ± (A, B); C never enters. C-related handoff files (6) unchanged by SHA-256: YES. |
| D6 | loop starting inside Γ at 0.75ε_EP: the direction of travel is ignored (loss picks the mode) | **INHERITED FROM H_A, not from P1** | [inherited: H_A loss] | P1 is Hermitian (FD matrix ‖H − H†‖ = 0.0e+00, real spectrum) and P2 is a real metric: neither is dissipative. H_A is non-Hermitian (‖H_A − H_A†‖ = 1.017 at ε = 0.5 ε_EP). Probe D6 PASS; drive-return: **missing mechanism: NO** Signed off: Venus (maths), Helios (physics), 2026-09-25. |
| D7 | loop starting outside Γ at 1.25ε_EP, slow drive (γT≳20): the direction picks the mode (cw and ccw pick opposite modes) | **INHERITED FROM H_A, not from P1** | [inherited: H_A loss] | P1 is Hermitian (FD matrix ‖H − H†‖ = 0.0e+00, real spectrum) and P2 is a real metric: neither is dissipative. H_A is non-Hermitian (‖H_A − H_A†‖ = 1.017 at ε = 0.5 ε_EP). Probe D7 PASS; drive-return: **missing mechanism (start 1.25 ε_EP): YES** **Signed off 2026-09-25:** Venus (maths) and Helios (physics). |

## Loaded inputs (read-only) and unchanged check

- Probe surface `C:\Users\Akitt\pairA-qg-probe-surface`: load_surface.load(), dictionary.build / winners / chirality / gap_fit, cover.run_cover, RESULTS.md (D1–D7 rows, verdict, sign-off).
- Handoff `C:\Users\Akitt\pairA-qg-handoff`: seed (A, B, V, EPS_EP, LAM_EP, H_A), tracker.align_evals, wick_lorentzian.chart(), outputs/Jhat.npz, outputs/summary.json, RESULTS_probe.md.
- Drive-return `C:\Users\Akitt\pairA-drive-return`: outputs/drive.npz, outputs/drive_start1p25.npz, RESULTS.md, RESULTS_start1p25.md. No drive was re-run.
- SHA-256 of every file in the three folders (50 files) before any import and after all computations: **unchanged**.

## Scope

Two-mode toy (H_A is 2×2). P1 and P2 are built to match the D1–D7 spec [hive-interpretation]; they are not derived from a gravity theory. No JT dual is claimed. P2 has the Euclidean dS₂ static-patch (round-sphere) form, with its period doubled [standard]. (JT would be R = −2, AdS₂, F = r² − r_h²; here F = ε_EP² − ε² gives R = +2.) C stays held. no 4d Einstein metric in this folder.

