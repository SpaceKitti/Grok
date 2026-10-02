# Job 5d: rugby-ball branes versus the Salam-Sezgin flux cap

Generated: 2026-10-02 21:31:45 GMT Summer Time (BST/local time)
Tags: [computed] [identity] [standard] [assumed] [tuned] [post-hoc] [hive-interpretation].
Final spec JOB_5d_SPEC.md sha256 B94289BF (expected B94289BF); STILL_TO_DO sha256 0A19A935 (initial context 0CDAF850); Job 5b run.py 586C6BC8; Job 5b RESULTS.md 6146CF25; ABPQ PDF B7CB0FE5 [computed read-only].

## Naming and ABPQ convention [standard]

Hive flux count N is ABPQ's N. ABPQ's own n is only the bulk-field-equation sign n = ±1; it is not Hive's generation/flux count.
F = (n/2g₁) sinθ dθ∧dφ; r²e^φ = 1/(4g₁²); deficit ε = 4G₆T; α = 1−ε; φ has period 2πα [assumed input from ABPQ §4].
Quantisation inputs: g/g₁ = N/[n(1−ε)] and (Q₊−Q₋)/2π + n/g₁ = N/[g(1−ε)] [standard].

## Stage A — wedged-sphere derivation [computed]

∫F = 2·π·α·n/g₁ and N = g∫F/(2π) = alpha*g*n/g1 [identity].
Derived formula: N = n·α·g/g₁ [computed]. A positive-tension brane cuts away area at fixed field strength, so less flux fits [identity].
ABPQ patch matching along the equator gives g(A₊−A₋) = N dφ/(1−ε) and eq. 4.6; the cut-sphere integral gives the same rule. These are two derivations, not independent checks [identity].
With Q₊ = Q₋ and T > 0 (0 < α < 1), |N| = α|n|g/g₁ ≤ |n|g/g₁; for ABPQ |n| = 1 this is |N| < g/g₁ [computed].
Stage-A cap check symbolic: α < 1 ⇒ |N| ≤ g/g₁: True [identity].

## Stage B — three routes to N = 3 [computed; tuned tags below]

| branch | required setting | consequence for N=3 | hand-set input | N=3 preferred over N=2,4? | verdict |
|---|---|---|---|---|---|
| (a) g=g₁, Q₊=Q₋ | α = 3.000000, ε = -2.000000 | T = -0.500000/G₆ = −1/(2G₆) | negative Planck-sized tension | no; branch only relabels N | FAIL [tuned] |
Branch (a): α = N/(n g/g₁) = 3.000000; ε = -2.000000; T = -0.500000/G₆. Positive-tension α<1 is violated [computed].
| (b) T>0, 0<ε<1 | g/g₁ = 3/alpha > 3 | α is any 0<α<1 | continuous gauge-coupling ratio | no; α and g/g₁ continuously relabel N | FAIL [tuned] |
Branch (b): for 0<α<1, g/g₁ = 3/α > 3. A hand-picked continuous g/g₁ is required; no fixed-knob preference for N=3 [computed].
| (c) g=g₁, T>0 | g₁ΔQ/2π = 3/α − n | ΔQ is hand-set; for n=+1: 3/α−1 | no; brane flux relabels N | FAIL [tuned] |
Branch (c): g₁ΔQ/2π = (3 - alpha)/alpha for n=+1, or (alpha + 3)/alpha for n=−1; the brane flux difference is a continuous hand-set offset [computed].

Knob maps for N = 2, 3, 4 [computed]:
| route | N | knob required | smooth one-to-one? |
|---|---:|---|---|
| (a) g=g₁, ΔQ=0 | 2 | α=2; ε=-1; T=(1−N)/(4G₆)=-0.250000/G₆ | yes: α=N |
| (b) T>0, ΔQ=0 | 2 | g/g₁=N/α=2/alpha | yes: g/g₁=N/α |
| (c) g=g₁, T>0 | 2 | g₁ΔQ/2π=N/α−n=-1 + 2/alpha (n=+1) | yes: ΔQ affine in N |
| (a) g=g₁, ΔQ=0 | 3 | α=3; ε=-2; T=(1−N)/(4G₆)=-0.500000/G₆ | yes: α=N |
| (b) T>0, ΔQ=0 | 3 | g/g₁=N/α=3/alpha | yes: g/g₁=N/α |
| (c) g=g₁, T>0 | 3 | g₁ΔQ/2π=N/α−n=-1 + 3/alpha (n=+1) | yes: ΔQ affine in N |
| (a) g=g₁, ΔQ=0 | 4 | α=4; ε=-3; T=(1−N)/(4G₆)=-0.750000/G₆ | yes: α=N |
| (b) T>0, ΔQ=0 | 4 | g/g₁=N/α=4/alpha | yes: g/g₁=N/α |
| (c) g=g₁, T>0 | 4 | g₁ΔQ/2π=N/α−n=-1 + 4/alpha (n=+1) | yes: ΔQ affine in N |
At fixed remaining knobs each map is linear in N, so no route prefers N=3 over its neighbours [identity].

## Stage C — report-only physical checks [standard; hive-interpretation]

Route (a): orientifold planes are real negative-tension objects [standard], but their tension is set by the string scale, not by this compactification's G₆. The required ratio |T|·2G₆ = 1; nothing in this model supplies exactly −1/(2G₆) [computed].
Route (c): ABPQ §4 eq. 4.8 treats Q₊−Q₋ as brane-localised flux data and states no separate quantisation of ΔQ. Therefore no discrete N list follows from ABPQ; ΔQ remains a hand-set continuous offset here [computed from source].
If 5d fails, the wall points to the uneaten-axion four-form route: a 4D four-form source is the live way to revive A1's mechanism [hive-interpretation].


## Fixed-knob radion neighbour probe [computed; tuned]

Probe uses inherited Λ₆ = 0.271377217, C = -3.000000 at the Job 5b n=3 window midpoint. It is an audit of neighbouring N, not a new selection mechanism [assumed].
| N | positive stationary minima | minimum V | dS? |
|---:|---:|---:|---|
| 2 | 0 | none | none |
| 3 | 1 | +1.429972843e-01 | True |
| 4 | 0 | none | none |
At this deliberately inherited C = -3.000000 point, N=3 is the only local dS minimum: True; |C|/C_nat = 5.953e+03 [computed, tuned].
This does not satisfy the pass rule: Λ₆ and C were fixed externally, not selected by any of branches (a)–(c), and C is tuned. No branch makes N=3 preferred without a hand-set input [computed].

## Grade [computed]

Pre-registered prediction [prediction]: FAIL [tuned] on all three branches. Each route is linear in N with a continuous or negative-tension knob, so branes relabel N but do not select it.
History [post-hoc]: Helios's original two-thirds-deficit guess and Venus's nα = ±1 line had the direction backwards, as Orion caught. Venus withdrew an earlier dS-bound guess; it is not used or printed here.
Job 5d grade: FAIL [tuned] — no branch makes N=3 preferred over N=2 and N=4 without an input set by hand to give 3 [computed].

## Read-only audit [computed]

Final spec, STILL_TO_DO, Job 5b sources and ABPQ source file unchanged [computed].
