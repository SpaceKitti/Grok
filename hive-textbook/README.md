# C*Hive working textbook

A living notes book for Akitti's MHD / Navier–Stokes hive.
Written to match the code in SpaceKitti/Grok, not to replace Davidson or Acheson.

How this is used: each chapter starts from a file in `chive_ns` or `examples`,
says what the math is doing in plain language, then points at a standard
reference for the missing foundation.

## Chapter plan

0. Map of the repo (what is code vs paper notes)
1. Vectors that fluids actually use (div, curl, project onto divergence-free)
2. Navier–Stokes in the form the solver uses
3. Vorticity and why stretching is the hard term
4. Spectral methods: FFT, dealiasing, the projection in `grid.py`
5. The clay: Oldroyd-B extra-stress in `clay.py`
6. MHD: induction, Lorentz force, what Davidson covers that we don't yet
7. Dissipation floors, scars, and the BKM-type checks
8. How to tell the notes in MHD / MHD2 / MHD4 drifted from the code

## Constants in the solver right now

From `chive_ns/constants.py`:

- φ = (1 + √5) / 2
- Δ_min = 0.04116  (scar floor / hadronic gap)
- ν_gum = 1 / (φ · 7)

Default clay (`clay.py`): η_p = 0.003, λ_relax = 0.6, α = 0.085, β_scar = 0.13.

These numbers are empirical in the code. Chapters should say which of them
are math and which are knobs.

## Off-the-shelf books we borrow from

- H.M. Schey, *Div, Grad, Curl, and All That*
- D.J. Acheson, *Elementary Fluid Dynamics*
- P.A. Davidson, *An Introduction to Magnetohydrodynamics*
- L.N. Trefethen, *Spectral Methods in MATLAB*
- C.R. Doering & J.D. Gibbon, *Applied Analysis of the Navier–Stokes Equations*

Later, if the clay chapter needs it: Bird, Armstrong, Hassager,
*Dynamics of Polymeric Liquids* (Oldroyd-B).

## Rule

If a paper note in MHD4 is not used by `chive_ns`, it does not get a chapter
until the code does. The book follows the solver.
