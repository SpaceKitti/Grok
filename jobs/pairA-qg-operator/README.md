# pairA-qg-operator

What it is (Akitti): the smallest gravity-side object whose cut, tips, monodromy and inside/outside switch are Pair A's. Two-mode toy.

Run: `python run.py` (PYTHONIOENCODING=utf-8). It writes RESULTS.md. No Einstein solver, no new MHD matrix, no git.

Loaded read-only (SHA-256 of every file checked before and after each run):
- C:\Users\Akitt\pairA-qg-probe-surface (D1–D7 via its dictionary.py / cover.py / load_surface.py, cross-checked against its RESULTS.md)
- C:\Users\Akitt\pairA-qg-handoff (seed, tracker, wick_lorentzian, outputs/Jhat.npz, outputs/summary.json, RESULTS_probe.md)
- C:\Users\Akitt\pairA-drive-return (outputs/drive.npz, outputs/drive_start1p25.npz, RESULTS.md, RESULTS_start1p25.md)

Files:
- spec_D.py: loads D1–D7 (tags, conditions) from the probe surface; asserts ε_EP = |a−b|/(2|v|) ≈ 0.51368066, λ_EP = −i(a+b)/2 ≈ −0.308425i, Γ = [−ε_EP, ε_EP], v = −0.360253, τ = 4π/ε_EP ≈ 24.46339, Jhat2 swap, Jhat4 = I, A WRITE, B WRITE, C held, inside no chirality, outside chirality on slow drive (Akitti's numbers used only for agreement checks). Hashing.
- curve.py: y² = 4v²(ε² − ε_EP²) checked against H_A eigenvalues (λ_EP ± y/2), monodromy of y, two-detour test, cover U_G (probe cover.py on the same loops), period.
- operator.py: P1 edge H_edge = −∂x² + x (Airy; tip only; its link to the EP is a [standard analogy] through the WKB momenta ±√(E − x), P1 itself is Hermitian and has no EP) and P2 mini-superspace F = ε_EP² − ε², ds_E² = dε²/F + F dτ_E² (chart, cone angle / regularity, λ_EP, curvature). Loaded by run.py via importlib because the name shadows Python's stdlib `operator`.
- match.py: D1–D7 PASS / FAIL against P1 + P2; D6, D7 = INHERITED FROM H_A, not from P1; Riemann–Hurwitz cross-check [computed] (curve = genus-0 double cover branched only at ±ε_EP, χ = 2; P2 = one sphere (chi=2) double-covering the round sphere, branched at ±ε_EP).
- run.py: runs everything, writes RESULTS.md.

Tag: P1 + P2 is [hive-interpretation] — built to match the D1–D7 spec, not derived from a gravity theory; no JT dual is claimed. no 4d Einstein metric in this folder.

P2 has the Euclidean dS₂ static-patch (round-sphere) form, with its period doubled [standard]. (JT would be R = −2, AdS₂, F = r² − r_h²; here F = ε_EP² − ε² gives R = +2.)

QG-side toy = edge operator P1 at each tip, on background geometry P2, with H_A's loss supplying D6/D7 [hive-interpretation]. (P2 is a metric, not an operator, so '+' here means 'together', not an operator sum.)
