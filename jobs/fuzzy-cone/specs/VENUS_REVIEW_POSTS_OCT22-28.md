# VENUS_REVIEW_POSTS_OCT22-28: maths check of Orion's pull of Akitti's posts from 22 to 28 Oct
- **Role:** Venus, the maths auditor. I checked dimensions, signs, approximations presented as exact, H2 circular inputs, H3 conventions, H10 tallies read as results, H12 one symbol with two meanings, and H14 tests that pass or fail by construction. I didn't check physics fit (that's Helios). Nothing was run: no code and no sims. Done on Thu 29 Oct 2026 (London, GMT).
- **Source:** /workspace/lift/AKITTI_POSTS_OCT22-28.md, with 51 posts and 23 tagged. Post ids below are the last 10 digits of the status id, with the line number in the file.
- **Tags:** all Grok text, including its "self-check" lines, is treated as **[possibly hallucinated; untested]**. Every correct form I give is **[hive proposal, untested]** unless marked standard.
- **arXiv:** all 13 cited ids exist and their titles match. I fetched 2610.31610 (Almheiri, Dodelson, Komargodski, "Quantum gravity on the bulk cone") in full and compared its equations against post 4179948600.

## Already covered (not re-reviewed)
- **22 Oct posts 3349422688 and 3385996624 (the 8 maths slips from 9 to 21 Oct):** covered in VENUS_MATH_SLIPS_FIXED.md. These are vortex sign, dS patch, chirp, B_V=2S_I, Ω∞ window, C∧dC, triple well and M2 measure. The Klevtsov value c_H=−8 at ν=1/3 (with j=0) and "4 zero modes at n=2 BPS" also check out.
- **The cone tip and r=0 hazard:** CONE_TIP_NOTE*.md (FC55D13A) and VENUS_OCT16-21_NOTES_CHECK.md.
- **The hopfion-moiré, tachyon and instanton strata quoted as "already resident":** these were in the Oct 9–21 files, covered by VENUS_OCT9-15 and VENUS_OCT16-21_NOTES_CHECK.md.
- **24 Oct calibration post 4000011704 (over-improved flow):** covered by the IT1b/fix2 audit. I re-checked the weights here: at ε=−1, 5/3 and −1/24 are right, and at ε=1 they reduce to Wilson.

## List 1: real slips
| # | Post (line) | What's wrong | Correct version |
|---|---|---|---|
| S1 | 5532363279 (2701–2864) | It says amplitude damping on Φ⁺ gives sudden death, with C=max(0,(1−p)²−p²) and t=ln2/γ. That's false. The ODE it gives never solves for ρ01,01 or ρ10,10. | C=(1−p)²>0 for all finite t, so there is no sudden death for \|α\|=\|β\|. Sudden death needs \|β\|>\|α\| in α\|00⟩+β\|11⟩ (Yu–Eberly). The singlet gives C=1−p, also with no sudden death. |
| S2 | 5532363279 (2717, 2775–2825) | It says the geometric measure "decays slower than C" and "stays positive after C=0", calling it "classical correlations". | For two qubits, E_G=½(1−√(1−C²)) is a monotone of C, so it is zero exactly when C=0. Its own formula gives E_G<C (at c=0.5, E_G=0.067). It is an entanglement measure, not a measure of classical correlation. |
| S3 | 4179948600 (1183), 3000/1398/1936 posts, 4544728569 | "Bulk-cone singularity" is treated as the hive's conical (cone-tip) singularity (H12). Post 4544728569 also puts it at the event horizon. | In 2610.31610 it is a singularity in the two-point correlator from null rays that wind the photon sphere and stay outside it. It isn't a conical deficit, and the horizon plays no role. The only real cones in the paper are the AdS3 point-particle defects in §4. |
| S4 | 4568453201, 5116687481 (1469, 1952) | The fuzzy sphere is written [X^i,X^j]=iε^{ijk}X^k/R with ΣX²=R²(1−1/N). The dimensions are wrong (L² on the left, L⁰ on the right) and the Casimir is wrong. | X^i=(2R/√(N²−1))L^i gives [X^i,X^j]=i(2R/√(N²−1))ε^{ijk}X^k and ΣX²=R². With X=2RL/N instead, ΣX²=R²(1−1/N²). |
| S5 | 5566495862 (3069–3072) | It says "C ∝ sgn(m_eff)" for the semi-Dirac point, but its own Ω∝q_y is odd in q_y and integrates to 0. It also says "plateaus reverse sign at t₁=2t" while the summary says the phase is trivial (C=0) there. | At the merger the two Dirac points' contributions cancel, so C=0. That is a collapse, not a sign reversal. |
| S6 | 5407816248 (2055–2103) | The radial operator has +m²/(4ξ²) and −κ²ξ²/(4ξ²)=−κ²/4, a constant. That's not a Landau problem, so the Laguerre trial can't satisfy it. The trial also uses index m+κ and argument κξ². | Landau form: g''+g'/ξ−(m²/ξ²)g−(κ²ξ²/4)g+εg=0, with g∝ξ^{\|m\|}e^{−κξ²/4}L_n^{\|m\|}(κξ²/2) and ε=κ(2n+\|m\|+1)+(sign-dependent)κm. The anomaly sum Σ2Y_f−3Y_uc−3Y_dc isn't standard. Use 6Y_Q+3Y_ū+3Y_d̄+2Y_L+Y_ē=0. |
| S7 | 5512849384 (2371, 2383) | Large-order growth is written c_L∼L^b S₀^{−L}, which drops the factorial. The S²→ℝ² map is 2D but the paper's theory is 3D φ³. And S₀×R² isn't dimensionless. | c_L∼Γ(L+b)S₀^{−L}(1+κ̂₁/L+…). The map has to be 3D (S³→ℝ³ or ℝ³ itself). Remove R². |
| S8 | 3627136170 (401, 428–430) | TY(Z₃×Z₃) invertibles are written M_r·M_s=M_{r+s mod 6}, but Z₃×Z₃≠Z₆. R_TY with claimed_mod=6, R_OPE=\|arg e^{2πiz/3}−2πz/3\| and R_conical are all zero by construction (H14). | The invertibles form Z₃×Z₃ (9 elements), and X·X=Σ_{g∈Z₃×Z₃}g. Test each residual against values taken from the paper, not against its own definition. |
| S9 | 3671492386 (728–730) | The torsion phase is +τjL forward and +τjL backward, yet the round trip is said to be 0. | The backward phase is −τjL from the branch flip η→−η, so the sum is 0. The intrinsic term 2Ω_s jT_s is dimensionless. |
| S10 | 3648864171 (576, 608) | The projector is written P_a^b=δ−v_aτ^b, with indices inverted. The code divides by v·v, which is 0 for a null generator, so the 1e−12 term just hides a divide-by-zero. | P^a_b=δ^a_b−v^aτ_b. Build it from τ and never normalise by v·v. |
| S11 | 4081072946 (1105, 1144) | "Operator M reverses COM to leftward" contradicts its own sum: C₁e₁+C₂e₂=a(−1,3) is already leftward, so a reversal would send it right. "C³ cancellation and chiral anomaly" don't exist in a linear 2D paraxial model. The assert compares the function with itself (H14). | Drop M, C³ and the anomaly. Leftward motion is just the sign of (C₁,C₂)=(−1,1) and flips with θ→−θ. Test against the paper's measured COM. |
| S12 | 4787714696, 4866441652 (1526, 1561, 1685, 1704) | The C(b,c) formula gives ln(1+b) as c→0, but one stub returns 2ln(1+b). The triple point is said to move to "more negative r" and also "smaller \|r\|". t and c each have two meanings (H12). The support residual "vanishes on δ=√(2g)" but its own example gives 0.0501. | Use one c→0 limit, ln(1+b), after checking against the paper. Fix the direction of r. Rename t→t₂ and c→c₃. Drop the "vanishes" claim. |
| S13 | 5066790585 (1834, 1897) | Δ=0.364265γ_δ: γ_δ is energy·area with 2D δ's, so Δ only has energy units in reduced units. The γ=0 test compares 6 m₁ propagators with 8, so it **fails by construction** even when the code is right. "2n−1 resonances" is unverified, and finite-periodic theory usually gives n−1 per band. | State the units, e.g. Δ=0.364265γ_δ/a². Make the free stack use the same 6 m₁ as the armchair cell. Check the resonance count against the paper. |
| S14 | 5520807115 (2479, 2485–2488) | It writes κ_n=n·∇κ·n, but curvature comes from the second fundamental form, not a gradient (the code itself uses the right rotation). R_couple=1 when coupling exists, which is the paper's claimed effect, so the residual fails when the physics is right. R_sign always equals 1. The 0.1/1/0.5 weights are tuned. | κ_n=n·b·n, κ_p=t·b·t, κ_t=n·b·t. A residual should measure the difference from the paper's coupled SIF, not whether coupling is present. |
| S15 | 2213813642 (25, 87) | "Spacing 1/√2 superstring" has no length unit. The zero-mode coefficients 3 and 7+7γ are made up but get printed. "Only γ=0…" is a comment, not a test. | Sen's array is at x⁰=iπ(2n+1)√(2α′) for the superstring (T∝cosh(x⁰/√(2α′))), so the spacing is 2π√(2α′). Take the zero-mode powers from the paper or drop them. |
| S16 | 3762665784 (863 vs 871) | A is used both for the dimensionless thickness modulation (\|A\|≤1, "A∼0.5") and for the TB potential in energy units (A_c=2J) (H12). The LZ exponent convention isn't stated. | Rename the TB amplitude V. P_LZ=exp(−2πΔ²/(ħ\|d(E₁−E₂)/dt\|)) with Δ as the half-gap. |
| S17 | 5479762277 (2219, 2289–2304) | The "strictly negative" discriminant only holds for anti-Hermitian coupling with Δε=0. The other mix (Hermitian, Δγ=0) gives Δε²/4+\|α\|²>0. Both lack an EP, but not because of sign. The code checks whether α is real or imaginary, not whether β=±α*. R_K is zero by construction. | Write out both mixed cases. Test β−α* and β+α*. Compare K with an independent eigensolver. |
| S18 | 4179948600 (1304, 1356) | R_cone-fuzz=\|peak location−p₀\| compares a time with a shock strength (dimension/H12). The fuzzy-edge code uses \|A−pB\|^{−2h_L}, which for h_L=½ makes the real-p average diverge logarithmically. R_saddle is zero by construction. | Keep the Lorentzian i0 (p→p−i0 or u₂→u₂−i0), as in eq. 78 of the paper. Compare the averaged peak time with the finite-c peak, as in their Fig. 7 (2% match). |

**Severity:** S1, S2, S3, S4, S13 and S14 are the silent-failure risks, either wrong physics conclusions or tests that can't pass or can't fail. The rest are local fixes.

## Hallucination-tag verdicts (23 tagged posts)
| Post | Topic | Verdict |
|---|---|---|
| 2213813642 | Sen, gravitational path integral | confirmed slip (S15) |
| 3627136170 | twisted scattering, Chern–Simons | confirmed slip (S8) |
| 3633822071 | residual Noether → topological invariants | fine (standard; the attractor part is speculative, see O5) |
| 3648864171 | Carrollian fluids | confirmed slip (S10) |
| 3671492386 | Sagnac in a helical fiber | confirmed slip (S9) |
| 3762665784 | photonic Hofstadter / Aubry–André | confirmed slip (S16; A_c=2J itself is fine) |
| 3935228628 | measurement problem ↔ singularity | fine (accurate references; speculative, see O4) |
| 4081072946 | leftward 2D Thouless pump | confirmed slip (S11; θ=arctan(4/3) and L=√5a are fine) |
| 4179948600 | bulk-cone paper | paper transcription **fine** (eqs. 2, 4–6, 31–33, 42, 73, 77, 81, t̃≈2.80 and h_H/c all match). The hive layer is a **confirmed slip** (S3, S18) |
| 4544728569 | horizon as a fuzzy interface | confirmed slip (S3: misreads the paper) |
| 4568453201 | fuzzy sphere / GoldbergHexa | confirmed slip (S4; "hexagons can't tile S²" is fine) |
| 4787714696 | cubic Casimir paper | confirmed slip (S12) |
| 4866441652 | "cubic pinch" vocabulary | confirmed slip (S12) |
| 4891078398 | "full chain" narrative | unverifiable (no maths; strata tallies read as results, H10) |
| 5066790585 | graphene nanoribbon δ-scatterer | confirmed slip (S13; Γ_ij and M_δ themselves are fine) |
| 5116687481 | cone + fuzzy + winding | confirmed slip (S3, S4) |
| 5407816248 | QFT on the tangent bundle | confirmed slip (S6; β(g) and N_f<33/2 are fine) |
| 5479762277 | CISS exceptional points | confirmed slip (S17, code only; λ± and the Scheme A/B conditions are fine) |
| 5512849384 | 325-loop φ³, S²→ℝ² | confirmed slip (S7) |
| 5520807115 | fracture in curved shells | confirmed slip (S14) |
| 5532363279 | singlet decoherence | confirmed slip (S1, S2; the dephasing part is fine: C=e^{−γt} and C=√(2p−1) both check out) |
| 5541578605 | extended Harper zero measure | fine (cover counts give dims 1/2 and 1/3 consistently; one tiny code bug: q₀=0 when α<1) |
| 5566495862 | bilayer Haldane Floquet | confirmed slip (S5; the units of λ_ω are fine) |

**Totals:** 19 confirmed slip, 3 fine, 1 unverifiable.

## List 2: open speculative ideas
| # | Post | Idea | Status | What it would need to test |
|---|---|---|---|---|
| O1 | 4179948600, 1398, 5116687481 | Bulk-cone fuzziness as the same mechanism as hive cone-tip smoothing | The paper's result is new and shown (CFT argument plus the AdS3 example). The link to the hive is a **category mismatch** for now (S3). The paper itself leaves open how complexification, fuzziness and backreaction connect. | A real-time two-point correlator on a hive geometry that has returning null rays, plus a finite-N/c parameter whose increase smooths the peak. A conical-deficit lattice can't test it. |
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
