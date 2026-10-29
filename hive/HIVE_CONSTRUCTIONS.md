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
- **What it does:** In Akitti's words (29 Oct): "it helps me as a tomography machine basically for the X algorithm on the feed, and helps organize my brain." in her words, "just a lattice to help me probe and organize things" (2105731792439247111, 1 Oct). Her own simulations run "fine with just regular s^2 physics" without it, "but i may need to add it in to the simulations as well to fix stuff" (same post). Other roles in the notes:
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
- **Clashes are intended** (Akitti, 29 Oct): the GoldbergHexa cannot "fire" all the way because it is tracking open problems, so some parts of it clash with each other, and that is intended. The clashes are real errors that still need fixing, but for some of them nobody anywhere has found a fix yet, so they stay on the shape as open problems rather than being patched over (Akitti's correction, 29 Oct). Her words (lightly corrected typos): "the goldberghexa itself cannot fire all the way since it's tracking open problems basically, so there's parts on it that clash. that's as intended"
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

---

## Appendix: equations (quoted word for word)
**GH-1** (2105558608830156964, 1 Oct):
`GoldbergHexa-ℝ²-stop ⟶ GoldbergHexa-S²-bolt × ℝ²_⊥`; leftovers `(R_QG|_Γ, λ_EP, I_E, 𝓑−𝓑_univ)`; lock `(ε_EP≈0.5137, I_E≈0.299, λ_EP≈−0.3084 i)`.

**GH-2** (Path B text, OCT1-8 file): `α=1−4Gμ, 2π(1−α)=8πGμ`, with the curvature only at the tip, scored shell by shell. Exterior integral `∫_{D_{r_c}} R[g] dA = 2π(1−α)` (2106801517357351243).

**GH-3** (2114568453201736076, 26 Oct) **[FLAG: CONTRADICTION]**: as written, the two relations do not fit together. With [X^i,X^j]=i(ε^{ijk}/R)X^k the matrices are X=L/R, so ΣX² = j(j+1)/R², not R²(1−1/N). The standard fuzzy sphere uses X=λL with λ=2R/√(N²−1), giving ΣX²=R² (as in Venus's draft, C8). This is likely a normalisation slip, and only the formula is affected. Venus: R²(1−1/N) is likely a slipped form of the λ=2R/N convention, which gives R²(1−1/N²):
`[X^i,X^j]=i(ε^{ijk}/R)X^k, Σ_i (X^i)² = R²(1−1/N)·1`

**GH-5** (2096696000639336601, 6 Sep, before the main window): `hex faces + exactly 12 pentaflake defects, χ=2, ΣK=4π=12×(π/3)`

**GH-4** (betti-berry-vacuum-filter RESULTS, computed): GP(m,0) has 10m²+2 faces (12 pentagons), 30m² face-adjacency edges, 20m² vertices, V−E+F = 2. For m=4: 162 faces, 150 hexagons. Face-site percolation p_c = 1/2 on the infinite lattice [standard, check only].
