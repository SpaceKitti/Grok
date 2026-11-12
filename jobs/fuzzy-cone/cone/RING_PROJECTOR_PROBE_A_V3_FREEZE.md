# Probe A v3 freeze (Venus, 2026-11-05 17:20 UK)
Freezes RING_PROJECTOR_PROBE_SPEC_A_V3.md 8d7f5092 with these pins (spec text unchanged):
P1 Units: primary r_peak = geodesic distance from pole / R (dimensionless). Raw core-unit value is output only.
P2 Change across N at a given b = r(81) - r(41); also report r(61). Monotone 41->61->81 required for YES.
P3 Converged = solver's frozen residual tolerance met; report residual. Non-converged -> UNDECIDED.
P4 Rank = count of projector eigenvalues > 0.5 (eigenvalues must be printed). Q_cap uses the cap radius already frozen in V2_1/ADDENDUM_B; state it in output.
P5 f per pole per solve; floor = max f over all 12 solves at that b.
P6 Interpretation: N is the only resolution on S^2_N, so YES means "ring moves with fuzz level at fixed b", not proof of a tip-specific effect; commutative-limit drift is part of it.
Grade with grade_result.py c188ec50. Cap: 1 run, no refits.
