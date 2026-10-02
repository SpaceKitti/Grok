# Review: the earlier lift work in SpaceKitti/Grok `jobs/` (read-only)

Helios, 2026-10-02 about 22:45 BST, for NanoRibbon. Source: a read-only sparse clone of SpaceKitti/Grok, main at commit 07c9d97 (22:19 BST), in `/workspace/oldlift/`. Nothing was written to the repo. Paths below are relative to `jobs/`; "L" = line number in that file.

**Dates.** Git can't date these jobs. All eight folders arrived in one "backlog push" on 2 Oct, 15:27 BST (commits 74d015a, 7cb73e1, f4b0073, e1cdd5f, 0fb663c, f0f15ad, 222ee52, 513f610). The dates written inside the files:
- jt-4d, qg-theory, qg-on-R1: "Signed off 2026-09-25: Venus (maths) and Helios (physics)" (README/RESULTS L3).
- qg-radial: "Signed off 2026-09-26" (RESULTS L3).
- handoff, lift-4d, lift-ode, mhd-qg-cut-connection: no date and no sign-off line.
- The order below is inferred from which folder loads which (e.g. `pairA-qg-lift-4d/load_surface.py` L9 loads the handoff's `Jhat.npz`). It is not a recorded date.

## 1. What the old plan was

**The starting object is not gravity.** Every job is built on "Pair A". That is a 2×2 non-Hermitian matrix, H_A(ε) = [[−ia, εv], [εv, −ib]], from a resistive MHD slab (`pairA-qg-handoff/seed.py` L7–21; `mhd-qg-cut-connection/RESULTS.md` L18–28).
- Its two eigenvalues meet at an exceptional point, ε_EP ≈ 0.5137.
- That number is fixed only by the box: ε_EP = 27π⁴/5120 from η = 0.05 and L = 2 (`pairA-qg-radial/RESULTS.md` L226–227, "confirmed by Akitti 2026-09-26").
- ε is "a dimensionless drive parameter" (`pairA-qg-radial/RESULTS.md` L9).

**The goal:** read the two eigenvalue sheets and their branch cut Γ = [−ε_EP, ε_EP] as a geometry, then "lift" it to a 4D metric. The tips ±ε_EP play the role of the "r = 0 bolts", where "the real section dies" (`pairA-qg-handoff/RESULTS.md` L17–23).

**The route, in stages:**
1. **Handoff** (`pairA-qg-handoff`). It names the tips "r = 0 bolts" with ε = ε_EP cos χ and a Euclidean period τ = 4π/ε_EP (RESULTS L17–19; `r0_bolts.py` L12–15). The "Wick/Lorentzian" real section is Γ, and it "dies at ±ε_EP" (L21–23). Histories A and B are scored WRITE and the imaginary cap C NOT-SELECTED (L40–43). The probes PASS (`RESULTS_probe.md`).
2. **Lift to a 4D chart** (`pairA-qg-lift-4d`). It writes F = ε_EP² − ε² with two charts: R1 (r = ε_EP, a product) and R2 (r = ε_EP sin χ, round) (`lift_metric.py` L10–25). It ends with "next is the ODE for r(ε) if you want a solved 4d metric" (RESULTS L21).
3. **Radial ODE** (`pairA-qg-lift-ode`). It solves for r(χ) from Euclidean Einstein + Λ, with a = ε_EP sin χ held fixed (`ode_r.py` L1–18).
4. **JT / AdS₂ rebuild** (`pairA-jt-4d`, signed off 09-25). It flips to F_JT = ε² − ε_EP², the AdS₂ sign (README L3; RESULTS L17). The 4D target becomes **R1 = AdS₂ × S², r = ε_EP**, and R2 is dropped ("R2 is not a target", RESULTS L14).
5. **Path-integral probe on R1** (`pairA-qg-on-R1`, 09-25). A "Z" summed over chosen closed contours in complex ε, with action ∮λ dε.
6. **Theory audit** (`pairA-qg-theory`, 09-25). Six layers (Hamiltonian, action, dissipation, Hilbert space, predictions, r from the action), graded against rules fixed before running.
7. **Radial firewall** (`pairA-qg-radial`, 09-26). Does any standard gravity family put a root at ε_EP with no Pair A input?
8. Side job: **mhd-qg-cut-connection**. It defines a "gravity letter" (a π-flux Z₂ holonomy on Γ) and tests what it shares with the MHD matrix.

## 2. How far it got (verdicts as written)

| Job | Verdict as written | Actually computed | Only planned or assumed |
|---|---|---|---|
| handoff | Probes 1 and 3 **PASS**; A, B "WRITE", C "NOT-SELECTED" (`RESULTS.md` L40–43; `RESULTS_probe.md` L5–6, L14) | Eigenvalues of H_A; branch tracking; the period integrals I_A = −I_B = −0.2986i; the 2π swap / 4π return (L25–32) | The WRITE / NOT-SELECTED labels are hard-coded: "Score rule: A WRITE; B conjugate of A WRITE; C NOT-SELECTED if ∩=0" (`histories.py` L52–56). The "analytic" line ends in a stray "wait" (`histories.py` L57). The "r = 0" and "Wick/Lorentzian" names are labels on the ε-plane. |
| lift-4d | "R1 bolt PASS", "R2 bolt PASS", "4π-cover PASS, 2π-polar FAIL" (`RESULTS.md` L14–16) | F(±ε_EP) = 0; the product ε_EP·τ = 4π | Both bolt PASSes are copies of one test, `r1_pass = reg["bolt_PASS"]`, `r2_pass = reg["bolt_PASS"]` (`bolts.py` L25–26). That test checks ε_EP·τ = 4π (`lift_metric.py` L35–43) for τ already defined as 4π/ε_EP (`load_surface.py` L16). So it is **circular**. No field equation is solved. |
| lift-ode | No verdict line. It lists "Numeric profiles regular at both bolts: r0 = 0.3, 0.5137, 0.7, 1" (`RESULTS.md` L14–18). Both seeds "Λ if solved: none" (L11–12) | Integration of r r″ − cot χ r r′ + r′² + r² − 1 = 0 (`ode_r.py` L10–13) | "Regular" means |r′(π)| < 0.05 (`run.py` L29). The profiles were never checked against constant Λ. See §4. |
| jt-4d | M1–M5 all **PASS**; "regions match NO" for the D6/D7 map (RESULTS L89–93, L109). Signed off | Curvatures by sympy; cone angles; Gauss–Bonnet; R1 = AdS₂×S² solves Einstein–Maxwell–Λ with residual 0 at Λ = 1.394888, E² = 2.394888 (L75) | "no JT dual claimed; no Einstein solution claimed" (L8). Λ and E² are chosen from ε_EP. R2 is a singular Kantowski–Sachs cosmology (L60, L70). |
| qg-on-R1 | D3 **PASS**, D4 **PASS** (RESULTS L70–74). Signed off | Contour actions, deformation invariance, Γ crossings | "Saddles" are "[by construction: chosen closed paths]" (L25). Z = 8.001 has "no measure, no fluctuation determinant" (L48). The loops "are not paths in R1 spacetime" (L9). |
| qg-theory | L1–L6 all **PARTIAL**; "THEORY STACK: (none)" (RESULTS L9–16, L142). Signed off | Reduced Einstein–Maxwell–Λ action with the boundary term; R1 stationary (residual 8.6e-16); on-shell action −πr₀² = −A/4 (L55–57); β-independence with the cone term (L59) | L1: the "gravity Hamiltonian" is H_A or a unitary rotation of it (L11, L28–29). L6: r = ε_EP is "circular: couplings chosen from ε_EP" (L16, L118–119). The one genuine prediction is H_A-level adiabatic physics (L107, L110). |
| qg-radial | **Overall: NOT HAVE.** F1–F3 PARTIAL [by construction], F4 MISSING (RESULTS L234–241). Signed off 09-26 | Raw roots of Einstein–Maxwell–Λ, linearised Stelle, CGHS / SRG / Liouville, and the AdS₂×S² chart, behind a firewall against Pair A numbers (L7) | No full LPPS shooting solve: "A full numerical LPPS shooting solve was not done" (L43). |
| mhd-qg-cut-connection | C1–C4 **PASS**: "connection type found" (RESULTS L46–51, L63) | A shared support and sheet jump between the MHD matrix and a π-flux holonomy on Γ | "Named type only. Not a theorem. Not 'they are the same operator.'" and "no black-hole claim" (L65–66). |

## 3. Where it stopped, and why

- **The wall is written down twice.** qg-theory ends with "THEORY STACK: (none)" and "NOT A FULL QG THEORY UNLESS L1 L2 L3 L4 are HAVE" (RESULTS L142–144). qg-radial ends with "Overall: NOT HAVE".
- **In plain words:**
  - The gravity side never got its own dynamics. Its Hamiltonian is H_A, and its loss is H_A's (qg-theory L11, L87).
  - Its S² radius is set by couplings chosen from ε_EP (L118–119).
  - No gravity family can produce ε_EP without feeding in the MHD box. qg-radial's post-hoc note says ε_EP "is an MHD box number (eta, L, v); gravity families with generic couplings cannot produce it without feeding the box in" (L228).
  - In the AdS₂ chart the tip position is pure coordinate choice: "eps_h is removable by a coordinate rescaling" (L212).
- **Open TODOs left:**
  - lift-4d's "next is the ODE" (L21) was done by lift-ode, but its full equations were never checked (§4).
  - qg-radial's LPPS shooting solve was never done (L43).
  - qg-radial L228: "The source of v is still open."
- **Follow-up:** none of these folders is followed by a later job I can see in this list. Folders not read: pairA-qg-operator, pairA-qg-probe-surface, pairA-qg-loss, pairA-qg-loss-sz, pairA-lambda-on-gamma, pairA-vortices-return, pairA-drive-return, pairA-drive-sweep, qg-all-families-crossing, qg-defect-scan-sweep, qg-family-sheet-jump-sweep, mhd-qg-cut-independent-check. They exist in `jobs/`, but they weren't on the list.

## 4. Physics read

**Tuned or circular (the jobs mostly say so themselves):**
- **The lift-4d bolt PASS is circular, and the 4π period is not smooth.** `lift_metric.py` L31–33 says a smooth 2π polar tip needs τ = 2π/ε_EP. The job used 4π/ε_EP and printed "2π-polar FAIL" while still grading the bolts PASS (`bolts.py` L25–26).
  - jt-4d later fixed this: the smooth period is 2π/ε_EP. 4π/ε_EP is "branched double cover (conical excess)" and needs a −2π cone term (RESULTS L18, L29, L44).
  - qg-theory adds that the action "is β-independent with the cone term… so the 4π/ε_EP identification gets no support from S_R1" (L59).
  - **So the old "4π bolt" is superseded.** A Euclidean bolt is smooth only at period 2π/κ [standard: Gibbons–Hawking 1977].
- **lift-ode's profiles are not Einstein solutions** [computed on the box, 22:40]. Its ODE uses only the ττ and S² equations. It drops the χχ equation, which requires r″ = cot χ · r′.
  - I re-integrated its four profiles (same ODE, same start, `/tmp`, nothing written to the repo) and computed Λ two ways, from R_ττ and from R_χχ:
    - r₀ = 0.3: Λ runs from −38.5 to 1.00 (ττ) and from −9.7 to 2.8 (χχ)
    - r₀ = 0.5137: Λ runs from −23.4 to 1.00 and from −13.2 to 2.8
    - r₀ = 0.7: Λ runs from −11.9 to 1.00 and from −9.6 to 2.7
    - r₀ = 1: Λ = 1 exactly, both ways
  - Only r₀ = 1 is a solution. The equations together force r′² + r² = 1 with r″ = cot χ r′, whose only regular solution is r = 1 [identity, by hand].
  - That one solution is the round S² × S² with Λ = 1, i.e. **Euclidean Nariai** [standard: Ginsparg–Perry 1983]. It owes nothing to Pair A, and it is smooth only at period 2π/ε_EP, not 4π/ε_EP.
- **jt-4d R1 is a real, standard geometry, but its numbers are chosen.** AdS₂ × S² solves Einstein–Maxwell–Λ (Bertotti–Robinson family). The job says it is "not derived from Pair A" (L75). Λ = (1 − ε_EP²)/(2ε_EP²) is picked so that r = ε_EP, so recovering r = ε_EP is circular (qg-theory L118–119).
- **The qg-on-R1 "path integral" is not a gravity path integral.** It sums chosen contours in a complexified drive parameter, with no measure or determinant (L9, L48). So it has no negative-mode content at all, and that content is exactly what the new L1 adds.
- **"Wick / Lorentzian" and "r = 0" in the handoff are names for features of a matrix spectrum.** Inside Γ the two eigenvalues differ in decay; outside they differ in frequency (`wick_lorentzian.py` L11). Nothing about spacetime signature was computed. jt-4d's tag "[hive-interpretation]" for the τ ↔ arg(ε − ε_EP) link (L91) is the honest label.
- **Nothing is wrongly claimed in the signed-off jobs.** jt-4d, qg-on-R1, qg-theory and qg-radial all state their limits plainly. The overclaims are in the unsigned handoff, lift-4d and lift-ode: "bolt PASS", "regular at both bolts", "allowed past Wick".

**Reusable for the new JOB_LIFT_SPEC:**
| Old result | Use in the new spec | Blocker / stage |
|---|---|---|
| jt-4d cone-angle and Gauss–Bonnet code (smooth period = 2π/κ; a 4π period gives a −2π cone term) | Bolt-smoothness check in the L1/L2 harness | L1, L2 |
| jt-4d R1 = AdS₂ × S² Einstein–Maxwell–Λ residual check (sympy G_ab) | Geometry check for the extremal end of the L2 charge scan (near-horizon AdS₂ × S²). L2 itself has Λ = 0 and a free Q/M, not jt-4d's Λ | L2 |
| qg-theory reduced Einstein–Maxwell–Λ action with the boundary term; on-shell −A/4; β-independence with the cone term (L41–59) | On-shell action / entropy check for L1 and L2 (I = −S at fixed Q) | 02 (Euclidean action, entropy); L1, L2 |
| qg-theory L6 and qg-radial F1 cold / charged-Nariai branch formulas | Reference values for a Λ > 0 version | 02 (Nariai) |
| lift-ode's only true solution, r = 1 (Euclidean Nariai S² × S²) | A Λ > 0 control for a later 02 test, not a Pair A result | 02 |
| qg-radial F2: the LPPS non-Schwarzschild branch meets Schwarzschild at m₂r_h ≈ 0.876 (cited there to Gregory–Laflamme 1993 / LPPS 2015, L56) | The same threshold that Reall ties to the GPY mode (μ*r₊ ≈ 0.88). So L1's eigenvalue also fixes where the Stelle branch starts | L1 GL cross-check; L4 Stelle item |
| mhd-qg-cut-connection's Z₂ (π-flux) holonomy, U(2π) = −1 | At most a cartoon of discrete Z_N hair [hive-interpretation, weak] | L3 / DGT–CPW, report-only |
| handoff, lift-4d, qg-on-R1, qg-theory L1/L3–L5 | Not reusable as gravity. They are history of the Pair A line | none |

## 5. Conflicts with the new spec

- **Two r = 0s.** The new spec separates the Euclidean R² origin (the bolt, where the S² stays finite) from the Lorentzian r = 0 singularity.
  - **The old R2 chart merges them.** Its S² shrinks (r = ε_EP sin χ → 0) at the same ±ε_EP where the τ circle closes (`lift-4d/lift_metric.py` L23–25). jt-4d found this chart has real curvature singularities there, "Big Bang at +ε_EP … Big Crunch at −ε_EP… not bolts" (RESULTS L70).
  - So the old R2 picture contradicts the new spec. jt-4d already dropped it ("R2 is not a target", L14).
  - **The old R1 agrees with the new spec.** The S² radius stays ε_EP at the tip, and there is no Lorentzian singularity at all.
- **The period.** The old handoff and lift-4d use τ = 4π/ε_EP. The new spec, following Gibbons–Hawking, uses the smooth period 2π/κ. The old 4π choice is a conical excess (jt-4d L29), so the new spec wins. The old swap/return needs only the degree-2 cover that the smooth period already gives (jt-4d L18, L95).
- **The sign of F inside Γ.** lift-4d and lift-ode are Euclidean inside Γ (F = ε_EP² − ε²). jt-4d is Euclidean outside Γ (F_JT = ε² − ε_EP²) and notes it is "the opposite of pairA-qg-operator's P2" (L17). The old stack contradicts itself here. The new spec uses neither convention, since it starts from Schwarzschild and RN.
- **"Wick dies at ±ε_EP" versus the new B4 / L-stages.** The old "real section dies at the tips" is a statement about a 2×2 spectrum. The new spec's Wick break is about spacetime, and the new toy note says that in the flat toy Wick never fails. That is no contradiction in substance, but the same words mean different things. Say "EP tip" for the old object, not "r = 0".
- **Akitti's link-post wording comes from this line.** "the real Lorentzian chart now ends at a_death, not at a=0" (AKITTI_LINK_POST L3298) and "--do-not-continue=a=0" (L92) match the handoff's "dies at ±ε_EP" and "allowed past Wick: A, B" (`RESULTS_probe.md` L16) [hive-interpretation: same vocabulary; no file links them explicitly].
