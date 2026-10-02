"""E2 meter: forming Harris sheet (thick + edge seed), not Crow, not SP-thin."""
import os
import sys
from pathlib import Path

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import jax
jax.config.update("jax_enable_x64", True)

import numpy as np
from chive_ns import run_framework


def _arr(x):
    return np.asarray(x, dtype=float)


def main():
    # δ=0.20 >> δ_SP ~ L/sqrt(S)~0.03 at S~L v_A/η with v_A~1, η=1e-3.
    out = run_framework(
        N=32, dim=2, steps=300, dt=0.002, diag_every=30, scheme="rk2",
        mode="mhd", ic="smooth", force_on=False, viscoelastic=False, nu=1e-3,
        ic_params=dict(u_scale=0.0),
        mhd_params=dict(
            B0=1.0, b_guide="x", harris=True, harris_width=0.20,
            harris_edge=0.05, eta_mag=1e-3, eta_hyper=0.0, hyper_kcut=0.0,
            glm_ch=0.0, freeze_ext=0.0,
        ),
    )
    t = _arr(out["time"])
    phi = _arr(out["flux_x_half"])
    rr = _arr(out["rec_rate_flux"])
    j = _arr(out["max_j"])
    print("E2 Harris forming sheet  mode=mhd  N=32  δ=0.20 + edge seed  "
          f"force_off  t={t[-1]:.3f}")
    print(f"{'t':>8} {'Φ=flux_x_half':>16} {'rec_rate_flux':>16} {'max|J|':>14}")
    for i in range(t.size):
        print(f"{t[i]:8.4f} {phi[i]:16.6e} {rr[i]:16.6e} {j[i]:14.6e}")
    j0, jpeak = float(j[0]), float(np.max(j))
    print(f"max|J| start={j0:.6e} peak={jpeak:.6e}  "
          f"Φ start={phi[0]:.6e} end={phi[-1]:.6e}")


if __name__ == "__main__":
    main()
