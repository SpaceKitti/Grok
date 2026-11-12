# FUZZY_CONE_SPEC_V2_1 (Venus). Supersedes V2 2d8e943a. Frozen before any build.
Holds only what post 2110455808366633013 says: strings stack together -> tension -> a fuzzy cone singularity at BOTH poles of her sphere. Dropped from V2: the ring-stack reading, the 1/alpha step rule, any alpha put in by hand, and the spindle metric with a chosen alpha. The cone angle is an OUTPUT, never an input.
Each piece and its reason:
- Fuzzy sphere S^2_N at finite N: her sphere, fuzzy by her standing default (fuzzy tips). Round, with no deformation put in.
- Stacked strings: n coincident vortices (strings) at each pole, i.e. winding n at the north and at the south pole, total flux 2n. Reason: this is the post's "strings stack". The fuzzy-sphere vortex is known in the literature (fuzzy-sphere abelian Higgs), and it is used here only as the field content.
- Energy: the self-dual form, 4b normalisation (e0bb1cd9), in matrix form. Reason: the fix verified in our sims.
- Tension to cone: tension mu per pole is MEASURED. The deficit is read from it as delta = 8 pi G mu (the standard string-deficit relation, used as a check, Vilenkin 1981); G is not chosen and delta/(8 pi G) = mu is reported. A self-consistent metric back-reaction is the next step and stays OPEN.
Required check: the Bradlow condition. Vortices on a compact sphere exist only if the area exceeds 4 pi x (flux) in core units. Pick R so that it holds with margin >= 2 for n=2, and report it. If it fails, that is a construction bug, not a result.
Tests (F1-F5 carried over, restated without alpha):
F1 control: as N grows, the matrix symbol approaches the continuum two-pole vortex on the round sphere (sup error <= 1% at the largest N).
F2 fuzzy tip survives: the gap from the continuum inside 3 lambda of each pole is >= 5% at N=21 and shrinks with N (log-log slope in [-1.5,-0.5]). No gap means FAIL; a gap that doesn't shrink means a bug.
F3 charge: flux in each polar cap (theta <= theta_c, with the cap set by r_c = 1.5 rho) is within 0.02 of n, and the pole projector rank equals n exactly.
F4 stacking -> tension -> angle: mu(n)/(pi|n|) within 2% of 1 at the largest N, so the deficit is proportional to n (the "angle encodes charge" test, done via tension). The finite-N deviation is reported as the fuzzy correction.
F5 energy: E/(2 pi |n|) -> 1 as N grows.
Fuzzy-start vs smooth-start: solve once from the coherent-state projector seed and once from a smooth continuum seed. At each N the final matrices must agree to 1e-6 (fuzziness lives in the equations, not the seed). Report both.
Short test run: n=1,2 at N=21 and 41 only. Grade F3, F5, the start check, and F4 at N=41 as provisional. F1 and F2 need N=81 later.
Nothing extra enters without a reason from our sims or findings, shown to Akitti as a result first.
