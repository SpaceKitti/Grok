# CONE_SIM_SPECS — the sims Grok asked for in Akitti's post 2110455808366633013
Revision 16 (from 58429B51, rev 15; record edit), reconciled line by line against Orion's X_COPY.md (45E4F6BB, 4862 lines; earlier 6D4391E2, B4062C3C, B2B73399), the source of record. "X:n" = X_COPY line n. Where X_COPY differs from my own reading, X_COPY wins.
Written by Helios, 15 Oct 2026 (BST). For Aethon to code AFTER Venus checks it. NOTHING IS LAUNCHED.
Credit: the cone-at-the-poles finding and the string-stacking set-up are Akitti's. The tweaks below are Grok's, shown in her post.
Tags: [from her posts; untested] · [Grok, in her post; untested; possibly hallucinated] · [standard: ref] · [identity] · [assumed] · [prediction] · [GR control].
## Symbol table (rev 7, H12; rev 9)
| Symbol | Meaning here | Not to be confused with |
|---|---|---|
| α, α_i | cone angle / 2π (deficit δ = 2π(1−α)) | α_M: MTVH's irrational number (X:3943) |
| κ | Ginzburg–Landau coupling λ/e² | κ_c: plane-curve curvature (C7, HP3) |
| μ, μ_i | SM1 matter tension | δ_i: geometric deficit angle (FFP's "μ_k") |
| δ_s, δ_t | strain parts of a deficit (C3) | δ_i |
| ρ | instanton size (INSTANTON_TESTS) | h(z): HP3 surface profile (was ρ(z)) |
| a | lattice spacing (INSTANTON_TESTS) | a_s, b_s: spiral constants; run.py's a (P1 cone parameter, cited as "run.py a") |
| L_φ | angular sites of the polar lattice | M_r, M_3, M_4: other lattice extents (were N_r, N_3, N_4); Law-GR/Law-hers/Law-HP: C3 row names (were L-…) |
| k | continuum YM instanton number | Q: measured lattice charge; Q → k as a → 0 |
| n, N_tip, n̂, p_w | winding; tip count; FFP normal; HP1 fixed-point weight | |
| ε (rev 8) | nc_scan row parameter (C1: "same (row, layout, ε, α)") | ε in S(ε): lattice over-improvement (INSTANTON_TESTS); MTVH ε(n₁/n₂ − α_M) |
| G1–G6 (rev 8) | Grok's claims | G: Newton's constant (only in [GR control] rows); lattice grids, renamed N0–N3′ in INSTANTON_TESTS (were G0–G3′) |
| c (rev 8) | FFP's constant c = 1/R² in (2.19)/(A.25) | IT2's coefficient c (dropped in INSTANTON_TESTS rev 5) |
| s, s_c (rev 8) | core size (nc_scan s; Gaussian width s_c in C3) | s(r): self-duality ratio in IT3 |
| N0–N3′, B10–B20 (rev 9) | INSTANTON_TESTS grid names | N_tip (tip count); N_CS (Chern–Simons number); N (MTVH four-form quantum) |
| d (rev 8) | C5 geodesic 2-vortex separation | d, d₀: instanton-centre distance from the tip axis (INSTANTON_TESTS) |

Gravity rule: the lift's gravity is unknown QG. G (or 4Gμ) is a free label, never an answer. Any GR line is a [GR control] row.

## Rev 16 — record edit (15 Oct 2026, ~19:14 BST)
- Header: rev 16, from 58429B51. Aethon's stationary scratch run (grid 48): run.py E4C4E2B7, README BBF56F14, STATUS 1334B54A, stationary_check.py 78737914, JSON FA2A0D6B.
- C4 (b): the rev 14/15 gradient-cut fall test is replaced by a grid-refinement fall test [Venus + Aethon, hive proposal adopted] on grids 48/64/80/96: control observed order p_c; each counted α < 1 mode needs observed order ≥ ½·p_c and fall factor ≥ 2 per grid step [assumed, from rev 15]; a levelling mode is a candidate lifted mode and its count is undecided. Context recorded: solver floor reached (gradient 3e-14 to 2e-13), K = 2 τ₀ = 5.348e-4, K = 4 τ₀ = 4.403e-4; eigenvalues don't move with the gradient at a stationary point; control zero-mode size set by the grid.
- Gauge-sector mixing recorded as NONE: the flag clears in all 4 cases (the earlier flag came from incomplete relaxation).
- τ₀ set per grid from that grid's control [Helios]; control-stop rule kept; a control zero mode within 10× of the solver floor (~1e-13) on any grid makes the fall test undecided [Venus].
- Report-only smoke facts: n = 1 α = 0.75 λ = −1.103e-3 (×2), count 0 undecided; n = 2 α = 0.5 −1.945e-5 (×2), −1.734e-5 (×2), count 4 (resolving the earlier −3.1e-5); μ(α)/μ(1) = 0.684, 0.368; negative α < 1 modes stay [hive proposal, untested] [NanoRibbon].
- Cost ~9–10 h on 4 workers, 2–3 GB (NanoRibbon); order: instanton graded rows first, then the cone run.

## Rev 15 — record edit (15 Oct 2026, ~19:08 BST)
- Header: rev 15, from EE2F24AE.
- C4 (b): tolerance line replaced [Venus]: log(mode fall factor) ≥ ½·log(control fall factor) per 10× gradient cut, AND mode fall factor ≥ 2. Reason recorded: floor-limited control fall ≈ 2× would make the half-rate rule pass a levelled mode (½ × 2 = 1×).

## Rev 14 — record edit (15 Oct 2026, ~19:05 BST)
- Header: rev 14, from D200835C (Venus confirmed rev 13 and withdrew her floor-stop reasoning; Orion: a τ₀ frozen at the floor while the modes are still falling is too big, so the cutoff is looser).
- C4: [Helios note] amended: a floor-stopped τ₀ is too big while the modes are still falling, so the cutoff is looser. Venus's ruling added: (a) [floor-limited] tag, with the floor value reported with each count it decides; (b) failable test: over the last two gradient cuts, every counted α < 1 mode must fall at least as fast as the control's zero modes, with fall factor per 10× cut ≥ ½ of the control's [Helios, assumed]. A levelling mode is listed as a candidate lifted mode and that count is undecided; passing counts stay gradable.
- 'Floor only makes the cutoff tighter' wording: not present outside the revision history (checked); nothing to remove.

## Rev 13 — record edit (15 Oct 2026, ~19:02 BST)
- Header: rev 13, from 874DA694 (Venus confirmed rev 12, including the Helios refinement).
- C4 τ₀ rule: α = 1 control stop added [Venus]: relax until a 10× gradient cut changes the largest control zero-mode |λ| by < 2×, then freeze τ₀; report each (gradient, largest zero-mode |λ|) pair. Helios note: if the zero modes track the gradient down to the solver's numerical floor, stop there and record it as such.

## Rev 12 — record edit (15 Oct 2026, ~18:59 BST); Aethon files: run.py 59978A1F, README 9E53FE7D, STATUS 85835182, xi_guard.py DC3CF39D, gauge_sector.py 52997D2A, scratch JSON 7F10C33A
- Header: rev 12, from 27CC9F84. Aethon's hashes: run.py 59978A1F, README 9E53FE7D, STATUS 85835182, xi_guard.py DC3CF39D, gauge_sector.py 52997D2A, scratch JSON 7F10C33A.
- C4/HP2: the 5-vs-10/λ_min guard PASSED (scratch): C4 counts 7 = 7 and 4 = 4, max diff ≤ 7.3e-12; all 24 HP2 rows match. Correction: the n = 1 gap is 1.2527e-1, not 4.73e-2, with 3 gauge modes below it at ξ = 1.
- Stationarity before any Hessian [Venus]: leftover gradient ≤ 1/10 of the smallest non-zero |λ| and ≤ τ₀/10 for counted modes [Helios refinement]; gradient reported per row; failing cases are report-only; gauge-mixing flag rerun at the stationary point (if still raised: real, report-only); μ(α)/μ(1) (0.685, 0.368) report-only until then; n = 2 −3.1e-5 mode rechecked.
- Gap rule: 'first eigenvalue above 100× the lowest' retired. τ₀ = 10 × the largest |λ| of the α = 1 control's known zero modes, on the same grid. Count |λ| ≤ τ₀; any eigenvalue in [τ₀/3, 3τ₀] ⇒ undecided; τ₀ frozen before any α < 1 row; control count ≠ known ⇒ τ₀ NOT COMPUTED (YET), counts report-only.

## Rev 11 — record edit (15 Oct 2026, ~18:48 BST)
- Header: rev 11, from 53D445AB (record edit; Venus passed rev 10 and keeps the guard on HP2 too).
- C4: report-only gauge-sector row added [hive proposal, untested] (NanoRibbon): ξ = 1 gauge modes recorded as μ = λ_gauge/ξ, ratio μ(α)/μ(α = 1), cross-checked against the penalty runs (expected to scale as penalty·μ). Never graded, never in the near-zero count.

## Rev 10 — record edit (15 Oct 2026, ~18:46 BST); Aethon files: run.py 6A6663FD, README E17556EE, STATUS ACD13751, xi_check.py 08F4507D
- Header: rev 10, from F204F8A7 (record edit).
- C4 (and HP2): penalty 10/λ_min replaces ξ = 1 [assumed; H3 deviation, accepted: Venus], with Aethon's grid-48 evidence and a 5/λ_min vs 10/λ_min guard that runs before grading (fail ⇒ cone count rows report-only).
- C5: frozen settings tuned on the α = 1 control only (24×24, R = 8, E_ref = 6.2639, penalty 10.0, target = seed moment; E/E_ref 1.0001/1.0000 at d = 2/4, moment within 1.6e-5); not to be retuned. The α = 0.75 smoke's non-monotone F(d) (0.145, 0.361, 0.344) is noted as smoke output, to be checked against 24 → 48 if it recurs.
- Aethon's file hashes recorded: run.py 6A6663FD, README E17556EE, STATUS ACD13751, xi_check.py 08F4507D.

## Rev 9 — Venus diff VENUS_CONE_DIFF_REV8 (CA22490F) applied (15 Oct 2026, ~18:25 BST)
- Header: rev 9, from 4FA92781.
- Symbol table, L_φ row: N_r/N_3/N_4 → M_r/M_3/M_4.
- Symbol-table heading now says rev 9 (Venus: still said rev 7).
- Symbol table: grid names N0–N3′/B10–B20 vs N_tip, N_CS, MTVH's N (Venus's minor new clash).

## Rev 8 — Venus diff VENUS_CONE_DIFF_REV7 (9C476E05) applied, with Helios's decisions (15 Oct 2026, ~18:15 BST)
- Header: rev 8, from 736DA1BD.
- l.87: α = 1 − 4Gμ allowed only in [GR control] rows; the frozen-exterior allowance is removed.
- l.123 (Shared inputs): α = 1 − 4Gμ moved to [GR control] rows only.
- l.175 (C4): inline '|λ| < 1e-8' stripped.
- C3: Richardson error NOT COMPUTED (YET) (needs 400/800-sample re-runs; run 2 has 200 at κ = 1); observed order to be reported.
- HP4: Richardson error NOT COMPUTED (YET), observed order to be reported.
- Symbol table: added ε, G1–G6 vs G vs grids (renamed N0–N3′ in both files), c, s/s_c, d.

## Rev 7 — Venus diff VENUS_CONE_DIFF_REV6 (F7F8F08D) applied (15 Oct 2026, ~18:10 BST)
- l.2: header said "Revision 3"; it now says rev 7, from E9A76637.
- Rev 6 heading: now gives the ~19 distinct removals and says the 27 log lines are separate from that count.
- C1 l.88: δ/2π = 4Gμ moved out of the main row into a labelled [GR control] row.
- C2 l.103: α_i-from-μ_i via δ = 2π·4Gμ struck.
- C3 l.124: 'α frozen at 1−4Gμ' removed from every main row, including Law-HP; it now appears only in a labelled [GR control] row.
- C3 prediction: 'frozen exterior' now means a fixed exterior α, measured or from a declared law (notation only).
- C3: 1e-8 tolerance superseded.
- C3: tolerance now 10× Richardson discretisation error over ≥ 3 resolutions [assumed]; G3's GR-exterior pass reference moved to a [GR control] row only.
- C3 undecided band restated in discretisation units.
- Rename L-GR/L-hers/L-HP → Law-GR/Law-hers/Law-HP (L clash).
- C4: pass rule tied to C4-b removed; C4 is now report-only.
- C4-b removed entirely.
- C4 l.144: stale 1e-8–1e-4 band stripped.
- C5: grade n = 2 only; n = 1 'moduli = cone, angle 2πα' is now report-only.
- C7 measured: κ→κ_c and a,b→a_s,b_s.
- HP3: ρ(z) renamed h(z) (ρ = instanton size).
- HP3 spec: b→b_s.
- HP4: 1e-8 noise floor raised to 10× discretisation error.
- MTVH α renamed α_M (α = cone angle).
- X:4799 (blank) → X:4798.
- Symbol table added (H12).
- C4 is now report-only (no graded row remains), alongside C2.
- X_COPY moved to 45E4F6BB (4862 lines). The 7 new lines are appended at X:4856–4862 (CITATION CHECKS item 5), so every earlier X:n is unchanged.
- X:4663 is relabelled as post 2110061492074865103, which quotes MSV 2110061370939211832 (X:4675). The label sits in INSTANTON_TESTS rev 3; CONE_SIM_SPECS cites MSV via X:3564/3583.
- Boundary conditions for the 4D tests (Braam–van Baal Cor. 1.4, confirmed, X:4858; Schenk NOT VERIFIED (YET)) are in INSTANTON_TESTS rev 3 only. CONE_SIM_SPECS has no 4D lattice rows.

## Rev 6 — Akitti's rule (15 Oct 2026, ~17:58 BST): a check that can't fail isn't run as a test
Every identity and by-construction graded row is REMOVED, not relabelled, and the tolerances that sat on those rows are dropped. The one exception is a single Gauss–Bonnet solver check (Aethon's request) in C2, labelled [solver check only, not a test]. Distinct removals: ~19 (Venus's count). The log lines below number 27, because they include duplicates (C1 Φ ×2, HP3(i) ×3, C7 identity ×2), one note and the 2108193… line, so the log is not the count. Log:
- C1: flux Φ_i/(2πn_i) column removed (by construction < 1; total flux would be an identity).
- C1: κ = 1 identity rows removed from grading.
- C1: flux tolerance rule (1e-6) and its rev-5 note removed.
- C1: κ = 1 identity control and its 1e-8 tolerance removed.
- C1: Φ/2πn output column removed.
- C2: Gauss–Bonnet identity row removed as a test (kept only as the single solver check, below).
- C2: (A.25) evaluation (identity), its 1e-6 normalised tolerance and the thin-string FFP 5.12 check removed.
- C2: Gauss–Bonnet residual removed from (b).
- C2: V5 parts (rev-3 statement, relabelled identity) removed.
- C2: GB 1e-8 / theorem-agreement pass rule and the rev-5 replacement removed; one Gauss–Bonnet solver check added, labelled [solver check only, not a test].
- C2: FFP (6.4) reproduction control and its 1e-8 tolerance removed.
- C2: single-tip non-existence control removed (theorem-forced).
- C2: noted that no graded test remains.
- C4: "count must equal standard count" numerics rule removed.
- C4: κ = 1 2n count (C4-a) removed.
- C5: Samols-on-the-plane match and α = 1 smoothness rows removed; α < 1 rows graded.
- C5: Samols plane control removed.
- C7: (a) K = 0 of the flat metric removed as a graded row (identity).
- C7: (d) dimensions check removed.
- C7: converted to a recorded result (Venus V6); the 1e-12 tolerance dropped.
- C7: identity controls removed.
- HP1: action and flux-integral rows removed (identities on the Witten route).
- HP2: the κ = 1 2n count removed.
- HP3: (i) removed (identity), with its 1e-10 tolerance.
- HP3: (i) spec removed.
- HP3: (i) note removed.
- 2108193…: "not found" (no Akitti post has that id).

## Rev 6 notes [rev 6, 15 Oct 2026 17:55 BST]: X_COPY 6D4391E2 §8 (12–15 Oct, X:4583–4799). No prediction moved.
- Her "one-to-one correspondence" (X:4704–4721), replying to Grok on MSV [Grok text POSSIBLY GROK-HALLUCINATED / UNTESTED], and her quote of Grok's Fubini–Lipatov reply (X:4722–4745: "strict one-to-one pairing of modes. No new levels appear") [from her posts; untested]. These sharpen the HP2/C4 criterion: one-to-one mode pairing with the flat (α = 1) spectrum means the Fubini–Lipatov kind, and new levels mean the topological kind. The HP2 prediction is unchanged.
- She re-shared the cone post to Grok (X:4746–4759). Nothing new.
- Monopole/dyon replies (X:4605–4662), her "spaghetti" note (X:4641–4662), "dilaton" (X:4760–4777), graphene layer sliding (X:4778–4798): no bearing on the cone sims.
- SIMS TO CHECK (X:4800–4833) still has items 1–17, renumbered by +217 here.

## Rev 5 (15 Oct 2026, ~17:55 BST): Venus pre-check E5CB1BF9 applied, with Helios's rulings
Backups: CONE_SIM_SPECS_3F1F.bak.md (3F1F4F1E), STACK_NOTES_9FB4.bak.md (9FB4F7CC). Her line numbers (F37EAC39) are mapped onto this text by section. Surviving predictions are word for word. Where a prediction was forced to change, it is relabelled and given a dated note.
Symbols (N1): κ = Ginzburg–Landau coupling λ/e² (as in SM1). κ_c = curvature of a plane curve (C7, HP3). μ_i = SM1 matter tension. δ_i = geometric deficit angle (FFP's "μ_k"; renamed here). n = winding; N_tip = number of cone tips; n̂ = FFP averaged normal. Background layouts are named by run.py row (P0 round, P1 one cone tip, P2, P12, CGR football [GR control]), never "1T/2T", because nc_scan's "1T/2T" is a vortex layout. Spiral constants are a_s, b_s; HP1's fixed-point weight is p_w. Old letters are kept inside quoted Grok text and inside the predictions (notation only).
Gravity rule (ruling 1; rev 8): δ = 8πGμ, i.e. α = 1 − 4Gμ, appears ONLY in labelled [GR control] rows. (The rev-7 allowance as a "frozen exterior relation" outside control rows is removed.) It is never the lift's gravity, and no sim derives an input α_i from μ_i.

## Rev 4 notes (15 Oct 2026, 17:45 BST): new X_COPY material only (§7 X:3820–4582, items 12–17 X:4827–4832). No existing prediction moved.
- (a) MTVH post 2108092102886211700 (X:3869–3983) [Grok-style text posted by Akitti; POSSIBLY GROK-HALLUCINATED / UNTESTED]. It adds a second integer charge n₂ at the same tip, μ = μ_crit(1+ε) with ε = ε(n₁/n₂ − α_M) and α_M irrational (the kernel uses √2 as a "schematic stand-in", X:3943), and states "the cone deficit and the S²→R² handoff are left unchanged" (X:3903). Effect on the cone sims: none changes. The deficit still enters only through μ, so C1–C3 read μ whatever sets it, and C4/C5/C7/HP1–HP3 are fixed-background tests. Two flags: (1) the post says the paper's section-4 S² uplifts have "a single free flux" (X:3893) [POSSIBLY GROK-HALLUCINATED / UNTESTED: means the four-form]. [rev 6, 15 Oct 2026 17:55 BST] Orion's V8 wording: the paper has "two two-form fluxes f₁, f₂ (eq. 4.1, p. 21) and one four-form quantum N (§4.2, p. 22)". (The rev-4 note saying the post contradicts the paper is removed.) (2) Venus withdrew the second-flux idea as a fix (NanoRibbon screenshot, X:4351) [hive record].
- Shape mode: the MTVH post does not make the sphere shape-mode spec a dependency of C1–C7. The paper's instability is a scalar below the BF bound (N3 check, line 19), not a shape wobble, and every main sim here is static or fixed-background. Item 16 (sphere wobble) stays the next job.
- (b) Her Σ correction (post 2108341100821799302, X:4414–4425, her own words): "the symbollic equation is upside down so it's not a³ = x. That's a summation symbol. x = Sigma a" [from her posts; untested]. Her version takes precedence over Grok's reading. It bears on C2 only if x is the tip tension and a runs over the piled strings, as in μ = Σ_a t_a (X:3897). That reading is [assumed] (the post doesn't name the variables), so Venus should confirm it. If it holds, C2 sets each tip's μ_k = Σ_a t_a (the sum over strings stacked at tip k) before applying FFP's Σ_k μ_k n̂_k = 0. This is an input rule, not a prediction change.

## CENTRAL QUESTION (frames C1–C7 and the hive proposals)
Is our cone singularity a geometric formation of the instanton itself? [Grok hypothesis, untested] (from Grok's replies in her post 2110455808366633013: "the singularity is the instanton announcing itself geometrically").
Call it H*. Each sim below says what would support H*, what would count against it, and what would leave it undecided. The predictions were written before this framing (spec 93613DDE) and are unchanged.
Grok's wording, X:778: "the cone angle might encode the instanton number — like the singularity is the instanton announcing itself geometrically".
Akitti's Yang–Mills instanton posts (X §6, X:3298–3819, 9 posts) now supply content. The points that bear on H*:
- k = (1/8π²)∫Tr F∧F = (1/8π²)∫_{S³∞} CS(A), integer-valued; self-dual solutions saturate S ≥ 8π²|k|; zero modes detect k via the index theorem (X:3745–3753) [from her posts; untested] (content is [standard: BPST / Atiyah–Singer]). Used in C1, C4 and HP1.
- Topological instantons restructure the fluctuation spectrum (genuinely new zero modes); the topologically trivial Fubini–Lipatov instanton flows continuously back to the vacuum (X:3346, X:3564, X:3583; source paper Monin–Shifman–Vainshtein arXiv:2307.09119, X:3336, X:3583) [from her posts; untested]. This gives a sharp test for H*: a cone that is an instanton must bring new zero modes. Used in C4 and HP2.
- Her own words (X:3357): "a non yang mills instanton seems to have the most stable spectral path yet glueballs seemingly exist so yang mills is probably a thing … But that could be due to lack of derivation" [from her posts; untested].
- The other §6 posts (Lyapunov bound X:3300–3317; multisymplectic YM X:3360–3555; jet bundles X:3797–3818; Guevara knots X:3755–3792) do not bear on the cone question; not used.

## 0. What I could read
Post 2110455808366633013 (14 Oct 2026 20:40 BST): text is only "🫩"; 4 images, all readable (saved in ./img/):
- img 1 (HUnXy4aW4…): Grok on Atiyah–Hitchin, monopoles, ADHM; "look at how the cone angle relates to the instanton number".
- img 2 (HUnXy4PW0…): Grok cites Groisser 1990, ADHM 1978, Bakas hep-th/9903256, and an unnamed arXiv paper where S² deficit angles are strings with tension and the angle constraint is a force-balance equation.
- img 3 (HUnXy4jX0…): Grok: Groisser is the best start; chase the deficit-as-tension paper for "the force-balance equation you're missing".
- img 4 (HUnXy4MWAA…): Grok: the stacked-string tension pinches the geometry at the poles; "the cone angle might encode the instanton number".
Quote post 2110480278460465169 (14 Oct 22:18 BST): one schematic image (HUnunZ7W…), readable. It adds the poles labelled 2π−δ₊, 2π−δ₋, "opening angle = 2π−δ, instanton charge k ∈ Z, match ⇒ real self-dual connection", and "strain alternative: δ = δ_t (tension) + δ_s (strain); force balance holds for combined source".
Nothing was unreadable. Reconciliation with X_COPY §3–4 (X:730–955): image texts match X:747–778 and X:880–886. X_COPY adds: image 477 reads chronologically first (X:779); the thread replies by @grok on strain (X:800) and the log-spiral image (X:849), now C7.
Citations (X:4834–4849):
- Bakas hep-th/9903256 is real (X:4843); I also opened it: AH via Donaldson rational maps and twistors, curve eq. (2), Toda eq. (15) [standard: Bakas 1999].
- ADHM, Phys. Lett. A 65 (1978) 185: NOT VERIFIED (YET) online (X:4842). This replaces my earlier [standard] tag.
- Groisser, Invent. Math. 99, 393–409 (1990) (X:4839). The abstract gives "a cone on CP²" for k = 1 only. "Vertex = small-instanton limit" was not checked in the full text: not verified (yet) (X:4841).
- Force-balance paper: Frolov–Fursaev–Page, hep-th/0112129, PRD 65 104029 (Orion ~90%, X:4846). I fetched the arXiv abstract and text on 15 Oct and confirmed eqs (1.1), (1.2), (2.18), (2.19), (5.12), (5.18), (5.19), (A.25) and the two §5.2 consequences. Used in C2.
One correction, not a sim: "ADHM … exactly what Atiyah and Hitchin studied" is tagged in X_COPY as a likely Grok slip (X:754, X:765, X:888, X:4849). AH comes from SU(2) monopoles via Nahm/Donaldson, not ADHM [standard: Atiyah–Hitchin 1988; Donaldson 1984].

## Grok's claims as testable statements
G1 cone angle encodes an integer instanton number k; a match means a real self-dual connection. G2 deficits from stacked strings obey a force-balance equation on S². G3 δ = δ_t + δ_s with force balance holding for the sum. G4 the cone vertex is the analogue of Groisser's small-instanton vertex. G5 Atiyah–Hitchin (2-monopole moduli) is the model for our cone. G6 the log spiral r = a e^{bθ} has K(θ) = −b²/(r²(1+b²)) with K → −∞ at the tip and → 0 far out (X:849). All [Grok, in her post; untested; possibly hallucinated]. The strain idea in G3 is credited to @Real123Here (X:789), not to Akitti.

## Shared inputs (read-only)
Run 2 outputs in /workspace/lift/sm1_inputs_run/ (RESULTS 84E12441, per_tip B3E611CA, nc_scan C8333CB4, profiles 8FCD0035), signed and pushed (1f73a49). Use only rows whose status is not FAILED / NOT COMPUTED (YET), and drop the normal-state entries by the column test max_phi2 < 1e-6 on nc_scan, not by label (V3: 24 such entries at (ε,κ) = (1, 0.25) are labelled "graded" with μ = πn exactly and would fake R = 1). The 32 filled normal-state entries have μ NOT COMPUTED (YET) and drop out. per_tip.csv is κ = 1 only, so μ_i and Φ_i at κ ≠ 1 are NOT COMPUTED (YET). profiles.csv is the critical stage, κ = 1 only, columns phi2, B, eps_m (no T_tt, no K). The literal G4 / critical-stage FAILs came from empty-tip relative μ_i (RESULTS 449); C1 uses empty tips report-only, so it is unaffected. Exterior: main rows take α from the measured cone data (run-2 background) or a declared T↔K law (NOT COMPUTED (YET)). Her framework's exterior relation in GR form, α = 1 − 4Gμ, is used only in [GR control] rows. Core filter: ∫K dA = 2π(1−α), ∫T_tt = μ, Π match, C¹ [from her framework]. Do not edit any SM1 file.

---
## C1 — Does the cone angle encode an integer charge? (G1)
**Status (H10, rev 5): a READ-OUT of signed run-2 data, not a pre-registered test.** Venus's read of nc_scan (n ≥ 2, μ numeric): κ = 0.25 R ∈ [0.851, 0.956]; 0.5 [0.922, 0.967]; 1: R = 1 to 3.2e-12; 2 [1.033, 1.087]; 4 [1.073, 1.184]. Overall R spans 0.85–1.18. The prediction below was written after that data existed and is kept as written; it cannot count as evidence.
Inputs: μ(n, κ) from nc_scan (μ_matter) and per_tip (μ_i), n = 1..4 as available, κ ∈ {0.25, 0.5, 1, 2, 4} as printed (rev 5: κ = 4 declared). n = 1 rows are excluded from the G1 test (R ≡ 1 by definition, B3). R uses μ(1,κ) on the SAME (row, layout, ε, α) background. Main rows use μ only (R is a ratio of tensions); no deficit formula enters. [GR control] row (labelled, separate): δ/2π = 4Gμ, 4G a free label.
Measured: ratios R(n,κ) = μ(n,κ)/(n·μ(1,κ)) (G drops out, so gravity-agnostic)
[rev 6] κ = 1 rows are not graded (R = 1 is the BPS identity).
[prediction] κ < 1: R < 1 (type I, vortices attract); κ > 1: R > 1 (type II) [standard: Jacobs–Rebbi 1979]. So away from κ = 1 the deficit is not an integer multiple of a unit, and G1 fails as a quantisation statement. The integer that survives is the winding n (flux 2πn), which is topological whatever the angle.
Pass/fail: G1 "quantised angle" PASSES only if |R − 1| ≤ 1e-6 [assumed] for every non-identity row with κ ≠ 1. Otherwise G1 is FAIL as a quantisation claim and "deficit ∝ n" is recorded as [identity, κ = 1 only].
Controls: n = 0 empty tips (μ_i/μ_matter tiny, report-only, as per G4′).
Use of her §6 notes: the instanton charge she quotes is an integral of Tr F∧F (X:3745–3747), and it is integer whatever the size. The deficit is an integral of energy (μ). C1 asks whether those two integrals coincide off the BPS line [from her posts; untested]. The prediction above is unchanged.
Outputs: c1_ratios.csv (n, κ, row, layout, ε, α, μ, R, max_phi2, status), C1_RESULTS.md.
H* — supports: |R−1| ≤ 1e-6 at κ ≠ 1 (angle quantised like a charge). Against: R ≠ 1 at κ ≠ 1 (angle continuous in μ; integer is only the winding). Undecided: no converged κ ≠ 1 rows, or only κ = 1 identity rows.
Cost: reuses run-2 numbers; no solver run. Note: needs run-2 rows at κ ≠ 1 that converged; if none, C1 is NOT COMPUTED (YET) for those κ.

## C2 — Force balance of N_tip cone tips on S² (G2)
Pure 2D geometry, gravity-agnostic. Background: S² with cone points of angle 2πα_i, metric e^{2u} g_round. Ruling 1 (rev 5): α_i (equivalently δ_i = 2π(1−α_i)) is a SCANNED INPUT. C2 never derives α_i from μ_i. FFP's deficit is written δ_i here; μ_i (SM1 tension) appears only in the [GR control] conversion row.
[standard: Troyanov 1989; Luo–Tian 1992] Constant positive curvature with cone angles α_i ∈ (0,1): for 2 tips it exists only if α₁ = α₂ (football; tips antipodal); for ≥ 3 tips it exists iff (1−α_i) < Σ_{j≠i}(1−α_j) for every i and Σ_i(1−α_i) < 2 (positive total curvature; rev 5, N2), and is then unique up to Möbius. This inequality is the candidate "force-balance equation" Grok says is missing. The paper Grok meant is now identified with ~90% confidence as Frolov–Fursaev–Page (FFP), hep-th/0112129 (X:4846; abstract confirmed). FFP's force balance is Σ_k μ_k n̂_k = 0 (eq. 2.18 exact for a thorny sphere; eq. 1.2/5.19 small deficit), or holonomy H₁⋯H_n = I (5.12), Tr[U₁⋯U_n] = 2 (5.18) [standard: FFP 2002]. Consequences in FFP §5.2: no sphere with a single cone, and two cones lie on one axis (antipodal).
Which assumption separates our 1T setups from FFP: FFP's thorny sphere is locally isometric to the round S² away from the tips, i.e. constant K outside infinitely thin strings (the vacuum-outside-thin-strings case of their §8 Einstein solution). Our one-tip backgrounds (P1) have non-constant K (teardrop). [rev 5, 15 Oct 2026, Venus precheck E5CB1BF9] The earlier words "and a finite vortex core carrying flux and stress" are dropped: on run 2 the metric is an input, and the core does not source K. FFP's generalised relation (2.19)/(A.25), Σ δ_k n̂_k = ∫_reg n(c − K) dA with c = 1/R² (any constant; dimension 1/length²), needs K > 0 everywhere (FFP App. A.2). It is an [identity] (Gauss map plus FFP 2.8), not a dynamical balance law. Their C-metric single-cone example (A.3) is a GR solution, used as pure 2D geometry and labelled so. Venus's sympy on run.py 38C1D32A: P1 has K(0) = (5a−3)/(2aR²) (run.py a), so K < 0 at the tip for α < 0.6 and K = 0 at α = 0.6. P2 has K < 0 near both tips for every a. CGR has K = 1/R²; P0 is round. So (A.25) applies only to P1 at α ∈ (0.7, 0.8, 0.9), where a single cone is not forbidden. For α ≤ 0.6 FFP neither allows nor forbids it. FFP's no-single-cone result applies to us only as a [GR control] row. It is not our gravity.
Inputs (rev 4, her Σ rule, X:4424, [from her posts; untested], reading [assumed]): per-tip μ_k = Σ_a t_a over the strings piled at that tip. Tip layouts from run 2 (1T, 2T and any others printed). [rev 7: the α_i-from-μ_i clause is struck (Venus diff REV6; superseded by the replacement below).]
[rev 5, 15 Oct 2026, Venus precheck E5CB1BF9] The derivation above is REPLACED (B7, ruling 1; circular, and it mixed δ with μ). Main rows: α_i from the background as given in run.py (P1 α ∈ {0.5, 0.6, 0.7, 0.8, 0.9}; P2, P12, CGR as printed), plus a scanned grid α_i ∈ {0.5, 0.6, …, 0.95} [assumed] for the theorem rows. Her Σ rule (μ_k = Σ_a t_a) enters only the [GR control] conversion row: δ_k = 8πGΣ_a t_a, 4G ∈ {0.01, 0.05, 0.1, 0.2} [assumed], labelled [GR control].
Measured: (a) the inequality per layout; (b) solve −Δ_round u + 1 = K₀ e^{2u} with cone singularities, on a 2D mesh (2nd-order FEM, refinement ≥ 4 levels, graded at the tips; rev 5) for constant K₀; record existence, tip positions after relaxation over Möbius; (c) the unequal-2-tip case (μ_N ≠ μ_S): show no constant-K metric (teardrop), and report the minimal curvature non-uniformity ‖K−K̄‖/K̄ needed.
[rev 6] The rev-3 C2 statement (V5 parts: 1T (A.25) RHS, thin-string no-solution, 2T antipodal) is removed: identity-forced, cannot fail.
[prediction] Equal-tension 2-tip rows: football exists, tips antipodal. Unequal 2-tip: no constant-K solution; balance needs curvature (matter) gradients, i.e. the core/bulk must carry stress. [rev 5, 15 Oct 2026, Venus precheck E5CB1BF9] The clause "i.e. the core/bulk must carry stress" is withdrawn (ruling 1; the metric is an input on fixed backgrounds). The rest of the prediction stands. ≥3 tips: exist iff inequality holds; equal tensions → symmetric arrangement.
Pass/fail: [rev 6] The theorem-agreement and Gauss–Bonnet rows are removed (by construction). Reported, not graded: tip positions after Möbius relaxation, mesh convergence ≤ 1e-4 relative over the last two levels [assumed], and (c)'s ‖K−K̄‖/K̄.
SOLVER CHECK (Aethon) [solver check only, not a test]: Gauss–Bonnet on the cone mesh, ∫K dA + Σ_i δ_i = 2πχ (χ = 2), evaluated on ≥ 3 refinements. The residual must fall at the observed order and be ≤ 1e-4 relative on the finest level [assumed]. It validates the solver and grades nothing.
Controls: n = 0 round sphere (u = 0); FFP Appendix B two-pole football. [GR control] rows: FFP §8 Schwarzschild with radial strings; 4D straight strings ending on the bubble with Israel junction. Labelled controls only.
Outputs: c2_balance.csv, c2_meshes/, C2_RESULTS.md.
H* — supports: the balance condition only admits tip sets whose deficits are integer multiples of one unit. Against: balance holds for continuous α_i (as the theorem says). Undecided: if FFP is not the paper Grok meant (~10% per Orion; secondary candidate Mondello–Panov arXiv:1505.01994, X:4847, not opened).
Note (rev 6): no graded C2 test remains on fixed backgrounds. Every existence statement above is theorem-forced, so C2 now reports existence, positions and ‖K−K̄‖/K̄ and carries the solver check. The H* lines are read-outs. Note: this is static existence only. Whether the balanced arrangement is STABLE is the sphere shape-mode job (next job, not needed here).

## C3 — Tension + strain split δ = δ_t + δ_s (G3)
[rev 5, 15 Oct 2026, Venus precheck E5CB1BF9] RESTRUCTURED AS CONDITIONAL (B8, ruling 2). On a fixed (not back-reacted) background, r_K = ∫K dA − 2π(1−α) is Gauss–Bonnet of the input metric, so it does not depend on σ and every σ "survives" by construction. C3 therefore needs a declared T↔K law, and the lift's law is unknown QG. Every row must declare its law:
- Row Law-GR [GR control]: K sourced by T through the 2+1 Einstein form (δ = 8πG∫T_tt). Labelled control only.
- Row Law-hers: a law taken from her posts. None found in X_COPY B4062C3C, so NOT COMPUTED (YET).
- Row Law-HP [hive proposal, untested]: a parametrised law K = K_bg + β·T_tt·w(r), β ∈ {0, 0.1, 1} [assumed]. It exists only as a hive proposal and is read only as a conditional ("if the core law were …").
Per-tip values and profiles at κ ≠ 1 are NOT COMPUTED (YET) (profiles.csv is κ = 1 only, N8). The σ = 0 "hash of residuals" reference is NOT COMPUTED (YET): run 2 printed no per-row r_K / r_T (N7).
The original text follows. The prediction is kept word for word and is now read conditionally, row by row.
Gravity-agnostic: works on fixed run-2 profiles.
Inputs: converged run-2 core profiles (profiles.csv) per row; a one-parameter strain family: add an anisotropic stress σ·w(r) with ∫w = 1, σ ∈ {−0.1, −0.01, 0, 0.01, 0.1}·μ [assumed], w a Gaussian of width s_c.
Measured: the two framework residuals r_K = ∫K dA − 2π(1−α) and r_T = ∫T_tt − μ with α taken from the measured cone data (run-2 background α) or from a declared T↔K law row (Law-hers, Law-HP: NOT COMPUTED (YET)), and Π/C¹ match at r_c. [GR control] row only: α frozen at 1 − 4Gμ, labelled.
[prediction] Under a fixed exterior α (measured, or from a declared law), any δ_s ≠ 0 whose energy is not inside ∫T_tt shifts ∫K and is rejected by Akitti's filter. Strain survives only if it is part of T_tt, and then it is already in μ, so "δ_s" is a relabelling of μ, not a new source. Pure shear (traceless, zero energy) leaves δ unchanged [prediction].
Pass/fail: a strain value survives iff |r_K|, |r_T| ≤ 1e-8 relative [assumed] and C¹ holds to 1e-6 [assumed]. [rev 5, 15 Oct 2026, Venus precheck E5CB1BF9] Tolerance replaced: absolute |r_K| ≤ 1e-8·2π and |r_T| ≤ 1e-8·μ_ref with μ_ref = π [assumed] [rev 7: SUPERSEDED, below discretisation of the 200-sample profiles] (the relative form divides by 2π(1−α) = 0 at α = 1). It applies only in a row with a declared law. [rev 7] Tolerance (discretisation-based) [assumed]: |r_K| ≤ 10·E_K and |r_T| ≤ 10·E_T, where E_K, E_T are the Richardson-estimated discretisation errors of ∫K dA and ∫T_tt from the σ = 0 row on ≥ 3 radial resolutions (200, 400, 800 samples). [rev 8] E_K, E_T are NOT COMPUTED (YET): run 2 has only 200 samples (κ = 1), so re-runs at 400 and 800 are needed, and the observed order must be reported (Richardson holds only in the asymptotic regime). Until then only the [GR control] row could run, and none of C3 is graded. C¹ is checked to 10× its own discretisation error. G3 "extra strain deficit" PASSES only if some σ ≠ 0 survives with a deficit different from the row's α reference (measured background α, or the declared law). [GR control] row only: with δ ≠ 2π·4Gμ, labelled.
Controls: σ = 0 must reproduce run 2 exactly (hash of residuals); [GR control] row: same with Einstein's equations solved in the core, labelled.
H* — supports: a surviving strain deficit tied to a topological number. Against: strain only survives inside T_tt (a relabelled μ). Undecided: residuals between 1× and 10× the discretisation error.
Outputs: c3_strain.csv, C3_RESULTS.md.

## C4 — Small-core limit vs Groisser's cone vertex (G4)
Gravity-agnostic (matter sector on fixed cone background).
Groisser's statement itself is NOT VERIFIED YET; spec tests our side only.
Inputs: κ = 1 and κ ∈ {0.5, 2} rows; core size s_c from nc_scan. Fluctuation operator of the abelian-Higgs vortex on the cone, n = 1, 2.
Measured: (a) number of zero modes of the second-variation operator [rev 5, 15 Oct 2026, Venus precheck E5CB1BF9] Threshold replaced: count a mode as zero if |λ|/λ_gap → 0 with a convergence trend over ≥ 3 grids [assumed], where λ_gap is the first non-zero eigenvalue. Background gauge fixing is declared (Rξ / background gauge, ξ = 1), so that gauge zero modes don't swamp the count (N5, H3). (b) whether any zero mode changes the core size (a scale modulus) or only moves tips.
[rev 10] Gauge fixing: a penalty of 10/λ_min replaces ξ = 1 [assumed; H3 deviation, accepted: Venus]. Evidence from Aethon's grid-48 check (xi_check.py 08F4507D): the physical modes match to about 1e-8. At ξ = 1, 5 of the 24 window modes are gauge modes (at n = 2 the lowest gauge mode, 1.597e-2, lies below λ_gap = 2.204e-2). With the penalty, all gauge modes sit at ≥ 10. GUARD (can fail; runs before anything is graded): on grid 48, the penalties 5/λ_min and 10/λ_min must give the same near-zero count and the same physical window modes. Otherwise the cone count rows (C4, and HP2, which shares C4's code) are report-only.
[rev 11] Gauge-sector row (NanoRibbon's request) [hive proposal, untested]: REPORT-ONLY, never graded, never in the near-zero count. For each case (n, κ, α), record the ξ = 1 gauge modes as μ = λ_gauge/ξ, and the ratio μ(α)/μ(α = 1). Cross-check against the penalty runs: the gauge modes there should scale as penalty·μ (5/λ_min and 10/λ_min). Output: a gauge-sector column block in c4_modes.csv.
[rev 12] Guard result (scratch): the 5/λ_min vs 10/λ_min guard PASSED. C4 counts are 7 = 7 and 4 = 4, with max diff ≤ 7.3e-12, and all 24 HP2 rows match (xi_guard.py DC3CF39D, scratch JSON 7F10C33A). Correction: the n = 1 gap is 1.2527e-1 (not 4.73e-2), with 3 gauge modes below it at ξ = 1.
[rev 12] Stationarity before any Hessian [Venus]: relax until the leftover gradient is ≤ 1/10 of the smallest |λ| reported as non-zero, AND ≤ τ₀/10 for the modes being counted [Helios refinement: a true zero mode has |λ| ≈ 0, so a rule tied to the smallest |λ| can never be met for it; the count uses the threshold scale τ₀ instead]. The gradient is reported on every row. A case that can't reach both has report-only count rows. The gauge-mixing flag is rerun at the stationary point; if it's still raised, the mixing is real and goes in as report-only gauge-sector data. μ(α)/μ(1) (0.685 and 0.368 in the smoke) stays report-only until then. The n = 2 −3.1e-5 mode is rechecked at the stationary point.
[rev 12] Gap rule (C4 and HP2): 'gap = first eigenvalue above 100× the lowest' is RETIRED. (That rule sat in Aethon's code, not in this spec; it supersedes the λ_gap definitions in C4's Measured line and HP2's pass/fail.) Replacement, calibrated on the α = 1 control on the same grid: count the control's known zero modes, and set τ₀ = 10 × the largest |λ| among them. A case at α < 1 counts the modes with |λ| ≤ τ₀. If any eigenvalue falls in [τ₀/3, 3τ₀], that count is UNDECIDED. τ₀ is frozen before any α < 1 row runs. If the control's count doesn't equal its known zero-mode number, τ₀ is NOT COMPUTED (YET) and the counts are report-only.
[rev 13] Control stop [Venus]: the α = 1 control has its own fixed stop. Relax it until cutting the leftover gradient by 10× changes the largest control zero-mode |λ| by less than 2×. Only then is τ₀ frozen. Report each (gradient, largest zero-mode |λ|) pair along the way. [Helios note, amended rev 14: if the zero modes keep falling in step with the gradient all the way to the solver's numerical floor, stop at the floor. A τ₀ frozen there is too big while the modes are still falling, so the cutoff is LOOSER, not tighter (Orion; Venus withdrew her floor-stop reasoning).]
[rev 14] Floor-limited τ₀ [Venus]: (a) a τ₀ stopped at the floor is tagged [floor-limited], and the floor value is reported with each count it decides. (b) [rev 16: the rev 14/15 gradient-cut fall test is REPLACED, see the next line.]
[rev 16] Context, Aethon's stationary scratch run (grid 48; JSON FA2A0D6B): it reached the solver floor, with gradient 3e-14 to 2e-13. Controls: K = 2 with τ₀ = 5.348e-4, and K = 4 with τ₀ = 4.403e-4. At a stationary point the eigenvalues don't move with the gradient, so a gradient-cut fall test can't discriminate. The control zero-mode size is set by the grid (smoke: 3.75e-3, 1.27e-3, 5.52e-4 on grids 12/16/20). Gauge-sector mixing: NONE. The flag clears in all 4 cases; the earlier flag came from incomplete relaxation.
[rev 16] Grid-refinement fall test [Venus + Aethon, hive proposal adopted; can fail]: runs on the graded run's own grids, 48/64/80/96 (not the smoke grids). Measure the control's observed order p_c over those grids. Each counted α < 1 mode needs an observed order ≥ ½·p_c (per-fit test) AND a total fall ≥ 2 over the whole 48→96 span [assumed; rev 17, Venus H2/H10: per-step ≥ 2 failed real modes on the 1.2× 80→96 step; control gives 2^p_c ≈ 13]. A mode that levels off is listed as a candidate lifted mode, and that count is UNDECIDED. Counts that pass stay gradable.
[rev 16] τ₀ per grid: each grid's τ₀ comes from that grid's own α = 1 control [Helios: the control zero-mode size depends on the grid, so one τ₀ can't serve every grid]. The control-stop rule (a 10× gradient cut changes the largest control zero mode by less than 2×) is kept. If a control zero mode is within 10× of the solver floor (about 1e-13) on any grid, the fall test is UNDECIDED, not passed [Venus].
[rev 16] Smoke facts, REPORT-ONLY: n = 1, α = 0.75 has λ = −1.103e-3 (×2), count 0, undecided (within 3× of τ₀). n = 2, α = 0.5 has −1.945e-5 (×2) and −1.734e-5 (×2), count 4 (the earlier −3.1e-5 resolved into these). μ(α)/μ(1) = 0.684 and 0.368. Negative α < 1 modes stay [hive proposal, untested] until the grid test decides [NanoRibbon].
[rev 16] Cost: about 9–10 h on 4 workers, 2–3 GB (re-confirmed by NanoRibbon). Order: the instanton graded rows first, then the cone run.
[prediction] At κ = 1 exactly 2n real zero modes, all positions, none a scale modulus [standard: Weinberg 1979 index; Taubes 1980]. κ ≠ 1: only the 2 overall translations (fewer on the sphere, where translations become rotations). So there is no small-instanton-like scale direction, and the cone vertex is not a moduli-space vertex in Groisser's sense. G4 is then an analogy only.
Pass/fail: [rev 7] no graded row remains in C4. C4-b is removed: at κ = 1 it can never pass, because abelian-Higgs vortices have no scale modulus [standard: Taubes 1980], so its outcome is fixed by construction. G4 is reported: spectra and mode types are recorded, not graded.
[rev 5, 15 Oct 2026, Venus precheck E5CB1BF9] Split (B9, ruling 3). Venus's "2n+1" was not a claim in the spec. It is the count that the old rule would produce if a scale mode existed, which the same rule would then call a numerics FAIL, so G4 could never pass. The two checks are now separate:
- (C4-a) [rev 6] removed: the κ = 1 count 2n is an index identity. The pinned-tip counts (κ ≠ 1: 0; κ > 1, n ≥ 2: negative modes) are reported, not graded.
- Instanton count, stated separately for comparison: an SU(2) YM instanton of charge k on ℝ⁴ has 8k moduli, or 8k − 3 after removing global gauge rotations, and these include a scale modulus [standard: Atiyah–Hitchin–Singer 1978]. Abelian-Higgs vortices have no scale modulus.
Controls: flat-plane vortex (α = 1); the BPST instanton scale modulus on R⁴ as a literature control (not computed here).
Use of her §6 notes: her MSV post separates topological instantons (spectrum restructures, new zero modes) from the Fubini–Lipatov kind (continuous spectral flow) (X:3564, X:3583) [from her posts; untested]. C4 records which kind our cone is, by the zero-mode count and the HP2 flow. Groisser's vertex claim is not verified (yet) (X:4841).
H* — supports: a scale zero mode whose collapse sends the core to the cone tip (Groisser-like vertex). Against: only position modes. Undecided: near-zero modes whose |λ|/λ_gap has no convergence trend over ≥ 3 grids. [rev 7: H* lines are read-outs only.]
Outputs: c4_modes.csv (n, κ, α, eigenvalues 1..20, mode type), C4_RESULTS.md.

## C5 — Vortex analogue of Atiyah–Hitchin: 2-vortex moduli metric near coincidence (G5)
Gravity-agnostic. This is the honest version of "cone angle vs number": AH is smooth with an RP² bolt [standard: Atiyah–Hitchin 1988; Bakas 1999].
Inputs: κ = 1, n = 2 on the plane and on the cone α ∈ {0.5, 0.75, 1}; separation d grid 0, 0.1..6 step 0.1 [assumed].
Measured: relative moduli metric F(d) (Samols' formula from zero-mode norms).
[prediction] In separation d the relative space looks like a cone of angle π (the two vortices are identical), and it is smooth in the coordinate w = z² [standard: Samols 1992]. So a "cone angle = 2π/n" appears in moduli space, but it is a quotient by exchange, not a curvature singularity or an instanton charge.
Pass/fail: [rev 6] the plane-Samols match (1e-4) and α = 1 smoothness (1e-3) are removed (known results; reproduction only). Graded: n = 2 only, α < 1 rows: whether the 2-vortex moduli space has a curvature singularity beyond the swap quotient and the inherited background point (angle to 1e-3 over ≥ 3 grids [assumed]). [rev 7] The n = 1 "moduli = cone, angle 2πα" part is by construction: reported, not graded. G5 "cone = AH-type defect" PASSES only if a true curvature singularity is found.
Controls: large d → flat with exponentially small corrections (report-only).
[rev 5, 15 Oct 2026, Venus precheck E5CB1BF9] (N6, ruling 4) The prediction above is the α = 1 statement and stands as written for α = 1. On a cone α < 1 the vortex pair sits on a background that has its own conical point, and the centre of mass is not free. So the "relative" metric is defined as the metric on the 2-vortex moduli space restricted to configurations symmetric about the tip (centre of mass at the tip), with d the geodesic separation. The swap cone (angle π in z, smooth in w = z²) [standard: Samols 1992] is a quotient by exchange and is independent of the background cone. [prediction, rev 5, added before any run] For α < 1 the moduli space also carries a conical point inherited from the background: for n = 1 the moduli space is the cone itself, angle 2πα. That point tracks α, not n. C5 reports both features separately.
H* — supports: a true curvature singularity at coincidence whose angle tracks n (rev 5: and is not explained by the background α or by the swap). Against: smooth in w = z² (angle π is an exchange quotient). Undecided: curvature not converged at w = 0.
[rev 10] C5 FROZEN, tuned on the α = 1 control only: 24×24 grid, R = 8, E_ref = 6.2639, C5_penalty = 10.0, C5_target = seed moment. On that control, E/E_ref = 1.0001 at d = 2 and 1.0000 at d = 4, with the moment within 1.6e-5. Not to be retuned. Note: the non-monotone F(d) in the α = 0.75 smoke (0.145, 0.361, 0.344) is smoke output, not a result. If the graded run shows it too, report it and check it against the 24 → 48 grid change before reading it as physics.
Outputs: c5_moduli.csv, C5_RESULTS.md.

## C7 — Grok's log-spiral cone curvature (G6; X item 3; thread reply X:844–849)
Pure geometry, gravity-agnostic, symbolic plus a numeric check. No run-2 input.
Source: @grok, x.com/grok/status/2110462552249348542; r(θ) = a e^{bθ}; K(θ) = −b²/(r²(1+b²)); limits −∞ (θ → −∞) and 0 (θ → ∞); local metric ds² = dr² + r²dθ² (X:849). [Grok, in her post thread; untested; possibly hallucinated]
Orion's flag kept (X:849, X:4806): a plane curve has no Gaussian curvature, so "K(θ)" is not defined as written.
Measured: [rev 6] (a) removed (identity). (b) the signed curvature κ_c (plane-curve curvature, not the GL κ) of the plane curve r = a_s e^{b_s θ}; (c) whether Grok's K equals any of: 0, κ_c, −κ_c², or −b_s²κ_c².
[prediction] (a) K = 0 identically: the metric printed is the flat plane in polar form, so it has no cone at all (deficit 0) [identity]. (b) κ = 1/(r√(1+b²)) [standard: log spiral]. (c) Grok's expression equals −b²κ². It is not the Gaussian curvature of the printed metric or of any surface named in the post. Its limits (−∞ at the tip, 0 far out) are those of −b²κ², so they hold for that expression but say nothing about a cone. (d) Dimensions check: Grok's K is 1/length², consistent only with a Gaussian curvature. [rev 5, 15 Oct 2026, Venus precheck E5CB1BF9] Part (d) is RELABELLED wrong (N3): −b²κ_c² and b·dκ_c/ds are also 1/length², so dimensions can't discriminate. (d) is dropped from the pass/fail. (a)–(c) stand; Venus confirmed (c) exactly (V6).
Pass/fail: [rev 6] not run. The outcome is already computed exactly by Venus (precheck V6): Grok's K = −b²κ_c², the Gaussian curvature of no surface stated in the post. RESULT RECORDED: G6 FAIL as stated [Grok, possibly hallucinated; untested]. The 1e-12 tolerance is dropped.
H* — supports: none possible from this item alone. Against: if (a) holds, the spiral is drawn on flat space and carries no deficit. Undecided: if the corrected version (HP3) gives a deficit tied to an integer.
Outputs: c7_spiral.md (symbolic), c7_spiral.csv.

## Hive proposals (kept separate from the main sims C1–C7; all [hive proposal, untested])

### HP1 (was C6) — [hive proposal, untested] instanton reduced to a vortex on a cone (most direct test of H*)
Idea: use a real instanton and watch whether it produces a cone. Witten's ansatz reduces cylindrically symmetric SU(2) self-dual instantons on R⁴ to abelian-Higgs vortices on the hyperbolic plane H², instanton number k = vortex number [standard: Witten 1977]; more generally circle-invariant instantons ↔ hyperbolic vortices [standard: Atiyah 1984]. Add a cone by taking the circle action with a fixed-point weight p (orbifold R⁴/Z_p or a Z_p-invariant sector), so the reduced H² has a cone point of angle 2π/p.
Inputs: k = 1..4, p = 1..4, BPS at the H² curvature-matched coupling; grids as C4. Gravity-agnostic (flat R⁴, no metric back-reaction). A [GR control] row may add back-reaction, labelled.
Measured: (a) the reduced vortex's μ and core on the H² cone; (b) the 4D action density, and whether the self-dual curvature concentrates so that the integrated holonomy around the fixed locus gives a deficit; (c) whether that deficit is set by k, by p, or by both.
[prediction] (written now, before any run) k fixes the action 8π²k and μ ∝ k [identity, BPS]; the cone angle 2π/p is an input of the quotient, independent of k. So instantons live happily ON a cone but do not MAKE one in flat space.
H* — supports: a deficit that appears without the quotient (p = 1) and grows with k. Against: deficit present only when put in by p, independent of k. Undecided: if a conical deficit appears only with back-reaction, i.e. only in the [GR control] row (gravity is unknown QG, so GR cannot settle it).
[rev 5, 15 Oct 2026, Venus precheck E5CB1BF9] REWRITTEN (B10, ruling 5). Flat ℝ⁴ with no back-reaction has no metric deficit to find, and gauge holonomy around the fixed locus is not a geometric deficit. In (b), "integrated holonomy … gives a deficit" is withdrawn as written. Gauge holonomy is reported separately and never counted as a deficit.
- Fixed-background row (flat ℝ⁴): the result is "against or undecided BY CONSTRUCTION". The supports branch cannot fire here.
- Supports can fire only in a declared back-reacted row: a [GR control] row (labelled; it cannot settle H*) or a [hive proposal, untested] law row. In such a row: a metric deficit at p_w = 1 that grows with k.
Pass/fail: [rev 6] the action (8π²k) and flux-integral (k) rows are removed: both are forced by the Witten map at BPS. The 4D tests are in INSTANTON_TESTS.md.
Controls: p = 1 (Witten, smooth H²); k = 0.
Outputs: hp1_reduced.csv, HP1_RESULTS.md. Needs a new code; after C1–C7.

### HP2 — [hive proposal, untested] spectral-flow test of the cone (from her MSV notes, X:3564, X:3573–3585)
Idea: follow the fluctuation spectrum of the vortex as the deficit is switched on, α from 1 to 0.5 in 26 steps [assumed], at fixed n ∈ {0, 1, 2}, κ ∈ {0.5, 1, 2}, gravity-agnostic (fixed background). An instanton-like cone should create new zero modes (topological restructuring); a non-topological one should flow continuously (Fubini–Lipatov type).
[prediction] The zero-mode count is fixed by n alone at every α (index set by the winding); no level crosses zero as α changes; n = 0 has no zero modes except background rotations. So the cone behaves like the Fubini–Lipatov case, not the BPST case.
Pass/fail (numerics): eigenvalues converged to 1e-8 [assumed] across two grids; [rev 5, 15 Oct 2026, Venus precheck E5CB1BF9] replaced by |λ|/λ_gap with a trend over ≥ 3 grids [assumed], as in C4. level tracking by overlap ≥ 0.99 [assumed].
H* — supports: a zero mode appears or disappears as α crosses some value at fixed n. Against: continuous flow with fixed count. Undecided: near-zero levels that do not settle on refinement.
Outputs: hp2_flow.csv. Shares code with C4.

### HP3 — [hive proposal, untested] corrected log-spiral version (Orion's flag, X:849)
A correct version of G6 has to be one of two things. (i) [rev 6] removed: the one-turn integral is an identity (Venus N4). (ii) A surface of revolution: profile h(z) chosen so the surface has a cone tip of angle 2πα and K = −h''/h (unit-speed profile), which can be negative and blow up near a tip. Grok's limits (K → −∞ near the tip, → 0 far out) would need to be checked against such an explicit profile.
Spec: for (ii) find any profile with K = −b_s²/(r²(1+b_s²)), r = geodesic distance from the tip, and report its tip angle. [prediction] (i) works as an identity; (ii) gives a negative-curvature horn whose tip angle is not fixed by b, so it does not encode an integer. [rev 5, 15 Oct 2026, Venus precheck E5CB1BF9] Part (ii) RELABELLED wrong (N4): K = −c/r², c = b²/(1+b²) ∈ (0,1), gives G ∝ r^{p±}, p± = (1 ± √(1+4c))/2, so G′(0) = 0 or ∞. No finite cone tip of angle 2πα ∈ (0, 2π) exists for any b. Correct statement: "no finite cone tip".

### HP4 — [hive proposal, untested] cone-formation string run + MHD matching circle (X item 15, X:4830; NanoRibbon screenshot X:4166–4179)
Source: the bot hive (NanoRibbon / Helios / Venus), not Grok or Akitti. Her own posts of 4–5 Oct describe the formation: strings pile up, build tension, make a cone, then flatten out (as relayed in X:4179).
Inputs: N strings of tensions t_a stacked at one tip, N = 1..4, tip tension μ = Σ_a t_a (her Σ rule); a vortex model whose energy depends on the tip angle (the screenshot's catch: the BPS vortex has μ = πn whatever the cone does, so it can't tell candidates apart). Use κ ∈ {0.5, 2} on the cone α ∈ {0.5, 0.75, 0.9, 1} [assumed].
Measured: μ(α) at fixed n; the matching-circle data Ψ|_{r_c} for an MHD solve (velocity, B, density), with the Π and C¹ matches from her framework.
[prediction] At κ ≠ 1, μ depends on α (the κ = 1 identity gives no α-dependence). The MHD matching solve is NOT COMPUTED (YET): no tool exists for it yet (X:4179).
Pass/fail: dμ/dα resolved above 10× the discretisation error of μ (Richardson estimate over ≥ 3 grids) [assumed]; [rev 8] that error is NOT COMPUTED (YET) (needs re-runs at 3 resolutions; observed order to be reported); framework residuals as in C3.
H* — supports: μ(α) quantised at integer steps. Against: smooth μ(α). Undecided: until the MHD solve exists.

## Literature items (Orion, not sims)
L1 Groisser, Invent. Math. 99, 393–409 (1990): title and abstract verified (X:4839–4841); vertex = small-instanton limit not verified (yet); full text NOT READ (YET). L2 FFP hep-th/0112129: abstract and text checked by me on 15 Oct; identification as Grok's paper ~90% (X:4846). L3 Bakas: verified. L4 ADHM Phys. Lett. A 65 (1978) 185: NOT VERIFIED (YET) online (X:4842). L5 ADHM-vs-Nahm slip (X:4849).

## Map: X_COPY SIMS TO CHECK (X:4800–4826) → specs
X_COPY now lists 17 numbered entries (items 12–17 added in B4062C3C).
| X item | What | Where |
|---|---|---|
| 1 (X:4804) | cone angle vs instanton charge | C1 (also C4, C5, HP1, HP2) |
| 2 (X:4805) | force balance; δ = δ_t + δ_s | C2 (FFP), C3 (strain) |
| 3 (X:4806) | log-spiral K(θ) | C7 (+ HP3) |
| 4 (X:4807) | c = 1 E = 0 fermion test | STACK_NOTES S1 |
| 5 (X:4808) | Lanczos on inverted oscillator | STACK_NOTES S2 |
| 6 (X:4809) | level-truncated OSFT, aperiodic shifts | STACK_NOTES S3 |
| 7 (X:4810) | slowest moiré envelope, τ(x) | STACK_NOTES S4 |
| 8 (X:4811) | order-by-order failure edge | STACK_NOTES S5 |
| 9 (X:4812–4824) | 12 hive --validate runs | STACK_NOTES S6 (one line each) |
| 10 (X:4825) | her own notes on checks | no sim (her words, recorded) |
| 11 (X:4826) | post 4 has no extra sim | NOT COMPUTED (YET); nothing to spec |
| 12 (X:4827) | instanton MSS bound as Euclidean stabiliser | STACK_NOTES S7 |
| 13 (X:4828) | Jangir helicity-asymmetry residual | STACK_NOTES S8 |
| 14 (X:4829) | MTVH second-charge residual | rev-4 note (a) above; STACK_NOTES S9 |
| 15 (X:4830) | cone-formation string run + MHD matching circle | HP4 [hive proposal, untested] |
| 16 (X:4831) | sphere-shape wobble | NEXT JOB (sphere shape-mode spec) [hive proposal, untested]; not a main sim |
| 17 (X:4832) | PISGD escape-rate scaling | STACK_NOTES S10 |
Every §3 cone-post item (1, 2, 3) has a run spec. Post 2108193… is not found. [rev 6, 15 Oct 2026 17:55 BST] No Akitti post has that id (X:4798); it is a truncated id or someone else's post. It stays NOT READ (YET) until the full id comes from whoever cited it.

## Order and dependencies
C1 and C3 reuse run-2 numbers (cheap). C7 is symbolic (cheapest). C2 needs a new 2D solver plus the FFP evaluation. C4, C5, HP2 need a fluctuation-operator code. HP1, HP3 come after. None needs the sphere shape-mode result; that is the next job (stability of the C2 arrangements).
Venus pre-check E5CB1BF9 ruled V0–V6 and S3 (see the rev-5 block). Still open: (V7) whether her "x = Σ a" (X:4424) is the tip-tension sum μ = Σ_a t_a, the reading C2 now uses [assumed]; (V8) settled by Orion's wording (rev 6); (V9) admit HP4. (V0) whether HP1–HP3 are admitted as hive proposals, with their predictions as written; (V4) whether the separating assumption in C2 (constant K outside infinitely thin strings in FFP vs non-constant K plus a finite core in our 1T) is stated correctly, and whether (A.25) needs K > 0 everywhere on our backgrounds; (V5) whether the rev-3 C2 prediction (added before any run) is admissible; (V6) C7's identification of Grok's K as −b²κ²; (V1) is the Luo–Tian inequality the right "force balance" to test G2 against; (V2) tolerances above, all [assumed]; (V3) whether C1 may use run-2 rows before run 3 (run 2 is signed, so I say yes, read-only).
