"""
F3 — Holographic defect. Own letter. Tiny discrete bulk, 3 layers.

  Bulk sites: r = 0,1,2 (IR → boundary), x-grid on [-2,2]
  Metric (named, not Damour/KSS):  ds² = dr² + (1+r)² dx²
  Spin connection of that warped product (Levi-Civita, no δ_Γ):
      ω_x^{r x} = ∂_r log(1+r) = 1/(1+r)
  Letter: holonomy of ω along a boundary loop, using the BOUNDARY layer
  value ω = 1/(1+2) dx   —  ∮ ω = 0 because d(x) around a closed curve
  in the (x,y) embedding has ∮ dx = 0 if we only take the x-component.

  Geodesic defect: each boundary point is joined to a single IR point (r=0
  identified). Parallel transport to the IR along radial links (A_r = 0)
  and back. Relative phase at the IR:
      χ(x) = β * x     with β = 1/3  (warp at r=2, not fitted to −1)
      U_3(θ) = exp(i [χ(x(θ)) − χ(x(0))])
  At θ=2π, x returns ⇒ U_3(2π) = 1.

No 4d black-hole theorem. No MHD jump in the definition.
"""

from __future__ import annotations

import numpy as np

from protocol import CENTER_OFF, CENTER_ON, GAMMA, N_THETA, loop_points, score_S

N_LAYER = 3
BETA = 1.0 / 3.0  # 1/(1+r_bdy), not fitted
FAMILY = "F3 holo"
INSERTED = False


def operator_block() -> str:
    return (
        "F3  3-layer discrete bulk\n"
        "    ds² = dr² + (1+r)² dx²    r=0,1,2\n"
        "    ω_x^{rx} = 1/(1+r)         (Levi-Civita of the warp)\n"
        "    radial links A_r = 0\n"
        "    IR identification at r=0; χ(x) = β x,  β=1/3\n"
        "    U_3[γ] = exp(i[χ(x_γ)−χ(x_0)])   geodesic monodromy through IR"
    )


def holonomy(center: complex) -> np.ndarray:
    theta, z = loop_points(center, N_THETA)
    x = z.real
    chi = BETA * x
    U = np.exp(1j * (chi - chi[0]))
    return U


def spatial_means() -> tuple[float, float]:
    """
    Tiny-loop |U-1| on a boundary scan. χ=βx ⇒ small plaquette holonomy
    is 0 (gradient, F=0). Signal is identically 0 on and off Γ.
    """
    return 0.0, 0.0


def run(mhd: dict) -> dict:
    U_on = holonomy(CENTER_ON)
    U_off = holonomy(CENTER_OFF)
    son, soff = spatial_means()
    sc = score_S(U_on, U_off, son, soff, mhd["n_sheet"], mhd["i2"], mhd["i4"], True, INSERTED)
    return {
        "family": FAMILY,
        "operator": operator_block(),
        "inserted": INSERTED,
        "defined_without_mhd": True,
        "U_on": U_on,
        "U_off": U_off,
        "score": sc,
    }
