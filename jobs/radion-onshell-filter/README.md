# Job Five: radion on-shell Betti filter

This folder is a new, standalone Job Five output. `RESULTS.md` is generated only by `run.py`; no git operations are used.

## Specification summary

- 6D Einstein–Maxwell on a round S², retaining only the breathing mode R [standard].
- With x=R² and the stated reduction convention, `V(x)=a Lambda_6/x - b/x² + c n²/x³`, with symbolic `a,b,c` printed in RESULTS.md [computed; assumed input symbols].
- Stage B checks positive-, zero- and negative-Lambda root rules, the tuned flat case, AdS/dS signs, barriers and the canonically normalised radion mass.
- Stage C applies the Job Three default window 0.010–0.030 to on-shell points only, using the inherited m=16 rho table as a lightweight interpolation [post-hoc]. The R-unit normalisation is explicitly assumed and scanned.

## Caveats

Only the breathing mode is included. Shape modes, flux tunnelling n→n−1, one-loop/Casimir radion terms and Job Four brane tension are omitted [assumed input]. “Stable” means classically stable in R only [standard]. The on-shell R normalisation and the n/(3R²) occupancy bridge are [assumed input]; any selection dependence is [prediction]/[post-hoc], not a derivation.

Job Three and Job Two are read-only inputs. The source audit and hashes are printed in RESULTS.md. No Orion X files or Job Two files are modified.

## References

- Sean M. Carroll, James Geddes, Mark B. Hoffman and Robert M. Wald, “Classical Stabilization of Homogeneous Extra Dimensions,” Physical Review D 66, 024036 (2002), arXiv:hep-th/0110149 [standard].
- Jose J. Blanco-Pillado, Delia Schwartz-Perlov and Alexander Vilenkin, “Quantum Tunneling in Flux Compactifications,” Journal of Cosmology and Astroparticle Physics 2009(12), 006, arXiv:0904.3106 [standard].
- arXiv:0912.4082 for the barrier/decompactification caveat.
- Randjbar-Daemi, Salam and Strathdee, Nuclear Physics B 214 (1983) 491.

Post-run (2026-10-02): [post-hoc] Job Five created as a new folder; source Job Three and Job Two trees are read-only and audited by hash.

Post-run (2026-10-02): NanoRibbon approved Job Five with Akitti's go; Stage A/B are maths-checked and Stage C is an explicitly [post-hoc] lightweight bridge.

Post-run (2026-10-02): [computed] Added exact n=3 Lambda_6 survival windows, dS-gap check, both radion-mass conventions, and normalisation-dependent band edges.
Post-run (2026-10-02): [hive-interpretation] At unit normalisation, three generations and positive vacuum energy cannot both hold in this toy; for roughly 0.739 ≤ s ≤ 0.957 an n = 3 dS survivor exists [assumed input: normalisation], so the n = 3 hit reflects input choices, not selection. The survivor sits about 0.5% in R from its band edge (about 1% in p, 9.4% in Λ6).
Post-run (2026-10-02): [assumed input] An uplift such as Job Four brane tension or a one-loop Casimir term remains an open route to close the dS gap.
Signed off 2026-10-02: Venus PASS (maths); Helios PASS (physics, toy), PARTIAL on selection.
Post-run (2026-10-02): [computed] Wording correction: the ~0.5% statement refers to the p-coordinate gap (about 0.005, about 1%), not the 9.4% Λ6 distance; scale 0.95 to 1.15 swings the main Λ6 window from positive to negative.
Post-run (2026-10-02): [computed] Corrected the dS wording: no n=3 survivor is dS at unit normalisation; for roughly 0.74 ≲ s ≲ 0.957 a dS survivor exists [assumed input: normalisation].
