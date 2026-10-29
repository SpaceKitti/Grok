# FUZZ_PLAN_V5
**POST-SMOKE CHANGE, derived from maths only; spec issue, not a fix-loop round; frozen before any rung runs. Signed: Venus. Co-sign: Helios, NanoRibbon (pending).**
Replaces only V4 §3 (test B observable) and the test B bands of V4 §1. Everything else in FUZZ_PLAN_V4 (cbf25723, untouched) stands: §2 test A as code check, §4 R2/R5 at h_L=1/2, §5 k=2 exact (other angles = reduced model), §6 D(N), §7 ladder rules, §8 code bugs.
Disclosure: smoke numbers (V4 pole-LDOS, p≈−0.5) existed before this file. No smoke number is used below. The only numbers computed were <1 s checks of closed forms derived here (§4.3), not runs of the graded code.

## 0. Notation (unchanged from spec)
N=2j+1, L^i spin-j, X^i=λL^i, λ=2R/√(N²−1). Algebra M_N with Hilbert–Schmidt trace. Δ_N(M)=R^{−2}Σ_i[L^i,[L^i,M]], spectrum l(l+1)/R², l=0..N−1, eigenbasis T_{lm} (fuzzy harmonics). g=exp(2πiL³/k), Ad_g(M)=gMg^{−1}, P_k=(1/k)Σ_{n=0}^{k−1}Ad_g^n projects onto A_k (Z_k-invariant matrices). Ad_g T_{lm}=e^{2πim/k}T_{lm}.
Exact identity: λ/R=2/√(N²−1). **At fixed R, varying λ is the same as varying N; every observable of this model is a function of (t/R², N, k).** Aethon's "depends only on N, not λ" is therefore a property of the model, not a defect. The defect is k-blindness (§1).

## 1. Why the V4 pole LDOS is k-blind (Aethon's m=0 result, stated and proved)
**Lemma 1.** Let |pole⟩=|j,j⟩ (the coherent state at the tip). Then ⟨pole|T_{lm}|pole⟩=0 for m≠0, and |⟨pole|T_{l0}|pole⟩|²=((2l+1)/N)·c_l, c_l=⟨j j; l 0|j j⟩²=((N−1)!)²N/((N+l)!(N−1−l)!).
*Proof.* T_{lm} is a rank-l spherical tensor operator. Wigner–Eckart: ⟨j m'|T_{lm}|j m''⟩=⟨j m''; l m|j m'⟩·⟨j‖T_l‖j⟩/√(2j+1); the CG vanishes unless m'=m''+m, so with m'=m''=j only m=0 survives. HS-normalisation Tr(T_{l0}†T_{l0})=1 with the CG orthogonality Σ_{m''}⟨j m'';l 0|j m''⟩²=(2j+1)/(2l+1) gives |⟨j‖T_l‖j⟩|²=(2l+1), hence the stated value. The closed form of c_l is the standard stretched CG (2j)!(2j+1)!/((2j+l+1)!(2j−l)!) rewritten with N=2j+1. (Aethon verified explicitly for N=5–7.) ∎
**Corollary.** m=0 ⊂ A_k for every k, so K_N(t;pole)=(k/4πR²)Σ_l(2l+1)c_l e^{−tl(l+1)/R²}; the factor k cancels in K_N/K_∞. **Classically the same holds**: on S²/Z_k the kernel at a fixed point x₀ is (1/k)·k·K_{S²}(x₀,x₀) up to the area factor, since g x₀=x₀ makes every image term equal the direct term. So any diagonal quantity AT the fixed point is k-blind, fuzzy or not. The cone angle lives only in image terms K(x,g^n x) with x≠x₀, i.e. in a trace over a neighbourhood of the tip.
**The V4 §3 Berezin symbol of the matrix Laplacian is dropped** (it was never defined as a map M_N→functions in V4). The only Berezin/Toeplitz object kept is the localiser F of §2, defined explicitly.

## 2. New primary test B observable: localised tip twisted heat trace
Cap function χ(θ): smooth, =1 for θ≤π/4, =0 for θ≥π/2, χ(θ)=s((π/2−θ)/(π/4)) with s(x)=e^{−1/x}/(e^{−1/x}+e^{−1/(1−x)}) on (0,1). Fixed geometric radius; never rescaled with N.
Matrix localiser (Toeplitz quantisation, diagonal by axial symmetry): F=Σ_m F_m|j,m⟩⟨j,m|,
  F_m = N·(1/2)∫₀^π χ(θ) C(2j, j+m) cos^{2(j+m)}(θ/2) sin^{2(j−m)}(θ/2) sinθ dθ,
using |⟨j,m|n(θ,φ)⟩|²=C(2j,j+m)cos^{2(j+m)}(θ/2)sin^{2(j−m)}(θ/2). Superoperator 𝓕(M)=½(FM+MF).
**Observable:** T_N(t) = Tr_{M_N}[ 𝓕 ∘ (P_k − 1/k) ∘ e^{−tΔ_N} ] = (1/k)Σ_{n=1}^{k−1} Tr_{M_N}[𝓕 ∘ Ad_g^n ∘ e^{−tΔ_N}].
Classical comparison T_∞(t): same with l unbounded and F→χ (multiplication).
**Classical limit (normalisation, one tip).** Near the north pole x₀, ∫χ(x)K(t;x,R_φx)dA→1/(4sin²(φ/2)) as t→0 (Gaussian with |x−R_φx|=2r sin(φ/2)). Σ_{n=1}^{k−1}1/(4sin²(πn/k))=(k²−1)/12. So T_∞(0⁺)=(1/12)(k−1/k): **exactly the per-tip value; χ covers one tip only** (the south pole has χ=0). Global (χ≡1) version gives 2·(1/12)(k−1/k), checked in §4.3.

## 3. Width and scaling (maths only)
Spectral form, for χ≡1 (closed form; the cap version equals half of it up to edge terms, see H1): T_N(t)=(1/k)Σ_{n=1}^{k−1}Σ_{l=0}^{N−1}χ_l(2πn/k)e^{−tl(l+1)/R²}, χ_l(φ)=sin((2l+1)φ/2)/sin(φ/2).
The character sequence χ_l(2πn/k) is periodic in l with period k and zero mean. So T_N−T_∞ = −(tail l≥N) = −e^{−τ}·B_k(N mod k)·(1+O(1/N)), τ=tN²/R², B_k from the Abel sum of the periodic tail. Hence:
- the fuzzy curve departs from the classical one at **t* = τ*_k R²/N²**, so **w=√t* ∝ R/N ∝ λ, p* = −1** (w/R ∝ N^p);
- t→0: T_N(0)=(1/k)Σ_n sin²(πnN/k)/sin²(πn/k), which depends on N mod k. **Rule: rungs use N≡1 (mod k)** (k=2: N odd; k=3: N=64,127-type), so B_k is fixed across rungs. λ is then recomputed exactly as 2R/√(N²−1).
- Threshold 10% (frozen from V4): |T_N/T_∞−1| = |B_k/T_∞(0)|e^{−τ} ⇒ τ*_k=ln(10|B_k|/T_∞(0)).
 k=2, N odd: B/T_∞ = 1 ⇒ **τ*_2 = ln 10 = 2.303**. k=3, N≡1: B/T_∞ = 1/2 ⇒ **τ*_3 = ln 5 = 1.609**. The ratio τ*_2/τ*_3 = 1.431 is k-dependent (criterion a).
**Note on √(Rλ) (V4 §1):** √(Rλ) is the coherent-state (position-probe) resolution, which is what the pole LDOS saw. The trace observable probes the spectral cutoff l≤N−1, wavelength ~R/N ~ λ. Both are correct for their own probes. V5 grades the trace, so its model is p*=−1, not −1/2. The V4 band [−0.6,−0.4] is retired with the LDOS and kept as report-only for it.

### 4.3 Hand checks done (<1 s each, closed form χ≡1, not the graded code)
t*N²/R² at 10%: k=2 N=129: 2.305; N=65: 2.302 (ln10=2.303). k=3 N=127: 1.597; N=64: 1.585 (ln5=1.609, O(1/N) drift). T_N(0)=2T_∞(0) for both k (B/T_∞ as derived).

## 4. Criteria (a)–(d)
(a) k: plateau (1/12)(k−1/k) and τ*_k both depend on k; LDOS did not. (b) λ at fixed R: t*=τ*R²/N²=τ*λ²(N²−1)/(4N²), so w moves with every rung. (c) can fail: p, τ*_k and the plateau are each predicted numbers; a wrong Δ_N, wrong Ad_g, wrong P_k or a cap that leaks to the other pole changes them. (d) explicit: §2 gives every matrix.

## 5. Frozen bands (per rung set, k=2 primary; k=3 report-only per V4 §5 exactness, but graded with same bands as a check)
- **B-p** (fit w/R ∝ N^p over the V3/V4 ladder, ≥4 rungs, N≡1 mod k): PASS p∈[−1.10,−0.90]; FAIL p outside [−1.30,−0.70] or local slopes drifting by >0.3; UNDECIDED otherwise. Justification: leading p=−1 exactly; corrections are O(1/N) in τ* (see §4.3 size), ≪0.1 for N≥32; FAIL edge excludes the coherent-state value −0.5.
- **B-τ** (τ*_k = t*N²/R² at the largest rung): PASS within 5% of ln(10|B_k|/T_∞(0)) (k=2: ln10); FAIL >15%; UNDECIDED between.
- **B-plateau** (T_∞ side, code check): T at smallest t within 5% of (1/12)(k−1/k) per tip.
- Fewer than 4 valid rungs: UNDECIDED. V3 L-q / L-h stand, applied to p from B-p.

## 6. Open for Helios (physics)
H1. Cap edge: Toeplitz F differs from χ by O(1/N) smearing on √(Rλ) at θ≈π/4–π/2, far from the tip; I claim it only adds a k-independent O(t) and O(1/N) piece and leaves τ*, p unchanged. Please confirm or bound it.
H2. Is p*=−1 (spectral cutoff) the physically wanted "tip smoothing" width, versus √(Rλ) for a point probe? V5 reports both (LDOS report-only).
H3. N≡1 mod k rule: confirm it is acceptable for the ladder at fixed R.
