# CHANGES vs F37EAC39 (CONE_SIM_SPECS), for Venus to diff
Helios, 15 Oct 2026 (BST). Backups: CONE_SIM_SPECS_3F1F.bak.md, CONE_SIM_SPECS_E75E.bak.md, STACK_NOTES_9FB4.bak.md, STACK_NOTES_B2F5.bak.md, INSTANTON_TESTS_v1.bak.md. Current CONE_SIM_SPECS sha256 prefix: E9A76637.
## Rev 5 (Venus precheck E5CB1BF9 + Helios rulings)
- Symbols: κ vs κ_c, μ_i vs δ_i, n, N_tip, n̂, background names, spiral constants, p_w.
- Shared inputs: normal-state entries dropped by max_phi2 < 1e-6 (V3); per_tip/profiles are κ = 1 only; G4 FAILs come from empty tips.
- C1: a read-out of signed run-2 data; κ = 4 declared; n = 1 rows excluded.
- C2: α_i is a scanned input (ruling 1); δ = 8πGμ only as [GR control]; old derivation replaced (B7); Luo–Tian condition Σ(1−α_i) < 2 added (N2); FFP identified (hep-th/0112129).
- C3: conditional on a declared T↔K law; GR as [GR control]; others NOT COMPUTED (YET).
- C4: |λ|/λ_gap with background gauge; split into C4-a/C4-b; SU(2) YM count stated separately.
- C5: added an α < 1 prediction (conical point inherited).
- C7: κ_c renamed; Venus V6 result.
- HP1: flat ℝ⁴ without back-reaction gives no metric deficit (B10, ruling 5).
- HP2: |λ|/λ_gap. HP3: κ_g = α/(r√(α²+b²)); (ii) relabelled wrong.
- X_COPY references remapped to 6D4391E2 (8 pre-existing references to blank lines fixed). §8 material added as dated notes. MTVH flux count uses Orion's V8 wording (two fluxes, not one). Post 2108193…: not found.
## Rev 6 (Akitti's rule: a check that can't fail isn't run as a test)
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
## INSTANTON_TESTS.md (new file; rev 2 applies Venus a–e)
- 3 failable tests: IT1 size law (ρ free, ρ(α) stated in advance), IT2 charge on a free lattice route (ΔN_CS merged in), IT3 self-duality at the tip (action excess report-only). Plus IT4, the Hessian moduli count, conditional on Aethon's costing. The Witten-route charge test is dropped.

## Rev 7 (Venus diff VENUS_CONE_DIFF_REV6 F7F8F08D; Orion CITATION CHECKS item 5; X_COPY 45E4F6BB)
CONE_SIM_SPECS E9A76637 → 736DA1BD:
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
STACK_NOTES: X:4799 → X:4798; X_COPY hash → 45E4F6BB.
INSTANTON_TESTS 255E756D → 5B8F1547 (rev 3): see its revision history, [rev 3] lines:
- [rev 3] IT1: the Wilson action is replaced by the scale-flat / over-improved S(ε), ε ∈ {0, −0.25}. Wilson flow shrinks instantons, which made the "runaway at every α" prediction by construction (Venus d/I4). The prediction is now the drift ratio D(α) and ρ/d, with numeric bands.
- [rev 3] BCs: periodic T⁴ excluded (Braam–van Baal Cor. 1.4, confirmed; Schenk NOT VERIFIED (YET); hep-th/9512144 is not cited, being an unrelated paper, X:4861). IT2 uses an open/Dirichlet box (Venus option (a)). **Twisted BCs rejected for IT2:** an 't Hooft twist fixes Q mod 1 by construction (Q ∈ ½ℤ or ℤ set by the twist vector: non-orthogonal twist gives Q = ½ [standard: García Pérez–González-Arroyo et al., hep-lat/9909112 §1, X:4860]). That would make the integer/half-integer outcome an input, and it collides with the α = 0.5 orbifold row, where ½ must be free to appear or not. IT4 uses the same open box, with the lifted global modes declared.
- [rev 3] IT2 tolerance: the fixed 0.05 is replaced by τ = c(ρ/ℓ)⁴ + E_disc, c = 3 [assumed], with shrinkage required across ≥ 2 box sizes (Venus caveat). IT4's boundary-lifted modes use the same (ρ/ℓ)⁴ rule.
- [rev 3] IT3: numeric thresholds added (0.02 / 0.1 [assumed]), graded at r ≥ 2a.
- [rev 3] IT4: projection orthogonal to the gauge orbits; the fate of the 3 global orientations stated; 30 Lanczos modes; cutoff λ/λ_gap (ρ²λ) with a → 0 over ≥ 3 grids (Venus I3).
- [rev 3] Lattice: polar-type, L_φ = 20k (20, 40), so α ∈ {1, 0.9, 0.75, 0.55, 0.5} are exact; α = 1 is the tip-artefact control; graded at r ≥ 2a; tip action reported separately; α = 0.5 labelled [orbifold, ℂ/ℤ₂, ½-charge allowed], α = 0.55 the generic angle (Venus I1, I2).
- [rev 3] Symbols: L split into N_r, L_φ, N_3, N_4 and the box extent ℓ; Q vs k stated; source label fixed: X:4663 is post 2110061492074865103, which quotes MSV 2110061370939211832 at X:4675.
- [rev 3] X_COPY references moved to 45E4F6BB. Its 7 new lines are appended at X:4856–4862, so earlier X:n are unchanged.

## INSTANTON_TESTS rev 4 (5B8F1547 → 21FC2E9B; Orion CITATION CHECKS item 6, X_COPY 204D12D3). CONE_SIM_SPECS and STACK_NOTES are untouched, pending Venus's rev 7 diff.
- [rev 4] Header: rev 4, from 5B8F1547.
- [rev 4] Action: citation is now hep-lat/9309009, NPB 413 (1994) 535, eq. (8) p. 4 and eq. (19) p. 7. The rev-3 'de Forcrand–García Pérez–Stamatescu 1997' citation is removed (wrong paper; X:4865 flags a wrong arXiv id, which is not cited). The 'ρ-independent action' wording is removed everywhere. ε rows are now 1 (Wilson, inward control), 0 (outward, +2/35 (a/ρ)⁴) and −1 (paper's value, outward); −0.25 is kept as a labelled hive row (d₂ = +0.05, Orion's computation, not the paper's).
- [rev 4] IT1 title: ε rows updated.
- [rev 4] IT1: only R(α) is graded, early-time (ρ ≤ 0.3·min(d₀, ℓ) [assumed]). The final ρ (box-set) and ρ/d are report-only. Drift signs pre-stated (inward at ε = 1, outward at 0, −1). Sign-flip rule added: a trend that flips between ε = 1 and ε = 0/−1 is a lattice effect, not support. Bands kept (1 ± 0.2 against, outside 1 ± 0.5 supports) [assumed]. J1 scope note added. D(α) renamed R(α).
- [rev 4] IT4: the ε = 0 Hessian is no longer called ρ-independent.
- [rev 4] IT4: scale-mode lift restated.
- [rev 4] IT4: grids are G0, G1, G2 (+G3 if ≥ 4 GB free, per Aethon's smoke); G3′ excluded; report-only if ρ/a < ~3 on G0 [assumed].
- [rev 4] IT4 title: grids updated.
- [rev 4] G0 = (8, 20, 13, 14), 29 120 sites, added.
- [rev 4] IT4 cost: G0 Hessian dimension added.
- [rev 4] rev-3 history line annotated as superseded.
- [rev 4] X_COPY references moved to 204D12D3 (4872 lines). Item (6) is appended at X:4863–4872, so every earlier X:n is unchanged. New citations: X:4865–4872.

## Rev 8 / INSTANTON_TESTS rev 5 (Venus REV7 9C476E05, with Helios's decisions; X_COPY 204D12D3 unchanged)
CONE_SIM_SPECS 736DA1BD → 4FA92781:
- Header: rev 8, from 736DA1BD.
- l.87: α = 1 − 4Gμ allowed only in [GR control] rows; the frozen-exterior allowance is removed.
- l.123 (Shared inputs): α = 1 − 4Gμ moved to [GR control] rows only.
- l.175 (C4): inline '|λ| < 1e-8' stripped.
- C3: Richardson error NOT COMPUTED (YET) (needs 400/800-sample re-runs; run 2 has 200 at κ = 1); observed order to be reported.
- HP4: Richardson error NOT COMPUTED (YET), observed order to be reported.
- Symbol table: added ε, G1–G6 vs G vs grids (renamed N0–N3′ in both files), c, s/s_c, d.
INSTANTON_TESTS 21FC2E9B → 3BF63D44:
- [rev 5] Header: rev 5, from 21FC2E9B.
- [rev 5] Symbols: site counts renamed M_r, M_3, M_4; ε, s, E_a and the grid names declared (the IT2 coefficient c is gone).
- [rev 5] Lattice: J1 decision (stay polar); per-orientation anisotropic coefficients; only 1×1 plaquettes at r < 2a; Cartesian 90°/180°-wedge cross-check row at α = 0.75 and 0.5.
- [rev 5] Action: Venus's ε = 0 O(a⁴) sign conflicts with the paper as read by Orion. The paper's sign (outward) is kept, and the conflict is flagged.
- [rev 5] Grids renamed G0–G3′ → N0–N3′; the L_φ-only step N1φ = (12, 40, 24, 24), ≤ 276 480 sites, added; site counts marked as upper bounds before the wedge cut; ℓ per grid given.
- [rev 5] IT1: grade the difference Δ(α) = drift(α) − drift(1) (early-time, same ε and grid); the ratio R and the 1 ± 0.2 / 1 ± 0.5 bands are dropped. Supports/against are on |Δ| vs k_Δ·E_a(Δ), k_Δ = 3 [assumed] stated before the run. The ε rows and sign-flip rule are kept; grid stability only after a Richardson estimate (Venus J2).
- [rev 5] IT2: c(ρ/ℓ)⁴ allowance and c = 3 dropped; with identity Dirichlet faces Q → integer as a → 0 at any ℓ [Venus derivation; check]; τ = 3·E_a(Q) [assumed]; a fractional deficit surviving a → 0 is a FAIL except ½ at α = 0.5; ℓ-independence is report-only.
- [rev 5] IT3: the 'not self-dual' grade is the tip value minus the α = 1 value, same shell and grid.
- [rev 5] IT3 grids renamed.
- [rev 5] IT3 against line updated.
- [rev 5] IT4: projection keeps only ω = 0 on the boundary, so the 3 orientations survive (J3). N3 is out (~10–13 GB); a → 0 over N0, N1, N2; box step N1φ (ℓ = 12a) → N2 (ℓ = 16a). Prediction replaced by Venus's corrected count, tagged [hive proposal, untested]: 7 after ℓ → ∞ on the cone (one eigenvalue tracks ρ/d₀, one scales with ℓ); 6 at finite ℓ is by construction and not graded; 8 at α = 1 is the control; the tip lifting rate is NOT COMPUTED (YET). The interim '6 for α < 1' estimate (and the steering message's 6-mode reasoning) is superseded. ε = 0 is kept for the Hessian (Venus may prefer −1).
- [rev 5] J4 recorded: no power-law leakage [Venus derivation; check].

## Rev 9 / INSTANTON_TESTS rev 6 (Venus REV8 CA22490F, with Helios's decisions)
CONE_SIM_SPECS 4FA92781 → F204F8A7:
- Header: rev 9, from 4FA92781.
- Symbol table, L_φ row: N_r/N_3/N_4 → M_r/M_3/M_4.
- Symbol-table heading now says rev 9 (Venus: still said rev 7).
- Symbol table: grid names N0–N3′/B10–B20 vs N_tip, N_CS, MTVH's N (Venus's minor new clash).
INSTANTON_TESTS 3BF63D44 → 7A4BEF8A:
- [rev 6] Header: rev 6, from 3BF63D44.
- [rev 6] K2 closed: 1×1 + 2×2 only (no 1×2; Lüscher–Weisz 5/3, −1/12 dropped); per-plane (4−ε)/3 and (ε−1)/48; ξ only in the plane prefactors β ∝ 1/ξ (rφ, φ3, φ4) and ∝ ξ (r3, r4, 34) [Venus derivation, confirmed at tree level]. The trapezoid terms and the ε = 0 sign on the polar lattice are NOT COMPUTED (YET), to be checked before IT1 is graded.
- [rev 6] K1 closed: Venus withdrew −17/210; +2/35 outward.
- [rev 6] Flow stops at a target ρ (K3), not t_max.
- [rev 6] Box series B10/B12/B16/B20 (L_φ = 20) added, with site counts. Box series at ρ = 3a, a-series at ρ/ℓ = 1/4, L_φ step B12 vs N1φ. N0 is dropped as a grid.
- [rev 6] Seeds/d₀: the d₀ = 2a (and 4a) rows are dropped; off-tip rows use d₀ ≥ 8a.
- [rev 6] IT1: graded on the a → 0 extrapolated Δ with E = √(E_a² + σ_seed²/8); a-series B12/B16/B20 at L_φ = 20; d₀ ≥ 8a.
- [rev 6] IT1: box inward drift noted; it cancels in Δ.
- [rev 6] IT2 l.45: wording is now 'identity faces ⇒ box ≅ S⁴ topologically ⇒ Q → integer, no leakage'. The 't Hooft/Dirichlet Green's function claim is removed; box action cost ~(ρ/ℓ)⁴ with inward push, p = 4 [Venus estimate, check].
- [rev 6] J4 wording (l.120) updated the same way.
- [rev 6] IT4: diagonalised at the stationary point d₀ = 0, centred on the tip; flow stops at ρ = 3a.
- [rev 6] IT4: orientation modes are D_AΛ_T with D²Λ_T = 0 and Λ_T = T on the boundary.
- [rev 6] IT4 grids: PRIMARY B10/B12/B16 at ρ = 3a (~3–3.8 GB); B20 out for IT4; B10's ρ/ℓ = 0.3 box lift stated; fit λ∞ + Aℓ^−4 with p = 4 pre-stated; report-only if even this doesn't fit. N0/N1/N2 dropped for IT4.
- [rev 6] IT4 prediction replaced: [hive proposal, untested; Venus] 6 as ℓ → ∞ at d₀ = 0 (2 ℝ² translations, dilatation = scale, 3 orientations); box lifts the dilatation at finite ℓ; α = 1 control is 8, also only as ℓ → ∞. The rev-5 '7' (and its ρ/d₀ diagnostics) is withdrawn: it needed an off-tip stationary point that doesn't exist.
- [rev 6] IT4 cost lines updated for B10/B12/B16.
- [rev 6] Open items K1–K6 updated.

## INSTANTON_TESTS rev 7 (7A4BEF8A → 04F36176; Venus REV9 62983822). CONE_SIM_SPECS F204F8A7 was PASSED by Venus and is untouched.
- [rev 7] Header: rev 7, from 7A4BEF8A.
- [rev 7] IT1 off-tip: window widened to ρ ≤ 0.4·min(d₀, ℓ) [assumed]; d₀ = 10a on B16/B20 only (window 4a > 3a floor; arithmetic shown); off-tip rows on B12 are report-only (centre 2a from the face).
- [rev 7] IT4 tip: single r = 0 site, zero-length links dropped, ξ from r = a/2, tip-site gauge copies projected out, tip-localised modes reported separately and not counted; α = 1 polar control first, must reach 8 as ℓ → ∞, else report-only; ρ = 4a on B16 if RAM allows.
- [rev 7] IT4: box series stated as fixed-a (ℓ → ∞ only); RAM updated to Venus's 0.46 / 0.80 / 1.89 GB, total 3.15 GB.
- [rev 7] IT4 residual rule made explicit (Venus's REV9 wording): residual > 1σ_fit ⇒ p = 4 rejected ⇒ report-only. B10 gets a (ρ/ℓ)² ≈ 9% next-order error in quadrature [assumed]. Noted: B10 box lift 0.008 < lattice lift 0.012.
- [rev 7] IT4: 'extrapolated a → 0' struck (cutoff line, user's l.72); graded quantity is now Δλ∞ = λ∞(α) − λ∞(1) on the same grid and ρ, so the (a/ρ)⁴ lift cancels.
- [rev 7] IT4 supports/against/undecided restated on Δλ∞, with tip-localised modes excluded.
- [rev 7] Cost line: RAM figures updated.
- [rev 7] Open items: K6 updated; K7 and K8 added.

## INSTANTON_TESTS rev 8 (04F36176 → E51ABDD1; Venus REV10 F657E190; off-tip IT1 rows only)
- [rev 8] Header: rev 8, from 04F36176.
- [rev 8] Seeds line: off-tip d₀ now held at d₀/ρ = 2.5 (10a on B16, 12.5a on B20).
- [rev 8] IT1 measured line: off-tip rows at fixed d₀/ρ = 2.5.
- [rev 8] Off-tip arithmetic: d₀/ρ = 2.5 on both grids (10a/4a, 12.5a/5a); B20 window 0.4×12.5a = 5a, centre 7.5a from the face; rings at r = (n+½)a so 12.5a is a ring, else the off-tip rows are report-only; B12 (d₀/ρ = 3.3) dropped from the order estimate.
- [rev 8] Open items: K8 restated (2-point off-tip series has no order estimate); K9 added (B16's 10a is not on an (n+½)a ring).

## INSTANTON_TESTS rev 9 (E51ABDD1 → CE6C871C; off-tip IT1 rows only, K8/K9)
- [rev 9] Header: rev 9, from E51ABDD1.
- [rev 9] Seeds line: B16 off-tip moved to d₀ = 10.5a, ρ = 4.2a.
- [rev 9] IT1 measured line: B16 off-tip values updated.
- [rev 9] K9: B16 off-tip on the n = 10 ring (d₀ = 10.5a, ρ = 4.2a, d₀/ρ = 2.5; window 4.2a; centre 5.5a from the face).
- [rev 9] K8: off-tip E_a from p_a = 2 [assumed, not measured]; observed B16 → B20 change reported; graded only if the on-tip a-series measures an order consistent with 2, else report-only.
- [rev 9] Open items: K8 and K9 marked resolved, with the ε = 0 caveat flagged.

## INSTANTON_TESTS rev 10 (CE6C871C → 26AA7355; Venus PASS with one edit, no re-diff)
- [rev 10] Header: rev 10, from CE6C871C (Venus PASS with one edit).
- [rev 10] K8 order gate made per ε: p_a = 2 at ε = 1 and −1, p_a = 4 at ε = 0 (d₂ = 0), all [assumed, not measured]. Each ε is graded off-tip only if the on-tip B12/B16/B20 series measures that order at that ε, else that ε is report-only.
- [rev 10] Report-only note added: off-tip ρ/ℓ 0.26 vs 0.25 shifts the box term by ~0.001 [Venus].
- [rev 10] Removed the note that the ε = 0 off-tip rows are likely report-only (superseded by p_a = 4 at ε = 0).

## INSTANTON_TESTS rev 11 (26AA7355 → 8C1E7672; record edit)
- [rev 11] Header: rev 11, from 26AA7355.
- [rev 11] Per-ε gate: ε = −0.25 hive row added with p_a = 2 [assumed, not measured; Venus] (d₂ = +0.05 ≠ 0). Venus's caveat recorded: small d₂ may make the on-tip series look like order 4; if it doesn't measure 2, that row is report-only.

## CONE_SIM_SPECS rev 10 (F204F8A7 → 53D445AB; record edit)
- Header: rev 10, from F204F8A7 (record edit).
- C4 (and HP2): penalty 10/λ_min replaces ξ = 1 [assumed; H3 deviation, accepted: Venus], with Aethon's grid-48 evidence and a 5/λ_min vs 10/λ_min guard that runs before grading (fail ⇒ cone count rows report-only).
- C5: frozen settings tuned on the α = 1 control only (24×24, R = 8, E_ref = 6.2639, penalty 10.0, target = seed moment; E/E_ref 1.0001/1.0000 at d = 2/4, moment within 1.6e-5); not to be retuned. The α = 0.75 smoke's non-monotone F(d) (0.145, 0.361, 0.344) is noted as smoke output, to be checked against 24 → 48 if it recurs.
- Aethon's file hashes recorded: run.py 6A6663FD, README E17556EE, STATUS ACD13751, xi_check.py 08F4507D.

## CONE_SIM_SPECS rev 11 (53D445AB → 27CC9F84; record edit)
- Header: rev 11, from 53D445AB (record edit; Venus passed rev 10 and keeps the guard on HP2 too).
- C4: report-only gauge-sector row added [hive proposal, untested] (NanoRibbon): ξ = 1 gauge modes recorded as μ = λ_gauge/ξ, ratio μ(α)/μ(α = 1), cross-checked against the penalty runs (expected to scale as penalty·μ). Never graded, never in the near-zero count.

## INSTANTON_TESTS rev 12 (8C1E7672 → 5DD76953; record edit, Venus's smoke rulings; ruling-1 note amended per NanoRibbon)
- [rev 12] Header: rev 12, from 8C1E7672. Aethon's hashes recorded: run.py 3F70F147, lattice.py F3BBD51D, README E6AFAF62, smoke_scratch.json 94C529B8.
- [rev 12] HOLD added: nothing graded runs until the singular-gauge re-smoke is in.
- [rev 12] Box cost: p = 4 withdrawn [Venus] (smoke excess 0.112/0.066/0.029/0.016 at ρ/ℓ 0.30/0.25/0.19/0.15 ⇒ p ≈ 2.7–2.8). Steps: seed-gauge check ⇒ singular gauge re-smoke ⇒ if still slower than (ρ/ℓ)⁴, Aethon's flat-space Dirichlet BPST comparison.
- [rev 12] [Helios, check; amended per NanoRibbon] note: singular gauge is singular at the centre (the tip site at d₀ = 0). The graded d₀ = 0 rows use the exact path-ordered holonomy for the centre links, with its convergence reported. The a/2 offset is a labelled control row only, reported side by side, never an alternative for graded rows.
- [rev 12] Spec gaps 1–4 accepted as [assumed]: ring ℓ = (M_r − ½)a with site counts 80 400 / 138 816 / 328 704 / 641 600; tip dual disc a/4 with tip triangles as 1×1 at weight 1; Wilson-only at r < 2a, no 2×2 at the faces, uncorrected O(a²) edge error reported; seed bootstrap for the gate's order error. Helios note: face distances and ρ/ℓ labels shift by the ½a (report-only).
- [rev 12] IT1: the absolute +2/35 sign gate is now NOT COMPUTED (YET) and report-only (face pull ≈ 100× the signal); IT1 graded only via Δ(α) at the same ℓ and seed; guard added: the α = 1 face pull, run twice, must reproduce seed-for-seed to better than E_Δ/3, else IT1 is report-only.
- [rev 12] IT4 fit: every live fixed p = 4 (IT2 tolerance, IT4 fit and residual rule, undecided line, J4, K4) replaced by p_box [measured, smoke], frozen before the Hessian runs. History lines are kept as written.

## CONE_SIM_SPECS rev 12 (27CC9F84 → 874DA694; record edit, Venus's guard-run rulings)
- Header: rev 12, from 27CC9F84. Aethon's hashes: run.py 59978A1F, README 9E53FE7D, STATUS 85835182, xi_guard.py DC3CF39D, gauge_sector.py 52997D2A, scratch JSON 7F10C33A.
- C4/HP2: the 5-vs-10/λ_min guard PASSED (scratch): C4 counts 7 = 7 and 4 = 4, max diff ≤ 7.3e-12; all 24 HP2 rows match. Correction: the n = 1 gap is 1.2527e-1, not 4.73e-2, with 3 gauge modes below it at ξ = 1.
- Stationarity before any Hessian [Venus]: leftover gradient ≤ 1/10 of the smallest non-zero |λ| and ≤ τ₀/10 for counted modes [Helios refinement]; gradient reported per row; failing cases are report-only; gauge-mixing flag rerun at the stationary point (if still raised: real, report-only); μ(α)/μ(1) (0.685, 0.368) report-only until then; n = 2 −3.1e-5 mode rechecked.
- Gap rule: 'first eigenvalue above 100× the lowest' retired. τ₀ = 10 × the largest |λ| of the α = 1 control's known zero modes, on the same grid. Count |λ| ≤ τ₀; any eigenvalue in [τ₀/3, 3τ₀] ⇒ undecided; τ₀ frozen before any α < 1 row; control count ≠ known ⇒ τ₀ NOT COMPUTED (YET), counts report-only.

## CONE_SIM_SPECS rev 13 (874DA694 → D200835C; record edit)
- Header: rev 13, from 874DA694 (Venus confirmed rev 12, including the Helios refinement).
- C4 τ₀ rule: α = 1 control stop added [Venus]: relax until a 10× gradient cut changes the largest control zero-mode |λ| by < 2×, then freeze τ₀; report each (gradient, largest zero-mode |λ|) pair. Helios note: if the zero modes track the gradient down to the solver's numerical floor, stop there and record it as such.

## CONE_SIM_SPECS rev 14 (D200835C → EE2F24AE; record edit)
- Header: rev 14, from D200835C (Venus confirmed rev 13 and withdrew her floor-stop reasoning; Orion: a τ₀ frozen at the floor while the modes are still falling is too big, so the cutoff is looser).
- C4: [Helios note] amended: a floor-stopped τ₀ is too big while the modes are still falling, so the cutoff is looser. Venus's ruling added: (a) [floor-limited] tag, with the floor value reported with each count it decides; (b) failable test: over the last two gradient cuts, every counted α < 1 mode must fall at least as fast as the control's zero modes, with fall factor per 10× cut ≥ ½ of the control's [Helios, assumed]. A levelling mode is listed as a candidate lifted mode and that count is undecided; passing counts stay gradable.
- 'Floor only makes the cutoff tighter' wording: not present outside the revision history (checked); nothing to remove.

## CONE_SIM_SPECS rev 15 (EE2F24AE → 58429B51; record edit)
- Header: rev 15, from EE2F24AE.
- C4 (b): tolerance line replaced [Venus]: log(mode fall factor) ≥ ½·log(control fall factor) per 10× gradient cut, AND mode fall factor ≥ 2. Reason recorded: floor-limited control fall ≈ 2× would make the half-rate rule pass a levelled mode (½ × 2 = 1×).

## CONE_SIM_SPECS rev 16 (58429B51 → 825ECD27; record edit)
- Header: rev 16, from 58429B51. Aethon's stationary scratch run (grid 48): run.py E4C4E2B7, README BBF56F14, STATUS 1334B54A, stationary_check.py 78737914, JSON FA2A0D6B.
- C4 (b): the rev 14/15 gradient-cut fall test is replaced by a grid-refinement fall test [Venus + Aethon, hive proposal adopted] on grids 48/64/80/96: control observed order p_c; each counted α < 1 mode needs observed order ≥ ½·p_c and fall factor ≥ 2 per grid step [assumed, from rev 15]; a levelling mode is a candidate lifted mode and its count is undecided. Context recorded: solver floor reached (gradient 3e-14 to 2e-13), K = 2 τ₀ = 5.348e-4, K = 4 τ₀ = 4.403e-4; eigenvalues don't move with the gradient at a stationary point; control zero-mode size set by the grid.
- Gauge-sector mixing recorded as NONE: the flag clears in all 4 cases (the earlier flag came from incomplete relaxation).
- τ₀ set per grid from that grid's control [Helios]; control-stop rule kept; a control zero mode within 10× of the solver floor (~1e-13) on any grid makes the fall test undecided [Venus].
- Report-only smoke facts: n = 1 α = 0.75 λ = −1.103e-3 (×2), count 0 undecided; n = 2 α = 0.5 −1.945e-5 (×2), −1.734e-5 (×2), count 4 (resolving the earlier −3.1e-5); μ(α)/μ(1) = 0.684, 0.368; negative α < 1 modes stay [hive proposal, untested] [NanoRibbon].
- Cost ~9–10 h on 4 workers, 2–3 GB (NanoRibbon); order: instanton graded rows first, then the cone run.
- rev 17: l.242 fall rule changed from ≥2 per grid step to ≥2 total over 48→96 (Venus); order ≥ ½·p_c kept per fit.
## INSTANTON_TESTS rev 13 (5DD76953 → 2139A805; Aethon's re-smoke diagnosis + NanoRibbon tip-site + Orion H15 + Venus ruling on offset)
- [rev 13] Header: rev 13, from 5DD76953. Aethon's scratch hashes: run.py 6BAAE14C, kernels.py F07C0646, tests.py CADC16DF (35/35), diag_faces_polar.json 0CD0F950; CHANGES pinned copy 60C9EBD4.
- [rev 13] HOLD: singular-gauge re-smoke → flowed re-smoke. Seed already singular gauge (Aethon); face jump from identity faces on unrelaxed seed (ℓ^−3.0; Cartesian grows 0.171→0.274), not box cost [hive proposal, untested: Aethon]. Unflowed p ≈ 2.7–2.8 report-only artefact. p_box only after short gradient flow; P_BOX = None and IT4 refuses until then.
- [rev 13] Flow: Wilson-type RK3, ε_f = 0.002 [assumed] (0.01/0.005 unstable); stability vs 0.001 on B10 to better than E_Δ/3; fixed t_f = 0.1 a² [assumed]; ≈ 1.35 s/step on B10 [measured, Aethon], ≈ 50 steps.
- [rev 13] ρ estimator: calibrate second-moment (r ≥ 2a) on BPST at ρ = 3, 4, 5a after same flow; correct by true/raw [measured, calibration]; raw 4.0–4.1a for true 3a; if ratio varies > 5% across 3–5a, interpolate and tag.
- [rev 13] Self-duality cut relative: s_meas − s_BPST(same ρ, lattice, flow) ≤ 0.02 [assumed]; absolute 0.02 withdrawn (exact BPST s = 0.074 in 2–4a shell).
- [rev 13] Tip-site centre (NanoRibbon): graded d₀ = 0 ON tip site with exact path-ordered holonomy; between-sites becomes "d₀ = 0 between sites [control]"; tip-site under same per-ε order gate. Must not stay NOT COMPUTED (YET).
- [rev 13] Lanczos for 30 modes on B10+ on the box, not TrinityOrb (Aethon).
- [rev 13] Open check (Orion H15; Aethon confirmed ε=1; Venus ruling): −0.0166 vs eq. (19) −0.0224; gap ≈ 0.0058, box trunc ≈ 0.0008 ⇒ ≈ 0.005 [unexplained, report-only]. Not box truncation. Does NOT block p_box (flat in ℓ) [Venus]. Check [hive proposal, untested: Venus], report-only: repeat at ρ = 4a; if next term after 1/ρ⁴ shrinks by ~(3/4)⁶ ≈ 0.18, else code-side → Aethon (H5). ε = 0 face rows NOT COMPUTED (YET).
- [rev 13] NOT COMPUTED (YET): Cartesian wedge row and Windows peak-memory probe. (K10–K12 added.)

## INSTANTON_TESTS rev 14 (2139A805 → 931AE72A; Venus ruling on p_box from Aethon's flowed re-smoke)
- [rev 14] Header: rev 14, from 2139A805. Aethon's flowed re-smoke hashes: run.py 4AE63C1B, lattice.py 008F11EB, kernels.py F07C0646, summary 9CF62C66, STATUS_REV13 98B3FB00 (28 rows B10–B20 at α = 1).
- [rev 14] Flowed re-smoke: t_f = 0.1a² does NOT heal the face jump. p_box [measured, flowed smoke] = 3.006±0.025 at ε = 1, 2.82–2.90 at other ε; S∞ = 0.9827 at ε = 1; outer-ring share on B10 0.055 (flowed) vs 0.083 (seed). Still the ρ⁴/(aℓ³) artefact.
- [rev 14] Longer flow REJECTED [Venus]: √(8t) ≈ 0.9a can't heal a jump at ℓ = 10–20a (needs t ≳ 12a², which shrinks the instanton). t_f stays at 0.1a².
- [rev 14] Rule: freeze p_box per ε at the measured value with its error [measured, flowed smoke], tagged [face artefact ρ⁴/(aℓ³), not physical box cost]. Used only to extrapolate ℓ → ∞; check: must reproduce S∞ = 0.9827 at ε = 1. Graded quantity stays Δ(α) (same-grid difference; face term cancels to the extent it doesn't depend on α); guard is the existing α = 1 seed-for-seed rule. Replaces the "P_BOX=None until flow" HOLD: after Venus confirms rev 14, Aethon freezes P_BOX and releases the graded rows.
- [rev 14] Clarification (Venus, from the rev 13 confirm): the p_box fit takes ρ/ℓ from the corrected flowed ρ, not the seed ρ.
- [rev 14] Can-fail check [hive proposal, untested: Venus]: if the face term goes as 1/a, then at fixed ℓ/ρ the excess must scale like a when a is halved (e.g. B10 at ρ = 3a vs B20 at ρ = 6a). If it doesn't, the artefact reading is wrong and p_box goes back to UNDECIDED.
- [rev 14] Other smoke results (report-only): s − s_BPST ≤ 0.009 (all rows pass 0.02 cut); flow step 0.002 vs 0.001 gives dS = 2.8e-9, action fell monotonically (E_Δ/3 test NOT COMPUTED (YET) until α < 1 rows); tip-site vs between-sites agree to 2e-5 on B20, holonomy converged to 4e-6 at 16 steps; ρ calibration true/raw varies 12–21% over 3–5a → interpolated and tagged; eq.(19) residual ratio at ρ = 4a is 0.36, not 0.18 → polar tip-core offset (fit c₄ ≈ 0.39; Cartesian 0.0004) [unexplained, report-only]. Cost: ≤ 57 s/step on B20, peak 0.9 GB.

## INSTANTON_TESTS rev 15 (931AE72A → 50B5BC50; Venus ruling on 1/a fail + t_f = ρ²/90; Orion H15 cleared IT1; NanoRibbon IT3 cost go after cone)
- [rev 15] Header: rev 15, from 931AE72A. Aethon's 1/a check FAIL hashes: run.py 1F27F720, lattice.py 35E9E049, inv_a_check.json 4EA9B36B (STATUS_REV14 28B31A6D).
- [rev 15] 1/a check FAIL recorded (rev 14 run, Aethon; stays on the record): α = 1, ε = 1, tip-site; B10 at ρ = 3a vs B20 at ρ = 6a; flowed excess ratio 1.446 vs 1.850 (1/a model) and 0.925 (a-independent), 22% off, outside 15% band; unflowed seed ratio 1.648 would pass at 11%; S∞ 0.98274 vs 0.9827, passes. Cause [Venus]: t_f fixed in lattice units ⇒ B20 got 4× less flow relative to ρ²; check badly designed, not tuned after the fact.
- [rev 15] Wording fix [Venus]: the ρ⁴/(aℓ³) model grows like ρ/a at fixed ρ/ℓ, so the excess scales like 1/a, not "like a". The rev 14 sentence was backwards; Aethon tested the right thing.
- [rev 15] Flow time: t_f = ρ²/90 [assumed, frozen now; Venus] (0.1a² on B10, 0.4a² on B20), applies to every graded row and the rerun. Lattice-unit t_f = 0.1a² WITHDRAWN for graded rows. Rerun the 1/a pair at this t_f with the same 15% band; if it fails again, p_box stays UNDECIDED and IT4 does not run. IT4 reads P_BOX only after the rerun passes. IT1 and IT3 do not need p_box.
- [rev 15] IT1 clearance: Orion (H15) cleared IT1 — eq. (19) holds at ε = 1. IT1 may run.
- [rev 15] IT3: three grids B12/B16/B20 (Richardson); ε = 0 [assumed, Helios] with ε = 1 labelled control on B16 only; |Q − 1| ≤ 0.05 after flow [assumed, Helios]; target-ρ stop → fixed t_f = ρ²/90; header/rule mismatch N2/N3 vs B16/B20 fixed to B12/B16/B20 throughout. NanoRibbon cost go for 15–20 h, effective once Venus confirms rev 15; IT3 runs AFTER the cone --full. Order: 1/a rerun → graded rows (IT1, plus IT4 if rerun passes) → cone --full → IT3. Three-grid cost NOT COMPUTED (YET); Aethon re-estimates; if > ~20 h, post the figure before it runs.
- [rev 15] Audit (report-only): 35 tests not yet re-run on the new code; cone seed not unit-tested; both must be done before graded rows. NOT COMPUTED (YET): Cartesian wedge row and Windows memory probe.

## INSTANTON_TESTS rev 16 (50B5BC50 → 378EE8E5; second 1/a FAIL + measured cost + NanoRibbon cuts and run order)
- [rev 16] Header: rev 16, from 50B5BC50. Aethon's hashes: run.py 223559B3, tests.py 216BFCF3 (47/47), STATUS_REV14 1A547BB5, inv_a_check_rho_tf.json AE205D82.
- [rev 16] Second 1/a FAIL recorded (rerun at t_f = ρ²/90, Aethon, scratch): flowed excess B10 0.06351 vs B20 0.06589, ratio 1.037 vs 1.850 (1/a), 44% off; 12% from 0.925 (a-independent) ⇒ looks like a real box cost [Aethon reading, needs Venus ruling]; S∞ 0.98274 passes. p_box stays UNDECIDED; IT4 HELD pending Venus (UNDECIDED-without-extrapolation, drop, or re-read as box cost); IT4 out of the run order.
- [rev 16] Measured cost (Aethon, TrinityOrb, 3 workers): ≥ 27.6 s/step on B16 at ε = 0; IT1 as specced ≈ 520 h (on-tip > 250 h); IT3 three-grid ≈ 42 h (lower bound). Rule (NanoRibbon): everything on TrinityOrb, nothing on the box.
- [rev 16] IT1 cut [cuts assumed, Helios]: ε = 0 only, tip-site only, 6 seeds, a-series at ρ/ℓ = 0.3 on B10/B12 (B16 dropped on cost ⇒ order gate 2-grid, report-only), window ρ ≤ 0.4ℓ [assumed; Venus to confirm]; ≈ 5.6 h [estimate, scaling assumed]. ε = ±1, −0.25, off-tip and between-sites rows deferred, NOT COMPUTED (YET).
- [rev 16] IT3 cut [cuts assumed, Helios]: B10/B12/B16, ε = 0 only (ε = 1 control deferred), one row at ρ/ℓ = 0.3 (ρ = 3, 3.6, 4.8a), 8 seeds; ≈ 16.2 h [estimate, scaling assumed].
- [rev 16] Run order (NanoRibbon): B16 point → cone --full (9–10 h) → cut IT1 → IT3. Runs over a few hours need a start time agreed with Akitti through NanoRibbon; cost estimates posted before any launch.
- [rev 16] Audit: 47/47 pass. Pending fixes (no result change): duplicated tests.py block, trivial α = 1 cone_seed test, stale rev 13 HOLD string. NOT COMPUTED (YET): Cartesian wedge row, Windows memory probe, E_Δ, graded IT1 runner.

## INSTANTON_TESTS rev 17 (378EE8E5 → BB71AAC3; record-only, Venus rulings 01:10 2026-10-16)
- [rev 17] Header: rev 17, from 378EE8E5. Record-only; Venus rulings (01:10, 2026-10-16).
- [rev 17] [Venus ruling] IT4: report-only per box, with NO ℓ→∞ extrapolation; not dropped; run order after IT3 (deferred for cost). p_box stays UNDECIDED; P_BOX does not freeze.
- [rev 17] [Venus ruling] K14(a) accepted: graded rows all sit at ρ/ℓ = 0.3, so 0.4ℓ is only an outer window limit.
- [rev 17] [Venus ruling] K14(b) accepted with one condition: over ρ/a = 3, 3.6, 4.8 step ratios are only 1.2 and 1.33 ⇒ IT3 must report observed order; Richardson at p = 4 only if observed order ∈ [2, 6], else IT3 UNDECIDED.
- [rev 17] [Venus ruling] K14(c) accepted: consistent with the B16 ρ/ℓ-only test; Δ(α) cancels the box cost only if that cost doesn't depend on α; α = 1 guard covers that.
- [rev 17] [Venus ruling] Cut IT1 graded on Δ(α) only; E_Δ from the 6-seed α = 1 repeat; 2-grid order gate report-only.
- [rev 17] Cost estimates (IT1 ≈ 5.6 h, IT3 ≈ 16.2 h) stand pending Aethon's re-cost. K14 CLOSED.
- [rev 17] Run order: B16 point → cone --full → cut IT1 → IT3 → IT4 (report-only).

- Rev 18 (2026-10-16): IT1 guard repeat now uses 6 paired seed perturbations; E_Δ uses σ_pair²/6; unflowed-BPST ρ calibration accepted as an H3 deviation; δ validity rule added. Record-only.

- Rev 19 (2026-10-16): δ=0.02 per-link rejected, smooth perturbation with ρ≤5% and nonzero-spread conditions; pre-flow time kept separate from t_f; Q gate read at t_f; guard uses unpaired 3σ₁√(2/3); RNG-stream pairing with a 0.5 correlation fallback; calibration log-slope term. Record-only.

- Rev 20 (2026-10-16): 6+6 wording fix; IT1 Q gate on |Q_δ−Q_0| alone [rule changed after smoke data]; failable δ=0 control per α; IT1 cost ~11–12 h. Record-only.
