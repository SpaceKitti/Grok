N=128  η=0.05  ε’s=87  n_arm=74  n_ep=10  n_junc=0  R_pair=0.5438
selection: two lowest-damped non-spurious modes per ε, matched in ε; n_selected/n_total=174/11136; drop highly damped Dirichlet tail n_bar>2N/3; keep thin locus of that pair (off ideal Γ=[-|ε|,|ε|] in the sense Im<0 resistive)
verdict C  UNDERPOWERED
4d metric / JT dual: NOT IN THIS FOLDER

# Alfvén fork measure

Dirichlet slab. Alfvén only. Not tearing. Dewar A.1 stubbed.

## N=2 check
a=0.12337 b=0.49348 v=-0.360253  max abs err vs pair_A refs = 2.201e-07  PASS

## A.2 operator
A = ε x + i η ∂_xx on [-1,1], Dirichlet.
Square Galerkin in φ_n=sin(nπ(x+1)/2), n=1..N. M=I, ∂_xx diagonal.
Rectangular (N+3)×N: not used (no larger basis to truncate).
N=128. η=0.05. ε grid includes [0.2, 0.35, 0.45, 0.513681, 0.6, 0.8, 1.0].
A.1 Dewar: STUB=True. No Dewar scalar operator file in this folder. A.1 not run.

## Fork selection
Track two lowest-damped (largest Im) non-spurious eigenvalues vs ε, nearest-neighbour matched. Isolated highly damped Dirichlet modes dropped (n_bar>2N/3). has_fork=True (max Re split=0.5438).

## Regions
data-driven ε★=0.62, z_EP=(-4.551914400963142e-15-0.3561034554062976j), min_gap=0.04583.
EP window = contiguous un-opened block around min-gap (not gated on Pair A λ_EP).
mid-arm = opened 1-D loci L/R in Re.
No third prong allowed. Junction is leftover of the two tracked branches only; empty of an extra prong.
n_arm=74 n_ep=10 n_junc=0 (junction leftover points=0).

## Unfold / diagnostics
mid-arm: spline polyline → arc length ℓ; N_bar from 1-D KDE ρ≥0 (monotone). s=ΔN_bar, ⟨s⟩=1.
No global polynomial. No |z-z_NN|√ρ. CSR not applied (thin arms).
EP: Airy zoom ζ∝(z-z_EP)^{2/3} is a microscope, not arm unfolding. No default AI†/AII†.
arm L: n_sp=36 class=rigid-track KS_GUE=0.386 KS_Pois=0.455 ⟨r⟩=0.976
arm R: n_sp=36 class=rigid-track KS_GUE=0.386 KS_Pois=0.455 ⟨r⟩=0.976
EP: n=10 kind=UNDERPOWERED gap_p=0.522 (√ germ ~ 0.5; not defaulted to Airy)
algebraic residual max=1.878e-11 (Galerkin eigenpairs).

## Verdict
**C**  UNDERPOWERED
arms are a rigid 1-D ε-track (⟨r⟩→1), not GUE; EP window underpowered. Local 2×2 germ at most
Never: we found QG. Never: JT is dual.
4d metric / JT dual: NOT IN THIS FOLDER
