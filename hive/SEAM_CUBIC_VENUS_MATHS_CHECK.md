# Venus maths check of SEAM_CUBIC_FRAMEWORK.md 0c73918b (2026-11-09 20:06 UK). Framework = Akitti's idea, compiled by Grok, untested. Nothing stripped.
## Real slips
S1 (L45) "two negative eigenvalues approach and kiss, cubic forms emerge": for a gradient system (energy Hessian) a pitchfork/fold/cusp is ONE eigenvalue passing through zero, not two eigenvalues colliding. Two eigenvalues of a real symmetric Hessian generically avoid crossing (codim 2, von Neumann-Wigner) unless a symmetry protects it. Collisions that do change stability are non-gradient (Hopf, Krein). Fix: "an eigenvalue reaches zero" for the normal forms; keep "kissing" only for symmetry-protected or non-gradient cases.
S2 "cubic" is used two ways: normal-form cubic (x^3 term) vs the threefold angular ripple (L3=3, cos 3phi) seen in B. Not the same object; B's threefold minimum is not by itself evidence of a cubic collapse.
## Checked OK
- Normal forms: pitchfork x' = mu x - x^3 needs a Z2 symmetry; breaking it (unequal winding, Lorentz feedback) gives the imperfect pitchfork x' = mu x - x^3 + eps, whose generic slices are folds; the 2-parameter family is the cusp. Matches L45.
- Zero Hessian eigenvalue = signature of the bifurcation point (intermediate patch): correct for folds/pitchforks.
- Downstream lag (L37, L65): consistent with slow passage through a bifurcation (delayed bifurcation): fold lag ~ eps^(2/3), pitchfork delay of loss of stability (memory effect). Standard (Neishtadt; Haberman). A real mathematical anchor for her lag claim.
## Open / speculative (kept as hers)
- Lag "inherits the dimension of the seam"; Page-time scale; ER=EPR seam; zero modes = residual channels = folded flux being one patch.
## Testable now with our data
- The Hessian freeze HESSIAN_B_SOFTMODE_FREEZE.md 30408148 tests "zero modes = intermediate patch" on the cone (b -> 1 trend).
Open-problem check: STILL_TO_DO.md has no seam entry; normal forms and delayed bifurcation are standard (Guckenheimer-Holmes; Neishtadt 1987); d=3 jamming open (arXiv:0911.1384).
