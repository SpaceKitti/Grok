# fuzz/ — FUZZ_PLAN_V4 (cbf25723) code; also V2 239CDA17, V3 411C6529, spec 9d50c331. [hive proposal, untested]
Box build: unit tests and tiny smoke checks only. Real runs happen on TrinityOrb only, after Akitti says go.
Every value, including λ, comes from `fuzz_config_v4.json` or the command line. `fuzz_config_v2.json` is kept so `smoke_v2/` can be reproduced.
VENUS_FUZZ_CODE_CHECK.md (0451ee0c) items are dealt with below (V1–V7).

## Files
- `fuzzy_sphere.py`: spin-j matrices, X, λ_N, g, the A_k mask, the adjoint Laplacian and coherent states (spec §1, §3A).
- `ldos.py`: the **main test B observable**, the pole LDOS K_N(t;pole) compared with the classical K_∞ (V4 §3). It gives t* and w = √t*.
- `step1_paper.py`: R1–R7 from paper (4.32)–(4.35) with the p values as inputs; R8 and R9 are symbolic.
- `observables.py`: test A (code check only, V4 §2), the Berezin twist proxy (report-only code check) and D_raw.
- `grading.py`: the V4 §1 bands, grade_D (V4 §6), the ladder rules (V3 §5.4 + V4 §7) and grade_La. grade_La([]) now returns UNDECIDED.
- `run_fuzz.py`: the CLI. Each k is labelled "exact orbifold" (k=2), "NO TIP" (k=1) or "REDUCED MODEL" (any other k), following V4 §5.
- `tests/test_fuzz.py`: 28 unit tests.
- `smoke_v2/`: old smoke outputs, unchanged. `smoke_v4/`: new smoke outputs.

## TrinityOrb (PowerShell)
Copy this folder to `C:\Users\Akitt\lift\fuzz` first.
```powershell
cd C:\Users\Akitt\lift\fuzz
$env:OPENBLAS_NUM_THREADS = "1"
python -m pip install numpy scipy sympy pytest
python -m pytest -q tests
Get-FileHash .\*.py, .\fuzz_config_v4.json -Algorithm SHA256
mkdir out
python run_fuzz.py --config fuzz_config_v4.json --mode step1 --out out\step1.json
# Run step 2 only if step1_pass is true. Replace 1.0 with Akitti's λ:
python run_fuzz.py --config fuzz_config_v4.json --mode step2 --lam 1.0 --Ns 32,64,128 --ks 2 --out out\step2.json
# Ladder (V3 §5 / V4 §7). Fixed R, λ_j = a/2^j, at least 4 rungs. Replace RVAL and the λ values:
python run_fuzz.py --config fuzz_config_v4.json --mode ladder --R RVAL --lams 1,0.5,0.25,0.125 --Ns 32,64,128 --ks 2 --out out\ladder.json
```

## Venus check items: what was done
- V1: equation numbers are mapped to paper (4.32)–(4.48). R9's general form, Im p_s = p0·√(h_L/h_H), is recorded. The target (Im·√h)² = 1/2 comes from the config, as the h_L = 1/2 case. R7's 0.494 against 1/2 is reported as the paper's own mismatch.
- V2: test A is relabelled a code check (V4 §2) and is not counted as evidence.
- V3: the Berezin twist proxy is now a report-only code check. The pole LDOS is the main observable.
- V4: D_raw is graded against the per-tip value (1/12)(k − 1/k) (V4 §6).
- V5: the test B bands are now PASS [−0.6, −0.4] and FAIL outside [−0.75, −0.25] (V4 §1).
- V6: any integer N is allowed, and the h = λ/4 grid and its floor are dropped (V4 §7).
- V7: grade_La([]) no longer crashes and has a unit test. Rungs with N ≤ 20 give "no a_tip".
- Other fixes:
  - R2 and R5 now use p_L^± and p_R^± through (4.34)/(4.35) and (4.32)/(4.33).
  - R4 is now computed as (ũ − ṽ)/2 instead of echoing its target.

## Open ambiguities
- A8: the LDOS derivation is mine (Wigner–Eckart). At the pole, ⟨j j; l 0|j j⟩² = ((N−1)!)²N/((N+l)!(N−1−l)!). The tests check this against explicit matrices. Only m = 0 modes contribute.
- A9: the LDOS ratio K_N/K_∞ **does not depend on k**, because k only scales both sides. The pole LDOS therefore carries no information specific to the cone angle.
- A10: w/R from the LDOS depends only on N, not on λ. So the per-rung L-B grades in the ladder are identical on every rung, which is the same objection Venus raised against the twist proxy.
- A11: I read "first t where |K_N/K_∞ − 1| crosses 0.10" as scanning upward from the smallest t. The deviation was monotone in every smoke check.
- A12: the classical sum is cut where t·l(l+1)/R² > 50 (config `ldos_exp_cut`). The t grid t/R² ∈ [1e-5, 1] with 2001 points is set in the config.
- A13: "Berezin symbol of the Laplacian" (V4 §3, secondary) is not implemented, because Δ is a superoperator and its symbol is undefined in the spec.
- The hive tip cone angle is still NOT COMPUTED (YET).

## Reduced model
Any k ≠ 2 is labelled REDUCED MODEL in the output. The α-Gamma contrast model is a reduced model and is not implemented.
