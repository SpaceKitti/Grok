# pairA-jt-4d

Akitti's build toward JT (AdS₂ sign) and a 4D metric on the Pair A eigenvalue curve y² = 4v²(ε² − ε_EP²), λ± = λ_EP ± y/2. Two-mode toy.

Run: `python run.py` (venv python, PYTHONIOENCODING=utf-8; needs numpy, scipy, sympy). Writes RESULTS.md.

Geometry inputs are numbers only (Akitti): ε_EP = 0.51368066, λ_EP = −0.308425i, v = −0.360253, τ_swap = 4π/ε_EP; A WRITE, B WRITE, C held. The geometry loads no files; the D6/D7 map reads the RESULTS.md of pairA-qg-probe-surface and pairA-qg-operator read-only (SHA-256 checked before/after).

Files:
- jt2d.py: the numbers, branch tracking of y, JT 2D F_JT = ε² − ε_EP² (R, sign regions, F_JT = y²/(4v²), surface gravity, cone angles, topology, Gauss–Bonnet).
- lift4d.py: 4D ansatz ds² = −F_JT dt² + dε²/F_JT + r² dΩ₂² (Ordinary S^2 (standard theta, phi) is used; GoldbergHexa (Akitti's custom probe lattice) not needed.); R1 r = ε_EP (AdS₂×S², an exact Einstein–Maxwell–Λ solution of the Bertotti–Robinson/Nariai family [standard, computed from G_ab]; Λ, E² printed), R2 r² = ε_EP² − ε² (Kantowski–Sachs cosmology inside Γ; χ forward, χ: 0 → π, ε = ε_EP cos χ from +ε_EP to −ε_EP: Big Bang at +ε_EP (χ = 0), Big Crunch at −ε_EP (χ = π), [by construction: χ-forward convention; time-reversal (χ → π−χ) swaps them]); R, Kretschmann, Einstein tensor (information only).
- match.py: M1–M5 PASS/FAIL.
- run.py: runs everything, writes RESULTS.md.

no JT dual claimed; no Einstein solution claimed (R1 geometry is a known Einstein–Maxwell–Λ solution [standard]; not derived from Pair A). No QG Hamiltonian derived.

M3: swap/return needs a degree-2 cover: the smooth period already gives one; 4π cone [by construction]. M5: [by construction, numerically confirmed].

R1 (AdS2 x S2, r = eps_EP) is the 4D target. R2 is not a target (kept as information only).

D6/D7 map (match.py): D6/D7 are one driven loop around +ε_EP straddling Γ, labelled by start point (0.75 / 1.25 ε_EP); the start points sit at F_JT < 0 / F_JT > 0. Printed verdict: see RESULTS.md ('regions match YES/NO'). chirality inherited from H_A, not from F_JT: F_JT and y² depend only on position, so the static geometry is identical for cw and ccw loops [standard]. The monodromy is a swap, its own inverse, so cw and ccw give the same label map (computed both ways in match.py); the D7 direction pick comes from the lossy evolution i∂_tψ = H_A(ε(t))ψ. arrow = chi forward; labels match chi — [by construction: χ-forward convention; time-reversal (χ → π−χ) swaps them] (the metric is symmetric under χ → π−χ; the check is a consistency check of the convention).

Revision 2026-09-25 (D6/D7 map, R2 χ-forward labels, GoldbergHexa note): signed off by Venus (maths) and Helios (physics).
