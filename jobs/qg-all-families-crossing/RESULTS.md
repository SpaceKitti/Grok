# All-families crossing sweep

New folder. Hive not opened. Pair A not rebuilt. P0 locked (pair A sees the wall).
No letter is $n_{\mathrm{MHD}}$ or $da=\pi\delta_\Gamma$.
$\gamma_{\mathrm{cross}}$ at $x=0.25$ through $\Gamma=[-0.513681,0.513681]$; $\gamma_{\mathrm{miss}}$ at $x=1.2$, same length.
If a theory cannot live on this mesh without a U(1) nickname, the row is **could not define**.

## 1 Chern–Simons / 3d gravity

```
Chern–Simons / 3d gravity
    S = (k/4π)∫ Tr(A dA + 2/3 A^3), k=8, G=SU(2) or U(1)
    2d spatial lattice, CS vacuum F=0, A_ℓ=0
    J = |∫_γ A|
```

J_on=0, J_off=0, ratio=0, wall site=vacuum A=0. verdict: **misses Γ**.

## 2 Ashtekar–Barbero / canonical LQG

```
Needs a 3d spatial graph, SU(2) spin networks, densitized triad, Hamiltonian constraint. This slit is a 2d label plane, not a 3-geometry. No fake holonomy.
```

J_on=nan, J_off=nan, ratio=nan, wall site=n/a. verdict: **could not define**.

## 3 Spin foam

```
Spin foam (2d)
    Z = ∑_{j_f} ∏_faces dim(j)  with flatness: only j compatible with F=0
    on this mesh every face amplitude is 1 (no curvature)
    J = |Z_path − 1| = 0
```

J_on=0, J_off=0, ratio=0, wall site=flat foam. verdict: **misses Γ**.

## 4 BF theory

```
BF theory
    S = ∫ B ∧ F
    eom F=0, B free; no δ_Γ source
    J = |∮ F along the short path| = 0
```

J_on=0, J_off=0, ratio=0, wall site=F=0. verdict: **misses Γ**.

## 5 Group field theory

```
Needs a field on G^d (typically SU(2)^4) and a combinatorially nonlocal action. Not a 2d mesh theory. No fake holonomy.
```

J_on=nan, J_off=nan, ratio=nan, wall site=n/a. verdict: **could not define**.

## 6 Causal dynamical triangulations

```
Causal dynamical triangulations (2d strip)
    S = λ N_2, regular causal ladder (diamonds), T=8 slices
    J = number of dual edges that meet the vertical probe
    no Γ in the action
```

J_on=8, J_off=8, ratio=1, wall site=uniform ladder. verdict: **global junk**.

## 7 Euclidean dynamical triangulations

```
Euclidean dynamical triangulations (2d)
    S = λ N_2, regular triangulation of the rectangle
    J = number of edges dual-crossing the vertical probe
    no Γ in the action
```

J_on=8, J_off=8, ratio=1, wall site=uniform triangulation. verdict: **global junk**.

## 8 Causal sets

```
Causal sets
    sprinkle N=400 points in [-2,2]², Minkowski t=Im, x=Re
    link if timelike; J = number of embedded links that meet the probe
```

J_on=195.833, J_off=115.75, ratio=1.69186, wall site=mean of 12 sprinklings. verdict: **misses Γ**.

## 9 Worldsheet string

```
Worldsheet string
    S_Nambu = ∫ dλ √(ẋ²) = 2δ on both probes
    no wall weight
```

J_on=0.1, J_off=0.1, ratio=1, wall site=equal length. verdict: **global junk**.

## 10 String field theory

```
Cubic/closed SFT lives on the string Hilbert space, not on this slit mesh. No fake holonomy.
```

J_on=nan, J_off=nan, ratio=nan, wall site=n/a. verdict: **could not define**.

## 11 Supergravity / M-theory reduction

```
11d / 10d SUGRA plus compactification. No 2d-mesh reduction here without inventing a U(1) nickname.
```

J_on=nan, J_off=nan, ratio=nan, wall site=n/a. verdict: **could not define**.

## 12 AdS/CFT holographic defect

```
AdS/CFT holographic defect
    3-layer bulk ds²=dr²+(1+r)² dx²
    boundary field χ=βx, β=1/3, no slit in χ
    J=|χ(x+iδ)−χ(x−iδ)|
```

J_on=0, J_off=0, ratio=0, wall site=smooth χ=βx. verdict: **misses Γ**.

## 13 Asymptotic safety (truncation)

```
FRG in theory space (g, λ, …). No local lattice letter on γ_cross. No fake holonomy.
```

J_on=nan, J_off=nan, ratio=nan, wall site=n/a. verdict: **could not define**.

## 14 Hořava–Lifshitz

```
Anisotropic z=3 gravity on a spacetime foliation. Not defined on this 2d MHD-label mesh. No fake holonomy.
```

J_on=nan, J_off=nan, ratio=nan, wall site=n/a. verdict: **could not define**.

## 15 Twistor / ambitwistor

```
CP^3 incidence / ambitwistor string. The ε-plane is not twistor space. No fake holonomy.
```

J_on=nan, J_off=nan, ratio=nan, wall site=n/a. verdict: **could not define**.

## 16 Shape dynamics

```
Conformal 3-geometry, York time, refoliation-invariant Hamiltonian. No 3-geometry here. No fake holonomy.
```

J_on=nan, J_off=nan, ratio=nan, wall site=n/a. verdict: **could not define**.

## 17 Noncommutative geometry

```
Connes triple (A,H,D) or Moyal plane. No spectral triple for this slit without putting Γ into D by hand. No fake holonomy.
```

J_on=nan, J_off=nan, ratio=nan, wall site=n/a. verdict: **could not define**.

## 18 Teleparallel / gauge gravity

```
Teleparallel / gauge gravity
    Weitzenböck: ω=0, e^a=dx^a, torsion T=de=0
    J=|∫_γ T|
```

J_on=0, J_off=0, ratio=0, wall site=T=0. verdict: **misses Γ**.

## 19 Loop quantum cosmology letter on this slit

```
LQC is holonomy-corrected FRW (μ-bar, volume operator on a cosmological cell). This slit is not a minisuperspace. No fake holonomy.
```

J_on=nan, J_off=nan, ratio=nan, wall site=n/a. verdict: **could not define**.

## 20 Akitti hybrid (CS + holo)

```
Akitti hybrid
    J_h = hypot(J_CS, J_holo) on the same meridian
    after family 1 and family 12 already have rows
    not n_MHD
```

J_on=0, J_off=0, ratio=0, wall site=hypot(1,12). verdict: **misses Γ**.

## 21 Uniform U(1) control

```
Uniform U(1) control
    A=(−By/2, Bx/2), B=1
    J=|B x δ|  (larger off the slit)
```

J_on=0.0125, J_off=0.06, ratio=0.208333, wall site=x=0.25 vs 1.2. verdict: **global junk**.

## Table

| family | J_on | J_off | ratio | wall site | verdict |
| --- | --- | --- | --- | --- | --- |
| 1 Chern–Simons / 3d gravity | 0 | 0 | 0 | vacuum A=0 | **misses Γ** |
| 2 Ashtekar–Barbero / canonical LQG | nan | nan | nan | n/a | **could not define** |
| 3 Spin foam | 0 | 0 | 0 | flat foam | **misses Γ** |
| 4 BF theory | 0 | 0 | 0 | F=0 | **misses Γ** |
| 5 Group field theory | nan | nan | nan | n/a | **could not define** |
| 6 Causal dynamical triangulations | 8 | 8 | 1 | uniform ladder | **global junk** |
| 7 Euclidean dynamical triangulations | 8 | 8 | 1 | uniform triangulation | **global junk** |
| 8 Causal sets | 195.833 | 115.75 | 1.69186 | mean of 12 sprinklings | **misses Γ** |
| 9 Worldsheet string | 0.1 | 0.1 | 1 | equal length | **global junk** |
| 10 String field theory | nan | nan | nan | n/a | **could not define** |
| 11 Supergravity / M-theory reduction | nan | nan | nan | n/a | **could not define** |
| 12 AdS/CFT holographic defect | 0 | 0 | 0 | smooth χ=βx | **misses Γ** |
| 13 Asymptotic safety (truncation) | nan | nan | nan | n/a | **could not define** |
| 14 Hořava–Lifshitz | nan | nan | nan | n/a | **could not define** |
| 15 Twistor / ambitwistor | nan | nan | nan | n/a | **could not define** |
| 16 Shape dynamics | nan | nan | nan | n/a | **could not define** |
| 17 Noncommutative geometry | nan | nan | nan | n/a | **could not define** |
| 18 Teleparallel / gauge gravity | 0 | 0 | 0 | T=0 | **misses Γ** |
| 19 Loop quantum cosmology letter on this slit | nan | nan | nan | n/a | **could not define** |
| 20 Akitti hybrid (CS + holo) | 0 | 0 | 0 | hypot(1,12) | **misses Γ** |
| 21 Uniform U(1) control | 0.0125 | 0.06 | 0.208333 | x=0.25 vs 1.2 | **global junk** |

## One sentence

**no named theory prefers the MHD wall**

Not a theorem. No Qin, leapfrog, Hall 3×3, dynamo phenomenology.
