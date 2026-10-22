# HP2 64×64 — negatives are truncation [report-only]

`run.py` 837D0BC9, spec CA9D5CBC. R=10, nev=21. Completed: n=2 κ=2 α=1 and 0.5, n=0 κ=1 α=1. Later series stopped (n=0 Lanczos).

## 1. |λ_min| 64 vs 48

h²=(48/64)²=0.5625, h⁴=0.3164.

- n=2 κ=2 **α=1** (no-cone): λ(32,48,64)=−7.344e−3, −3.440e−3, −2.022e−3. Ratio 64/48=**0.588** → h².
- n=2 κ=2 **α=0.5**: −7.995e−3, −3.633e−3, −2.086e−3. Ratio **0.574** → h².
- Same sector, second pair: −3.198e−4, −7.811e−5, −2.749e−5. Ratio 0.352 → h⁴.
- n=0 κ=1 α=1 first **positive** cluster: +9.295e−3 (32) → +1.180e−3 (64). No negative n=0 mode.

Shrinkage continues at even-powered grid rate. No finite negative continuum value.

## 2. Radial profiles

n=2 κ=2 α=1 lowest pair: r50≈1.01 (core scale, stable vs N). Tip-cell weight rings 1/3/5: 0.14/0.42/0.65 at 64 (was 0.26/0.69/0.91 at 32 — five rings cover less physical radius). Mostly |δΦ|.

n=2 κ=2 α=0.5: r50≈1.32, tip 0.09/0.27/0.46. Core-local, slightly less tip-peaked.

n=0 κ=1 α=1: 15 gauge zeros |λ|≲2e−12 (high tip weight; tip is not a lattice site). Next six modes +1.180e−3.

## 3. Continuum or vanishing?

n=2 κ=2 negatives vanish with N. Next positives in the 21-mode window also fall ~h² (0.139→0.066→0.039); this window has not sat on a massive floor. Nothing approaches a nonzero **unstable** continuum value.

## 4. Verdict

Numerical artifact, not physical instability. The α=1 control already has the same negative pair as the cone, so the deficit is not the source. |λ_min|64/48=0.588 matches h²=0.562. Modes sit in the vortex core (r50~1) and λ→0 under refinement: truncated near-zero / discrete overshoot. n=0 is a gauge kernel plus a shrinking positive cluster.

## Hive paths

`C:\Users\Akitt\Grok\jobs\cone-sims\out\hp2_check_64_nev20\` (REPORT.md, MANIFEST.md, evals/evecs npy, profiles/).

48×48: `out\hp2_check_48_nev20\`. 32×32: `out\hp2_reduced_32_nev20\`. 32 evecs: `out\hp2_iter10k\`.
