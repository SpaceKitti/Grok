"""Loss term on R1: T1 Im V = eta_g * F_JT. Numbers hard-coded.
Source: pairA-qg-handoff / pairA-jt-4d values as given by Akitti (eps_EP, lambda_EP, v); F_JT from pairA-jt-4d."""
from __future__ import annotations

import numpy as np

EPS_EP = 0.51368066          # source: pairA-qg-handoff / pairA-jt-4d (Akitti)
LAM_EP = -0.308425j          # source: pairA-qg-handoff (Akitti)
V = -0.360253                # source: pairA-qg-handoff (Akitti)
GAMMA = (-EPS_EP, EPS_EP)    # the cut Gamma
T_CHOICE = "T1: Im V = eta_g * F_JT (T2 = eta_g (eps^2/eps_EP^2 - 1) is T1 with eta_g -> eta_g/eps_EP^2: rescaling only; T3 not used)"

I2 = np.eye(2, dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
PLACEMENTS = {"P0 scalar (M = 1)": I2, "P1 sigma_z (M = sigma_z)": SZ}


def F_JT(eps):
    return np.asarray(eps) ** 2 - EPS_EP ** 2


def loss(eps, eta, M):
    """i * eta * F_JT(eps) * M  (vanishes at +-eps_EP)."""
    return 1j * eta * complex(F_JT(eps)) * M
