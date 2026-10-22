# IT1 grade diagnostics (rev 20, spec 22C77378)

Re-grade of saved `out/it1/*.json` only. No rows rerun. Frozen δ = 0.005 from `out/delta_frozen.json`. Output: `out/it1_grade_v2.json`.

## 1. Why `guard_pass` was false

`guard.B10.ok` and `guard.B12.ok` both pass: |meanA − meanB| is 0.116 < 0.345 (B10) and 0.142 < 0.443 (B12).

The old `guard_pass` was the AND of three things: alpha=1 A-vs-B, cal rows present, and the δ=0 control. The extra fail is **`delta0_control`**. Cal rows are present (`rel_shift` B10 0.0408, B12 0.0556).

v2 splits this: `guard_pass` is the A-vs-B test only (now true). `fail_reasons: ["delta0_control"]`. `status` stays `REPORT-ONLY (delta0_control)`.

## 2–3. `delta` and label

v2 `"delta"` is 0.005 from the freeze file. `"test"` is `IT1 (cut, rev 20)`. `IT1_DELTA` in `run.py` stays `None`.

## 4. Why the δ=0 control fails

Rule: |Δ̄_δ − Δ_0| ≤ 3 E_Δ at every α on each box. Δ_0 = drift_δ=0(α) − drift_δ=0(1). A constant-in-α perturbation would pass. Fail means the perturbation changes the α-slope of the drift.

| box | α | Δ_δ | Δ_0 | \|diff\| | bound 3E | \|diff\|/bound | |
|---|---|---|---|---|---|---|---|
| B10 | 0.9 | −0.2932 | −0.3549 | 0.0617 | 0.0400 | 1.54 | fail |
| B10 | 0.75 | −0.8180 | −0.9894 | 0.1715 | 0.1363 | 1.26 | fail |
| B10 | 0.55 | −1.9061 | −2.2661 | 0.3599 | 0.3968 | 0.91 | pass |
| B10 | 0.5 | −2.3004 | −2.7068 | 0.4064 | 0.5419 | 0.75 | pass |
| B12 | 0.9 | −0.2823 | −0.3636 | 0.0813 | 0.0400 | 2.03 | fail |
| B12 | 0.75 | −0.7781 | −1.0037 | 0.2256 | 0.1363 | 1.66 | fail |
| B12 | 0.55 | −1.7835 | −2.2636 | 0.4801 | 0.3968 | 1.21 | fail |
| B12 | 0.5 | −2.1272 | −2.6698 | 0.5426 | 0.5419 | 1.001 | fail |

|Δ_δ| < |Δ_0| at every cell: the perturbation compresses the α-dependence.

**Does the shift scale with δ? Is 0.005 too large?**

Pick rows (α=1, mean of 6 draws vs unperturbed base):

| δ | B10 Δdrift | B10 rel | B10 ρ-shift | B12 Δdrift | B12 rel | B12 ρ-shift |
|---|---|---|---|---|---|---|
| 0.005 | −0.754 | 20.2% | 0.97% | −1.025 | 23.2% | 1.30% |
| 0.01 | −2.813 | 75.6% | 4.09% | −3.787 | 85.7% | 5.27% |
| 0.02 | −8.055 | 216% | 13.5% | −10.67 | 242% | 16.8% |

Doubling 0.005 → 0.01 multiplies the drift shift by ~3.7, not 2. The response is superlinear. 0.005 already moves drift(1) by 20–23% (rev 20 smoke said 24–29%). It is the only candidate with ρ-shift ≤ 5%; 0.01 fails the pick on B12. A smaller amplitude is not on the frozen list. The control is doing what rev 20 specified: this IT1 grade is report-only.

## 5. B12 `window_flags_delta0` all true

Flag if |drift_h1 − drift_h2| > 0.20 max(|h1|, |h2|). Windows are 1.0–1.5 t_f and 1.5–2.0 t_f. Report-only.

| α | B12 h1 | B12 h2 | rel | flag | B10 h1 | B10 h2 | rel | flag |
|---|---|---|---|---|---|---|---|---|
| 1.0 | −5.021 | −3.866 | 0.230 | yes | −4.130 | −3.343 | 0.191 | no |
| 0.9 | −5.431 | −4.188 | 0.229 | yes | −4.522 | −3.663 | 0.190 | no |
| 0.75 | −6.119 | −4.783 | 0.218 | yes | −5.196 | −4.261 | 0.180 | no |
| 0.55 | −7.470 | −5.950 | 0.204 | yes | −6.531 | −5.478 | 0.161 | no |
| 0.5 | −7.916 | −6.315 | 0.202 | yes | −6.994 | −5.896 | 0.157 | no |

On B12 the later half is ~20–23% smaller in |drift| than the earlier half: the δ=0 flow is still settling through the fit window. B10 stays just under the 20% cut.
