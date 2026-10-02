# Object C — branch-cut operator

New folder. Hive not opened. Tearing not re-tested.
Negative input: `ep-reconnection-operator/RESULTS.md` — Δ'>0 FKR, not an EP₂.
GSG 2004 is used as a 2×2 recipe, not as a dynamo.

## Matrix definitions

### Pair A — two Alfvén labels on Γ (derived, not a dynamo rename)

Generator: $A = \varepsilon x + i\eta\partial_{xx}$ on $x\in[-1,1]$ (Dirichlet).
Ideal spectrum of $\varepsilon x$ is the cut $\Gamma(\varepsilon)=[-|\varepsilon|,|\varepsilon|]$.
Two-mode Galerkin on $\varphi_n=\sin\bigl(n\pi(x+1)/2\bigr)$, $n=1,2$:

`H_A(ε) = [[ -i η(π/2)^2,  ε v ], [ ε v,  -i η π^2 ]]  with v=⟨φ1,x φ2⟩=-0.360253, η=0.05`

Explicit numbers: $v=-0.360253$, $\eta=0.05$.
Off-diagonal is Hermitian shear; diagonal is unequal Ohmic loss. Not the GSG dynamo matrix.

### Pair B — two readings of the same meridian

B1 (dissipation vs CS defect at 0): `H_B1(ε) = [[ -i η, ε ], [ -ε, 0 ]]`
B2 (GSG grading, MHD shear vs CS/Landau width): `H_B2(ε) = [[ ε, η ], [ -η, -ε ]]`

Shared parameter $\varepsilon$ = shear. $\eta$ = resistivity-as-cut-width, held fixed.

## Pair A checklist

- EP₂ found: **True** at $\varepsilon=0.5137$, $\lambda=-0.3084\,i$
- Jordan (alg 2, geom 1): **True**
- Puiseux $p=1/2$: **True** (fitted $p=0.5000$)
- 4π monodromy: **True**
- On the cut $\Gamma=[-0.5137,0.5137]$: **True** ($\mathrm{Re}\,\lambda=0$ is the midpoint of $\Gamma$; $\mathrm{Im}\,\lambda$ is the two-mode Ohmic shift)
- Unique real labeling fails for $|\varepsilon|<\varepsilon_{\mathrm{EP}}$ (complex-conjugate pair). That interval is the open cut in parameter space.
- Pair A overall: **PASS** as an MHD cut 2×2.
- N×N Alfvén generator: two least-damped modes stay gapped (min gap $0.050$). The continuum itself is still a cut, not a discrete EP₂. The operator we keep is the 2×2 label map, not a new eigenvalue of $L^2$.

## Pair B checklist

- B1 EP₂: **False** — B1: no real-ε EP2 (min|disc|=0.0025 at ε=0). Ohmic (−iη) and CS@0 miss each other on real shear; EP would need η=0 (gravity-only) or complex coupling.
- B2 EP₂: **True** at $\varepsilon=0.05$, $\lambda=(5.969091637317863e-18+0j)$; Jordan=True, Puiseux=True ($p=0.500038423801657$), 4π=True, on cut=True. Overall **PASS**.
- Same $\varepsilon$? relative distance 0.823 (A at 0.5137, B2 at 0.05). NO — not a MHD–QG theorem.

## One sentence

**one-sided**

An EP₂ lives on the MHD label/cut 2×2 (pair A) and/or on the GSG-graded slit (B2), but the two readings do not share a critical $\varepsilon$. Keep CS orthogonal to a QG claim.

No Qin. No leapfrog. No black-hole or spin-foam theorem.
