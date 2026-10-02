# MHD–QG cut connection

New folder. Hive not opened. Tearing not rerun. Same-ε EP₂ theorem not rerun.

Locked: tearing is Δ'>0 FKR, not an EP₂. Pair A is a label 2×2 on Γ, not “the MHD operator.”
Ohmic vs CS do not form an EP₂ at pair A’s ε. Connection ≠ same operator.

## (0) Geometry of Γ

Slit $\Gamma=[-|\varepsilon|,|\varepsilon|]$ at working $\varepsilon=\varepsilon_{\mathrm{EP}}=0.5137$.
Two sheets glued along $\Gamma$. Endpoints are square-root branch points. Standard faces: Arg $=+\pi$ / $-\pi$.
Figure: `outputs/0_gamma_two_sheets.png`.
Label-2×2 jump around the $+$ endpoint: swap at 2π=True, $\Delta n_{\mathrm{MHD}}(2\pi)=1$, $\Delta n_{\mathrm{MHD}}(4\pi)=2$.
Exports `n_sheet`, `Arg_Γ`, jump in `outputs/track0_exports.npz` / `outputs/C_table.csv`.

## (1) MHD letter — pair A (not tearing)

Generator $A=\varepsilon x + i\eta\partial_{xx}$ on $[-1,1]$, two Dirichlet sines.

```
H_A(ε) = [[ -i a,  ε v ],
          [  ε v, -i b ]]
a = η(π/2)^2 = 0.12337
b = η π^2     = 0.49348
v = ⟨φ1, x φ2⟩ = -0.360253
η = 0.05
ε_EP = |b-a|/(2|v|) = 0.513681
```
Letters: two field-line / Alfvén labels. Continuum interval Γ=[−|ε|,|ε|].
Locked N×N fact: the continuum is a cut (min gap ~0.05); discrete EP₂ lives only in this 2×2 map.

## (2) Gravity letter — separate operator on the same Γ

Not pair A’s matrix. No EP₂ demand at ε=0.514.

```
da = π δ_Γ                         # Z2 / square-root edge defect
U_G[γ] = exp(i π I(γ, Γ)) = (−1)^{I(γ,Γ)}
ΔCS[γ] = I(γ, Γ)/2
U_G(θ) = exp(i θ/2) around one endpoint   # U(2π)=−1, U(4π)=+1
```
This is a discrete holonomy / spin-foam edge sitting on Γ, not a 2×2 fusion.

## (3) Connection table C1–C4

| test | formula | number | pass |
| --- | --- | --- | --- |
| C1 shared support | $1_Γ^{MHD}(s)=1_Γ^{QG}(s),\ \mathrm{supp}(da)=\Gamma=[−|ε|,|ε|]$ | overlap=1.000000, Hausdorff=0.0e+00, Γ=[-0.5137,0.5137] | **PASS** |
| C2 shared sheet jump | $\Delta n_{\mathrm{MHD}}(\gamma)=\Delta n_{\mathrm{QG}}(\gamma),\ \gamma: |ε−ε_{\mathrm{EP}}|=r$ | Δn_MHD(2π,4π)=(1,2), Δn_QG(2π,4π)=(1,2), U_G(2π)=-1.000+0.000j, U_G(4π)=1.000-0.000j | **PASS** |
| C3 map, not fusion | $\Phi(n)=e^{i\pi n}=U_G,\quad \Phi(\text{label swap})=−1$ | Φ(n) vs U_G at (0,2π,4π) = (1, -1, 1) vs (1, -1, 1); n_jumps_on_loop=2 | **PASS** |
| C4 residual lock | $R_{\mathrm{MHD}}(s)=1_{s\in\Gamma}/|\Gamma|,\ R_{\mathrm{QG}}(s)=\tfrac12 1_{s\in\Gamma}/|\Gamma|$ | same_support=True, corr=1.000000, R_MHD/R_QG on Γ=2.0000 (expect 2), s-window=[-1.03,1.03], Γ=[-0.5137,0.5137] | **PASS** |

- C1 shared support: Gravity edge defect is defined on the MHD slit. Supports coincide. Not a fusion of matrices.
- C2 shared sheet jump: MHD sheet index from H_A continuation; QG from π-flux holonomy. Matrices differ; Δn matches.
- C3 map, not fusion: Φ is a 0-form dictionary (sheet index → holonomy). It is not H_A = H_G.
- C4 residual lock: Densities are proportional indicators of Γ. No EP2 required. Coordinate is s, one ε.

Coordinate for C4 is arc length $s$ at one $\varepsilon$ (the slit at $\varepsilon_{\mathrm{EP}}$). No collage of different $\varepsilon$ into one point.
Figure: `outputs/4_C4_overlay.png`.

## (4) One sentence

**connection type found: C1 shared support + C2 shared sheet jump + C3 jump map + C4 residual lock**

Named type only. Not a theorem. Not “they are the same operator.” C1 and C4 are support of the slit (Track 2 sits on Γ). C2 and C3 are the non-tautological dictionary: MHD continuation and the π-flux covering share $\Delta n$ and $\Phi(n)=U_G$.
No Qin, no leapfrog, no Hall 3×3, no dynamo phenomenology, no black-hole claim.
