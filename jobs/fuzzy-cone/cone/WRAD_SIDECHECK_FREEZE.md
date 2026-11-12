# wrad side-check freeze (Venus, 2026-11-05 18:46 UK)
Side diagnostic, no verdict changes (Probe A BROKEN, round-2 UNDECIDED, Probe B BROKEN stand).
Runs: b=2, n=2, N in {41,61,81}, wrad=1e4, round-2 solver settings, seed_fuzzy(). 3 solves, once. Print nit, residual, Tr B_d, 2TrB_d/N', |Q-4|, max| |x_hat|^2 - 1 |.
Rule: compare to round-2 rows (wrad=1e3). SOFT-CONSTRAINT if |Q-4| falls by >=5x at all three N. NOT-WRAD if it falls by <2x at all three. UNDECIDED otherwise or if any solve diverges.
Also required: 2TrB_d/N' must equal Q_total-4 to 1e-10 in every row (identity check).
