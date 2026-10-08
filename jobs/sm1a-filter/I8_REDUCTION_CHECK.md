# I8 to I6 reduction check, both cross-term signs: REPORT-ONLY

**REPORT-ONLY. Outside the graded SM1 Part A run. Requested in Venus's grade (holes 1 and 2) on 2026-10-08. It does not change any graded output.** Written by `I8_REDUCTION_CHECK.py`, which takes run.py's own I8, I6, content and factorisation code by AST and does not import or run run.py. Run at 2026-10-08 16:17:36 GMT Summer Time on TrinityOrb, Python 3.14.7, sympy 1.14.0.

| file | graded hash | before | after |
|---|---|---|---|
| run.py | 803FD2DA | 803FD2DA | 803FD2DA |
| README.md | 12CEC48F | 12CEC48F | 12CEC48F |
| RESULTS.md | 7148A1DC | 7148A1DC | 7148A1DC |
| CANDIDATES.md | DAD867CE | DAD867CE | DAD867CE |
| OVERLAPS_ALPHA.md | D93AC9BD | D93AC9BD | D93AC9BD |
| ANOMALIES.md | B55D5D1F | B55D5D1F | B55D5D1F |

Code taken from run.py: class ConventionError@291, class NPhi@295, _CONVERT_KEY@305, N_CONVENTION@306, def convert@316, def _need@330, def count_dirac@336, def content@372, CANDS@388, t3/c3/t2/fY/fX/r2/r4/p1@1108, TR3@1109, TR2@1110, def trF@1113, def I6_poly@1129, def I8_poly@1136, I6_MONO@1145, def factorise@1161.

## What it checks

Putting the 6D anomaly polynomial on the sphere with X-flux n should give the 4D one: I6 = -n dI8/dF_X, with tr R^2 replaced by -2 p1. The sphere's own curvature drops out, because its 4-forms vanish on a 2-sphere. run.py prints I8 with the cross term -(1/96) tr R^2 tr F^2; Venus says the sign that matches I6's convention (real F) is +(1/96). This script tries both and compares each reduction with the graded I6 coefficients printed in ANOMALIES.md (and with run.py's own I6 code path, which reproduces them). The +n orientation is shown too.

## Result per candidate

| candidate | content | n | run.py I6 path = graded I6 | -(1/96), -n | +(1/96), -n | -(1/96), +n | +(1/96), +n |
|---|---|---|---|---|---|---|---|
| S1 | ALT + nu^c | 3 | YES | reproduces | reproduces | FAILS (fY^2 fX, t2 fX) | FAILS (fY^2 fX, t2 fX) |
| S2 | ALT | 3 | YES | FAILS (p1 fX) | reproduces | FAILS (fX^3, fY^2 fX, t2 fX) | FAILS (fX^3, fY^2 fX, p1 fX, t2 fX) |
| S3 | MAIN + nu^c | 3 | YES | FAILS (p1 fX) | reproduces | FAILS (fX^3, fY^2 fX, t2 fX, t3 fX) | FAILS (fX^3, fY^2 fX, p1 fX, t2 fX, t3 fX) |
| S4 | MAIN | 3 | YES | FAILS (p1 fX) | reproduces | FAILS (fX^3, fY^2 fX, t2 fX, t3 fX) | FAILS (fX^3, fY^2 fX, p1 fX, t2 fX, t3 fX) |
| S5 | S5 + nu^c | 3 | YES | FAILS (p1 fX) | reproduces | FAILS (c3, fX^3, fY^2 fX, fY^3, t2 fX, t3 fX, t3 fY) | FAILS (c3, fX^3, fY^2 fX, fY^3, p1 fX, t2 fX, t3 fX, t3 fY) |
| S6 | MAIN + nu^c | 3 | YES | FAILS (p1 fX) | reproduces | FAILS (fX^3, fY^2 fX, t2 fX, t3 fX) | FAILS (fX^3, fY^2 fX, p1 fX, t2 fX, t3 fX) |
| S7 | ALT + nu^c | 1 | YES | reproduces | reproduces | FAILS (fY^2 fX, t2 fX) | FAILS (fY^2 fX, t2 fX) |
| S8 | ALT + nu^c | 2 | YES | reproduces | reproduces | FAILS (fY^2 fX, t2 fX) | FAILS (fY^2 fX, t2 fX) |
| S9 | ALT + nu^c | 4 | YES | reproduces | reproduces | FAILS (fY^2 fX, t2 fX) | FAILS (fY^2 fX, t2 fX) |
| R1 | ALT + nu^c | 3 | YES | reproduces | reproduces | FAILS (fY^2 fX, t2 fX) | FAILS (fY^2 fX, t2 fX) |
| R2 | ALT | 3 | YES | FAILS (p1 fX) | reproduces | FAILS (fX^3, fY^2 fX, t2 fX) | FAILS (fX^3, fY^2 fX, p1 fX, t2 fX) |
| R3 | ALT + nu^c | 1 | YES | reproduces | reproduces | FAILS (fY^2 fX, t2 fX) | FAILS (fY^2 fX, t2 fX) |
| R4 | ALT + nu^c | 2 | YES | reproduces | reproduces | FAILS (fY^2 fX, t2 fX) | FAILS (fY^2 fX, t2 fX) |
| R5 | ALT + nu^c | 4 | YES | reproduces | reproduces | FAILS (fY^2 fX, t2 fX) | FAILS (fY^2 fX, t2 fX) |
| R6 | MAIN + nu^c | 3 | YES | FAILS (p1 fX) | reproduces | FAILS (fX^3, fY^2 fX, t2 fX, t3 fX) | FAILS (fX^3, fY^2 fX, p1 fX, t2 fX, t3 fX) |

With the -n orientation, +(1/96) reproduces the graded I6 for every candidate: YES. -(1/96) fails for: S2, S3, S4, S5, S6, R2, R6.

## Cross-term terms of I8 per content, both signs

### ALT content + nu^c

- graded I8 (ANOMALIES line 280) reproduced by run.py's I8_poly: YES
- terms linear in r2, as printed (-1/96): -fY**2*r2/48 + r2*t2/24
- terms linear in r2, corrected (+1/96): fY**2*r2/48 - r2*t2/24
- corrected I8 (+1/96): fX**2*fY**2/2 - fX**2*t2 + fY**4/16 + fY**2*r2/48 - fY**2*t2/12 + fY**2*t3/8 - r2*t2/24 - t2**2/12 - t2*t3/4
- factorisation as printed (ANOMALIES line 283) reproduced: YES
- factorisation, corrected (+1/96): factorises over Q (rank 2): I8 = -(-fY**2 + 2*t2)*(24*fX**2 + 3*fY**2 + r2 + 2*t2 + 6*t3)/48
- factorises yes/no: printed sign yes, corrected sign yes, unchanged: YES

### ALT content without nu^c

- graded I8 (ANOMALIES line 287) reproduced by run.py's I8_poly: YES
- terms linear in r2, as printed (-1/96): fX**2*r2/96 - fY**2*r2/48 + r2*t2/24
- terms linear in r2, corrected (+1/96): -fX**2*r2/96 + fY**2*r2/48 - r2*t2/24
- corrected I8 (+1/96): -fX**4/24 + fX**2*fY**2/2 - fX**2*r2/96 - fX**2*t2 + fY**4/16 + fY**2*r2/48 - fY**2*t2/12 + fY**2*t3/8 - r2**2/4608 - r2*t2/24 - r4/5760 - t2**2/12 - t2*t3/4
- factorisation as printed (ANOMALIES line 290) reproduced: YES
- factorisation, corrected (+1/96): irreducible tr R^4 left over: no factorisation (Q16 reject at Part B's consistency gate)
- factorises yes/no: printed sign no, corrected sign no, unchanged: YES

### MAIN content + nu^c

- graded I8 (ANOMALIES line 294) reproduced by run.py's I8_poly: YES
- terms linear in r2, as printed (-1/96): fX**2*r2/6 + 5*fY**2*r2/144 + r2*t2/24 + r2*t3/24
- terms linear in r2, corrected (+1/96): -fX**2*r2/6 - 5*fY**2*r2/144 - r2*t2/24 - r2*t3/24
- corrected I8 (+1/96): -c3*fY/9 - 2*fX**4/3 - 5*fX**2*fY**2/6 - fX**2*r2/6 - fX**2*t2 - fX**2*t3 - 95*fY**4/1296 - 5*fY**2*r2/144 - fY**2*t2/12 - 11*fY**2*t3/72 - r2**2/288 - r2*t2/24 - r2*t3/24 - r4/360 - t2**2/12 - t2*t3/4 - t3**2/12
- factorisation as printed (ANOMALIES line 297) reproduced: YES
- factorisation, corrected (+1/96): irreducible tr R^4 left over: no factorisation (Q16 reject at Part B's consistency gate)
- factorises yes/no: printed sign no, corrected sign no, unchanged: YES

### MAIN content without nu^c

- graded I8 (ANOMALIES line 301) reproduced by run.py's I8_poly: YES
- terms linear in r2, as printed (-1/96): 5*fX**2*r2/32 + 5*fY**2*r2/144 + r2*t2/24 + r2*t3/24
- terms linear in r2, corrected (+1/96): -5*fX**2*r2/32 - 5*fY**2*r2/144 - r2*t2/24 - r2*t3/24
- corrected I8 (+1/96): -c3*fY/9 - 5*fX**4/8 - 5*fX**2*fY**2/6 - 5*fX**2*r2/32 - fX**2*t2 - fX**2*t3 - 95*fY**4/1296 - 5*fY**2*r2/144 - fY**2*t2/12 - 11*fY**2*t3/72 - 5*r2**2/1536 - r2*t2/24 - r2*t3/24 - r4/384 - t2**2/12 - t2*t3/4 - t3**2/12
- factorisation as printed (ANOMALIES line 304) reproduced: YES
- factorisation, corrected (+1/96): irreducible tr R^4 left over: no factorisation (Q16 reject at Part B's consistency gate)
- factorises yes/no: printed sign no, corrected sign no, unchanged: YES

### S5 content + nu^c

- graded I8 (ANOMALIES line 308) reproduced by run.py's I8_poly: YES
- terms linear in r2, as printed (-1/96): fX**2*r2/6 + 5*fY**2*r2/144 + r2*t2/24 + r2*t3/24
- terms linear in r2, corrected (+1/96): -fX**2*r2/6 - 5*fY**2*r2/144 - r2*t2/24 - r2*t3/24
- corrected I8 (+1/96): -2*c3*fX/3 - c3*fY/9 - 2*fX**4/3 - 5*fX**2*fY**2/6 - fX**2*r2/6 - fX**2*t2 - fX**2*t3 + 2*fX*fY**3/27 - fX*fY*t3/3 - 95*fY**4/1296 - 5*fY**2*r2/144 - fY**2*t2/12 - 11*fY**2*t3/72 - r2**2/288 - r2*t2/24 - r2*t3/24 - r4/360 - t2**2/12 - t2*t3/4 - t3**2/12
- factorisation as printed (ANOMALIES line 311) reproduced: YES
- factorisation, corrected (+1/96): irreducible tr R^4 left over: no factorisation (Q16 reject at Part B's consistency gate)
- factorises yes/no: printed sign no, corrected sign no, unchanged: YES

tr R^4 terms do not involve the cross term, so the tr R^4 nets are unchanged; I6 and A-a/A-b are unchanged.

