# Helios amendments to IT1B_FUZZY_INSTANTON_PLAN.md (673b5264) — 2026-10-29
HIVE PROPOSAL, UNTESTED. Paper only. Akitti's notes set the setup; O1–O5 stay NOT ADOPTED until she okays. Her open problems stay OPEN.
Co-sign: CONDITIONAL on H1–H4 below being folded into a new file + hash.

H1 (E_pred — answer: NO, not as written). The 0.4 and 0.2857 (=2/7) coefficients are Wilson-lattice O(a²),O(a⁴) artefact terms; they belong to the lattice regulator, not to fuzziness. The fuzzy regulator is a spectral cutoff l≤N−1, so its corrections need not have these coefficients (or even pure x=(λ/ρ)² powers). Amend: E_pred_fuzzy(x)=c1·x+c2·x², with c1,c2 FITTED at k=1 (no tip) over the ladder, frozen, then X_k=E_k−E_pred_fuzzy for k=2. Also fit the same at k=1 with a free λ¹ term; if it is needed (|c0|>2σ), report it. Lattice E_pred reported alongside as reference only. G2 becomes: k=1 fit residual ≤0.01, FAIL >0.03.

H2 (cap×plane reduced model — answer: sound as a local model if R≫ρ). Curvature of the cap shifts the BPST action by O(ρ²/R²). Amend: require R≥10ρ, and run G1 at two R (10ρ, 20ρ); the action shift must scale ≈ρ²/R² (ratio 3–5) else UNDECIDED. G1 1% band only holds at R≥10ρ. Mixed model (2 fuzzy + 2 commutative directions) is fine as a regulator; topological charge must be computed with the fuzzy trace on the cap. Remains REDUCED MODEL label (k≠2 and any product).

H3 (G0 typo check). With X=(2R/√(N²−1))L, [X^i,X^j]=iλε^{ijk}X^k with λ=2R/√(N²−1) — consistent with V6 A1. OK.

H4 (cost). Per x3,x4 site: SU(2) field = few N×N complex matrices; commutators cost ~N³. Cost ∝ L²·N³·steps, so the largest rung dominates (each doubling of N ≈ 8× cost). Example ladder N0=7: N=7,13,25,49 → rung 3 ≈ 340× rung 0. Absolute wall time: NOT COMPUTED (YET) — needs a timed smoke at rung 0 on TrinityOrb after Akitti's go-ahead; if rung-3 projection > 4 h, report before launching rung 3.

Signed: Helios (conditional on H1–H4).
