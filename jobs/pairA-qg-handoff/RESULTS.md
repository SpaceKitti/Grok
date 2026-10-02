# Pair A QG handoff

USED HELPER: `C:\Users\Akitt\mhd-qg-cut-connection\geometry.py`

## Pair A numbers
a=0.12337  b=0.49348  v=-0.360253  η=0.05
ε_EP=0.5136806633116171  λ_EP=(-0-0.308425j)
EP check |ε v|=0.185055 vs |b-a|/2=0.185055 match=True
Dirichlet slab. Two Alfvén labels. H_A is the cut Hamiltonian.

## Triad legs and n_points
Triad = two real sheets + joining structure on Γ (not a two-arm fork).
leg plus (real sheet +): n=41
leg minus (real sheet −): n=41
leg join (complex pair on Γ, tips ±ε_EP): n=41

## r=0 bolts
ε=ε_EP cos χ. bolts χ=0 → ε=0.5136806633116171, χ=π → ε=-0.5136806633116171
period τ=4π/ε_EP=24.463390413308

## Wick/Lorentzian
real-section support = Γ
dies at ±ε_EP

## flip
2π swap, 4π return
swap_2pi=True  return_4pi=True  Jhat2^2=I=True

## φ and ||Jhat4-I||
φ=-0.7049416032418798
||Jhat4-I||_F=9.780845916487249e-16
||Jhat2@Jhat2-I||_F=8.860527786933542e-16

## J(z) n_points on Γ
n_points=21 (odd, includes 0 and both tips)
J(+ε_EP) defective=True rank=1 geom=1
J(−ε_EP) defective=True rank=1 geom=1
endpoint holonomy = Jhat2 (Layer 1 gauge)

## A/B/C scores
A real slit: Re I=0  Im I=-0.29862325  intersection=1  WRITE
B conjugate opposite sheet: Re I=0  Im I=0.29862325  intersection=1  WRITE
C imaginary cap: Re I=1.5048268e-11  Im I=-3.841677e-11  intersection=0  NOT-SELECTED

