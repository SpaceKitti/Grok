# Job 5b — rugby-ball tension and Casimir radion filter

Folder: `C:\Users\Akitt\radion-5b-tension-casimir\` on TrinityOrb. This is a new folder built from the Job Five radion reduction; Job Five and Job Three are read-only inputs. No git.

Run with UTF-8 and the specified interpreter:

```powershell
$env:PYTHONIOENCODING='utf-8'; C:\Users\Akitt\Grok\.venv\Scripts\python.exe -B run.py
```

`run.py` writes `RESULTS.md` and never hand-edits it. The code fixes the scan ranges, Casimir grid, and PASS thresholds before the first run. Output tags distinguish `[computed]`, `[identity]`, `[assumed input]`, `[standard]`, `[tuned]`, `[prediction]`, `[hive-interpretation]`, and `[standard: beyond toy]`.

## Scope and conventions

- Unit normalisation is `s = 1`; the inherited Job Five dS window `0.739 ≤ s ≤ 0.957` is printed beside the result.
- The filter variable is `p = (B²/2)/(B²/2 + Λ₆)`. The comparison is explicitly against Job Three's `n = 3` bands, not the band for `n_e = n/α`.
- Part T uses `V_J,α(x;n) = α V_J,1(x;n/α)` for the rugby-ball tension identity. The primary Einstein-frame convention keeps the round-sphere Weyl factor, giving prefactor `α`; the alternate fixed-physical-`M₄²` convention gives `1/α`. Both are positive and preserve stationary points, signs, barriers, and `p`; only `|V|` and `m²_radion` change.
- Part C adds `C/x⁴` and compares `C` with `N/(4π)³`. Only the breathing mode is varied; this is not a complete compactification.

## References and caveats [standard: beyond toy]

- Carroll–Guica, hep-th/0302067: rugby-ball curvature/tension cancellation.
- Candelas–Weinberg (1984) and Ponton–Poppitz, hep-ph/0105021: Casimir stabilisation context.
- Tunnelling caveats: arXiv:0904.3106 and arXiv:0912.4082.
- ABPQ, hep-th/0304256, for the broader compactification/phenomenology context.

These references motivate the toy calculation; they do not make its filter or truncation a theorem. Tunnelling, extra moduli, backreaction, flux quantisation, and the full KK spectrum are outside this job.

## Post-run

`RESULTS.md` records the computed Part T table, both radion-mass conventions, every Part C grid point, naturalness ratios, the 5%-of-Λ₆-range grade rule, inherited Job Three band hashes, and the read-only source audit. The signed interpretation is: α < 1 is expected to miss both n = 3 bands; any overlap from α > 1 is negative tension and unphysical.

Final Post-run (2026-10-02 19:35 BST): Part T PARTIAL for physical alpha<=1 (dS/barriers exist but p misses both n=3 bands; alpha=1.5 overlap is negative-tension), Part C PASS at 7.1% Lambda6 span. The large-C overlap is flagged by the naturalness column.

## Post-run follow-up (2026-10-02 19:37 BST)

- Part K [computed]: fixed `C` breaks the Job 5c k-family degeneracy, so Part C is the first ingredient in this project that sees `n`; the restoring control is `C → k⁴C` (for the absolute `n=k` table relative to `n=3`, `C → C·(k/3)⁴`) and matches to machine precision. The literal `C/k⁴` row is retained as a breaks-more illustration.
- Part T needs no k-check: tension only relabels the flux, `V_α(x;n) = αV₁(x;n/α)` [identity].
- The main filter variable is `p_flux = (B²/2)/(B²/2 + Λ₆)`, with Casimir energy outside the denominator [identity]. A separate `p_with_C` variant includes `C/x⁴` [assumed input]; because Casimir energy can be negative, that denominator can approach or cross zero.
- The old 2-point/0.02-grid figure is retained as `[grid-step]`. Root-finding gives the C = −3 qualifying interval `0.259397739–0.283356695`, or 8.557% of the scanned Λ₆ range. The fine C scan finds smallest qualifying `|C| = 1`, with `|C|/C_nat ≈ 1.984×10³` for N = 1.
- Therefore the Part C PASS requires `|C|` about 10³–10⁴ times natural for N = 1 [tuned], unless N is comparably large: N ≈ 1,984 for `|C|=1`, or N ≈ 5,953 for `|C|=3`.
- Final follow-up grade: Part T PARTIAL (physical α≤1 misses both bands); Part C PASS. Fixed-C breaking strength decreases with n as the printed ε_C check shows [computed].
- The Casimir scan uses numerical cubic roots when C is on; the C = 0 reference is the closed-form 5c check [identity].

## Post-run grader fold-in (2026-10-02 19:49 BST)

- Helios relabelled Part C from PASS to PARTIAL [tuned]: the 5% coverage threshold is unchanged and the interval passes it, but the successful `|C|/C_nat ≈ 2×10³` for N=1 is unnatural. This is a physics-grader relabel, not a threshold change; about 2,000 light fields would be needed to make it natural, a huge hidden sector.
- One-universe selection at fixed `(Λ₆,C)` found only `n=3` surviving at the lower edge, midpoint, and upper edge; no re-grade flag was triggered. Part K remains the first n-sensitive ingredient [computed].
- The C<0 collapse channel is physical: `V→−∞` as `x→0`. At the qualifying points the decompactification/out barrier is lower than the collapse/in barrier, so it controls the tunnelling caveat.
- Scope [standard: beyond toy]: the toy freezes the dilaton that SLED models carry, so this result covers the radius direction only; it does not analyze the coupled dilaton/collapse dynamics.
- Final overall line: Part T PARTIAL, Part C PARTIAL [tuned], Part K first n-sensitive ingredient [computed].
