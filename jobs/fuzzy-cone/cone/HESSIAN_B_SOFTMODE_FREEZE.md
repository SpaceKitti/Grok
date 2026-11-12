# B soft-mode Hessian diagnostic, freeze (Venus, 2026-11-09 20:05 UK). Output only, no solves, 1 run.
Inputs: saved R3 npz, S1 seed 0, N=61, b in {2, 1.2, 1.05} (3 rows). Code 63b69fbc unchanged; energy = Model.energy.
H1 Parametrisation: Hermitian X_a only (drop the unused anti-Hermitian half of A, 3N'^2 exact flat dirs), plus Phi (re, im).
H2 Gauge slice: project out span{ dX_a = i[Lam,X_a], dPhi = i Lam Phi : Lam Hermitian N'xN' }, orthonormalised numerically (report its rank).
H3 Spectrum: Lanczos (scipy eigsh, HVP via jax.jvp of grad) on the projected Hessian; lowest 40 eigenvalues; tol 1e-10.
H4 Report per row: gauge-slice rank, lowest 40 eigenvalues, n_neg (< -1e-6), n_soft (|lam| <= 1e-6), lam_min_nonzero; also overlap of soft modes with the 3 rotation generators (X_a -> eps R X + i[L'_k,X], Phi -> i(L'_k Phi - Phi L_k)).
Reading (output only, no verdict): n_soft ~ 12 above rotations = flat valley (Sym^6 S^2); n_soft = rotations only = locked minimum; n_neg > 0 = saddle; trend of lam_min_nonzero vs b is Helios's jamming-threshold question.
Open-problem check: STILL_TO_DO.md N1 negative-modes thread (no entry for this check); Hessian stability of BPS vortices is standard (Bradlow CMP 135 (1990); Garcia-Prada BLMS 26 (1994)); d=3 jamming is open (van Hecke arXiv:0911.1384) but this 2D check makes no jamming claim.
Idea owner: Akitti (jamming soft-mode criterion, posts 2119595984288116749, 2119613243593302457); diagnostic Helios + Venus, gauge slice Aethon (hive work).
Grading rule: none graded; projector rank 3/3 (G1 basis-free) re-printed per row as validity, Q_total output only.
Dimension note: 2D fuzzy S2 stepping stone; d=3/4 jamming gap noted, not tested.
