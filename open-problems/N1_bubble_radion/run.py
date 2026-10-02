#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Job N1: cheap term-by-term bubble versus radion comparison."""
from __future__ import annotations

import datetime as dt
import hashlib
import itertools
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
UNIFYING = Path(r"C:\Users\Akitt\open-problems\UNIFYING_THREAD.md")
STILL = Path(r"C:\Users\Akitt\open-problems\STILL_TO_DO.md")
RADION = Path(r"C:\Users\Akitt\radion-5b-tension-casimir")
RADION_RUN = RADION / "run.py"
RADION_RESULTS = RADION / "RESULTS.md"
EXPECTED_UNIFYING = "CDE3C256"
EXPECTED_STILL = "1AEC133B"
LAMBDA_WINDOW = (0.259398, 0.283357)
C_RADION = -3.0
N_FLUX = 3
KAPPAS = (1.0, 1.4)
# Fixed before the first run: standard static Rayleigh--Plesset potential convention.
P_AMBIENT = -1.0
SIGMA = 1.0
GAS_NORMALISATION = 1.0
OUT: list[str] = []


def emit(line=""):
    print(line, flush=True)
    OUT.append(line)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bubble_terms(kappa: float):
    # U_b(r) = 4π p∞ r³/3 + 4πσ r² + gas work.
    # For κ>1, gas work = 4πG/[3(κ−1)] r^[3(1−κ)].
    # For κ=1, gas work = −4πG log(r/r0), not a power.
    gas_power = None if kappa == 1.0 else 3.0 * (1.0 - kappa)
    return [
        {"name": "ambient pressure", "power": 3.0, "sign": -1, "coefficient": P_AMBIENT},
        {"name": "surface tension", "power": 2.0, "sign": 1, "coefficient": SIGMA},
        {"name": "gas", "power": gas_power, "sign": 1, "coefficient": GAS_NORMALISATION},
    ]


RADION_TERMS = [
    {"name": "vacuum Λ₆", "power": -1.0, "sign": 1},
    {"name": "curvature", "power": -2.0, "sign": -1},
    {"name": "flux", "power": -3.0, "sign": 1},
    {"name": "Casimir", "power": -4.0, "sign": -1},
]


def candidate_for_power(power: float | None, alpha: float):
    if power is None:
        return None
    mapped = power / alpha
    for term in RADION_TERMS:
        if abs(mapped - term["power"]) < 1e-10:
            return term
    return None


def best_alpha_for_kappa(kappa: float):
    terms = bubble_terms(kappa)
    # A physical κ=1.4 can match two bubble powers only at α=-1:
    # 3/α=-3 and 2/α=-2. Enumerate all pair-derived candidates anyway.
    candidates = set()
    for a, b in itertools.combinations(terms, 2):
        if a["power"] is None or b["power"] is None:
            continue
        for ra, rb in itertools.permutations(RADION_TERMS, 2):
            if ra["power"] == 0 or rb["power"] == 0:
                continue
            aa = a["power"] / ra["power"]
            ab = b["power"] / rb["power"]
            if abs(aa - ab) < 1e-10 and abs(aa) > 1e-12:
                candidates.add(round(aa, 12))
    scored = []
    for alpha in sorted(candidates):
        rows = []
        power_matches = 0
        sign_matches = 0
        for term in terms:
            target = candidate_for_power(term["power"], alpha)
            if target is not None:
                power_matches += 1
                if term["sign"] == target["sign"]:
                    sign_matches += 1
            rows.append((term, target, term["power"] / alpha if term["power"] is not None else None))
        scored.append((power_matches, sign_matches, alpha, rows))
    if not scored:
        return None, terms
    scored.sort(key=lambda q: (q[0], q[1], -abs(q[2])), reverse=True)
    return scored[0], terms


def blake_threshold(kappa: float):
    # U'_b/(4πr²) = p∞ + 2σ/r − G r^(−3κ).
    rcrit = (3.0 * kappa * GAS_NORMALISATION / (2.0 * SIGMA)) ** (1.0 / (3.0 * kappa - 1.0))
    pcrit = GAS_NORMALISATION * rcrit ** (-3.0 * kappa) - 2.0 * SIGMA / rcrit
    return rcrit, pcrit


def radion_fold():
    # For V=AΛ/R−B/R²+D/R³+C/R⁴, V'=V''=0 gives
    # B R²−3 D R−6 C=0 and then Λ from V'=0.
    A = 4.0 * sp.pi
    B = 4.0 * sp.pi
    D = sp.pi / 2.0 * N_FLUX**2
    C = C_RADION
    R = sp.symbols("R", positive=True)
    roots = sp.solve(B * R**2 - 3.0 * D * R - 6.0 * C, R)
    positive = [float(sp.N(q, 16)) for q in roots if q.is_real and q > 0]
    candidates = []
    for radius in positive:
        lam = (2.0 * float(B) * radius**2 - 3.0 * float(D) * radius - 4.0 * C) / (float(A) * radius**3)
        candidates.append((lam, radius))
    lam, radius = max(candidates)
    return radius, lam


# Read-only source audit before emitting results.
U_HASH = sha(UNIFYING)
S_HASH = sha(STILL)
RR_HASH = sha(RADION_RUN)
RS_HASH = sha(RADION_RESULTS)

emit("# Job N1: bubble versus radion")
emit("")
emit("Generated: %s (BST/local time)" % dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"))
emit("Tags: [computed] [identity] [standard] [assumed] [tuned] [post-hoc] [hive-interpretation].")
emit("Inputs read-only: UNIFYING_THREAD sha256 %s (expected %s); STILL_TO_DO sha256 %s (expected %s)." % (U_HASH[:8].upper(), EXPECTED_UNIFYING, S_HASH[:8].upper(), EXPECTED_STILL))
emit("Radion source read-only: run.py sha256 %s; RESULTS.md sha256 %s." % (RR_HASH[:8].upper(), RS_HASH[:8].upper()))
emit("")
emit("## Conventions [assumed]")
emit("")
emit("Bubble static potential: U_b(r) = 4π p∞ r³/3 + 4πσ r² + gas work, with p∞ = -1 (liquid under tension), σ = 1, and gas normalisation G = 1.")
emit("For κ > 1 the gas term is +4πG r^[3(1−κ)]/[3(κ−1)]; at κ = 1 it is −4πG log(r/r₀), not a power [identity].")
emit("Radion potential: V(R) = 4πΛ₆/R − 4π/R² + (π/2)n²/R³ + C/R⁴, with n = 3, C = −3 and Λ₆ in [%.6f, %.6f] [computed inherited input]." % LAMBDA_WINDOW)
emit("Allowed map tested exactly as fixed: R = c r^α with α ≠ 0 monotone and c > 0, plus a positive constant energy rescale; no r^β multiplier [assumed rule].")
emit("")
emit("## Term powers and signs [computed]")
emit("")
emit("Radion powers/signs: Λ₆/R (+), curvature/R² (−), flux/R³ (+), Casimir/R⁴ (−).")
for kappa in KAPPAS:
    best, terms = best_alpha_for_kappa(kappa)
    emit("")
    emit("κ = %.1f (%s) [standard]:" % (kappa, "isothermal" if kappa == 1.0 else "adiabatic air"))
    if best is None:
        emit("No two-power candidate exists because the gas term is logarithmic.")
        continue
    power_matches, sign_matches, alpha, rows = best
    emit("Best power candidate: α = %.6f, matching %d/3 powers and %d/3 signs [computed]." % (alpha, power_matches, sign_matches))
    emit("| bubble term | r power | mapped R power | radion candidate | sign match |")
    emit("|---|---:|---:|---|---|")
    for term, target, mapped in rows:
        power_text = "log" if term["power"] is None else "%.6f" % term["power"]
        mapped_text = "log" if mapped is None else "%.6f" % mapped
        target_text = "none" if target is None else target["name"]
        sign_text = "—" if target is None else ("yes" if term["sign"] == target["sign"] else "NO")
        emit("| %s | %s | %s | %s | %s |" % (term["name"], power_text, mapped_text, target_text, sign_text))
    gas_note = "remains logarithmic" if kappa == 1.0 else "maps to a positive power"
    emit("The α = −1 pair sends ambient r³ → flux R⁻³ and surface r² → curvature R⁻²; both signs disagree. The κ=%.1f gas term %s and has no radion candidate." % (kappa, gas_note))

emit("")
emit("## Blake threshold versus radion fold [computed]")
emit("")
for kappa in KAPPAS:
    rb, pb = blake_threshold(kappa)
    emit("κ = %.1f: Blake fold radius r_B = %.9f; critical ambient pressure p∞,B = %+.9f (negative, tension) [computed]." % (kappa, rb, pb))
rfold, lfold = radion_fold()
emit("Radion C = %.1f, n = %d stationary-point fold: R_fold = %.9f, Λ₆,fold = %.9f; supplied dS window is %.6f–%.6f [computed]." % (C_RADION, N_FLUX, rfold, lfold, LAMBDA_WINDOW[0], LAMBDA_WINDOW[1]))
emit("Threshold coincidence is not a valid PASS comparison: the complete allowed term/sign map already fails. A positive energy rescale cannot repair powers or signs [identity].")
emit("")
emit("## Knobs and grade [computed]")
emit("")
emit("Formal map knobs are α and κ, so two exponents could be fitted while one of the bubble's three terms remains as an overconstraint. The rule pins κ to 1 or 1.4; choosing κ by hand would be [tuned], leaving only α as a continuous knob.")
emit("Blake requires p∞ < 0. Under the only two-power candidate α = −1, the tension term lands on the positive flux sign at R⁻³, not on a negative radion term. The negative curvature and attractive Casimir terms have the needed sign, but their powers do not complete the map; Casimir is the radion collapse side [computed; prediction].")
emit("Spec ambiguity resolved [post-hoc]: the files state the allowed map and grade but do not print a bubble potential convention or map orientation. This run uses the standard integrated Rayleigh–Plesset static potential above and allows α < 0 because monotone was not restricted to increasing; restricting α > 0 only makes the power mismatch stronger.")
emit("Overall Job N1 grade: FAIL — physical κ choices have no complete power-and-sign map under R = c r^α and a positive energy rescale [computed].")
emit("")
emit("## Read-only audit [computed]")
emit("")
assert sha(UNIFYING) == U_HASH and sha(STILL) == S_HASH
assert sha(RADION_RUN) == RR_HASH and sha(RADION_RESULTS) == RS_HASH
emit("UNIFYING_THREAD.md, STILL_TO_DO.md and Job 5b sources unchanged [computed].")
(HERE / "RESULTS.md").write_text("\n".join(OUT) + "\n", encoding="utf-8", newline="\n")
