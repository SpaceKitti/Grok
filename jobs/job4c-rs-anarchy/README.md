# Job 4c: RS flavour anarchy (Akitti's warped-throat picture)

Folder: `C:\Users\Akitt\Job4c_rs_anarchy\` (the spec gives no folder name). Files: `run.py` (the only code), `RESULTS.md` (written only by run.py, never hand-edited), this README.
This README was written before the first run. The only numbers in it are inputs, rules, and Venus's pre-registered estimate.

## Spec
- Helios's spec: `C:\Users\Akitt\open-problems\01_sm_from_sphere\JOB_4c_SPEC.md` (sha256 EAE66844), cleared by Venus. It is read-only here.
- Steering from NanoRibbon (for Akitti cat), including Venus's fixes:
  1. **Convention:** one F(c) for every field. c > 1/2 means UV-localised and light; c < 1/2 means IR-localised and heavy. This holds for Q, u and d alike. A source that flips the sign for singlets is mapped by c → −c for those singlets.
  2. **Leftover freedom:** fixed by F(c_Q3) = F(c_u3), i.e. c_Q3 = c_u3. The spec's top-mass condition is replaced, because it was redundant.
  3. **J:** J = Im(V_us V_cb V_ub* V_cs*). |J| is graded, not J, on the central 68% and 95% of log|J|. |V_ub| is graded on its own quantiles in the same way.
  4. **F(c):** coded with expm1. At c = 1/2 it uses the limit F² = 1/(kL). kL = 35 (the spec says ln(M_Pl/TeV) ≈ 35).
  5. **Stage A** has 8 free c's for 8 targets, so the fit is a solvability check, not a prediction. Its only real test is whether every c lies in ½ ± 0.5.
  6. **Stage C** reports the spread of the c's two ways: the eight light c's, and the full set including the top pair (c_Q3, c_u3).
- 4b is used read-only for the Stage C comparison: `C:\Users\Akitt\sm-yukawa-4b-ckm\RESULTS.md` (9E8D0411), Fit 1 and Fit 2, wall numbers.

## Model [standard: Gherghetta–Pomarol hep-ph/0003129; Huber–Shafi hep-ph/0010195; Agashe–Perez–Soni hep-ph/0408134]
- F(c) = sqrt((1 − 2c)/(1 − exp(−(1 − 2c)kL))), the zero-mode value at the IR brane. For c > 1/2 it is ≈ sqrt(2c − 1)·exp(−(c − 1/2)kL).
- M_u = (v/√2) F_Q Y_u F_u and M_d = (v/√2) F_Q Y_d F_d, with v = 246.22 GeV [standard]. The CKM matrix is V = U_uL† U_dL, from the left singular vectors.
- Anarchy [assumed input, fixed in advance]: each |Y_ij| is log-uniform on [1/3, 3], each phase is uniform on [0, 2π), all independent. Overall scale Y* = 1 for the graded run; Y* = 3 is a report-only row.
- Inputs [assumed input]:
  - Quark masses at μ = 1 TeV from Xing–Zhang–Zhou arXiv:0712.1419, Table IV (SM, m_H = 140 GeV), read from the arXiv PDF.
  - |V_us|, |V_cb|, |V_ub|, |V_cs| and J from PDG 2026, Eq. (12.27) and the J line after it, read from the PDG PDF.
  - CKM running up to 1 TeV is neglected [standard: weak in the SM].

## Stages and rules (fixed in run.py before the first run)
- **Seeds:** Stage A fit sample SEED_A = 40401; Stage B prediction sample SEED_B = 40402 (independent of the fit sample). 10⁴ draws each.
- **Stage A [standard]:** solve for the 8 free c's so that the medians over the Stage A sample hit the 6 masses, |V_us| and |V_cb|. Least squares in ln(median/target).
  - Solvability: all 8 medians within 10% of their targets.
  - Naturalness test [prediction]: every c in [0, 1] = ½ ± 0.5.
- **Stage B [prediction]:** freeze the c's, draw 10⁴ new (Y_u, Y_d) pairs, and record |V_ub| and |J|.
  - PASS: both measured values inside the central 68% (quantiles 0.16–0.84).
  - PARTIAL: both inside the central 95% (0.025–0.975) but not both inside 68%.
  - FAIL: either outside 95%.
  - Also reported: the fraction of draws that hit all seven of 4b's targets within 4b's ×2 band. 4b's targets are at M_Z, a scale mismatch this report flags.
- **Report-only rows:** Y* = 3 (refit, then B quantiles), and kL = ln(M_Pl/TeV) with M_Pl = 1.22 × 10¹⁹ GeV (refit, then B quantiles).
- **Stage C, report only:**
  - 4b comparison: predicted/measured for anarchy against 4b's rank-1 relation and wall numbers.
  - c spread: light 8 and full 9, against about 0.3.
  - Brockett double-bracket paragraph [hive-interpretation], with a small [computed] check that the flow keeps eigenvalues.
- run.py is run once.

## Pre-registered estimate [pre-registered estimate, Venus, /tmp/c4c.py; leading order, kL=35]
- c_Q ≈ 0.62, 0.56, 0.07
- c_u ≈ 0.69, 0.54, 0.07
- c_d ≈ 0.67, 0.62, 0.60
- spread of the light c's ≈ 0.16, full spread ≈ 0.62
- leading-order V_us·V_cb ≈ 0.0092 against measured 0.0037 (ln ≈ 0.9), with a log-spread guess of about 1 [assumed], so PARTIAL is a live outcome

run.py prints a side-by-side table of these numbers against the fitted values.

## Scope
- Zero modes only. Kaluza–Klein gluon exchange gives flavour-changing effects, and the ε_K problem pushes the KK scale to many TeV in anarchic RS [standard: beyond toy; Csáki–Falkowski–Weiler arXiv:0804.1954]. 4c does not test that.
- No running between the TeV scale and the throat, and no brane-kinetic terms.
- The Higgs sits exactly on the IR brane.

## Tags
[standard] literature or textbook input · [computed] produced by run.py · [assumed] / [assumed input] set by hand · [tuned] fitted · [prediction] stated before the run · [post-hoc] added after seeing the run · [hive-interpretation] our reading · [standard: beyond toy] literature result outside the toy · [pre-registered estimate] Venus's number before the run.

## References
- T. Gherghetta, A. Pomarol, "Bulk fields and supersymmetry in a slice of AdS", Nucl. Phys. B 586 (2000) 141, hep-ph/0003129.
- S. J. Huber, Q. Shafi, "Fermion masses, mixings and proton decay in a Randall–Sundrum model", Phys. Lett. B 498 (2001) 256, hep-ph/0010195.
- K. Agashe, G. Perez, A. Soni, "Flavor structure of warped extra dimension models", Phys. Rev. D 71 (2005) 016002, hep-ph/0408134.
- C. Csáki, A. Falkowski, A. Weiler, "The flavor of the composite pseudo-Goldstone Higgs", JHEP 0809 (2008) 008, arXiv:0804.1954.
- Z.-z. Xing, H. Zhang, S. Zhou, "Updated values of running quark and lepton masses", Phys. Rev. D 77 (2008) 113016, arXiv:0712.1419.
- Particle Data Group, Review of Particle Physics 2026, "12. CKM quark-mixing matrix" (Ceccucci, Ligeti, Sakai, revised March 2026).
- Job 4b: `C:\Users\Akitt\sm-yukawa-4b-ckm\` (RESULTS 9E8D0411).

## Post-run
Single run of run.py on TrinityOrb, run started 2026-10-02 21:31:03 BST (RESULTS header), RESULTS.md written 21:33:56 BST, runtime 173.3 s, exit 0, no crash and no rerun. Thresholds, seeds (40401 / 40402) and the c range were not changed. All numbers below are quoted from RESULTS.md (line numbers in brackets); RESULTS.md was not hand-edited.

**Grades.** Stage A: solvable (max |ln(median/target)| = 2.62e-11), naturalness PASS, all nine c's in ½ ± 0.5 [L30, L50–51]. Stage B: **PASS**. |V_ub| measured 0.003763 against the 68% band 0.00322–0.01716 (median 0.00764; 20.6% of draws below the measured value). |J| measured 3.16e-05 against the 68% band 4.581e-06–1.281e-04 (median 2.836e-05; 52.9% below) [L74–75, L82].

**Post-run comparison with Venus's pre-registered estimate** [pre-registered estimate, Venus, /tmp/c4c.py; leading order, kL=35]:
- c's (RESULTS L56–66): every fitted c lies within 0.018 of Venus's value. The largest shifts are c_Q1 (+0.0174) and c_Q2 (+0.0140), and both go upward. Fitted values: c_Q = 0.6374, 0.5740, 0.0725; c_u = 0.6955, 0.5471, 0.0725; c_d = 0.6673, 0.6255, 0.6075.
- Spread (L98): light set 0.1485 (Venus 0.16); full set 0.6231 (Venus 0.62).
- Leading-order V_us·V_cb (L52): 0.00943 against |V_ub| = 0.003763, ln ratio 0.919. Venus estimated 0.0092 and ln ≈ 0.9.
- Outcome: Venus flagged PARTIAL as a live outcome with a log-spread of about 1 [assumed]. The run gives PASS. The full-sample median sits lower than the leading-order product: median/measured is 2.031 (ln +0.709), against 2.507 at leading order [L94, L96]. The 68% band in ln(predicted/measured) runs from −0.155 to +1.517 [L96]. The measured |V_ub| is inside 68%, but near the low edge (rank 0.206 against the 0.16 edge) [L74] [post-hoc observation].

**Post-hoc notes** [post-hoc]:
- The two report-only rows (Y* = 3 and kL = 37.04) give |V_ub| and |J| quantiles identical to the graded row [L88–89]. This is expected, not a bug. The Stage B observables depend only on the F ratios within each sector, and the eight targets fix those ratios. Y* (an overall ×3 on the same draws) and kL are absorbed by refitting the c's. Only the c's move: with Y* = 3, c_Q3 = c_u3 rises to 0.357. So these rows test the c range (still all in [0, 1]), not the predictions.
- "Eight light c's" (Venus fix e) is implemented as the seven c's other than the top pair: c_Q1, c_Q2, c_u1, c_u2, c_d1, c_d2, c_d3. This set reproduces Venus's 0.16. The ninth c, c_u3, is tied to c_Q3, which leaves 8 free c's in the fit.
- Light set spread × kL = 5.20, against ln(m_c/m_u) = 6.18 and ln(m_b/m_d) = 6.88 [L98]. The rest of the hierarchy comes from the zero-mode normalisation and the Yukawa draws, not from the spread alone.
- The Brockett check [hive-interpretation] behaves as stated: eigenvalue drift 1.7e-13, final off-diagonal 3.1e-14 [L100].
- Cosmetic: `light` and `light8` in run.py are duplicates (7 distinct light c's); left as is so the graded run is unchanged.

## Sign-off
- Venus (maths): PASS (21:42 BST); typical of anarchy, not a sharp prediction
- Helios (physics): PASS as a reproduction (21:40 BST); the warped throat with O(1) random Yukawas reproduces the hierarchy with every c in range, but not the number three (an input). Soft test: the 68% bands are about ×5 wide in V_ub and ×28 in |J|. [standard: beyond toy] anarchic RS flavour problem: KK-gluon/ε_K pushes the KK scale to many TeV (Csáki–Falkowski–Weiler), untested here and the next wall if 4c is extended.