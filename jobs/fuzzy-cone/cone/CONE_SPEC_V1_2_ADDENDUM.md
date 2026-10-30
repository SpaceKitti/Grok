# CONE_SPEC_V1_2 addendum (Venus). Supersedes V1_1 92e96f63 on items 2 and 6. Everything else in V1_1 stands. Frozen before any graded run.
Blocker 4 / P2 (tip profile from her fuzzy cone):
- Tip seed: on each fuzzy-sphere shell r_j, the field is the coherent-state pole projector (seed C, width ρ0=2R/sqrt(N+1)) wound n times under θ->θ/k. The profile is whatever the shells give; no r^p is typed in anywhere. The code must contain no |n|/α or |n|k in the seed (grep check, C-8).
- Then a static relaxation on the cone (1D radial solve on its own fine grid, Δr <= w_N/10, field free between r=0 and r_c). Measure p by fitting φ ~ r^p on [2w_N, 0.5r_c].
- P2 pass: |p_fit - |n|k| <= 0.05|n|k, with p_fit changing by < 0.02|n|k when Δr is halved. Otherwise UNDECIDED.
- Smooth input is allowed only for the far field r > r_c, where the cone is pure gauge (zero field strength) by construction; the code says so in a comment.
- If the fuzzy seed won't relax onto the cone, the tip stays OPEN, and nothing is swapped for a textbook profile without Akitti's okay.
Blocker 2: the window issue is solved by the fine radial grid. r_c = 1.5ρ [hive proposal].
Blocker 3: as V1_1 item 3 (a = ρ/3, ρ/4, ρ/5 at L26, a^2 fit). L20 vs L26 is the box check only (|ΔQ| <= 0.005).
Blockers 1 and 5: P3/P5 report-only; the box tail of Q at r > r_c is reported, and graded only if it is > 0.01.
