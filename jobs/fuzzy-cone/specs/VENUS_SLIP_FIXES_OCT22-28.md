# VENUS_SLIP_FIXES_OCT22-28: drafted fixes for the 18 maths slips (22–28 Oct posts)
- **From:** Venus (maths auditor), Thu 29 Oct 2026 (London, GMT). Source: VENUS_REVIEW_POSTS_OCT22-28.md, AKITTI_POSTS_OCT22-28.md.
- **Status:** drafts only. Nothing posted, no code, no sims. Corrected forms are **[standard]** where noted, otherwise **[hive proposal, untested]**.
- **Attribution:** where a slip sits in Grok's reply text or code, it says "Grok's text". Nothing here is a correction of Akitti's own wording unless it says so.
- **Bulk cone (S3, S18):** Akitti said the paper's bulk cone has the "same shape" as the hive tip. She never said they were identical. These items explain what the paper's bulk cone is and how far the shape analogy goes. They don't correct her.

## Drafted fixes
### S1 · 5532363279 (L2701–2864) · Grok's text
- **Original:** "amplitude damping on Φ⁺ → sudden death, C=max(0,(1−p)²−p²), t=ln2/γ"
- **Draft:** Amplitude damping on Φ⁺ gives C=(1−p)², with p=1−e^{−γt}. That stays positive for every finite t, so there is no sudden death [standard]. Sudden death in α|00⟩+β|11⟩ needs |β|>|α| (Yu–Eberly). The singlet gives C=1−p, which also never hits zero early.
- **Why:** the ODE as written never solves for ρ01,01 or ρ10,10. The max(0,…) form comes from a different initial state.

### S2 · 5532363279 (L2717, 2775–2825) · Grok's text
- **Original:** "geometric measure decays slower than C … stays positive after C=0 … classical correlations"
- **Draft:** For two qubits, E_G=½(1−√(1−C²)), which is a monotone function of C. So E_G=0 exactly when C=0, and E_G<C (C=0.5 gives E_G≈0.067) [standard, Wei–Goldbart]. E_G measures entanglement, not classical correlation.
- **Why:** the claim contradicts its own formula.

### S3 · 4179948600 (L1183), 3000/1398/1936, 4544728569, 5116687481 · what the paper's bulk cone is
- **Original:** "bulk-cone singularity" is used next to the hive's cone tip, and 4544728569 places it at the event horizon.
- **Draft:** In arXiv:2610.31610 (Almheiri–Dodelson–Komargodski), the bulk-cone singularity is a singularity in the boundary two-point correlator ⟨O(t)O(0)⟩. It appears at boundary times joined by bulk null geodesics, including rays that wind the photon sphere and come back to the boundary. Those rays stay outside the horizon, so the horizon plays no role. The paper's conical geometries are a separate thing: the AdS3 point-particle defects in §4.
- **How the "same shape" analogy carries over:** both are places where a smooth classical answer goes singular and finite-N/c effects might smooth it. That's the analogy, and it's still open (O1).
- **Where it stops:** the paper's object is a singularity in time in a correlator, sitting on a light cone in the space of boundary points. The hive tip is a conical deficit in space. They're different kinds of thing, so the two can't share an equation or a residual (H12 symbol clash) until O1's bridge exists.
- **Fix:** keep the two names apart, for example "bulk-cone (correlator) singularity" and "cone-tip (conical) singularity". Remove "at the horizon" from 4544728569.

### S4 · 4568453201, 5116687481 (L1469, 1952)
- **Original:** "[X^i,X^j]=iε^{ijk}X^k/R, ΣX²=R²(1−1/N)"
- **Draft:** X^i=(2R/√(N²−1))L^i with L^i in the N-dim irrep gives [X^i,X^j]=i(2R/√(N²−1))ε^{ijk}X^k and ΣX²=R² [standard, Madore]. With the normalisation X=2RL/N instead, ΣX²=R²(1−1/N²).
- **Why:** as written, the left side has units L² and the right side L⁰. The Casimir is also wrong.

### S5 · 5566495862 (L3069–3072) · Grok's text
- **Original:** "C ∝ sgn(m_eff)" … "plateaus reverse sign at t₁=2t"
- **Draft:** At t₁=2t the two Dirac points merge into a semi-Dirac point and their Berry curvatures cancel, so C=0. The Chern number collapses to zero. It doesn't reverse sign. Ω∝q_y is odd in q_y and integrates to 0, which agrees with C=0.

### S6 · 5407816248 (L2055–2103) · Grok's text
- **Original:** radial operator with "+m²/(4ξ²) … −κ²/4", Laguerre trial L_n^{m+κ}(κξ²)
- **Draft:** Use Landau form: g''+g'/ξ−(m²/ξ²)g−(κ²ξ²/4)g+εg=0. Then g∝ξ^{|m|}e^{−κξ²/4}L_n^{|m|}(κξ²/2) and ε=κ(2n+|m|+1)+(sign-dependent)κm [standard]. For the anomaly, use the standard hypercharge sums, e.g. 6Y_Q+3Y_ū+3Y_d̄+2Y_L+Y_ē=0 (left-handed Weyl convention).
- **Why:** −κ²/4 is a constant, so the operator as written has no Landau problem and the Laguerre trial can't solve it.

### S7 · 5512849384 (L2371, 2383) · Grok's text
- **Original:** "c_L∼L^b S₀^{−L}", "S²→ℝ²", "S₀·R²"
- **Draft:** c_L∼Γ(L+b)S₀^{−L}(1+κ̂₁/L+…) [standard large-order form]. The paper's φ³ theory is 3D, so the map has to be 3D (S³→ℝ³, or ℝ³ itself). S₀ is dimensionless, so drop R².

### S8 · 3627136170 (L401, 428–430) · Grok's text/code
- **Original:** "M_r·M_s=M_{r+s mod 6}", with residuals R_TY, R_OPE and R_conical
- **Draft:** For TY(Z₃×Z₃) the invertibles form Z₃×Z₃, which has 9 elements and isn't Z₆. The duality defect obeys X·X=Σ_{g∈Z₃×Z₃} g [standard]. Each residual should be checked against values taken from the paper.
- **Why:** with claimed_mod=6 and the definitions as written, all three residuals are zero by construction (H14).

### S9 · 3671492386 (L728–730) · Grok's text
- **Original:** forward "+τjL", backward "+τjL", round trip "=0"
- **Draft:** The branch flip η→−η makes the backward phase −τjL, so the torsion terms cancel to 0 on the round trip. The intrinsic term 2Ω_s jT_s is dimensionless and stays.

### S10 · 3648864171 (L576, 608) · Grok's text/code
- **Original:** "P_a^b=δ−v_aτ^b", normalised by v·v (+1e−12)
- **Draft:** P^a_b=δ^a_b−v^aτ_b, with τ_a v^a=1 [standard Carrollian]. Build it from τ and never divide by v·v.
- **Why:** v is null, so v·v=0. The 1e−12 term just hides a divide-by-zero.

### S11 · 4081072946 (L1105, 1144) · Grok's text
- **Original:** "Operator M reverses COM to leftward", "C³ cancellation", "chiral anomaly"
- **Draft:** The COM moves left because (C₁,C₂)=(−1,1), giving displacement a(−1,3), and it flips under θ→−θ. Drop M, C³ and the anomaly, because none of them exist in a linear 2D paraxial model. The assert should compare against the paper's measured COM.
- **Why:** reversing motion that's already leftward would send it right. Also, the assert compares the function with itself (H14).

### S12 · 4787714696, 4866441652 (L1526, 1561, 1685, 1704) · Grok's text/code
- **Original:** c→0 limit "2ln(1+b)" vs "ln(1+b)", triple point at "more negative r" and "smaller |r|", "vanishes on δ=√(2g)"
- **Draft:** Use one c→0 limit, ln(1+b), and check it against the paper. Pick one direction for the triple point's shift in r. Rename the second t to t₂ and the second c to c₃. Remove "vanishes", because the post's own example gives 0.0501.

### S13 · 5066790585 (L1834, 1897) · Grok's text/code
- **Original:** "Δ=0.364265γ_δ", γ=0 test (6 vs 8 m₁), "2n−1 resonances"
- **Draft:** With 2D δ's, γ_δ has units energy·area, so write Δ=0.364265γ_δ/a² or say "reduced units". Make the free stack use the same 6 m₁ propagators as the armchair cell. Present the resonance count as "to check against the paper", since finite-periodic theory usually gives n−1 per band.
- **Why:** as written, the γ=0 test fails by construction.

### S14 · 5520807115 (L2479, 2485–2488) · Grok's text/code
- **Original:** "κ_n=n·∇κ·n", R_couple=1 when coupling exists, R_sign≡1, weights 0.1/1/0.5
- **Draft:** Take curvatures from the second fundamental form b: κ_n=n·b·n, κ_p=t·b·t, κ_t=n·b·t [standard]. The residual should be the difference from the paper's coupled SIF. Remove R_sign and the tuned weights.
- **Why:** R_couple flags exactly the effect the paper claims, so it fails when the physics is right.

### S15 · 2213813642 (L25, 87) · Grok's text
- **Original:** "spacing 1/√2 superstring", zero-mode coefficients 3 and 7+7γ, "Only γ=0…"
- **Draft:** For the superstring, T∝cosh(x⁰/√(2α′)) has zeros at x⁰=iπ(2n+1)√(2α′), so the spacing is 2π√(2α′) [standard, Sen]. Take the zero-mode powers from the paper or drop them. "Only γ=0" is a comment, not a test.

### S16 · 3762665784 (L863 vs 871)
- **Original:** A used for both the thickness modulation ("A∼0.5") and the TB potential ("A_c=2J")
- **Draft:** Keep A for the dimensionless modulation (|A|≤1) and use V for the TB amplitude (V_c=2J). State the LZ convention: P_LZ=exp(−2πΔ²/(ħ|d(E₁−E₂)/dt|)), with Δ the half-gap [standard].

### S17 · 5479762277 (L2219, 2289–2304) · Grok's text/code
- **Original:** "discriminant strictly negative" for the mixed case, code tests whether α is real or imaginary, R_K
- **Draft:** Write out both mixed cases. With anti-Hermitian coupling and Δε=0, the discriminant is <0. With Hermitian coupling and Δγ=0, it is Δε²/4+|α|²>0. Neither has an EP, but not because of the sign. The code should test β−α* and β+α* directly, and K should be compared with an independent eigensolver.
- **Why:** R_K is zero by construction.

### S18 · 4179948600 (L1304, 1356) · Grok's code; how the paper's fuzzy edge works
- **Original:** "R_cone-fuzz=|peak location−p₀|", kernel |A−pB|^{−2h_L}, R_saddle
- **Draft:** In the paper, the singularity is smoothed by keeping the Lorentzian i0 (p→p−i0, or u₂→u₂−i0, eq. 78). The check is whether the averaged peak time matches the finite-c peak (their Fig. 7, a 2% match). Compare a time with a time.
- **Why:** p₀ is a shock strength, not a time (dimension/H12). Without the i0, |·|^{−1} at h_L=½ makes the average diverge logarithmically. R_saddle is zero by construction. This is about Grok's code, not the shape analogy, which stays open as O1.

## Open speculative ideas (kept intact, separate)
| # | Post | Idea | Status | What it would need to test |
|---|---|---|---|---|
| O1 | 4179948600, 1398, 5116687481 | Bulk-cone fuzziness as the same mechanism as hive cone-tip smoothing | The paper's result is new and shown (CFT argument plus the AdS3 example). The link to the hive is a category mismatch for now (S3). The paper itself leaves open how complexification, fuzziness and backreaction connect. | A real-time two-point correlator on a hive geometry that has returning null rays, plus a finite-N/c parameter whose increase smooths the peak. A conical-deficit lattice can't test it. |
| O2 | 4544728569, 4568453201 | The horizon as a fuzzy interface, with ANEC-violating negative energy from non-commuting coordinates | Open and speculative. The paper says nothing about horizons. | A stress tensor defined in the matrix model, then a computed ANEC integral on a shell, compared with the commutative limit. |
| O3 | 4568453201, 5116687481 | Finite-N fuzzy geometry smears a cone tip | Fuzzy cones and orbifolds exist in the NC literature, so this is plausible but not shown here. | An explicit fuzzy-cone algebra, and a check that the spectral density near the tip converges to the classical one as N→∞ with a finite-N cutoff that scales like 1/N. |
| O4 | 3935228628 | The singularity "regime flip" and measurement collapse are the same missing selection rule | Both are well-known open problems. The link is a conjecture (Penrose–Diósi; the one-dimensional closed-universe Hilbert space claim). | A model where one parameter controls both decoherence and singularity resolution and gives a testable rate. |
| O5 | 3633822071, 4891078398 | Residual Noether charges lock into invariants on attractors | The gapped and higher-form part is known (Kapustin–Sopenko; higher-form symmetries). The attractor and "9-basin" part is undefined. | A defined dynamical system with a conserved quantity whose value is a homotopy or cohomology class of the basin. |
| O6 | 4866441652 | One-cut→two-cut "pinch" is the same as an eigenvalue kiss of the Hessian under Brockett flow | Speculative analogy, flagged as "geometric only". | A shared order parameter (for example a Painlevé-II scaling exponent at both transitions) computed on each side. |
| O7 | 2213813642 | Sen's string-scale cut-off (γ=0) is the same as the rolling-tachyon array spacing | Sen's result is published. The identification is a hive overlay (H2: the spacing is put in as γ=0). | A derivation showing the D-instanton spacing sets l_UV in the one-loop index, without assuming it. |
| O8 | 4081072946, 3000 | "Left-leaning chirality" coupling to the Thouless cycle | Undefined ("Operator M"). | A concrete operator and a predicted change in (C₁,C₂). With no operator there's nothing to test. |
| O9 | 5407816248 | Tangent-bundle QFT gives SU(2)×SU(3) and fractional charges | The paper's claim, unconfirmed by others. | Check the standard anomaly sums and that κ=3Y reproduces Q_u=2/3 and Q_d=−1/3 (as written, κ_Q=1/2≠1/3). |
| O10 | 4891078398 | The photon on the Hopf fiber plus a torsion mass mechanism | Speculative. Torsion gravity and Hopf-fibration electromagnetism exist separately. | An action and a computed mass spectrum. |
| O11 | 5512849384 | Matching the 325-loop φ³ instanton action to hive φ³/φ⁴ notes | Open, but mis-posed (S7). | Use the same dimension (3D), take S₀ from the hive's own bounce equation, and compare with the paper's S₀. |
| — | 3349422688 | AdS4↔AdS3 filter, vortex as a holographic dual, lattice graviton, radial RG | Already listed by Akitti on 22 Oct; I haven't changed them. | As she stated. |
