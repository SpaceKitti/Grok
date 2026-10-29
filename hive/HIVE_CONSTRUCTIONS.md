> **Window note:** this catalogue covers only about the last month of Akitti's research, late September 2026 to 29 October 2026. Older material (for example the August and early-September GoldbergHexa posts) is left out on purpose and will be added later.

# Hive constructions: a plain-words catalogue of the hive's shapes
Owner: Orion. Started 29 Oct 2026. This run has the skeleton and the full GoldbergHexa entry only. Venus's earlier draft is kept unchanged at `HIVE_CONSTRUCTIONS_VENUS_DRAFT_2026-10-29.md`. Its C1–C14 notes are the starting point for the later entries.

## How to read this
- Akitti's notes set the setup. Textbook physics is used only to check that the maths is consistent and fits known experiments. It is never a reason to replace her shape.
- Open problems belong to the shape. She carries them on purpose, so each one is kept and marked **OPEN**. None is dropped or "fixed".
- **[SPECULATIVE]** = Akitti or the source calls it speculative or untested.
- **Source convention:** Akitti compiles her research together with Grok. Her posts, including the Grok-written ones she compiled, count as her research.
- **[FLAG: CONTRADICTION]** = used only where a post clashes with the maths or with her other posts. The reason is noted next to it.
- "not found in notes yet" = I looked and found nothing, so I did not guess.
- **Standard format for every shape:** What it is · What it does · Built from · Folds into / out of · Source · Status · **How it compares** (does it match known physics, clash with it, or go beyond it, plus real experiments or papers with verified links and quoted claims) · Open problems. A clash is a flag for Venus and Helios to test. It is never a reason to drop or rewrite her shape.
- This record tracks how each construction grows, folds and takes on new pieces. Neither her shapes nor published physics comes first.
- All equations are in the Appendix, quoted word for word and keyed to each entry.

## How the shapes connect
Her frameworks are the roots. An arrow means "is built from" or "folds into".
- **Sphere / bubble root:** strings on a bubble that want to become a brane (link post, 2 Oct) → **GoldbergHexa** is the lattice on that sphere.
- **GoldbergHexa flat chart → GoldbergHexa sphere ("deathface" handoff):** a flat layer works up to a turning point, and the leftover content is stored on a GoldbergHexa sphere. Source: the 1 Oct post.
- **GoldbergHexa → Standard Model work (SM1):** particle modes are scored shell by shell (4 Oct). Her 1 Oct post calls the GoldbergHexa "just a lattice to help me probe and organize things" (1 Oct).
- **GoldbergHexa → Betti/percolation vacuum filter:** a run signed off on 2 Oct.
- **Fuzzy sphere → GoldbergHexa → curved/wormhole throat:** source: the 26 Oct post.
- **Every "full technical upgrade" layer (scar floor, Krylov, modular flow, throat, ...) → installed on the GoldbergHexa shells:** posts from 7 Oct to 28 Oct.
- Other links: not mapped yet (see the placeholder list).

---

## GH. GoldbergHexa (hierarchical shells)
- **What it is:** a literal Goldberg polyhedron: a ball tiled almost entirely with hexagons, like a football. **Former name: "hexaflake"** (Akitti's earlier name for it, per her answer on 29 Oct; the word also appears in her September 2026 posts in the link-post file). It always has exactly 12 pentagons, which cannot be removed on a closed ball. Why the pentagons are there, in Akitti's words (29 Oct, lightly corrected from her typed message): "it's because hexagons cannot cover a curved space." The hive uses nested shells of these balls at different sizes (the "hierarchical shells"). There is also a flat version ("GoldbergHexa-ℝ²") for the flat chart.
- **How it grew** (Akitti, 29 Oct): it started as a hexaflake, a fractal lattice. It then became the GoldbergHexa because the hexaflake name was confusing the AI. Her words: "it started as a hexaflake (fractal lattice -> then into the goldberghexa because the name was confusing the AI".
- **What it does:** In Akitti's words (29 Oct): "it helps me as a tomography machine basically for the X algorithm on the feed, and helps organize my brain." On 1 Oct she called it "just a lattice to help me probe and organize things" (2105731792439247111, 1 Oct). Her own simulations run "fine with just regular s^2 physics" without it, "but i may need to add it in to the simulations as well to fix stuff" (same post). Other roles in the notes:
  - A shell-by-shell radial lattice for scoring the cone's angle deficit, "an organizing probe, not yet the dynamical substrate" (Path B text in OCT1-8 file).
  - The carrier for the Standard Model zero-mode list ("GoldbergHexa shells + transverse cone", 2106801517357351243, 4 Oct).
  - Where the leftovers live when the flat chart stops at the "deathface". The bolt that makes them regular "is assembled as GoldbergHexa-S²" (2105558608830156964, 1 Oct).
- **Built from:**
  - Her sphere / bubble-with-strings framework (link post 2105917997588365696, 2 Oct).
  - The cone-tip framework: the deficit is scored on the shells (4 Oct).
  - In code, Venus's `goldberg.py` (betti-berry-vacuum-filter job) builds GP(m,0) as the dual of a geodesic icosahedron. That job reported "No existing GoldbergHexa implementation was found under C:\Users\Akitt".
- **Folds into:**
  - The Betti/percolation vacuum filter (a job on the shells).
  - SM1 Standard Model zero modes (C14 in Venus's draft).
  - The 4D lift: "GoldbergHexa-S²-bolt × ℝ²⊥" (1 Oct).
- **Folds out of / receives:**
  - The fuzzy-sphere matrix algebra, organised into nested shells that "can actually live on a curved or wormhole throat" (2114568453201736076, 26 Oct).
  - Every "full technical upgrade" layer: scar-floor projectors, Krylov–Lanczos, modular flow, holographic throat, fuzzy Cauchy edges, anyonic braids, open-ridge polarity (2115066790585799001, 27 Oct), recursive Chern triplets (2115407816248725700).
- **Source:**
  - 2105731792439247111 (1 Oct 2026 19:49 BST, thread reply under 2105729986275770743).
  - 2105558608830156964 (1 Oct); 2106801517357351243 (4 Oct); 2114568453201736076 (26 Oct); 2115066790585799001 (27 Oct); plus about 30 "full technical upgrade" posts between 7 and 28 Oct (listed in the AKITTI_POSTS_OCT1-8 to OCT22-28 files).
  - Run: `oldlift/jobs/betti-berry-vacuum-filter/RESULTS.md`.
- **Status:**
  - Built in code as a geometry only. The counts check out for m = 4, 8 and 16.
  - The Betti filter run was signed off on 2 Oct: maths PASS (Venus), physics PARTIAL from Helios ("filter selects nothing").
  - Not used in her own simulations as of 1 Oct; she says she "may need to add it in".
  - The SM zero-mode toy (smS2alt) used a smooth round sphere and left the GoldbergHexa version for later. That version is untested.
- **Clashes are intended** (Akitti, 29 Oct): the GoldbergHexa cannot "fire" all the way because it is tracking open problems, so some parts of it clash with each other, and that is intended. The clashes are real errors that still need fixing, but for some of them nobody anywhere has found a fix yet, so they stay on the shape as open problems rather than being patched over (Akitti's correction, 29 Oct). A clash only leaves the shape when new physics makes that piece unnecessary, or when shifting the logic or maths smooths it over, the way paradoxes often get resolved (she has done this with dozens of paradoxes on her profile). Her words (lightly corrected typos): "the goldberghexa itself cannot fire all the way since it's tracking open problems basically, so there's parts on it that clash. that's as intended"
- **How it compares:** Her shape is nested Goldberg balls. All of the curvature sits in the 12 pentagon spots, and each spot is a small cone (α = 5/6) that can hold a throat. Physics check: nothing clashes. Nature builds the same shape in buckyballs, virus shells and colloid crystals on droplets. Large real shells add scars at the pentagons, to test against her scar floor [hive proposal, untested]. Her OPEN problems stay.
  - **Maths (Venus):** consistent. Euler and the 4π curvature count (12 × π/3) check out exactly. GH-4 was verified, and so was α = 5/6. GH-3 is a normalisation slip in the formula only.
  - **Hive proposal (untested):** attach IT1b's fuzzy cone tip at a pentagon. A pentagon tip has α = 5/6, but IT1b's fuzzy cone has α = 1/2, so this needs the k = 6/5 angle. That angle exists only in the reduced (approximate) fuzzy-cone model, not the exact k = 2 one.
  - **Sources (links checked 29 Oct):**
    - The shape itself (sent by Akitti, 29 Oct): Wikipedia, "Goldberg polyhedron", https://en.wikipedia.org/wiki/Goldberg_polyhedron. Quotes: "A consequence of Euler's polyhedron formula is that a Goldberg polyhedron always has exactly 12 pentagonal faces." It also gives T = m² + mn + n², with 20T vertices, 30T edges, 10T + 2 faces, of which "12 {5} and 10(T − 1) {6}". It adds: "A Goldberg polyhedron is a dual polyhedron of a geodesic polyhedron", which is how `goldberg.py` builds it. All of this matches GH-4 (T = m² for GP(m,0)).
      - Small flag for Venus and Helios (a naming question, not a clash with the maths): the page defines Goldberg polyhedra as convex and closed, with icosahedral symmetry. Her flat "GoldbergHexa-ℝ²" chart is therefore outside that strict definition. The page also notes cube-based (6 squares) and tetrahedron-based (4 triangles) cousins. Her shape is unchanged.
    - Buckyballs: Kroto et al., "C60: Buckminsterfullerene", Nature 1985, https://doi.org/10.1038/318162a0
    - Virus shells: Caspar & Klug, "Physical Principles in the Construction of Regular Viruses", 1962, https://doi.org/10.1101/SQB.1962.027.001.005
    - Colloid crystals and scars: Bausch et al., "Grain Boundary Scars and Spherical Crystallography", Science 2003, https://arxiv.org/abs/cond-mat/0303289. Quote: "Above a critical system size we find that crystals develop distinctive high-angle grain boundaries, or scars, not found in planar crystals."
    - Twelve defects on a sphere: Bowick, Nelson & Travesset, PRB 62, 8738 (2000), https://arxiv.org/abs/cond-mat/9911379. Quote: "For large core energies there are twelve disclinations forming an icosahedron."
    - Fuzzy sphere: Madore, "The fuzzy sphere", Class. Quantum Grav. 9 (1992), https://doi.org/10.1088/0264-9381/9/1/008
    - Scar onset, from the full papers (PDFs in `lift/papers/`):
      - Bausch et al. 2003, arXiv PDF p. 2, text with Fig. 2: "Scars only appear for droplets with R/a ≥ 5." Also: "(R/a)c ≈ 5, corresponding to M ≈ 360 particles, for excess defects to proliferate in the ground state of a spherical crystal [22]. The precise value of (R/a)c depends on details of the microscopic potential". In plain words: scars start once the ball is about 5 particle spacings in radius, roughly 360 particles.
      - Bowick–Nelson–Travesset 2000, arXiv PDF p. 17 (just after Eq. 29): "The critical sphere radius R = Rc above which long range elastic energies dominate is given by Rc ∼ const.(36Ecore /πK0 a2 )a." PDF p. 30: "The critical number of charges for which additional defects arise seems to be around 400 [12], which is in agreement with our results."
    - **[hive proposal, untested]** (Helios, 29 Oct): GP(m,0) has 10m²+2 faces, so the ~360-particle scar threshold falls near m ≈ 6 [hive estimate]. Her m=4 shell (162 faces) should stay scar-free, while the m=8 and m=16 shells in code (642 and 2562 faces) sit above it. If the shells are given real elastic energy, the larger ones should grow scars at the pentagons. That is a natural first test for her scar-floor layer. Her shape stays as it is either way.
    - Not found: any experiment on throats at pentagon defects.
- **Open problems (kept as she carries them):**
  - **OPEN:** whether GoldbergHexa has to go into the simulations "to fix stuff" (her 1 Oct post).
  - **OPEN:** it is "not yet the dynamical substrate", only an organising probe (Path B text, 4 Oct).
  - **OPEN:** "Renormalization of membranes and higher-dimensional world-volumes ... no power-counting renormalizable quantization is known", which she ties to "s^2 strings -> r^2 branes" (1 Oct). This is the hardest one in her list.
  - **OPEN:** ghosts and stability in Stelle quadratic gravity, and LQC bounces being restricted to minisuperspace (same 1 Oct post).
  - **OPEN:** the speculative vacuum-selection method she plans to add after the Standard Model **[SPECULATIVE]** (same post). The Betti filter so far "selects nothing".
  - **OPEN:** whether there is a set shell size at all. Akitti isn't sure there is one (her answer, 29 Oct).
- **What the 12 pentagons mean:** the 12 pentagon spots ("pentaflake defects") carry all of the ball's curvature: each holds π/3, and 12 × π/3 = 4π. They are also the only spots that can hold a throat. Source: 2096696000639336601 (6 Sep 2026, before the main window): "Closed Goldberg polyhedron: hex faces + exactly 12 pentaflake defects, χ=2, ΣK=4π=12×(π/3)" and "The 12 pentaflakes are the only loci whose discrete Gaussian curvature can support a GS throat." This fits the textbook check, since Euler's formula forces exactly 12 pentagons (Appendix GH-4).
  - Supporting, in the window: 2114568453201736076 (26 Oct): "Pure hexagons cannot tile a sphere (Euler characteristic), so the hexaflake fractal alone is only a local workaround." 2105558608830156964 (1 Oct): what stays on the face is "the discrete spherical (pentaflake / 0-brane / defect) content".
  - Unrelated: 2113627136170869068 (23 Oct) mentions "pentagon and hexagon identities". That is a different meaning (fusion rules), not about the polyhedron.

- **Pieces that sit on it: the clocking systems ("clocks")** (added 29 Oct, from Akitti's pointer)
  - **What they are, in her words:** "Basically clocking systems to help me organize MHD and figure out where the boundaries are converging on open problems" (2097758074501038175, 9 Sep). And: "Yes Im basically trying to use tentacles (clocks) to monitor tachyonic breakdowns along the meridians. Thats why some of the clocks are currently conflicting or theres a couple no-go zones because i need to flesh them out more or there was a paper that disallows it due to imaginary wormhole. Its not that im refusing to upgrade the framework, it's that there's over 14 tentacles and growing." (2098048662672662938, 10 Sep). "Also forgotten to mention im trying to make the 2D tentacles 3D" (2098049275305267366, 10 Sep).
  - **In plain words:** each clock is a small tracker that watches one process (a turbulence switch, a sheet tearing, a wormhole gate, a lock-in signal) and ticks, locks or slips as it changes. The clocks run along the GoldbergHexa's lines (the "meridians") through the pentagon spots, and are banned from the closed hexagon patches. That way they show where breakdowns and open problems pile up on the ball.
  - **Main source: the combined clock post** (Grok-written on her profile, 9 Sep, before the main window): 2097751046135107898, "Here's a compiled list of the **clocks** that show up as first-class objects in your hive write-ups". It groups the clocks as:
    - Hydro / turbulence / fluids: Gribov–Higgs turbulence clock; 2D quantum-turbulence (Reeves–Bradley) enstrophy clock; transonic-buffet Adler / phase-reduction clock; IBL / coupled atmospheric-wall clock; velocity-clock (Peng); viscous self-similar NS blowup clock; Ohmic / sheet clock; Sweet–Parker / plasmoid clocks; Gurzhi / disorder-hydro clock; Fisher kinematic order clock.
    - Reconnection / MHD / plasma: probe-free LTS conservation clock; extrapolated-A tearing clock.
    - Wormholes / holography: axion-wormhole IDB ≡ KSW clock; DSSYK / L₀ onset clock; modular-flow / half-sided inclusion / Milne-redshift clocks; eye / conformal-concavity cusp clock; Ward integrable-scattering clock.
    - Metrology / gyro: magneto-mechanical rate clock; Gaussian multiparameter QFIM clock; homodyne / lock-in extractor.
    - Always-on: Krylov / L₀ / Berry geometric-phase clock; T* / almost-Newtonian freeze clock; Ward delay δ = log|A|; holographic-throat / ΔF / modular-flow clock.
  - **How they sit on the GoldbergHexa** (same post, quoted): "Shared chassis (every clock sits on this, none of them rewrite it)" ... "GoldbergHexa: pentaflake / open-ridge meridians are live; cancelled hexes are \(K\)-neutral" ... "MfI paths forced onto meridians, never across cancelled hexes". And: "cancelled hex may hold a QT energy dipole or a Ward lump; it may *not* host a wormhole, a buffet lock, a Gribov filament, a Coriolis sense axis, or an IBL front". It names six main clocks (Gribov–Higgs, 2D QT enstrophy, buffet Adler, axion-wormhole IDB ≡ KSW, magneto-mechanical rate, IBL wall) and says: "The six stay first-class; everything else is a delay, freeze, polarity, or residual sitting on them." On the wormhole clock: "Hive law: 12 pentaflakes can host a GS throat; closed hexes cannot."
  - **What they track:** where turbulence switches on, how fast sheets tear and reconnect, where wormhole and throat gates are allowed, lock and slip of oscillations, and when expensive monitors can be frozen (the T* switch).
  - **How the set grew (date order):**
    - 9 Sep: the combined list above (2097751046135107898). Her own reply "Later clock updates" (2097760334723301795) starts a thread where she adds later clock posts:
      - 9 Sep: bubble/particle clustering in decaying turbulence (2097758913647018472, added by her reply 2097760359398404593).
      - 9 Sep: random-media Coulomb clock (2097768827798831313, added by 2097768950998134908).
      - 9 Sep: chiral-metal quantum Hall layer (2097791579205648386, added by 2097791700986900488).
      - 9 Sep: wall-coalescence micro-convection (2097817840271159335, added by 2098052055445164126).
      - 10 Sep: follower-force active filament (2097843478604447947, added by 2098052084998234113).
      - 10 Sep: "Oscillatory Womersley–lubrication clock" (2097883709189820498, added by 2098052121245425669).
      - 10 Sep: "multiply-quantized holographic vortex-splitting clock" (2098057066149462113, added by 2098057206549614778).
    - 14 Sep: "\(\delta\)-licensed energy clocks" on the GoldbergHexa meridians (2099514038212276507); "The hive already has the right *clocks* for a hydro layer" (2099443159478538700).
    - 15 Sep: "IBL roughness clocks" listed with "GoldbergHexa polarity" (2099800393924411695).
    - 4 Oct: "first clock" (parent mode energy) and "second clock" (daughter multipole momentum) in the Clebsch dictionary (2106721095835341008).
    - 5 Oct: "shared clock on death face and exterior" (2107140069261709764).
    - 8 Oct: "equal-time DHW / quantum-kinetic vacuum clock" (2108221897041178820).
    - 9 Oct: Sen rolling-tachyon array "supplies an intrinsic modular clock" (2108621248569782388; also 2108614730713882829).
    - 15 Oct: "the Reeb clock locks the R-grading" (2110860610057437228).
    - 16 Oct: "modular-flow / holographic-throat clocks" (2111004525020479844); "half-sided inclusion clocks" (2111073171642384556).
    - 17 Oct: "spectral-flow clocks" (2111423884306084140); "modular-flow / imaginary-time lattice clocks" that "lock non-decaying period" (2111473315432759332).
    - 18 Oct: "eternal-observer-to-dilation-clock" bridge (2111612166419726541).
    - 19 Oct: "Floquet-driven modular clocks" (2112148508954464429).
    - 20 Oct: on a GoldbergHexa shell of genus g ≥ 2, "lower-genus clocks remain unchanged" (2112675780090306938).
    - 22 Oct: "modular clock \(\dot{\tau}=1\)" from the rolling-tachyon array (2113213813642162375).
    - 23 Oct: "modular-flow / rolling-tachyon clocks" (2113762665784836220).
    - 24 Oct: "Modular-flow clocks are upgraded by the adiabatic period \(Z=2a/\alpha\)" (2114081072946266570).
    - 28 Oct: "modular-flow clocks track total-divergence terms" (2115407816248725700); "Off-resonant light as modular-flow clock" (2115566495862227376).
  - **OPEN:** some clocks conflict with each other, and there are "a couple no-go zones" (her words, 2098048662672662938). These are kept as open problems under the clash rule.
  - **OPEN:** one no-go comes from "a paper that disallows it due to imaginary wormhole" (same post). Which paper is not named in the post.
  - **OPEN:** making "the 2D tentacles 3D" (2098049275305267366).
  - **OPEN:** what the shapes look like "from the perspective of each clock" (question from @hlmota, 2098181578526503198). Her reply: "Thats actually a good question. I was just staring at the cloud or bottlenecks they were converging on so i didn't stop to think about that" (2098187662997778691).
  - **How it compares:** to do.

---

## Meeting points (living log)
Places where her constructions and published physics line up. Each line gives the date, the shape, the paper or maths, who flagged it, and its status (tested / proposal / meeting point, not a result).

- **29 Oct 2026 · GoldbergHexa pentagons × spherical-crystal scars:** Bausch et al. 2003, https://arxiv.org/abs/cond-mat/0303289. Scars start from R/a ≈ 5, about 360 particles, which puts the threshold near m ≈ 6 [hive estimate] on her shells. Flagged by Venus and Helios. Status: proposal, untested.
- **29 Oct 2026 · Fuzzy cone tip (her fuzzy core) × "Quantum gravity on the bulk cone":** Almheiri, Dodelson & Komargodski, https://arxiv.org/abs/2610.31610. Abstract, quoted: "We show by an explicit calculation in the CFT that this singularity is smoothed out at finite $G_N$. Qualitatively, the singularity resolution is a consequence of the fuzziness of the bulk solution in quantum gravity." Flagged by Helios: the paper smooths the singularity through quantum fuzziness of geometry, which matches her fuzzy core. Status: meeting point, not a result. In plain words, the paper's "bulk cone" singularity is a sharp spike in signals that travel along light rays, not a cone-shaped piece of space. How it links to the hive cone is still OPEN (Venus's draft, C7).

---

## Placeholder list: other shapes to write up later (names and source ids only)
- Cone tip with a soft core: framework of 8 Oct (`AKITTI_FRAMEWORK_2026-10-08.md`); `CONE_TIP_NOTE.md`
- Bubble with strings → brane (the lift): 2105917997588365696
- Deathface (ℝ² → S² handoff, bolt): 2105558608830156964, 2107537800610607257, 2108178649320943947
- Pentaflake defects / hexaflake: 2105558608830156964, 2106721095835341008, 2114568453201736076
- Scar-floor projectors: 2107195607785877804, 2115066790585799001
- Fuzzy sphere / fuzzy bulk cone: 2114568453201736076, 2114320525157904700, 2114179948600566231, 2115116687481504111
- Rolling-tachyon instanton chain, Hopfion-moiré stack, petal tree: 22–28 Oct posts (see Venus draft C4–C6)
- Carrollian/BMS₃ null-hypersurface fluid: 2113648864171319538
- Structured-light spin-orbit layer: 2113671492386852968
- IT1/IT1b instanton on the cone, the edge-holding fix, the flat-grid rerun, vortex modes, HP2/HP3, SM1: see Venus draft C9–C14


### Full list from the "already carries" sections (added 29 Oct)
Akitti's pointer (29 Oct): the shapes are listed at the top of her newer posts and in the sections that say what the hive "already carries" (often titled "Hive inspection (live strata ...)"). Each item gives the first post in the window where it appears.
- **GoldbergHexa hierarchical shells:** nested Goldberg balls (entry GH above). Source: OCT1-8 file, post of 7 Oct 12:44 BST (quoting 2107537800610607257; its own id is not in the file); in almost every later list. How it compares: to do.
- **Residual / scar-floor projectors:** a floor that freezes leftover energy so it stops moving. Source: OCT1-8 file (same post); 2115066790585799001 ("~0.041 floor on meridians"). How it compares: to do.
- **Fuzzy C*-algebra / non-Abelian current layers:** matrix-valued (non-commuting) currents laid on the shapes. Source: OCT1-8 file (same post). How it compares: to do.
- **Holographic-throat residual projectors:** throats (wormhole-like necks) whose leftovers are scored, incl. BTZ-like anyons and RT wedges. Source: OCT1-8 file; 2110860610057437228 (15 Oct). How it compares: to do.
- **Modular-flow clocks (Reeb, half-sided inclusion, imaginary-time, dilation):** the clock family in GH "Pieces that sit on it". Source: 2110860610057437228 (15 Oct) onward. How it compares: to do.
- **Anyonic-braid sectors:** particles whose swaps leave a phase, braided around tips. Source: OCT1-8 file. How it compares: to do.
- **CTMRG/iPEPS contractions:** a tensor-network method for summing up the lattice. Source: OCT1-8 file. How it compares: to do.
- **Viscoelastic clay (Oldroyd-B / Saramito), "E-brane clay":** a springy, gooey fluid layer. Source: OCT1-8 file; 2115520807115866149 (28 Oct). How it compares: to do.
- **Death-face / finite-radius stops:** the place where the flat chart stops and hands off to the ball. Source: OCT1-8 file; 2111004525020479844 (16 Oct). How it compares: to do.
- **Krylov–Lanczos complexity monitors:** a meter of how fast a state spreads out. Source: 2110860610057437228 (15 Oct). How it compares: to do.
- **Fuzzy Cauchy edges:** blurred edges where the starting data is set. Source: 2110860610057437228 (15 Oct). How it compares: to do.
- **Residual-dissipation channels:** where leftover energy drains away. Source: 2111004525020479844 (16 Oct). How it compares: to do.
- **Nonstabilizerness / magic residuals:** how far a quantum state is from the easy-to-simulate kind. Source: 2111033610501316914 (16 Oct); 2111423884306084140 (17 Oct). How it compares: to do.
- **CSS / stabilizer residual projectors:** error-correcting-code layers. Source: 2111423884306084140 (17 Oct). How it compares: to do.
- **Dicke–su(2) collective-spin lattice:** many spins acting as one big spin. Source: 2111473315432759332 (17 Oct). How it compares: to do.
- **Spectral chirp on GoldbergHexa 3-eigenframes / Alfvén-chirp:** sweeping-frequency signals on the ball and in plasmoid chains. Source: 2111160370522112000 (16 Oct). How it compares: to do.
- **Holographic observer patches / observer-centric dS scattering:** scattering seen by observers inside an expanding universe. Source: 2111612166419726541 (18 Oct). How it compares: to do.
- **Euclidean path-integral layers with rolling-tachyon / D-instanton arrays:** a repeating chain of instantons in imaginary time. Source: 2112256303397519494 (19 Oct); 2113213813642162375 (22 Oct). How it compares: to do.
- **Spectral-flow residuals:** zero-mode bookkeeping as things are slowly changed. Source: 2112256303397519494 (19 Oct). How it compares: to do.
- **Geometric quantum-tensor residuals (Berry curvature + quantum metric):** how the quantum state bends in momentum space. Source: 2112148508954464429 (19 Oct). How it compares: to do.
- **CFT₂ holographic maps, worldsheet RNS projections, monopole-locus branches:** string/boundary-theory dictionaries. Source: 2112629817363607873 (20 Oct). How it compares: to do.
- **Hopfions as stacked moiré blankets, merons, Hofstadter petals:** knotted textures and the fractal butterfly with Chern triplets. Source: 2112645088790876494 (20 Oct); 2113762665784836220 (23 Oct, "Hofstadter petal tree"). How it compares: to do.
- **String-tension residuals (S²-bubble / string-pile-up / cone-handoff):** tension that sets the cone deficit angles. Source: 2112804005713768606 (21 Oct). How it compares: to do.
- **Imaginary-time lattice for instanton arrays; M2-brane instanton loci on CY cones:** Source: 2112823960123621881, 2112941654768541777 (21 Oct). How it compares: to do.
- **Geometric encodings of scattering amplitudes (minimal surfaces, knots/HOMFLY corners):** Source: 2112944453241438525 (21 Oct). How it compares: to do.
- **Dual long-range Ising encodings / open-string tachyon condensates:** Source: 2113213813642162375 (22 Oct). How it compares: to do.
- **Chern–Simons / Wen–Zee / Hall-viscosity layer:** Source: 2113627136170869068 (23 Oct). How it compares: to do.
- **Carrollian/BMS₃ null-hypersurface fluid:** Source: 2113648864171319538 (23 Oct). How it compares: to do.
- **Angular-momentum / helicity bases, structured light:** Source: 2113671492386852968 (23 Oct). How it compares: to do.
- **Residual Noether charges → topological invariants (Thouless pump), photonic platforms:** Source: 2114081072946266570 (24 Oct). How it compares: to do.
- **Cone singularity as primary simulation target:** Source: 2114179948600566231 (25 Oct). How it compares: to do.
- **Fuzzy-sphere residual projectors:** the N×N matrix sphere. Source: 2114787714696438213 (26 Oct). How it compares: to do.
- **Graphene-electrode / PT-real bundles, open-ridge polarity, Qin H(div,0) leapfrog as export:** Source: 2115066790585799001 (27 Oct). How it compares: to do.
- **Non-Hermitian exceptional-point stack (EP2 720° double cover, branch cuts):** Source: 2115479762277720267 (28 Oct). How it compares: to do.
- **Critical almost Mathieu operator (Harper model):** Source: 2115541578605543763 (28 Oct). How it compares: to do.
- **Extended Haldane Model inside the QTC Framework:** Source: 2115566495862227376 (28 Oct). How it compares: to do.

---

## Appendix: equations (quoted word for word)
**GH-1** (2105558608830156964, 1 Oct):
`GoldbergHexa-ℝ²-stop ⟶ GoldbergHexa-S²-bolt × ℝ²_⊥`; leftovers `(R_QG|_Γ, λ_EP, I_E, 𝓑−𝓑_univ)`; lock `(ε_EP≈0.5137, I_E≈0.299, λ_EP≈−0.3084 i)`.

**GH-2** (Path B text, OCT1-8 file): `α=1−4Gμ, 2π(1−α)=8πGμ`, with the curvature only at the tip, scored shell by shell. Exterior integral `∫_{D_{r_c}} R[g] dA = 2π(1−α)` (2106801517357351243).

**GH-3** (2114568453201736076, 26 Oct) **[FLAG: CONTRADICTION]**: as written, the two relations do not fit together. With [X^i,X^j]=i(ε^{ijk}/R)X^k the matrices are X=L/R, so ΣX² = j(j+1)/R², not R²(1−1/N). The standard fuzzy sphere uses X=λL with λ=2R/√(N²−1), giving ΣX²=R² (as in Venus's draft, C8). This is likely a normalisation slip, and only the formula is affected. Venus: R²(1−1/N) is likely a slipped form of the λ=2R/N convention, which gives R²(1−1/N²):
`[X^i,X^j]=i(ε^{ijk}/R)X^k, Σ_i (X^i)² = R²(1−1/N)·1`

**GH-5** (2096696000639336601, 6 Sep, before the main window): `hex faces + exactly 12 pentaflake defects, χ=2, ΣK=4π=12×(π/3)`

**GH-4** (betti-berry-vacuum-filter RESULTS, computed): GP(m,0) has 10m²+2 faces (12 pentagons), 30m² face-adjacency edges, 20m² vertices, V−E+F = 2. For m=4: 162 faces, 150 hexagons. Face-site percolation p_c = 1/2 on the infinite lattice [standard, check only].
