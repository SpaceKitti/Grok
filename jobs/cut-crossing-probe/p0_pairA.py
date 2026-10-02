"""
P0 — pair A labels. Principal branch of the 2×2 discriminant.
Must pass or the probe is broken.

  disc(ε) = (ε v)^2 − ((b−a)/2)^2 = v^2 (ε^2 − ε_EP^2)
  letter(ε) = sqrt_principal(disc(ε))
  J = |letter(x+iδ) − letter(x−iδ)|   # jump across the real axis
  n = floor(Arg(letter)/π)

Not continued through the cut: the wall is the jump of the principal sheet.
"""

from __future__ import annotations

import numpy as np

from protocol import (
    A_DAMP,
    B_DAMP,
    DELTA,
    EPS_EP,
    V,
    X_OFF,
    X_ON,
    ratio,
    verdict,
    z_after,
    z_before,
)


def disc(eps: complex) -> complex:
    return (eps * V) ** 2 - ((B_DAMP - A_DAMP) / 2.0) ** 2


def letter(eps: complex) -> complex:
    return np.sqrt(disc(eps) + 0j)


def n_sheet(eps: complex) -> int:
    """Sheet label: ±1 on the cut faces (Im-dominant sqrt), 0 off the cut."""
    w = letter(eps)
    if abs(w.imag) < 0.5 * abs(w.real) + 1e-15:
        return 0
    return 1 if w.imag > 0 else -1


def J(x: float) -> float:
    return float(abs(letter(z_before(x)) - letter(z_after(x))))


def operator_block() -> str:
    return (
        "P0  pair A principal sqrt\n"
        "    disc(ε)=(ε v)^2−((b−a)/2)^2\n"
        "    letter=√disc  (principal branch)\n"
        f"    γ_cross: {X_ON:+.2f}±i{DELTA},  γ_miss: {X_OFF:+.2f}±i{DELTA}"
    )


def run() -> dict:
    j_on = J(X_ON)
    j_off = J(X_OFF)
    r = ratio(j_on, j_off)
    n_on = (n_sheet(z_before(X_ON)), n_sheet(z_after(X_ON)))
    n_off = (n_sheet(z_before(X_OFF)), n_sheet(z_after(X_OFF)))
    dn_on = abs(n_on[0] - n_on[1])
    dn_off = abs(n_off[0] - n_off[1])
    passed = bool(r >= 3.0 and dn_on >= 1 and dn_off == 0)
    return {
        "family": "P0 pair A labels",
        "operator": operator_block(),
        "J_on": j_on,
        "J_off": j_off,
        "ratio": r,
        "n_on": n_on,
        "n_off": n_off,
        "passed": passed,
        "verdict": "sees the wall" if passed else "probe-broken",
        "defined_without_mhd": False,  # this IS the MHD letter
        "inserted": False,
    }
