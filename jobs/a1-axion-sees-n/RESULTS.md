# Job A1: does an S² axion see n?

Generated: 2026-10-02 20:59:24 GMT Summer Time (BST/local time)
Tags: [computed] [identity] [standard] [assumed] [tuned] [post-hoc] [hive-interpretation].
Inputs read-only: UNIFYING_THREAD sha256 CDE3C256 (expected CDE3C256); STILL_TO_DO sha256 1AEC133B (used current hash, expected 1AEC133B).
Job 5b source read-only: run.py sha256 586C6BC8; RESULTS.md sha256 6146CF25.

## Setup [assumed]

Base is Job 5b V(R) = 4πΛ₆/R − 4π/R² + (π/2)n²/R³ + C/R⁴, in its s = 1 units; C = -3.0 is retained in the written base but set to zero for the isolated k-family attribution test [assumed].
Test vacuum: θ = π, the half-period displaced axion vacuum, with monodromy branch step m = -1; q = θ/(2π) = 0.5. This is not the axion's own minimum θ = 0 [assumed input].
Candidate 2-form/flux cross-term: V_ax = η m q n/R³, η = 1.0, effective coefficient ηmq = -0.500000 [assumed input]. Natural means 0.1–10.0 in Job 5b units [identity/rule].
At θ = 0, V_ax = 0 and the control is blind; that control is reported but is not the displaced-vacuum grade [identity].

## Scaling test [computed]

Under n → k n, Λ₆ → Λ₆/k², R → k²R: the Job 5b n²/R³ term scales as k⁻⁴, while the linear axion term scales as k⁻⁵. A positive energy rescale cannot make both scalings equal [identity].
Symbolic base k-family identity: True [identity].
Symbolic linear-axion scaling identity: True [identity].
| base Λ₆ | k | p control (θ=0) | p axion (θ=π) | axion Δp/p_control | V_ax scaling residual |
|---:|---:|---:|---:|---:|---:|
| 0.259397739 | 1 | 0.410686991 | 0.506044835 | +2.321911e-01 | 0.000000e+00 |
| 0.259397739 | 2 | 0.410686991 | 0.458976534 | +1.175824e-01 | 5.000000e-01 |
| 0.259397739 | 3 | 0.410686991 | 0.443055510 | +7.881555e-02 | 6.666667e-01 |
| 0.259397739 | 4 | 0.410686991 | 0.435037103 | +5.929117e-02 | 7.500000e-01 |
| 0.259397739 | 5 | 0.410686991 | 0.430204811 | +4.752481e-02 | 8.000000e-01 |
| 0.259397739 | 6 | 0.410686991 | 0.426973687 | +3.965720e-02 | 8.333333e-01 |

| 0.271377217 | 1 | 0.377194656 | 0.480758172 | +2.745625e-01 | 0.000000e+00 |
| 0.271377217 | 2 | 0.377194656 | 0.430330368 | +1.408708e-01 | 5.000000e-01 |
| 0.271377217 | 3 | 0.377194656 | 0.413031778 | +9.500962e-02 | 6.666667e-01 |
| 0.271377217 | 4 | 0.377194656 | 0.404250789 | +7.172989e-02 | 7.500000e-01 |
| 0.271377217 | 5 | 0.377194656 | 0.398932260 | +5.762967e-02 | 8.000000e-01 |
| 0.271377217 | 6 | 0.377194656 | 0.395363569 | +4.816853e-02 | 8.333333e-01 |

| 0.283356695 | 1 | 0.337509923 | 0.454116604 | +3.454911e-01 | 0.000000e+00 |
| 0.283356695 | 2 | 0.337509923 | 0.399133338 | +1.825825e-01 | 5.000000e-01 |
| 0.283356695 | 3 | 0.337509923 | 0.379715065 | +1.250486e-01 | 6.666667e-01 |
| 0.283356695 | 4 | 0.337509923 | 0.369676683 | +9.530612e-02 | 7.500000e-01 |
| 0.283356695 | 5 | 0.337509923 | 0.363520169 | +7.706513e-02 | 8.000000e-01 |
| 0.283356695 | 6 | 0.337509923 | 0.359351472 | +6.471380e-02 | 8.333333e-01 |

Control θ = 0: n²-only family remains blind: True [computed].
Displaced θ = π: linear-n family breaks the rescaling: True; max |Δp/p| = 1.825825e-01; max scaling residual = 8.333333e-01 [computed].
Naturalness check: |effective coefficient| = 0.500000 is within factor-10 range [0.1, 10.0]: True [computed].
A1 grade: PASS — the displaced half-period vacuum supplies a natural linear-in-n monodromy term; the own-minimum vacuum is blind [computed].

Spec ambiguity resolved [post-hoc]: UNIFYING_THREAD says Aethon's 6D axion form is assumed input but does not print its coefficient or radial power. This cheap test uses the minimal linear monodromy cross-term η m q n/R³, the allowed n-sensitive mechanism; a derived 6D form could change the physics grade.

## Read-only audit [computed]

UNIFYING_THREAD.md, STILL_TO_DO.md and Job 5b sources unchanged [computed].
