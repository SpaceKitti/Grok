# LIFT step L1: harness calibration on Euclidean Schwarzschild (GPY negative mode)

> **HARD RULE (Akitti, 22:41): the lift's gravity is quantum gravity, and it is UNKNOWN.** Here Einstein GR (Euclidean Schwarzschild) is **only a calibration/control row**: a harness check against a known limit that the unknown quantum gravity has to reproduce, or explicitly depart from. It is never the lift's gravity and never the answer. **L1 has NO gravity-independent part** (spec L16). Run alongside L1, but not part of the L1 row, is the spec's requirement-1 harness test [kinematic, no gravity theory]. It checks only that the smooth-tip checker works, on a toy metric. It does not test requirement 1 for the lift, and it unblocks nothing. **A PASS means the harness is calibrated. It does NOT mean the lift is done or unblocked.** Every GR row is tagged [standard: GR control].

Folder: `C:\Users\Akitt\open-problems\LIFT\L1\` (the spec gives no folder, so this is the default named in the job brief). Files:
- `run.py`: the whole job.
- `RESULTS.md`: written only by `run.py`.
- `README.md`: this file.

Spec: `C:\Users\Akitt\open-problems\JOB_LIFT_SPEC.md`, **SHA-256 prefix 77D663CE** (Venus passed it at 22:56; it replaces 9E2B9281). It is used for the sections "L1, first runnable step", "What this changes in the stages" (bolt rule, on-shell action, Stelle/GL item) and "Local Grok Build lift checks" (the requirement-1 harness test).
- The review it cites, `LOCAL_LIFT_CHECKS_REVIEW.md`, had SHA-256 prefix 3D9294B7 at the graded run. Venus has since passed 7F9BAA67, and run.py's expected hash is now 7F9BAA67 (see Post-run notes).
- run.py checks both hashes and stops if either does not match.
- Neither file was edited.
- No graded run was ever made against 9E2B9281. That build was replaced before any TrinityOrb run.

Run (TrinityOrb, PowerShell): `$env:PYTHONIOENCODING='utf-8'; $env:PYTHONDONTWRITEBYTECODE='1'; C:\Users\Akitt\Grok\.venv\Scripts\python.exe -B run.py`

## What run.py does
Theory of every GR row: Euclidean Einstein gravity with Λ = 0 and Q = 0, so ds² = V dτ² + dr²/V + r²dΩ², V = 1 − 2M/r, in units G = M = 1 [standard: GR control]. All modes are **real**, and counts are of real modes.

1. **GPY negative mode (spec pass (a), (b)).**
   - This is Prestidge's master ODE (4.4), with ansatz (4.1)–(4.3), written out for n = 4 Schwarzschild by sympy.
   - Bolt r₊ = 2M: the regular Frobenius series is used (roots 0 and −1). There ψ = χ, so the period is unchanged.
   - Point r_s = 3M (rV′ − 2V = 0): the roots are 0 and 3, and sympy shows there is **no log term**. So r_s is an apparent singularity, and Prestidge's (4.5) holds automatically. The integration goes round r_s on a complex semicircle, and the upper and lower detours must agree; that agreement is printed.
   - Shooting: the condition is that the coefficient of the growing e^{kr}/r² branch vanishes at R = max(40, 30/k).
   - Count: 400-point scan of M²λ ∈ [−5, −0.005], with each sign change refined by brentq.
   - Pass rule: (a) |M²λ + 0.192| ≤ 0.002 (Prestidge eq. (5.12); Reall eq. (1.7)); (b) exactly one mode.
   - Resolution checks are run on the bolt offset, R, the detour radius and the tolerance.
2. **(c) Lorentzian.**
   - The s-wave count = 0 is [identity: Birkhoff], and that is the graded (c).
   - Report-only: the Regge–Wheeler and Zerilli potentials for ℓ = 2–4 are checked to be positive outside the horizon, which means no growing mode.
3. **(d) Conformal column.**
   - The trace kinetic term has the wrong sign: yes (GHP/Prestidge split; Reall §1.3).
   - Rotated (Gibbons–Perry): yes. This is the standard GHP/Gibbons–Perry prescription, applied by hand [standard], not a computed result; "Wick artefact" in RESULTS means this prescription.
   - The lowest eigenvalue of the trace operator −∇² (s-wave, τ-independent) is computed in boxes r ≤ 20…160 M. It is positive and goes like π²/R² → 0⁺. That gives 0 negative trace modes after rotation; unrotated, the count is formally infinite.
4. **Bolt rule [standard: GR control; kinematic].**
   - κ is taken from the metric, as √V divided by the proper distance from the bolt, fitted to offset 0. Then β* = 2π/κ.
   - The check compares β* with 8πM. The cone angle and the Gauss–Bonnet sum on the cigar are evaluated for β*, 8πM and 4π.
   - The 4π period has to be flagged as a cone. The period is derived, never fixed and then checked against itself (cf. OLD_LIFT_REVIEW.md, lift-4d).
5. **Requirement 1 harness test [kinematic, no gravity theory]** (spec, "Local Grok Build lift checks"; qg-operator 09-25).
   - The same tip harness is run on the old Pair A P2 metric ds² = dε²/F + F dτ², F = ε_EP² − ε², with no field equation and no gravity theory.
   - ε_EP = 2π/12.231695, taken from the quoted smooth period [assumed]. The test is repeated at ε_EP = 0.25 and 1.
   - Both the smooth period 2π/κ and the old 4π/ε_EP are tested.
   - Gauss–Bonnet must give ∫K dA + Σ(2π − cone angle) = 2πχ with χ = 2.
   - RESULTS ends this test with one plain sentence: smooth or cone, the cone angle and the period, for both periods.
   - P2 itself is [hive-interpretation], built to match a spec. This test calibrates the smooth-tip check only.
6. **Report only.**
   - On-shell action with the GH term and flat subtraction against I = βM/2 = +A/4 = 4πM² [standard: GR control]. The −A/4 form applies to compact spaces only (Venus 22:40).
   - GL/Stelle code check: λr₊² against −0.768, and μ*r₊ = √(−λ)·r₊ against LPPS 0.876 (LPPS cited for the 0.876 only) and Reall's μ* = 0.44. The identity reasoning m₂² = −λ is Venus's. This is a code check, not evidence.

**Spec pass rule** (fixed before the run): PASS if (a), (b), (c) and (d) all hold; otherwise FAIL. That makes it a reproduction. The bolt check and the requirement-1 harness test are printed with their own PASS/FAIL lines; they are not terms in the spec's L1 formula.

## Choices and ambiguities resolved (executor)
- **Folder:** the spec names none, so I used `LIFT\L1\` as the brief said.
- **Integrating past r_s:** a complex-contour detour replaces Prestidge's series jump. That is valid because sympy shows r_s has no log term; path independence is printed.
- **Graded (c):** the spec's (c) "Lorentzian check finds no growing mode" is graded on the s-wave identity (Birkhoff), which is the GPY sector. RW/Zerilli for ℓ ≥ 2 is report-only, as the brief says.
- **Trace operator:** taken as a positive multiple of −∇² for Λ = 0 [standard; the constant was not re-derived]. The sign and the count do not depend on it.
- **Scan window:** M²λ ∈ [−5, −0.005]. A bound state shallower than −0.005 M⁻² is outside it [finite-size]. The lower end is 10× a pointwise bound estimate [assumed].
- **ε_EP** comes from the quoted period 12.231695 (spec: ε_EP ≈ 0.514). The result does not depend on ε_EP.

**Development on the box (non-graded scratch runs, disclosed).** Every scratch run used copies, never TrinityOrb.
1. The first scratch run against the box copy stopped at the hash check, because the spec had already changed to 77D663CE. Nothing was computed.
2. I rebuilt to 77D663CE and added the requirement-1 test.
3. Two scratch runs found that my first κ extraction was too inaccurate (relative error about 1e-6): the bolt check and the requirement-1 test both printed FAIL against tolerances 1e-6 and 1e-8. Cause: mainly a wrong Richardson (extrapolation) factor; the 1/√ endpoint quadrature was suspected but is not the main source (Helios could not reproduce a 1e-6 error from it; scipy's quad is accurate to about 1e-15 there). I changed the **method**: an exact factorisation F = s·G(s) at the tip, a smooth u = √s integrand, and a quadratic fit to offset 0. Both checks then pass. This is [post-hoc, during development]. **No threshold or tolerance was changed.**
4. One crash during that rework (a division by zero from round-off) was fixed.
5. A text-formatting bug in the scan sentence was fixed.
6. The plain-sentence summary of the requirement-1 result was added on request (parent, 22:55).

The P1 numbers (λ, the count) were seen in the scratch runs before the graded run, and no L1 threshold changed after that.

## Tags
Tags used: [computed] [identity] [standard] [standard: GR control] [assumed] [post-hoc] [finite-size] [hive-interpretation] [kinematic, no gravity theory]. Nothing is [tuned].

## Refs (as in the spec)
- Prestidge, PRD 61 (2000) 084002, hep-th/9907163, eqs. (3.11)–(3.12), (4.1)–(4.6), (5.12). Re-read from arXiv for this build.
- Reall, PRD 64 (2001) 044005, hep-th/0104071, §1 (eqs. (1.4)–(1.10)).
- Gross–Perry–Yaffe 1982; Gibbons–Hawking 1977; Gibbons–Hawking–Perry 1978; Gibbons–Perry 1978 (not read).
- Lü–Perkins–Pope–Stelle, PRL 114 (2015) 171601, arXiv 1502.01028 (the 0.876 only).
- OLD_LIFT_REVIEW.md and LOCAL_LIFT_CHECKS_REVIEW.md (3D9294B7 at the graded run; now 7F9BAA67, Venus PASS).

## Post-run notes
- **Graded run:** one run on TrinityOrb, 22:57:58–22:58:33 BST (RESULTS stamped 22:58:00; runtime 32 s as printed). Exit code 0. **No rerun.** run.py on TrinityOrb had SHA-256 prefix 3C2A1904, the same file as the last box scratch run. Spec 77D663CE and review 3D9294B7 matched. The 16 top-level files in open-problems\ were unchanged by the run.
- **Graded vs scratch:** RESULTS matches the last box scratch run (Python 3.13.5, numpy 2.5.3) line for line, except for the header (time and versions), the runtime, the file count (box copy 2, TrinityOrb 16), round-off in the resolution-check changes (≤ 1e-14), and one report-only line. That line is the count of eigenfunction sign changes on [r_s + ρ, 0.6R]: the scratch run gave 1 and the graded run gives 0. On [r₊, r_s − ρ] both give 0. Nothing grades this count. Checked (Helios, L1_GRADE_HELIOS.md): the sign change sits at r ≈ 36.9 M, where |χ| ≈ 8e-13 of its bolt value, so it is round-off in the growing tail; the eigenfunction has no node where it is non-negligible. M²λ agrees to all 8 printed digits.
- **Grade by the spec's rule: PASS.**
  - (a) M²λ = −0.19191426, inside −0.192 ± 0.002.
  - (b) Exactly 1 negative TT s-wave mode in [−5, −0.005].
  - (c) Lorentzian s-wave count is 0 [identity: Birkhoff]. Report-only: the RW/Zerilli potentials for ℓ = 2–4 are positive, so there is no growing mode there.
  - (d) The conformal column is separate: rotated, with 0 negative trace modes. R²·(lowest) = 8.47, 9.16, 9.51, 9.69 for R = 20–160 M, heading towards π².
  - Upper and lower detours differ by 1.3e-13.
- **Bolt check: PASS** [standard: GR control]. κ from the metric is 0.2499999999, so β* = 25.13274124 against 8πM = 25.13274123. The 4π period gives cone angle π and is flagged as a cone.
- **Requirement-1 checker calibration [kinematic, no gravity theory]: PASS** (RESULTS.md labels this "Requirement 1 harness test"; it shows the smooth-tip checker works, not that requirement 1 is met). In one sentence: with the smooth period 2π/κ = 12.231695 the tip is **smooth** (cone angle 2π, area 4π), and with the old lift's period 4π/ε_EP = 24.463390 the tip is **a cone** (cone angle 4π at each tip, area 8π), with Gauss–Bonnet balancing at χ = 2 in both cases (8π + 2(2π − 4π) = 4π), as Venus's check says. The same holds at ε_EP = 0.25 and 1.
- **Report only:**
  - On-shell action I = 12.56624 at R_b = 1e5 M, against 4πM² = 12.56637; the relative difference is −1.0e-5 and falls like M/R_b.
  - GL/Stelle code check: λr₊² = −0.767657 and μ*r₊ = 0.876160, against LPPS 0.876 (+1.8e-4).
- **What PASS means:** the harness is calibrated against the GR control, and the smooth-tip check is calibrated. **It does NOT mean the lift is done or unblocked.** L1 has no gravity-independent part, and the lift's gravity (unknown quantum gravity) is not tested here.
- Erratum (wording only, per Helios fix 3): RESULTS line "Theory of every row: Euclidean Einstein" should read "every GR row"; RESULTS left unchanged so its graded hash C89D68A2 stands.
- Erratum (wording only, per Helios fix 7): RESULTS (d) "These modes are a Wick artefact, not physical" is the standard GHP/Gibbons–Perry prescription [standard], not a computed claim; RESULTS left unchanged so its graded hash C89D68A2 stands.
- Note for L2: kappa fit offsets are fixed numbers, not scaled to the horizon; near-extremal RN reaches ~5e-7 vs the 1e-6 tolerance. Scale them for L2.
- Provenance [post-hoc, provenance only]: graded run used run.py 3C2A1904 against LOCAL_LIFT_CHECKS_REVIEW 3D9294B7 (recorded in RESULTS). Afterwards the expected review hash in run.py was updated to 7F9BAA67 (Venus PASS); that constant is the only change, and the new run.py hash is 37786C0A.
- README wording fixes per L1_GRADE_HELIOS.md (E6CDC593) fixes 1–7 and sign-offs added about 23:15 BST; no numbers changed; the only code change is the review-hash constant above.

## Sign-off
Venus (maths): PASS about 23:03 2026-10-02, GR-control calibration only; κ method change [post-hoc, development] accepted, no tolerance changed; README 3F04A909 / RESULTS C89D68A2 / run.py 3C2A1904.
Helios (physics): PASS as GR-control harness calibration only [standard: GR control]. TT Lichnerowicz operator, bolt regularity and decay independently re-derived; M²λ = −0.19191426 reproduced on the box and by an independent Chebyshev solve; κ computed from the metric (fix genuine, disclosed [post-hoc], no tolerance moved); Lorentzian 0 is [identity: Birkhoff]. Says nothing about the lift's (unknown quantum) gravity and unblocks nothing on its own. Wording fixes in L1_GRADE_HELIOS.md. 2026-10-02 ~23:10 BST.
