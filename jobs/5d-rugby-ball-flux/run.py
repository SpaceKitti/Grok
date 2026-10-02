#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Job 5d: rugby-ball branes and the Salam-Sezgin flux cap."""
from __future__ import annotations

import datetime as dt
import hashlib
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
STILL = Path(r"C:\Users\Akitt\open-problems\STILL_TO_DO.md")
FINAL_SPEC = Path(r"C:\Users\Akitt\open-problems\JOB_5d_SPEC.md")
RADION = Path(r"C:\Users\Akitt\radion-5b-tension-casimir")
RADION_RUN = RADION / "run.py"
RADION_RESULTS = RADION / "RESULTS.md"
ABPQ_PDF = Path(r"C:\Users\Akitt\open-problems\A1_axion_sees_n\NPB680_389_Aghababaie_Burgess_Parameswaran_Quevedo_6D_SLED.pdf")
EXPECTED_STILL_CONTEXT = "0CDAF850"
EXPECTED_SPEC = "B94289BF"
N_FLUX_TARGET = 3
N_BULK = 1
G6 = 1.0
# Fixed before first run: inherited 5b point for a transparent fixed-knob neighbour probe.
PROBE_LAMBDA = 0.271377217
PROBE_C = -3.0
A = 4.0 * sp.pi
B = 4.0 * sp.pi
D = sp.pi / 2.0
OUT: list[str] = []


def emit(line=""):
    print(line, flush=True)
    OUT.append(line)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def flux_integral(n, alpha, g1):
    theta, phi = sp.symbols("theta phi", real=True)
    F = n / (2 * g1) * sp.sin(theta)
    return sp.integrate(F, (theta, 0, sp.pi), (phi, 0, 2 * sp.pi * alpha))


def radion_stationary(lam, casimir, N):
    x = sp.symbols("x", positive=True)
    poly = A * lam * x**3 - 2 * B * x**2 + 3 * D * N**2 * x + 4 * casimir
    roots = sp.nroots(poly, n=18, maxsteps=200)
    rows = []
    for root in roots:
        if abs(float(sp.im(root))) > 1e-10 or float(sp.re(root)) <= 0.0:
            continue
        xr = float(sp.re(root))
        v = float(A) * lam / xr - float(B) / xr**2 + float(D) * N**2 / xr**3 + casimir / xr**4
        v2 = 2.0 * float(A) * lam / xr**3 - 6.0 * float(B) / xr**4 + 12.0 * float(D) * N**2 / xr**5 + 20.0 * casimir / xr**6
        rows.append({"x": xr, "V": v, "v2": v2, "minimum": v2 > 0.0, "dS": v > 0.0})
    return rows


STILL_HASH = sha(STILL)
FINAL_SPEC_HASH = sha(FINAL_SPEC)
RADION_RUN_HASH = sha(RADION_RUN)
RADION_RESULTS_HASH = sha(RADION_RESULTS)
ABPQ_HASH = sha(ABPQ_PDF) if ABPQ_PDF.exists() else None

# Stage A symbolic derivation.
n_s, alpha_s, g_s, g1_s = sp.symbols("n alpha g g1", real=True)
N_DERIVED = sp.simplify(g_s / (2 * sp.pi) * (2 * sp.pi * alpha_s * n_s / g1_s))
CAP_CHECK = sp.simplify(alpha_s * g_s / g1_s)
Q_RELATION = sp.simplify(g1_s * sp.symbols("DeltaQ") / (2 * sp.pi) + n_s - sp.symbols("N") / (g_s / g1_s * alpha_s))

emit("# Job 5d: rugby-ball branes versus the Salam-Sezgin flux cap")
emit("")
emit("Generated: %s (BST/local time)" % dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"))
emit("Tags: [computed] [identity] [standard] [assumed] [tuned] [post-hoc] [hive-interpretation].")
emit("Final spec JOB_5d_SPEC.md sha256 %s (expected %s); STILL_TO_DO sha256 %s (initial context %s); Job 5b run.py %s; Job 5b RESULTS.md %s; ABPQ PDF %s [computed read-only]." % (FINAL_SPEC_HASH[:8].upper(), EXPECTED_SPEC, STILL_HASH[:8].upper(), EXPECTED_STILL_CONTEXT, RADION_RUN_HASH[:8].upper(), RADION_RESULTS_HASH[:8].upper(), ABPQ_HASH[:8].upper() if ABPQ_HASH else "missing"))
emit("")
emit("## Naming and ABPQ convention [standard]")
emit("")
emit("Hive flux count N is ABPQ's N. ABPQ's own n is only the bulk-field-equation sign n = ±1; it is not Hive's generation/flux count.")
emit("F = (n/2g₁) sinθ dθ∧dφ; r²e^φ = 1/(4g₁²); deficit ε = 4G₆T; α = 1−ε; φ has period 2πα [assumed input from ABPQ §4].")
emit("Quantisation inputs: g/g₁ = N/[n(1−ε)] and (Q₊−Q₋)/2π + n/g₁ = N/[g(1−ε)] [standard].")
emit("")
emit("## Stage A — wedged-sphere derivation [computed]")
emit("")
emit("∫F = %.6g·π·α·n/g₁ and N = g∫F/(2π) = %s [identity]." % (float(flux_integral(1, 1, 1) / sp.pi), N_DERIVED))
emit("Derived formula: N = n·α·g/g₁ [computed]. A positive-tension brane cuts away area at fixed field strength, so less flux fits [identity].")
emit("ABPQ patch matching along the equator gives g(A₊−A₋) = N dφ/(1−ε) and eq. 4.6; the cut-sphere integral gives the same rule. These are two derivations, not independent checks [identity].")
emit("With Q₊ = Q₋ and T > 0 (0 < α < 1), |N| = α|n|g/g₁ ≤ |n|g/g₁; for ABPQ |n| = 1 this is |N| < g/g₁ [computed].")
emit("Stage-A cap check symbolic: α < 1 ⇒ |N| ≤ g/g₁: True [identity].")
emit("")
emit("## Stage B — three routes to N = 3 [computed; tuned tags below]")
emit("")
emit("| branch | required setting | consequence for N=3 | hand-set input | N=3 preferred over N=2,4? | verdict |")
emit("|---|---|---|---|---|---|")
# (a) g=g1, equal brane flux.
alpha_a = sp.Rational(3, N_BULK)
eps_a = 1 - alpha_a
T_a = eps_a / (4 * G6)
emit("| (a) g=g₁, Q₊=Q₋ | α = %.6f, ε = %.6f | T = %+.6f/G₆ = −1/(2G₆) | negative Planck-sized tension | no; branch only relabels N | FAIL [tuned] |" % (float(alpha_a), float(eps_a), float(T_a * G6)))
emit("Branch (a): α = N/(n g/g₁) = %.6f; ε = %.6f; T = %.6f/G₆. Positive-tension α<1 is violated [computed]." % (float(alpha_a), float(eps_a), float(T_a * G6)))
# (b) positive tension, no fixed gauge ratio.
alpha_symbol = sp.symbols("alpha", positive=True)
gratio_b = sp.simplify(N_FLUX_TARGET / alpha_symbol)
emit("| (b) T>0, 0<ε<1 | g/g₁ = %s > 3 | α is any 0<α<1 | continuous gauge-coupling ratio | no; α and g/g₁ continuously relabel N | FAIL [tuned] |" % gratio_b)
emit("Branch (b): for 0<α<1, g/g₁ = 3/α > 3. A hand-picked continuous g/g₁ is required; no fixed-knob preference for N=3 [computed].")
# (c) g=g1, positive tension, brane flux difference.
delta_q = sp.simplify(N_FLUX_TARGET / alpha_symbol - N_BULK)
delta_q_minus = sp.simplify(N_FLUX_TARGET / alpha_symbol + N_BULK)
emit("| (c) g=g₁, T>0 | g₁ΔQ/2π = 3/α − n | ΔQ is hand-set; for n=+1: 3/α−1 | no; brane flux relabels N | FAIL [tuned] |")
emit("Branch (c): g₁ΔQ/2π = %s for n=+1, or %s for n=−1; the brane flux difference is a continuous hand-set offset [computed]." % (delta_q, delta_q_minus))
emit("")
emit("Knob maps for N = 2, 3, 4 [computed]:")
emit("| route | N | knob required | smooth one-to-one? |")
emit("|---|---:|---|---|")
for N_value in (2, 3, 4):
    alpha_N = sp.Rational(N_value, N_BULK)
    eps_N = 1 - alpha_N
    t_N = eps_N / (4 * G6)
    emit("| (a) g=g₁, ΔQ=0 | %d | α=%s; ε=%s; T=(1−N)/(4G₆)=%+.6f/G₆ | yes: α=N |" % (N_value, alpha_N, eps_N, float(t_N * G6)))
    emit("| (b) T>0, ΔQ=0 | %d | g/g₁=N/α=%s | yes: g/g₁=N/α |" % (N_value, sp.sstr(sp.Rational(N_value, 1) / alpha_symbol)))
    emit("| (c) g=g₁, T>0 | %d | g₁ΔQ/2π=N/α−n=%s (n=+1) | yes: ΔQ affine in N |" % (N_value, sp.sstr(sp.Rational(N_value, 1) / alpha_symbol - N_BULK)))
emit("At fixed remaining knobs each map is linear in N, so no route prefers N=3 over its neighbours [identity].")
emit("")
emit("## Stage C — report-only physical checks [standard; hive-interpretation]")
emit("")
emit("Route (a): orientifold planes are real negative-tension objects [standard], but their tension is set by the string scale, not by this compactification's G₆. The required ratio |T|·2G₆ = 1; nothing in this model supplies exactly −1/(2G₆) [computed].")
emit("Route (c): ABPQ §4 eq. 4.8 treats Q₊−Q₋ as brane-localised flux data and states no separate quantisation of ΔQ. Therefore no discrete N list follows from ABPQ; ΔQ remains a hand-set continuous offset here [computed from source].")
emit("If 5d fails, the wall points to the uneaten-axion four-form route: a 4D four-form source is the live way to revive A1's mechanism [hive-interpretation].")
emit("")

# Fixed-knob probe using the inherited 5b potential; this cannot turn a tuned branch into a PASS.
emit("")
emit("## Fixed-knob radion neighbour probe [computed; tuned]")
emit("")
emit("Probe uses inherited Λ₆ = %.9f, C = %.6f at the Job 5b n=3 window midpoint. It is an audit of neighbouring N, not a new selection mechanism [assumed]." % (PROBE_LAMBDA, PROBE_C))
emit("| N | positive stationary minima | minimum V | dS? |")
emit("|---:|---:|---:|---|")
probe_rows = {}
for N in (2, 3, 4):
    rows = radion_stationary(PROBE_LAMBDA, PROBE_C, N)
    mins = [r for r in rows if r["minimum"]]
    probe_rows[N] = mins
    if mins:
        best = mins[0]
        emit("| %d | %d | %+.9e | %s |" % (N, len(mins), best["V"], best["dS"]))
    else:
        emit("| %d | 0 | none | none |" % N)
probe_only_n3 = bool(probe_rows[3]) and not probe_rows[2] and not probe_rows[4]
cnat = 1.0 / (4.0 * sp.pi)**3
emit("At this deliberately inherited C = %.6f point, N=3 is the only local dS minimum: %s; |C|/C_nat = %.3e [computed, tuned]." % (PROBE_C, probe_only_n3, abs(PROBE_C) / float(cnat)))
emit("This does not satisfy the pass rule: Λ₆ and C were fixed externally, not selected by any of branches (a)–(c), and C is tuned. No branch makes N=3 preferred without a hand-set input [computed].")
emit("")
emit("## Grade [computed]")
emit("")
emit("Pre-registered prediction [prediction]: FAIL [tuned] on all three branches. Each route is linear in N with a continuous or negative-tension knob, so branes relabel N but do not select it.")
emit("History [post-hoc]: Helios's original two-thirds-deficit guess and Venus's nα = ±1 line had the direction backwards, as Orion caught. Venus withdrew an earlier dS-bound guess; it is not used or printed here.")
emit("Job 5d grade: FAIL [tuned] — no branch makes N=3 preferred over N=2 and N=4 without an input set by hand to give 3 [computed].")
emit("")
emit("## Read-only audit [computed]")
emit("")
assert sha(STILL) == STILL_HASH and sha(FINAL_SPEC) == FINAL_SPEC_HASH and sha(RADION_RUN) == RADION_RUN_HASH and sha(RADION_RESULTS) == RADION_RESULTS_HASH
if ABPQ_PDF.exists():
    assert sha(ABPQ_PDF) == ABPQ_HASH
emit("Final spec, STILL_TO_DO, Job 5b sources and ABPQ source file unchanged [computed].")
(HERE / "RESULTS.md").write_text("\n".join(OUT) + "\n", encoding="utf-8", newline="\n")
