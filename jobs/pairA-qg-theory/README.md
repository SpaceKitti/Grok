# pairA-qg-theory: layered QG-theory audit on Pair A / R1

**Signed off 2026-09-25:** Venus (maths) and Helios (physics).

Question: how much of a quantum-gravity theory stack (L1–L6) can be built on the Pair A surface and the R1 geometry? Each layer is graded strictly as HAVE / PARTIAL / MISSING, using criteria written here **before running** and not changed afterwards.

Run: `python run.py` (Grok\.venv python, PYTHONIOENCODING=utf-8). It writes RESULTS.md and then stops.

No claim that QG is solved, no JT dual, no Einstein solution derived from Pair A. Ordinary S² (no GoldbergHexa). A and B WRITE, C held.

## Inputs (read-only, SHA-256 of every file before and after)
- `pairA-qg-handoff`: `seed.py` gives the numbers a, b, v and H_A. H_A is used **only** as the comparison target in L1 and never inside the L3 dynamics.
  - a = 0.12337 and b = 0.49348 are the constants on H_A's diagonal: H_A(ε) = [[−i a, v ε], [v ε, −i b]]. They are the damping (loss) rates of the two uncoupled modes, with v = −0.360253 the coupling per unit ε.
  - This follows from the matrix itself. The handoff gives no other physical name for them (RESULTS.md lists "a=0.12337 b=0.49348 v=-0.360253").
  - Consequences: λ_EP = −i(a+b)/2 = −0.308425 i, ε_EP = |b−a|/(2|v|) = 0.51368066, and y² = 4v²ε² − (a−b)² = 4v²(ε² − ε_EP²) [identity].
  - The constants a, b are not the sheet labels A, B.
- `pairA-qg-probe-surface`: D1–D7 rows, SURFACE READY.
- `pairA-jt-4d`: R1 = AdS₂×S², r = ε_EP, F_JT = ε² − ε_EP², Λ and E² as stated there. `lift4d.scalar_curvature` is imported for the 2D curvature.
- `pairA-qg-on-R1`: Z toy with S = ∮λ dε; D3 and D4 PASS.
- `pairA-drive-return`: the D6/D7 driven-loop weights (outputs/drive.npz, drive_start1p25.npz), used for the L3 cross-check.
- `pairA-drive-sweep` (present): 0.75 ε_EP weights, used for the P-rate comparison.

## Files
- `H_QG.py`: L1, routes (a) and (b).
- `action_R1.py`: L2, reduced action on R1.
- `loss_qg.py`: L3, in-folder drive.
- `hilbert.py`: L4.
- `predict.py`: L5.
- `r_from_action.py`: L6.
- `run.py`: runs everything and writes RESULTS.md.

## Grading criteria (fixed before running)

**L1: gravity Hamiltonian.** Spectrum match is measured as the max |eigenvalue error| of H_QG vs H_A on a complex ε grid (−3…3 ε_EP × −1…1 ε_EP, avoiding the EPs by more than 1e-6).
- HAVE: all of the following for at least one route:
  - max error ≤ 1e-8;
  - EPs at ±ε_EP;
  - λ_EP shift;
  - 2π swap / 4π return at both tips (continuation);
  - the route is not reducible to H_A, meaning it is neither H_A literally nor an ε-independent similarity transform of H_A (tested numerically).
- PARTIAL: the spectrum matches but every route is reducible to H_A; or the error is > 1e-8.
- MISSING: no operator written.

**L2: action on R1.**
- HAVE: all of the following:
  - S_R1 written with a source;
  - R1 stationary for it (reduced field-equation residual ≤ 1e-10);
  - the Γ crossing of an EP loop printed;
  - the restricted action on the Euclidean piece computed;
  - S_R1 on the Euclidean piece [ε_EP, b] equals c·S1(b) + k with c ≠ 0, k fixed (least-squares residual ≤ 1e-8 over base points b = 1.10, 1.25, 1.50, 2.00 ε_EP), where S1(b) is the once-around ∮λ dε from base b.
- PARTIAL: S_R1 written and R1 stationary, but no such constant relation. In that case ∮λ dε stays a choice.
- MISSING: no S_R1.

**L3: dissipation on the gravity side.** Winner-level classification over γT = 20, 40, 100, 2π and 4π, ccw and cw, start sheets A and B, with loop r = 0.25 ε_EP around +ε_EP (drive-return convention).
- D6-like (0.75 ε_EP start): ccw = cw winner for both start sheets, and the winner does not depend on the start sheet.
- D7-like (1.25 ε_EP start): ccw ≠ cw for both start sheets, and each direction's winner does not depend on the start sheet.
- HAVE: D6-like at 0.75, D7-like at 1.25, **and** a loss term with a gravity-side origin that is independent of H_A.
- PARTIAL: reproduced, but the loss term is H_A's (the line 'L3 = H_A embedded in H_QG (honest)' is printed); or an independent loss that fails to reproduce.
- MISSING: not reproduced and no loss term.
- Cross-check against drive-return: max |Δw|, reported.

**L4: Hilbert space / measure.**
- HAVE: all of the following:
  - a fiber together with a measure on ε-space, sourced, with tip behaviour stated;
  - an inner product well defined everywhere, including the tips;
  - H_QG acting on the ε direction (not only as a parameter);
  - normalizable states.
- PARTIAL: a fiber and a measure, but ε is only a parameter, or the inner product fails at the tips, or states are not normalizable.
- 'PARTIAL — fiber only': only 2 states in total.
- MISSING: no space defined.

**L5: predictions not fitted.** Each item is tagged PREDICTED / FITTED / [by construction/identity]. A **genuine PREDICTED** item must meet all of the following:
- not fitted;
- not an identity or a direct consequence of the inputs or construction;
- compared with an independent computation, agreeing within a tolerance stated here in advance.

P-adiab tolerance: the fitted exponent p of (1 − w) ∝ (γT)^p at the 1.25 ε_EP start, from γT = 100 and 200, must satisfy |p − (−2)| ≤ 0.3.
- HAVE: ≥ 2 genuine PREDICTED.
- PARTIAL: fewer than 2.
- MISSING: none computed.

**L6: r(ε) from the action.**
- HAVE (DERIVED): the r-equation of S_R1 fixes r = ε_EP without ε_EP entering through the couplings.
- PARTIAL: 'CONSISTENT (circular: couplings chosen from ε_EP)'.
- MISSING: S_R1 has no r-equation; r = ε_EP stays as the working chart.

**Final lines:** 'THEORY STACK: <HAVE layers>' and 'NOT A FULL QG THEORY UNLESS L1 L2 L3 L4 are HAVE'.
