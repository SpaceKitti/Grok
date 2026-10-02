#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Job A1: test whether an S2 axion can see the integer n."""
from __future__ import annotations

import datetime as dt
import hashlib
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
UNIFYING = Path(r"C:\Users\Akitt\open-problems\UNIFYING_THREAD.md")
STILL = Path(r"C:\Users\Akitt\open-problems\STILL_TO_DO.md")
RADION = Path(r"C:\Users\Akitt\radion-5b-tension-casimir")
RADION_RUN = RADION / "run.py"
RADION_RESULTS = RADION / "RESULTS.md"
EXPECTED_U = "CDE3C256"
EXPECTED_S = "1AEC133B"
# Job 5b units and C=-3 window endpoints, read from its generated report.
A = 4.0 * sp.pi
B = 4.0 * sp.pi
D = sp.pi / 2.0
N_BASE = 3
C_RADION = -3.0
BASE_LAMBDAS = (0.259397739, 0.271377217, 0.283356695)
K_VALUES = (1, 2, 3, 4, 5, 6)
# Fixed before the first run.
ETA = 1.0                         # dimensionless monodromy coefficient
MONODROMY_STEP = -1               # integer branch step/sign
THETA = sp.pi                     # half-period vacuum, not the axion minimum
Q_HALF = float(THETA / (2 * sp.pi))
AXION_COEFF = ETA * MONODROMY_STEP * Q_HALF  # coefficient of n/R^3
NATURAL_RANGE = (0.1, 10.0)
BREAK_TOL = 1e-10
OUT: list[str] = []


def emit(line=""):
    print(line, flush=True)
    OUT.append(line)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def v_base(lam, n, x):
    return float(A) * lam / x - float(B) / x**2 + float(D) * n**2 / x**3 + C_RADION / x**4


def v_axion(lam, n, x, q=Q_HALF):
    # Simplest non-minimum monodromy cross-term: eta*m*q*n/R^3.
    return float(ETA * MONODROMY_STEP * q) * n / x**3


def minimum_x(lam, n, q=Q_HALF):
    coeff = float(D) * n**2 + float(ETA * MONODROMY_STEP * q) * n
    disc = float(B)**2 - 3.0 * float(A) * lam * coeff
    if disc <= 0.0:
        return None
    return (float(B) - disc**0.5) / (float(A) * lam)


def p_flux(lam, n, q=Q_HALF):
    """Job 5b p_flux share, which is invariant under the base k-family rescaling."""
    x = minimum_x(lam, n, q)
    if x is None:
        return None
    flux_energy = n**2 / (8.0 * x**2)
    return flux_energy / (flux_energy + lam)


# Read-only source audit.
U_HASH = sha(UNIFYING)
S_HASH = sha(STILL)
RR_HASH = sha(RADION_RUN)
RS_HASH = sha(RADION_RESULTS)

# Sympy scaling identities: base terms scale k^-4; linear axion term scales k^-5.
k_s, n_s, lam_s, x_s, eta_s, q_s, m_s = sp.symbols("k n Lambda x eta q m", positive=True)
V0 = A * lam_s / x_s - B / x_s**2 + D * n_s**2 / x_s**3
Vax = eta_s * m_s * q_s * n_s / x_s**3
BASE_IDENTITY = sp.simplify(V0.subs({n_s: k_s * n_s, lam_s: lam_s / k_s**2, x_s: k_s**2 * x_s}, simultaneous=True) - V0 / k_s**4) == 0
AXION_IDENTITY = sp.simplify(Vax.subs({n_s: k_s * n_s, x_s: k_s**2 * x_s}, simultaneous=True) - Vax / k_s**5) == 0

emit("# Job A1: does an S² axion see n?")
emit("")
emit("Generated: %s (BST/local time)" % dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"))
emit("Tags: [computed] [identity] [standard] [assumed] [tuned] [post-hoc] [hive-interpretation].")
emit("Inputs read-only: UNIFYING_THREAD sha256 %s (expected %s); STILL_TO_DO sha256 %s (used current hash, expected %s)." % (U_HASH[:8].upper(), EXPECTED_U, S_HASH[:8].upper(), EXPECTED_S))
emit("Job 5b source read-only: run.py sha256 %s; RESULTS.md sha256 %s." % (RR_HASH[:8].upper(), RS_HASH[:8].upper()))
emit("")
emit("## Setup [assumed]")
emit("")
emit("Base is Job 5b V(R) = 4πΛ₆/R − 4π/R² + (π/2)n²/R³ + C/R⁴, in its s = 1 units; C = %.1f is retained in the written base but set to zero for the isolated k-family attribution test [assumed]." % C_RADION)
emit("Test vacuum: θ = π, the half-period displaced axion vacuum, with monodromy branch step m = %d; q = θ/(2π) = %.1f. This is not the axion's own minimum θ = 0 [assumed input]." % (MONODROMY_STEP, Q_HALF))
emit("Candidate 2-form/flux cross-term: V_ax = η m q n/R³, η = %.1f, effective coefficient ηmq = %.6f [assumed input]. Natural means %.1f–%.1f in Job 5b units [identity/rule]." % (ETA, AXION_COEFF, NATURAL_RANGE[0], NATURAL_RANGE[1]))
emit("At θ = 0, V_ax = 0 and the control is blind; that control is reported but is not the displaced-vacuum grade [identity].")
emit("")
emit("## Scaling test [computed]")
emit("")
emit("Under n → k n, Λ₆ → Λ₆/k², R → k²R: the Job 5b n²/R³ term scales as k⁻⁴, while the linear axion term scales as k⁻⁵. A positive energy rescale cannot make both scalings equal [identity].")
emit("Symbolic base k-family identity: %s [identity]." % BASE_IDENTITY)
emit("Symbolic linear-axion scaling identity: %s [identity]." % AXION_IDENTITY)
emit("| base Λ₆ | k | p control (θ=0) | p axion (θ=π) | axion Δp/p_control | V_ax scaling residual |")
emit("|---:|---:|---:|---:|---:|---:|")
max_dp = 0.0
max_residual = 0.0
for lam in BASE_LAMBDAS:
    for k in K_VALUES:
        n = N_BASE * k
        lam_k = lam / k**2
        p0 = p_flux(lam_k, n, q=0.0)
        pa = p_flux(lam_k, n, q=Q_HALF)
        dp = abs(pa / p0 - 1.0) if p0 is not None and pa is not None else float("nan")
        # V_ax(k n, k²R) / [k^-4 V_ax(n,R)] = k^-1.
        residual = abs(1.0 / k - 1.0)
        if k > 1:
            max_dp = max(max_dp, dp)
            max_residual = max(max_residual, residual)
        emit("| %.9f | %d | %.9f | %.9f | %+.6e | %.6e |" % (lam, k, p0, pa, dp, residual))
    emit("")

natural = NATURAL_RANGE[0] <= abs(AXION_COEFF) <= NATURAL_RANGE[1]
control_blind = BASE_IDENTITY and all(abs(p_flux(lam / k**2, N_BASE * k, 0.0) / p_flux(lam, N_BASE, 0.0) - 1.0) < BREAK_TOL for lam in BASE_LAMBDAS for k in K_VALUES)
axion_breaks = AXION_IDENTITY and max_residual > BREAK_TOL and max_dp > BREAK_TOL
emit("Control θ = 0: n²-only family remains blind: %s [computed]." % control_blind)
emit("Displaced θ = π: linear-n family breaks the rescaling: %s; max |Δp/p| = %.6e; max scaling residual = %.6e [computed]." % (axion_breaks, max_dp, max_residual))
emit("Naturalness check: |effective coefficient| = %.6f is within factor-10 range [%.1f, %.1f]: %s [computed]." % (abs(AXION_COEFF), NATURAL_RANGE[0], NATURAL_RANGE[1], natural))
if natural and axion_breaks:
    grade = "PASS"
elif axion_breaks:
    grade = "PARTIAL [tuned]"
else:
    grade = "FAIL"
emit("A1 grade: %s — the displaced half-period vacuum supplies a natural linear-in-n monodromy term; the own-minimum vacuum is blind [computed]." % grade)
emit("")
emit("Spec ambiguity resolved [post-hoc]: UNIFYING_THREAD says Aethon's 6D axion form is assumed input but does not print its coefficient or radial power. This cheap test uses the minimal linear monodromy cross-term η m q n/R³, the allowed n-sensitive mechanism; a derived 6D form could change the physics grade.")
emit("")
emit("## Read-only audit [computed]")
emit("")
assert sha(UNIFYING) == U_HASH and sha(STILL) == S_HASH
assert sha(RADION_RUN) == RR_HASH and sha(RADION_RESULTS) == RS_HASH
emit("UNIFYING_THREAD.md, STILL_TO_DO.md and Job 5b sources unchanged [computed].")
(HERE / "RESULTS.md").write_text("\n".join(OUT) + "\n", encoding="utf-8", newline="\n")
