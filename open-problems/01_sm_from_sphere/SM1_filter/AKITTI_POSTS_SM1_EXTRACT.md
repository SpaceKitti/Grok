# AKITTI_POSTS_SM1_EXTRACT: what Akitti's Oct 1–8 X posts say for JOB_SM1

Helios, 2026-10-08 (BST). Box file only. No spec edited, nobody messaged, X not touched.

**Inputs (SHA-256 checked):** `AKITTI_POSTS_OCT1-8.md` F1C6CC26 (153 posts); `AKITTI_POSTS_OCT1-8_QUOTED.md` 674F5BAF (quoted posts, media index, 1 Article); `AKITTI_FRAMEWORK_2026-10-08.md` 6CD5F259; `JOB_SM1_FILTER_SPEC.md` 3D19F785. Media stills were viewed with Read (`akitti_posts_media/`). Akitti is she/her.

**How to read the quotes.** Every quote sits between « and » and is copied character for character from F1C6CC26 (or from 674F5BAF where marked [quoted]). An automatic check at the end confirms each «…» string is in the source. Words outside « » are mine.

**Akitti's own framing (relayed by NanoRibbon, Oct 8):** the posts are her pattern-mapping and research done together with Grok. Nothing in them is formally derived, and parts may be Grok hallucinations.

**Attribution tags (one per quote):**
- **[Akitti]**: her own words. Short, casual, first-person posts and replies (typos, her voice).
- **[Akitti-account post, authorship unverified]**: a long, formal post on her account. The API can't tell whether she wrote it or pasted it. Where the text has assistant-style markers (it talks to "you" about "your simulation", ends with "would you like…", "You're right—I inverted the point", calls her "Akitti" in the third person), I list the markers, but I don't call it AI text unless she or the text says so.
- **[Akitti-shared AI text]**: used only where there's direct evidence. Either she says so (2107576486328754344: «I just had grok compile it into one post so I could think»), or it's a screenshot of a Grok answer.
- **[quoted]**: another account's post (from 674F5BAF).
- **[hive-interpretation]**: my reading. Never inside « ».

**Check flags (one per technical claim):** **VERIFIABLE** (standard physics or a cited paper we can check) · **HER PATTERN/IDEA** (keep as an [Akitti] direction, not a result) · **POSSIBLY GROK-HALLUCINATED** (a specific number, formula or "result" with no source, e.g. scored survivor lists).

**PROVISIONAL** marks anything whose meaning still depends on a post, image or video we don't have. These are listed in §7.

**Line-1200 attribution (as instructed):** post 2106801517357351243 (2026-10-04 18:39:58 BST, top-level, quotes her own 2106768405814550691) is tagged **[Akitti-account post, authorship unverified]**. Its framework block (lines 1153–1191) matches 6CD5F259 word for word, apart from the LaTeX vs plain-text maths formatting (checked with diff). Its tail, the "current schematic S²/lattice zero-mode list" with three survivor classes (lines 1193–1204), is in the same post. Those classes appear below only as candidate hosts or modes: PROVISIONAL and not graded. The quoted 2106768405814550691 is her own post, so it is in F1C6CC26 (lines 1044–1143), not in the QUOTED file. 674F5BAF has only its video still (stylised art, see §10). The line-1215 reply 2106829842167804113 is tagged [Akitti].

---

## 1. Q1–Q16: do her posts answer them?

Summary table (details and quotes below):

| Q | status | whose words carry it |
|---|---|---|
| Q1 core disk | PARTLY | [Akitti] + unverified long posts |
| Q2 Π | PARTLY | unverified long post only |
| Q3 U(1)_X vs MHD B; Ψ values; pressure | SILENT on values and pressure; PARTLY on separation (unverified) | — |
| Q4 μ, G, α values | SILENT | — |
| Q5 r_c, r_c/R | SILENT (meaning PARTLY, unverified) | — |
| Q6 what sources μ | PARTLY | [Akitti] + unverified |
| Q7 zero modes and T_tt | SILENT ([Akitti]); one unverified line | — |
| Q8 "shifts either integral" | PARTLY (absolute-residual form) | unverified |
| Q9 T_zz, J, I_z | SILENT | — |
| Q10 HELD list | SILENT | — |
| Q11 three families a gate | SILENT ([Akitti]) | — |
| Q12 (Venus) tachyon rule | SILENT | — |
| Q13 warped throat as host | SILENT ([Akitti]) | — |
| Q14 Goldberg lattice as host | PARTLY | [Akitti] |
| Q15 tolerance τ | SILENT (code tolerances are illustrations only) | — |
| Q16 (Venus) irreducible 6D anomaly | SILENT on the rule | — |

### Q1: what is the core disk D_{r_c}? — PARTLY
- 2106768405814550691 (Oct 4 16:28 BST) [Akitti-account post, authorship unverified; assistant-style markers: «Use the integral as a check on the branch you already simulated»]: «Let the branch locus be a line, and let \((r,\phi)\) be polar coordinates in a transverse plane, with \(\phi\sim\phi+2\pi\). Outside a core radius \(r_c\) the simulated geometry is the cone». Flag: the cone metric is **VERIFIABLE** (standard cosmic-string transverse geometry). Using it as *her* simulated exterior is **HER PATTERN/IDEA**.
- 2107582409306771923 (Oct 6 22:22 BST) [Akitti]: «The cone singularity literally formed when I ran simulations.  There's two cones because a string has two end points. Analogously similar to Hořava–Witten.» Flag: **HER PATTERN/IDEA**. No simulation output, plot or code is posted in Oct 1–8, and none of the 32 video stills shows one (§10). The parent post it answers is now in 674F5BAF as [quoted] Millbstrd 2107579938681319654: «2 tips, and the figure 8 seem forced».
- 2107219672017842217 (Oct 5 22:21 BST) [Akitti]: «S^2 Bubble -> branching singularity of mhd + quantum gravity lives on this bubble,l -> strings form -> strings pile up -> string tension from pileup causes cone singularity -> flattens to r^2». Flag: **HER PATTERN/IDEA**.
- 2107537800610607257 (Oct 6 19:25 BST) [Akitti-shared AI text: she says in 2107576486328754344 «I just had grok compile it into one post so I could think»]: «Pairing rule: the figure-8 pinch is the core of a co-dimension-2 defect; the \(S^2\) is its wrapping cycle; the background chart still stops at finite radius.» Flag: **HER PATTERN/IDEA**, in Grok's wording.
- [hive-interpretation] The core disk is the transverse disk around a codimension-2 branch locus inside her simulation. That supports reading "core disk" as a transverse disk (spec Reading II / 2-tip style), not the spec's default rugby-ball internal tip. Nothing she says picks one geometry from the spec's list. «two cones» together with «two end points» argues *for* 2-tip constructions (§3).

### Q2: what is Π? — PARTLY
- 2106768405814550691 [Akitti-account post, authorship unverified]: «MHD exterior. There is a restriction \(\Pi\) from core data to the MHD fields such that» … «as traces on the matching circle. The branch is then one configuration read in two regimes.» Flag: **HER PATTERN/IDEA**. No formula for Π is given anywhere.
- The field list is only what the framework already says: velocity, magnetic field, density (line 1161, identical to 6CD5F259).
- [hive-interpretation] "restriction" plus "traces on the matching circle" is closest to the spec's Π-a (pointwise restriction/trace). Nothing in the posts rules out Π-b or Π-c. Venus's interpretation is not contradicted.

### Q3: U(1)_X vs MHD B; values of Ψ|r_c; pressure — SILENT on values and pressure
- No numbers for v, B or ρ on r_c appear anywhere. The only "values" are placeholders in [Akitti-shared AI text] code in 2106881531725652263: «mhd_trace = {"v": 0.0, "B": 0.0, "rho": 1.0}  # on r = r_c». Flag: **POSSIBLY GROK-HALLUCINATED**, at best an illustration. Do not use as input.
- Separation of the fluid and gauge readings, from 2106721095835341008 (Oct 4 13:20 BST) [Akitti-account post, authorship unverified; third-person «hive» register]: «The name “Clebsch” lands on two different mathematical objects. Fluid Clebsch variables are a classical velocity potential.» and «One table, three readers. The fluid layer is not called.» The first sentence is **VERIFIABLE** (standard terminology). The «three readers» table is **HER PATTERN/IDEA**. [hive-interpretation] This keeps fluid (MHD) variables out of the gauge/CG reading, which loosely backs the spec's default that the MHD B is not identified with any U(1)_X. Weak evidence.
- Pressure: never mentioned.

### Q4: values of μ (or Gμ), G, α — SILENT
- 2106881531725652263 [Akitti-shared AI text] code: «mu = 0.05          # measured string tension». **POSSIBLY GROK-HALLUCINATED**: a placeholder, not a measurement. G is never given a value.
- 2108178649320943947 (Oct 8 13:52 BST) [Akitti-account post, authorship unverified] code default «def hive_instanton_residuals(alpha=0.8, eps_EP=0.513681, IE=0.299,». **POSSIBLY GROK-HALLUCINATED** (α=0.8 is a default argument). Also not on topic: this is the parked instanton/MSS layer.
- The repeated "numerical locks" «\(\varepsilon_{\rm EP}\approx0.513681\), \(I_E\approx0.299\), \(\lambda_{\rm EP}\approx-0.3084\,i\)» and «scar floor \(\sim 0.041\)» are **POSSIBLY GROK-HALLUCINATED** (no derivation or source in Oct 1–8; they're cited as «previously posted»). They are also not SM1 inputs. → Missing-post list §8: where they were first posted.

### Q5: r_c and r_c/R — SILENT (meaning only)
- No value. 2107537800610607257 [Akitti-shared AI text]: «That pinch is a local core diagnostic, not the background radial origin of the deathface.» [hive-interpretation] The core radius r_c (finite-radius matching circle) and the "deathface" finite-radius stop are kept separate as loci. No ratio to R is given.

### Q6: what sources μ (string count, endpoint tensions, T_b) — PARTLY
- 2106848956730785938 (Oct 4 21:48 BST) [Akitti]: «@Millbstrd The wedge is a deficit angle and it is automatic from the tension. Tension happens when a string becomes infinitly long or when too many strings pile up together. In our hive example it is strings piling from s^2 -> r^2». Flag: "deficit is set by tension" is **VERIFIABLE** (α = 1 − 4Gμ for a straight cosmic string; Vilenkin 1981; Deser–Jackiw–'t Hooft 1984 for 2+1 point masses). "Pile-up from S²→R² sources it" is **HER PATTERN/IDEA**.
- 2106142937948324193 (Oct 2 23:03 BST) [Akitti]: «Adding flux alone never makes a cone. You'd only get one if a string with tension sat at the tip & pulled on the shape.» Flag: **HER PATTERN/IDEA**. Loosely consistent with GR: a deficit needs a localized T_tt, and flux can only contribute through its own energy density. It is not a theorem as stated.
- 2107224531714670767 (Oct 5 22:40 BST) [Akitti-account post, authorship unverified; assistant marker «So the sequence that was catching you»]: «\mu_i=\sum_{a\in E_i}t_a,\qquad» with «where \(E_i\) is the set of endpoints on tip \(i\), \(t_a\) is the tension contributed by endpoint \(a\)». Flag: **POSSIBLY GROK-HALLUCINATED** as a formula. The sum rule is a natural ansatz with no source. The paired «1-\alpha_i=\frac{1}{2\pi}\sum_{a\in E_i}q_a,» is also unsourced, and it is inconsistent with α = 1 − 4Gμ unless q_a = 8πG t_a, which the post doesn't say.
- T_b normalization: SILENT.

### Q7: which zero modes enter T_tt — SILENT (Akitti); one unverified line
- 2106881531725652263 [Akitti-shared AI text]: «the stress integral collapses to the summed \(T_{tt}\) of the retained modes». **POSSIBLY GROK-HALLUCINATED** as a rule, since zero modes carry no classical T_tt without a state. Not her statement.

### Q8: "shifts either integral": absolute or relative? — PARTLY
- 2106768405814550691 [Akitti-account post, authorship unverified]: residuals «\mathcal{R}_\alpha&=\Bigl|\int_{D_{r_c}}R\,dA-2\pi(1-\alpha)\Bigr|,\\» and «(or below a fixed numerical tolerance). A core that changes the exterior angle, or that cannot be read as the MHD configuration on \(r=r_c\), is rejected.» [hive-interpretation] These are absolute targets against the fixed exterior, which matches the spec default. Flag: **HER PATTERN/IDEA** (her filter design). The integral identity itself is **VERIFIABLE** (see §4 C2).

### Q9: T_zz, J, I_z — SILENT.
### Q10: HELD candidates — SILENT. (The framework line «Output only the survivors.» is unchanged.)
### Q11: are three families a gate? — SILENT (Akitti). [Akitti-account post, authorship unverified] 2107799344195760276 (Oct 7 12:44 BST) talks about generation number from fixed points (**VERIFIABLE** as standard heterotic orbifold lore), but it sets no gate.
### Q12 (Venus): tachyon rule — SILENT.
### Q13: warped throat as a host — SILENT (Akitti). Throats appear only inside [Akitti-shared AI text] in 2106881531725652263 as a back-reaction illustration.
### Q14: Goldberg lattice as a host — PARTLY
- 2105731792439247111 (Oct 1 19:49 BST) [Akitti]: «On my computer the simulations im running im not using the GoldbergHexa to run rhings because everything is running fine with just regular s^2 physics constructions... The goldberghexa was just a lattice to help me probe and organize things but i may need to add it in to the simulations as well to fix stuff..» Flag: **HER PATTERN/IDEA**. [hive-interpretation] The Goldberg lattice is an organizing probe, not a physical host, which matches the spec's "probe, not candidate". Tension with Gate 0: see §4 C3.
- Same post [Akitti], scope: «Im going to attempt adding the standard model in a non ad-hoc fashion this weekend to the hive construction.» (the weekend was Oct 3–4). Also the open-problem order: vacuum selection after SM, Stelle/LQC next, membranes «the hardest». This matches the framework's priority list.

### Q15: tolerance τ — SILENT. All tolerances in the posts are code defaults (e.g. «def wall_closes(a1, mu1, a2, mu2, q, t, tol=1e-8):», 2107591866921177245 [Akitti-account post, authorship unverified]). **POSSIBLY GROK-HALLUCINATED** as values. Not inputs.
### Q16 (Venus): irreducible 6D anomaly — SILENT on the rule. Green–Schwarz anomalous U(1)s are discussed in [Akitti-shared AI text] 2106881531725652263 / 2107056665161867400 (**VERIFIABLE** as standard physics), but no reject rule is given.

### Her stance on the filter (attribution check for the line-1215 reply)
- 2106829842167804113 (Oct 4 20:32 BST, reply to a post we don't have, 2106828033017413645) [Akitti]: «No, this just is an analytic tool that constrains what is happening so I can find the mirror port for quantum gravity. And strings cannot be the same because different strings map to different particles. String ≈ particles and not all particles are the same. So think of this more as a selection method.» Why [Akitti]: short, casual, first person, «mirror port», no assistant markers. Flag: **HER PATTERN/IDEA**. [hive-interpretation] The filter is a selector, not a derivation, which supports the spec's survivors-only output. «different strings map to different particles» means string labels have to stay distinct per candidate (bears on the μ_i decomposition, Q6). PROVISIONAL until we have what she was saying «No» to (§7).
- 2106850162010185866 (Oct 4 21:53 BST) [Akitti]: «@Millbstrd Yes but only after we add the knobs at the tip for the standard model. (Theoretically speaking) I mean it could all turn out to be wrong. I need to build simulations to be sure of the right path.» PROVISIONAL: we don't know what she says «Yes» to.
- 2107583263963480253 (Oct 6 22:26 BST) [Akitti]: «nothing. Nothing happens because of all the open problems. I already have Einstein's equations embedded.» and 2107879215366557809 (Oct 7 18:02 BST) [Akitti-account post, authorship unverified; polished first-person, plausibly hers]: «Einstein’s equations are already embedded in this framework, but they inherently break down during these trans-Planckian transitions.» → bears on §4 C1.


---

## 2. Physical parameter values

**No usable values in Oct 1–8.** No post gives μ, Gμ, G, α, r_c, R, Ψ|r_c, T_b or τ. Every number that looks like an input is a code default or placeholder inside long unverified or AI-shared posts. All are flagged **POSSIBLY GROK-HALLUCINATED** and must not be entered into SM1:

| symbol | number in posts | where | why not usable |
|---|---|---|---|
| μ | «mu = 0.05          # measured string tension» | 2106881531725652263 [Akitti-shared AI text] | placeholder, G undefined |
| Ψ|r_c | «mhd_trace = {"v": 0.0, "B": 0.0, "rho": 1.0}  # on r = r_c» | same | placeholder |
| α | «alpha=0.8» default in «def hive_instanton_residuals(alpha=0.8, eps_EP=0.513681, IE=0.299,» | 2108178649320943947 [unverified] | default argument; parked instanton layer |
| tol | «tol=1e-8» in «def wall_closes(a1, mu1, a2, mu2, q, t, tol=1e-8):» | 2107591866921177245 [Akitti-account post, authorship unverified] | code default |
| "locks" | «\(\varepsilon_{\rm EP}\approx0.513681\), \(I_E\approx0.299\), \(\lambda_{\rm EP}\approx-0.3084\,i\)», «scar floor \(\sim 0.041\)» | 2108178649320943947, 2107537800610607257 | no source in this window; not SM1 inputs |

Asks are unchanged: α_ext (or Gμ), G convention, r_c, R, Ψ|r_c (with units), the Π definition, T_b. Only Akitti or her simulation can supply them.

---

## 3. New constructions that would change the candidate list (all PROVISIONAL, none graded)

**N1. Two-tip / double-cone host with a matching wall.** 2107224531714670767 [Akitti-account post, authorship unverified]: «Cones on both ends remove the “afterward” step by giving each side its own tip stratum.» and «Place one cone at the branching locus and a second cone at the opposite end of the bubble wall. Each tip carries its own deficit and tension,». Her own words back the direction in 2107582409306771923 [Akitti]: «There's two cones because a string has two end points. Analogously similar to Hořava–Witten.» Flags: the *direction* is **HER PATTERN/IDEA**. The post's per-tip formulas, the wall condition «\mu_1\big|_W=\mu_2\big|_W,\qquad» and the mass rule «All other modes acquire a mass squared proportional to the mismatch \((\alpha_1-\alpha_2)^2+(\mu_1-\mu_2)^2\)» are **POSSIBLY GROK-HALLUCINATED** (no derivation or source). [hive-interpretation] For SM1: (a) add per-tip residuals (R_α,i, R_μ,i) where a candidate has two tips. (b) A rugby-ball-type candidate is a natural match for the *count* of tips, but her tips sit in the transverse plane of a branch locus and may carry different (α_i, μ_i). The spec should ask Akitti whether unequal tips are allowed or whether the wall forces equality.

**N2. Hořava–Witten conical interval.** 2107799344195760276 (Oct 7 12:44 BST) [Akitti-account post, authorship unverified; third-person «the @Akitti hive»]: «Gravity remains free to propagate in the bulk; the Standard-Model-scale gauge fields and chiral matter are anchored at the two fusion points where the cone tips meet the \(E_8\) walls.» Flags: the HW setup, «Anomaly cancellation still requires one \(E_8\) vector multiplet on each wall», and the E8 maximal subgroup chains are **VERIFIABLE** (Hořava–Witten 1996; standard heterotic model building). Putting SM matter at "cone tip × E8 wall" fusion points is **HER PATTERN/IDEA** (direction backed by her «Analogously similar to Hořava–Witten.»). [hive-interpretation] This is a possible host class if the spec doesn't already have M-theory-on-interval / heterotic orbifold-at-tip candidates. It is not a computed candidate.

**N3. Second flux quantum on the S² bubble (flag manifold).** 2108092102886211700 (Oct 8 08:08 BST) [Akitti-account post, authorship unverified; third-person hive register], citing arXiv:2610.08939: «On the hive the existing S^{2} bubble sources its tension from a single string pile-up,» … «\epsilon=\epsilon\Bigl(\frac{n_1}{n_2}-\alpha\Bigr),\qquad\mu=\mu_{\mathrm{crit}}(1+\epsilon).» Flags:
- **VERIFIABLE (checked against the abstract and full text, arXiv:2610.08939, Menet–Tomasiello–Van Hemelryck, "Non-supersymmetric M-theory vacua and dark bubbles"):** AdS₅ × flag-manifold F₆ vacua with two G₄ flux quanta (n₁, n₂). M5 bubbles wrap a two-cycle and get near-extremal by tuning n₁/n₂ close to an irrational value, giving R⁻¹ ~ Λ₄^{1/4}. The AdS₅×S² uplifts from 7d gauged sugra are perturbatively unstable and give only R⁻¹ ~ Λ₄^{1/2}. The post's table line «| section-4 \(S^2\) uplifts | existing single-parameter bubble | mark unstable, do not promote |» matches the paper's Sec. 4 result.
- **POSSIBLY GROK-HALLUCINATED:** the mapping onto her tension (μ = μ_crit(1+ε)). The paper's ε is the M5 *tension* deviation, σ = σ_crit(1−ε) (a sign difference), not a string pile-up tension. The code default «def near_extremal(n1, n2, alpha=np.sqrt(2), tol=1e-3):» uses √2, but the paper's target is n₁₂(p₁) ≈ 0.795888 (an algebraic number of degree 8), not √2.
- [hive-interpretation] For SM1: if the spec has any AdS₅×S² M-theory/7d-sugra uplift candidates, the paper is a checkable reason to downgrade them (perturbative instability). The "second charge" idea itself is not yet an SM1 candidate.

**N4. The line-1200 "survivor" classes (2106801517357351243 tail).** [Akitti-account post, authorship unverified]: «Chiral spin-2 magnetoroton», «Lattice chiral edge modes (left-handed doublets / right-handed singlets) localized on distinct radial shells of the GoldbergHexa hierarchy», «Transverse-traceless helicity-\(\pm2\) modes of the locked Hessian (Gate A).», each ending in a claim such as «Residuals vanish.» Flag: **POSSIBLY GROK-HALLUCINATED.** It is a scored survivor list with no computation, no inputs (Q4 is empty) and no code output. The chiral spin-2 magnetoroton is a **VERIFIABLE** physical mode (Liang et al., Nature 628, 78 (2024), "Evidence for chiral graviton modes in fractional quantum Hall liquids"; her 2106510530278019502 discusses it). Treating it as an SM1 zero mode is not standard. [hive-interpretation] Don't add these as SM1 candidates or treat them as a pre-run. Only class 2 (L-doublets / R-singlets) resembles SM chiral content, and that's a schematic label. The same list is repeated as «The survivors are exactly the three classes listed in the October notes» in 2106881531725652263 [Akitti-shared AI text]. That's circular, not confirmation.

**N5. Local D3-branes at a CY₃ cone singularity ("SM on open-string endpoints at the tip").** 2106881531725652263 [Akitti-shared AI text, with Google-style citation markers «[1, 5, 6, 7]» and «To help tailor the next steps for your quantum gravity probe, could you clarify:»]: «Because the Standard Model lives on open string endpoints confined to the tip of your cone, it acts as a "gauge sector."» Flag: the bottom-up D3-at-singularity programme is **VERIFIABLE** (standard: Aldazabal–Ibáñez–Quevedo–Uranga 2000; Verlinde–Wijnholt). Her direction (tip = SM sector) is **HER PATTERN/IDEA**: [Akitti] 2106850162010185866 «only after we add the knobs at the tip for the standard model». [hive-interpretation] Add this class only if the spec lacks it.

**N6. "Three knobs" requirement for an SM spectrum on a cone.** 2106845569306284454 (Oct 4 21:35 BST) [Akitti-account post, authorship unverified]: «A usable quasiparticle spectrum on a cone needs three independent knobs—deficit angle, winding/holonomy, and extra internal degrees of freedom—because a pure geometric tip only sets the local curvature scale and does not by itself produce a tower of states with Standard-Model quantum numbers.» Flag: **VERIFIABLE** in spirit (a bare 2D cone gives only Bessel-index shifts; gauge quantum numbers need internal d.o.f./holonomies, cf. orbifold Wilson lines). [hive-interpretation] This supports the spec's demand that each candidate specify holonomy + internal data, not geometry alone.

---

## 4. Contradictions and tensions with the spec / framework

**C1. GR use vs "never put GR in as the answer".** 2106768405814550691 [unverified]: «The deficit parameter is not free: if \(\mu\) is the integrated string tension measured in the simulation, the Einstein equation on a transverse disk fixes» → «With exterior deficit \(\alpha=1-4G\mu\)». Her own words: [Akitti] 2107583263963480253 «I already have Einstein's equations embedded.» and 2107879215366557809 [unverified, plausibly hers] «Einstein’s equations are already embedded in this framework, but they inherently break down during these trans-Planckian transitions.» [hive-interpretation] This is consistent with the framework if GR is used only for the exterior/consistency check (α = 1 − 4Gμ as frozen exterior data) and never to derive the core. The spec should say that explicitly. Flag: α = 1 − 4Gμ is **VERIFIABLE** (Vilenkin 1981; in G = c = 1 units, deficit 8πGμ).

**C2. Curvature normalization (R vs Gaussian K) and the α convention.** The framework and 2106768405814550691 write «R=2\pi(1-\alpha)\,\delta^{(2)}(\mathbf{x}),» and ∫R dA = 2π(1−α). That's correct for the **Gaussian curvature K** of a 2D cone. With R the 2D Ricci scalar (R = 2K), ∫R dA = 4π(1−α). The post's own check «∫DrcR[gcore] dA=8πGμ.» is consistent only with the K reading (deficit 2π(1−α) = 8πGμ). **VERIFIABLE** (Gauss–Bonnet). Separately, 2107224531714670767 [unverified] defines «\alpha_i=1-\frac{\beta_i}{2\pi},\qquad» with β_i the angular range, which makes α_i the *deficit fraction*. Under that definition the deficit is 2πα_i, not 2π(1−α_i), yet the same line writes «\int_{D_i}R\,dA=2\pi(1-\alpha_i),». It contradicts itself and the framework's ds² = dr² + α²r²dφ² (where β = 2πα). Flag: **POSSIBLY GROK-HALLUCINATED** (convention error). → The spec should pin "R ≡ Gaussian curvature K (or write 2K)" and "α = β/2π". This needs Akitti's confirmation.

**C3. Gate 0 vs "regular s^2 physics".** [Akitti] 2105731792439247111: «everything is running fine with just regular s^2 physics constructions». The spec's Gate 0 rejects round S² candidates if α_ext < 1. [hive-interpretation] Not necessarily a conflict: in her chain the S² is the *pre-handoff bubble* («S^2 Bubble -> branching singularity of mhd + quantum gravity lives on this bubble,l» … «string tension from pileup causes cone singularity -> flattens to r^2», [Akitti] 2107219672017842217), and the cone forms at the handoff. Gate 0 should apply to the core-at-the-tip, not to the S² bubble stage. Ask Akitti.

**C4. Core-disk default.** As in Q1: the spec defaults to the rugby-ball internal tip, but the posts describe a transverse disk around a branch line inside her simulation (Reading II). Not a hard contradiction. The spec's default isn't supported by the posts.

**C5. Flux vs tension as the source of the deficit.** [Akitti] 2106142937948324193 «Adding flux alone never makes a cone.» [hive-interpretation] Consistent with rugby-ball-type candidates *if* their deficits are attributed to brane tension (T_b) and flux only stabilizes the sphere. That's how such models are usually set up (**VERIFIABLE**: Carroll–Guica 2003; Navarro 2003; Gibbons–Güven–Pope 2004). A candidate whose deficit comes from flux alone would contradict her rule. The spec should state which it uses.

**C6. Equal vs distinct tips.** 2107224531714670767 [unverified] requires «\mu_1\big|_W=\mu_2\big|_W,\qquad» for a stationary wall. [Akitti] 2106829842167804113: «strings cannot be the same because different strings map to different particles». Not a contradiction (equal total tension ≠ identical strings), but the spec should not assume identical endpoint content at both tips.

**C7. Survivor list presented as a result.** 2106801517357351243 / 2106881531725652263 assert «Residuals vanish.» and «The survivors are exactly the three classes listed in the October notes». The framework says «Supply the current \(S^2\)/lattice zero-mode list (or schematic chiral/anomaly assignments) and score it against the two integrals and the MHD restriction. Output only the survivors.» Without inputs (Q4) no residual can be evaluated. So these are claims, not outputs. SM1 should treat them as untested (§3 N4).

**C8. «No particle content is produced by the branch.»** 2107224531714670767 [unverified] vs her direction of adding SM «knobs at the tip» ([Akitti] 2106850162010185866). [hive-interpretation] Compatible: particles come from strings ending on tips, not from the branch/wall. The spec's "zero modes localized at the tip" fits.


---

## 5. Other SM1-relevant posts (attribution + flag)

| post (BST) | tag | quote | flag |
|---|---|---|---|
| 2106479506898948311 (Oct 3 21:20) | [Akitti] | «So the tension in the strings cause a "missing wedge" and that wedge is the cone singularity. curvature is zero off the tip of the choice and infinite on it, concentrated in a delta function whose strength is exactly the deficit angle.» | **VERIFIABLE** (standard cone geometry) |
| 2106150288184779232 (Oct 2 23:32) | [Akitti-account post, authorship unverified; AI-overview formatting: «------------------------------» section breaks, «## 1. The Conical Deficit Angle (Cosmic Strings)»] | «$$\Delta \phi = 8\pi G T$$» | **VERIFIABLE** (Vilenkin 1981). Consistent with α = 1 − 4Gμ |
| 2106839277602824288 (Oct 4 21:10) | [Akitti] | «@Millbstrd The cone singularity happens because of the string tension» | **HER PATTERN/IDEA** (consistent with VERIFIABLE GR) |
| 2106841892038021615 (Oct 4 21:20) | [Akitti] | «I'm looking at the cone singularity. Which is basically like there's an ultra flat plane EXCEPT for the spike. Or two planes, one is completely flat and one is a spike connecting to that flat plane.» | **HER PATTERN/IDEA** (her picture of the exterior) |
| 2106842298470527148 (Oct 4 21:22) | [Akitti-shared AI text: talks about her in the third person, «Akitti is not talking about knots right now»] | «A single conical endpoint therefore does not, by itself, generate a quasiparticle spectrum; extra structure (different deficit angles, different windings, or additional degrees of freedom) would still be required if one wanted distinct “strings” or a full spectrum.» | **VERIFIABLE** in spirit (same as N6) |
| 2106842667992961342 (Oct 4 21:23) | [Akitti] | «@Millbstrd This is helpful though for when I attach the standard model to what's happening though (later maybe next week)» | her endorsement of the line above → treat "a single tip isn't enough" as HER direction |
| 2106730680860164419 (Oct 4 13:58) | [Akitti-account post, authorship unverified; assistant markers «So your read is right.»] | «Yes. It is an analysis tool, not a new ingredient.» … «They help you sort what can meet at the singularity. They do not generate the singularity.» | CG as selection rule: **VERIFIABLE** (3j triangle rule). The cone «only shifting the labels» is **HER PATTERN/IDEA** |
| 2106738208675442712 (Oct 4 14:28) | [Akitti-account post, authorship unverified] | «Gaussian curvature vanishes identically for \(r>0\) (the metric is locally Euclidean). All curvature is concentrated at the origin as a delta-function source whose integrated strength equals the deficit:» | **VERIFIABLE**. Note it says *Gaussian* curvature, which supports the K reading in C2 |
| 2107220265818325212 + 2107220397020049720 (Oct 5 22:23–22:24) | [Akitti] | «Something feels backwards here cause if the branching singularity is on the bubble then why is the standard model embedded into the cone tip» / «@Millbstrd Oh wait maybe cause a 2D-> 3d/4d lift» | **HER PATTERN/IDEA**. She confirms the SM sits at the cone tip; the reason (a 2D→3D/4D lift) is unresolved |
| 2107225360240656675 (Oct 5 22:44) | [Akitti] | «The gap was more strings other than the ones piling together from interactions. 😂» | **HER PATTERN/IDEA**. Later strings carry the particles (cf. N1) |
| 2107591866921177245 (Oct 6 23:00) | [Akitti-account post, authorship unverified] | «The wall closes only on the joint kernel. Build it as a filter on the two tips.» | **POSSIBLY GROK-HALLUCINATED** as a rule (no source); her endorsed direction is "wall closure" (next row) |
| 2107587339572617401 / 2107591301101236541 (Oct 6 22:42 / 22:58) | [Akitti] | «Wait why do the strings have to be massless if these have a vibrational state?» / «All you had to say was it's for wall closure, not a requirement for vibrational states» | **HER PATTERN/IDEA**. "Massless" in the two-tip filter means wall-closure only. PROVISIONAL (the @grok replies are missing) |
| 2107615006166495672 (Oct 7 00:32) | [Akitti-account post, authorship unverified] | «None of this is a proof, or even a discretization, of the Millennium problem. The hive is a hand-built filter on a pair of parameters \((\alpha,\mu)\) inside the thread’s larger deathface/branch-cut construction» | an honest disclaimer that matches Akitti's Oct 8 framing. The m² ∝ mismatch is **POSSIBLY GROK-HALLUCINATED** |
| 2107592883054186727 (Oct 6 23:04) | [Akitti] framing, with an embedded open-problem list that matches the framework | «Standard Model attachment: zero-mode content, chiral assignments, anomaly cancellation and schematic Yukawa or gauge-coupling ratios have not been computed from the \(S^2\) (or lattice) data..» | **HER PATTERN/IDEA**: she states herself that SM attachment is *not computed*, which supports C7 |
| 2105729986275770743 (Oct 1 19:42) | [Akitti] | «Well grom mentions that we still need to derive some stuff because there isnt proof our constructions are the right path... which is fair..» | her own caveat (cf. her Oct 8 statement) |
| 2107217541122699558 (Oct 5 22:13) | [Akitti] | «it's mostly been learning stuff that exists or integrating other people's work (the papers) and trying to fill the holes» | context: most "merge" posts are integrations of papers, not her derivations |
| 2106839910049337839 (Oct 4 21:12) | [Akitti] | «I'm not focused on holography right now. It's just there in the BG. My focus is Magnetohydrodynamics and quantum gravity» | scope: holography candidates are background, not focus |
| 2105917997588365696 (Oct 2 08:09) | [Akitti] | «Thinking about a bubble that starts forming strings on the outside, The strings want to turn into a brane....» | **HER PATTERN/IDEA** (string→brane, the parked membrane problem) |
| 2108175375633399899 (Oct 8 13:39) | [Akitti] | «Me when I realized the s^2 -> r^2 was following a weak path towards gravity solution this morning.» | **HER PATTERN/IDEA**. PROVISIONAL (parent 2108175007566234095 missing) |
| 2108175014336065627 (Oct 8 13:37) | [Akitti] | «Grok told me yesterday to wait to integrate any of the openai stuff into the hive yet» | not SM1. Shows she's aware Grok output needs checking |

---

## 6. Check-flag ledger (one line per technical claim used above)

**VERIFIABLE (standard physics / checkable paper):**
1. α = 1 − 4Gμ, deficit 8πGμ for a straight cosmic string (2106768405814550691, 2106150288184779232). Vilenkin 1981; DJtH 1984.
2. Cone geometry: flat off the tip, ∫K dA = deficit (2106479506898948311, 2106738208675442712). Gauss–Bonnet.
3. The framework integral ∫R dA = 2π(1−α) is correct **with R ≡ Gaussian K**; it is 4π(1−α) for the Ricci scalar (C2).
4. CG/3j triangle and m-selection rules (2106738208675442712, 2106730680860164419).
5. Fluid Clebsch potentials vs Clebsch–Gordan coefficients are distinct objects (2106721095835341008).
6. Chiral spin-2 magnetoroton observed in FQH (2106510530278019502). Liang et al., Nature 628, 78 (2024). The post's own numbers (e.g. «\(\alpha\approx0.15\)», «\(30\,\mu\mathrm{eV}\)») were not checked against the paper.
7. HW interval: E8 per wall, GS/CS anomaly cancellation, E8 maximal-subgroup chains (2107799344195760276). Hořava–Witten 1996.
8. D3-branes at CY₃ cone singularities as local SM models (2106881531725652263). Bottom-up programme, AIQU 2000.
9. arXiv:2610.08939 content (flag manifold, two flux quanta, R⁻¹ ~ Λ^{1/4}, S² uplifts unstable). Checked on arXiv this session.
10. A bare cone needs holonomy + internal d.o.f. for gauge quantum numbers (2106845569306284454, 2106842298470527148). Standard in orbifold model building.
11. Rugby-ball deficits are sourced by brane tension, with flux stabilizing the sphere (C5). Carroll–Guica 2003; Gibbons–Güven–Pope 2004.

**HER PATTERN/IDEA (keep as [Akitti] directions):**
12. Chain: S² bubble → branch singularity (MHD + QG) → strings → pile-up → cone → R² (2107219672017842217).
13. Cone formed in her simulations; two cones because a string has two endpoints; HW-like (2107582409306771923).
14. Tension from pile-up / infinite length sets the wedge (2106848956730785938). Flux alone makes no cone (2106142937948324193).
15. Filter = selection method for the "mirror port", not a derivation; different strings ↔ different particles (2106829842167804113).
16. Goldberg lattice = probe/organizer, not used in sims (2105731792439247111).
17. SM sits at the cone tip; "knobs at the tip" still to add (2106850162010185866, 2107220265818325212).
18. Π as a trace/restriction on the matching circle; absolute residuals with tolerance (2106768405814550691; framework-consistent).
19. GR is embedded but breaks down at the transitions (2107583263963480253, 2107879215366557809).
20. "Massless" in the two-tip filter means wall closure only (2107591301101236541).

**POSSIBLY GROK-HALLUCINATED (specific number/formula/result with no source):**
21. The three-class survivor list and «Residuals vanish.» (2106801517357351243 tail; repeated in 2106881531725652263).
22. μ_i = Σ t_a and 1−α_i = (1/2π) Σ q_a; wall equalities; m² ∝ (α₁−α₂)² + (μ₁−μ₂)² (2107224531714670767, 2107591866921177245, 2107615006166495672).
23. α_i = 1 − β_i/2π with ∫R = 2π(1−α_i): an internal convention error (2107224531714670767).
24. "stress integral = summed T_tt of the retained modes" (2106881531725652263).
25. All code placeholders: μ=0.05, mhd_trace {v:0, B:0, ρ:1}, α=0.8, tol values, alpha=√2 (§2).
26. "Numerical locks" ε_EP ≈ 0.513681, I_E ≈ 0.299, λ_EP ≈ −0.3084 i, scar floor ~0.041 (no source in window; see §8).
27. Mapping arXiv:2610.08939's ε onto her tension as μ = μ_crit(1+ε) (sign and object mismatch with the paper).
28. SM matter anchored at "cone tip × E8 wall" fusion points as a *result* (2107799344195760276). The direction is hers; the claim of compatibility is unsourced.
29. Cone spectral zeta → RH critical line (2106917398238666898). Not SM1. The Bessel/zeta spectral facts are VERIFIABLE; the "forces critical line" step is not. She says herself in 2107217541122699558 «I just noticed they looked similar.»

---

## 7. PROVISIONAL items (after 674F5BAF landed)

**Resolved by 674F5BAF:**
- 2107582409306771923 / 2107878903977029789: the quoted/parent Millbstrd 2107579938681319654 is in §1 of 674F5BAF ([quoted] «2 tips, and the figure 8 seem forced»). Her replies are defences of the two-tip picture. Resolved.
- 2108092102886211700: the quoted item is a bare link. The paper behind it is arXiv:2610.08939 (verified, see N3). Resolved.
- 2106721095835341008: quoted star_stufff post resolved (a CG/ringdown remark). Not SM1-critical.
- 2107556209838403806: Article «Infinitely many faucets dumping water on a cheesecloth» resolved (torus Green's function). Not SM1.
- 2108178649320943947: quoted entrance225 post on instanton/MSS resolved. Parked topic, not SM1.
- 2106801517357351243 (line 1200): it quotes her own 2106768405814550691, which is in F1C6CC26. Its media is a stylised video still (§10). Nothing quoted changes the attribution → stays [Akitti-account post, authorship unverified].
- 2106485527075598802: its image is a screenshot of a Grok answer → [Akitti-shared AI text] (a category-difference explanation). Not SM1.

**Still PROVISIONAL (content we still lack):**
- 2106667393342673253: quoted 2106520162400903671 is **Not Found** (labelled so in 674F5BAF). Not SM1 (a «Whose work did i scan?» dispute).
- Replies whose parent tweet is in neither file. We can't tell what she's answering:
  2106829842167804113 (line 1215; parent **2106828033017413645**) · 2106850162010185866 (parent **2106849596471194006**) · 2106848956730785938 (parent **2106846370376159299**) · 2106839277602824288 (parent **2106836877344936360**) · 2106841892038021615 / 2106842298470527148 (parent **2106841417435820293**) · 2106839910049337839 (parent **2106831916297265564**) · 2107214299500552569 (parent **2107207631161208906**) · 2107217541122699558 (parent **2107215028407377941**) · 2107219130655109199 (parent **2107216726102323513**) · 2107576486328754344 (parent **2107574076470636546**) · 2107583263963480253 (parent **2107582473206906939**) · 2107587339572617401 (parent **2107586883224047915**, @grok) · 2107591301101236541 (parent **2107587523891359932**, @grok) · 2107592883054186727 (parent **2107591404428071233**) · 2106484862228004871 (parent **2106482611723874479**) · 2105729986275770743 (parent **2105727827014480090**) · 2108175375633399899 (parent **2108175007566234095**).
- All 32 video posts: only the preview still is available. The meaning of the video beyond the still is unknown (§10).

## 8. Claims that need a post we don't have (for Orion, public X)

1. **The posted simulation**: [Akitti] «The cone singularity literally formed when I ran simulations.» No sim output exists in Oct 1–8. Ask for or locate any earlier post with sim plots/code, plus the values of α (or μ), r_c and Ψ|r_c behind it (Q4/Q5/Q3).
2. **The first posting of the "numerical locks"** ε_EP ≈ 0.513681, I_E ≈ 0.299, λ_EP ≈ −0.3084 i, scar floor ~0.041 (cited as «previously posted»). Pre-Oct-1 posts.
3. **«the speculative vacuum selection method we worked on weeks ago»** (2105731792439247111) and the Betti–Berry spike source. Pre-Oct-1.
4. **The "current GoldbergHexa / lattice zero-mode list"** that the line-1200 tail claims to score. Any earlier post with actual zero-mode records (the AI text in 2106881531725652263 asks «What is the exact format or data structure of your current GoldbergHexa zero-mode list?», which implies none was posted).
5. **What line 1215 answers**: parent 2106828033017413645. Also 2106849596471194006 (what «Yes but only after we add the knobs» answers) and 2106846370376159299 (the wedge question).
6. **The @grok replies** 2107586883224047915 and 2107587523891359932 (massless-strings / wall-closure exchange). Also 2107574076470636546 (what «the above notes» answers).
7. **Akitti's "SM this weekend" result** (Oct 3–4, promised in 2105731792439247111). Nothing in Oct 1–8 shows a computed SM attachment, and 2107592883054186727 says SM attachment items «have not been computed». Check Oct 9+ posts.
8. 2106520162400903671 (Not Found; non-research). Low priority.


---

## 9. (A) Soundness check of AKITTI_POSTS_OCT1-8_QUOTED.md (674F5BAF)

**Verdict: FAIL, on one criterion only (skip-list leakage). Every other check passes.** The file is usable for research once the 8 skip-listed IDs (and their 17 images) are dropped or explicitly accepted.

| check | result |
|---|---|
| hash | PASS. `sha256sum` = 674f5baf… (F1C6CC26, 6CD5F259, 3D19F785 also re-verified) |
| quoted-post blocks keyed to real posts | PASS. 42 blocks, 42 distinct her-post IDs, all in F1C6CC26. Every `Quotes:` link in F1C6CC26 (42 links, 41 distinct targets) has a block, and the quoted ID matches in all 42 pairs. 40 targets fetched + 1 Not Found = 41 |
| media index ↔ files | PASS. 87 entries (44 hers + 43 quoted), 87 files in `akitti_posts_media/`, 0 missing, 0 extra, 0 duplicate, 0 zero-byte. All 44 'hers' entries point to posts in F1C6CC26. 32 of her entries are type video (preview still only) |
| secrets / cookies / tokens | PASS. Regex sweep (auth_token, ct0, bearer, cookie, token, secret, api key, password, AAAAAAAA, guest_id, oauth) finds no credential material |
| Not Found item labelled | PASS. «**UNAVAILABLE:** API returned "Not Found Error" (Could not find post with ids: [2106520162400903671].)», keyed to her 2106667393342673253 |
| skip-list IDs absent | **FAIL.** 8 of Orion's 21 skip-list IDs appear. (a) **6 quote blocks** for skip-listed posts of hers: 2106672601833820539, 2106674026642837755, 2106682097691988054, 2106708205589901802, 2106711202089111579, 2106726113825128727 (the Oct 4 quant_astro dispute, quoting her own older posts), with **15 quoted images** (2106672227592683776_1–2, 2106673745494511841_1–2, 2106681080841425164_1–4, 2106708045892116842_1–2, 2106711082547253710_1–4, 2106725882744467596_1). (b) **2 'hers' media entries**: 2106015545657057707_1.jpg (welding post) and 2106409453017014275_1.jpg (unfollow post) |

Notes for Ledger: the 6 dispute posts' *text* is already in F1C6CC26, so the leak is the quote blocks and images, not new text. The 15 dispute images weren't opened by me (non-research), so I can't say whether they show other people's handles or personal information. Check before any push. Non-research quoted content not on the skip list is also present (e.g. the anime image-prompt post quoted by 2107169443159666924, a political quote). It isn't a criterion failure, but it's worth a flag.

## 10. (B) Video triage (32 posts, preview stills only)

Method: post text from F1C6CC26 plus the still from `akitti_posts_media/` (viewed with Read). **No still shows equations, a diagram with labels, a simulation frame or a whiteboard.** All 32 are stylised AI-generated art. So none qualifies as LIKELY RESEARCH on what we can see. Posts whose *text* is research are MAYBE: the video might contain more than the still, but I don't guess. Within MAYBE, SM1-relevant ones come first. Nothing posted in Oct 1–8 shows the simulation she says formed the cone.

**LIKELY RESEARCH: none.**

| # | post | date (BST) | post text (one line) | still shows | verdict | reason |
|---|---|---|---|---|---|---|
| 1 | 2107224531714670767 | 10-05 22:40 | Double cone: one tip at the branch locus, one at the far end of the bubble wall; open strings between tips; wall as matching surface | two glass cone/spindle shapes with rainbow light ribbons crossing between them | MAYBE | Illustrates N1's two-tip construction (SM1-relevant), but it's AI art: no equations, no sim, no labels |
| 2 | 2107537800610607257 | 10-06 19:25 | Grok-compiled notes: deathface stop, branch cut / figure-8 pinch, cone vs bolt test | iridescent figure-8 of two eye-like rings, small spike under the crossing | MAYBE | Pictures her figure-8 + cone motif (Q1/Q5 relevant); decorative, no data |
| 3 | 2106768405814550691 | 10-04 16:28 | Exterior cone fixed by tension; core residuals; 'string mirror equation' | rainbow spike at the centre of a circular disk/platform | MAYBE | Text is the framework source; still is a stylised cone, no diagram or sim |
| 4 | 2106801517357351243 | 10-04 18:39 | Framework text + three-class 'survivor' list (line 1200) | glassy crystalline face with rainbow haze | MAYBE | Text central to SM1; still is a portrait-style artwork |
| 5 | 2106738208675442712 | 10-04 14:28 | Conical-singularity metric, delta curvature, CG rules on a cone | rainbow circuit-patterned cone peak with lightning | MAYBE | Cone illustration only; no equations visible |
| 6 | 2106845569306284454 | 10-04 21:35 | Three knobs (deficit, holonomy, internal d.o.f.) for an SM spectrum on a cone | radial rainbow beams around a central spike | MAYBE | Text SM1-relevant (N6); still decorative |
| 7 | 2106881531725652263 | 10-04 23:57 | Local string pheno at a cone tip; open problems; filter pipeline (AI text) | cyborg head in profile | MAYBE | Text relevant; still is unrelated portrait art |
| 8 | 2108092102886211700 | 10-08 08:08 | Second flux quantum on the S² bubble (arXiv:2610.08939 merge) | web of rainbow strands around dark holes | MAYBE | Text relevant (N3); still abstract |
| 9 | 2107799344195760276 | 10-07 12:44 | Hořava–Witten conical interval, E8 walls, SM at tip×wall | cyborg head with visor | MAYBE | Text relevant (N2); still is portrait art |
| 10 | 2105558608830156964 | 10-01 08:21 | Deathface: R²→S² handoff, GoldbergHexa stop/bolt rule | chrome humanoid with a glowing chest emblem, floating dark polyhedra | MAYBE | Research text (deathface); still decorative |
| 11 | 2106721095835341008 | 10-04 13:20 | Fluid Clebsch vs Clebsch–Gordan: one table, three readers | glass tubes around a crystalline hexagonal core | MAYBE | Research text (Q3 separation); still abstract |
| 12 | 2107056665161867400 | 10-05 11:33 | TT gravitons, gapless channel; GS vs Wen–Zee (AI dialogue) | glass skull with rainbow light | MAYBE | Research text; still decorative |
| 13 | 2106490112863547848 | 10-03 22:02 | Quantum Hall fluid on a cone, braiding phases | iridescent funnel/vortex in a holed liquid sheet, city backdrop | MAYBE | Research text; still loosely evokes a cone, no data |
| 14 | 2106510530278019502 | 10-03 23:23 | Chiral spin-2 magnetoroton (Liang et al. data) | cyborg face with glowing wires | MAYBE | Research text (VERIFIABLE paper); still is portrait art |
| 15 | 2105755883904831888 | 10-01 21:25 | Betti–Berry spike as vacuum-selection filter | iridescent bubbles/domes on a circuit floor | MAYBE | Research text (parked problem 3); still decorative |
| 16 | 2106917398238666898 | 10-05 02:20 | Cone spectral zeta ↔ Riemann zeta / critical line | twisted glass spike with flowing strands | MAYBE | Research text but off-SM1 (RH); still decorative |
| 17 | 2107097912098353203 | 10-05 14:17 | Peigné–Liesse colour projectors merge | iridescent organic web/membrane structure | MAYBE | Research text; still decorative |
| 18 | 2107140069261709764 | 10-05 17:05 | Gerhardt Kerr-AdS exterior quantization merge | iridescent iris/crater with hexagon-grid centre | MAYBE | Research text (paper merge); still decorative |
| 19 | 2107180272105988526 | 10-05 19:45 | Holographic thermal propagator merge | chrome skull at a reflective surface | MAYBE | Research text; still unrelated |
| 20 | 2107195607785877804 | 10-05 20:45 | Quantum Love numbers / near-extremal RN merge | chrome skull with long hair | MAYBE | Research text; still unrelated |
| 21 | 2107438091082277052 | 10-06 12:49 | Perez-Lona magnetic higher-form symmetry merge | crystalline spiky tree with rainbow rays | MAYBE | Research text; still decorative |
| 22 | 2107816196988936193 | 10-07 13:51 | Landau background gauge QG merge | honeycomb core with iridescent petals | MAYBE | Research text; still decorative |
| 23 | 2107839957888798956 | 10-07 15:26 | Turbulent cascade arrow / phase-null merge | iridescent robot body | MAYBE | Research text; still unrelated |
| 24 | 2107909026923385012 | 10-07 20:00 | Quantum twisting microscope / quantum metric merge | faceted hexagon-pentagon sphere with rays | MAYBE | Research text; still decorative (Goldberg-like ball, no data) |
| 25 | 2107922042888614313 | 10-07 20:52 | Spontaneous Hawking radiation in spin chains merge | chains forming a net with rainbow light | MAYBE | Research text; still decorative |
| 26 | 2107944105708077188 | 10-07 22:20 | Fractal QCD phase structure / imaginary rotation merge | dark fractal sponge | MAYBE | Research text; still decorative |
| 27 | 2107961366476718365 | 10-07 23:28 | Gravitational spin Hall / black-hole shadows merge | chrome skull cityscape | MAYBE | Research text; still unrelated |
| 28 | 2108178649320943947 | 10-08 13:52 | Instanton-enforced MSS bound merged on the deathface | face with glowing wires | MAYBE | Research text (parked); still portrait art |
| 29 | 2105676116161946069 | 10-01 16:08 | link only, no text | glowing flower-like bursts on a dark node lattice | NOT RESEARCH | No text; abstract art (can't rule out a research video, but nothing shown) |
| 30 | 2107169443159666924 | 10-05 19:01 | two links; quotes an anime image-prompt post | anime woman licking a blue gem | NOT RESEARCH | Image-prompt art |
| 31 | 2107377354800820401 | 10-06 08:48 | link only, no text | spaceship-like craft in a streaking light tunnel | NOT RESEARCH | No text; sci-fi art |
| 32 | 2107413077712834585 | 10-06 11:10 | «Dsdd» + link | spaceship-like shape in a pink-streaked void | NOT RESEARCH | No meaningful text; sci-fi art |

Totals: LIKELY 0 · MAYBE 28 · NOT RESEARCH 4.

---

## 11. Posts with no SM1 relevance (not cited above)

75 of 153 posts. They were read and give nothing for Q1–Q16, values, candidates or contradictions.

**Paper-merge / 'hive upgrade' posts not already listed in §10** (third-person «@Akitti hive» register, [Akitti-account post, authorship unverified]; each cites an arXiv paper, so the paper is VERIFIABLE but the 'hive law' mapping is POSSIBLY GROK-HALLUCINATED). Off-SM1 topics: thermal propagators, Love numbers, higher-form symmetry, Landau gauge, turbulence, twisting microscopy, Hawking spin chains, fractal QCD, spin-Hall shadows, hybrid qubits:
2107930897714459040 (10-07)

**Everything else** (social, personal, memes, link-only, the quant_astro / OpenAI disputes, bounce/instanton/RH asides, short replies with no technical content):
2105443056770256925 (10-01), 2105549281235210292 (10-01), 2105568726632526210 (10-01), 2105659975196635626 (10-01), 2105661509875691722 (10-01), 2105678551500616063 (10-01), 2105725112548991066 (10-01), 2105730233080893872 (10-01), 2105732211781583013 (10-01), 2105743566278656245 (10-01), 2105747522497261789 (10-01), 2105756203800543479 (10-01), 2105768214194168239 (10-01), 2105904621877067847 (10-02), 2106012529675903180 (10-02), 2106060925098705268 (10-02), 2106063846938902646 (10-02), 2106067825999720475 (10-02), 2106083503871828034 (10-02), 2106085090354934183 (10-02), 2106093670441120019 (10-02), 2106136131922256291 (10-02), 2106157385480048943 (10-03), 2106279918967443504 (10-03), 2106324574082412742 (10-03), 2106380415627887048 (10-03), 2106456438323466691 (10-03), 2106520537501511791 (10-04), 2106674214602522788 (10-04), 2106689725398421960 (10-04), 2106716338123100661 (10-04), 2106717955283464194 (10-04), 2106718765086015689 (10-04), 2106756997047574716 (10-04), 2106840296264704267 (10-04), 2106841136891617771 (10-04), 2106869644997115979 (10-04), 2106888389483982908 (10-05), 2106912773397725430 (10-05), 2106913153833402469 (10-05), 2106918709797556714 (10-05), 2106933192011694572 (10-05), 2107013859873845548 (10-05), 2107031744708825166 (10-05), 2107057305305206963 (10-05), 2107095549539213744 (10-05), 2107096086896636363 (10-05), 2107098953682710952 (10-05), 2107126543466291705 (10-05), 2107218004094095543 (10-05), 2107223907917087053 (10-05), 2107228856289550445 (10-05), 2107253071159971954 (10-06), 2107263315768713235 (10-06), 2107530735934669115 (10-06), 2107591925998002185 (10-06), 2107585498881675671 (10-06), 2107615107043795083 (10-07), 2107616117795455398 (10-07), 2107865606322307435 (10-07), 2107871564402225590 (10-07), 2107916271769497602 (10-07), 2107920345089167785 (10-07), 2107940518957117885 (10-07), 2107967019073347810 (10-07), 2107968488350334997 (10-07), 2107976381430931513 (10-08), 2107987707926331518 (10-08), 2108003346762141872 (10-08), 2108009936902869236 (10-08), 2108021275515826280 (10-08), 2108136541671641272 (10-08), 2108177483879301132 (10-08), 2108176464373793200 (10-08)

---

## 12. Quote verification

Automatic check: 144 «…» quotes; 144 found verbatim in F1C6CC26 or 674F5BAF; 0 not found.
