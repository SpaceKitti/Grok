"""Tiny cmhd density smoke: uniform rho=1 is a continuity no-op.

Does not retune MHD. mode="mhd" is the old incompressible toy.
"""
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
    return np.asarray(x)


def main():
    out = run_framework(
        N=16, dim=2, steps=8, dt=5e-4, diag_every=8, scheme="rk2",
        mode="cmhd", force_on=False, viscoelastic=False,
        mhd_params=dict(eta_hyper=0.0, glm_ch=0.0),
    )
    rho = np.fft.ifftn(_arr(out["rho_hat"])).real
    max_rho_m1 = float(np.max(np.abs(rho - 1.0)))
    hist_m1 = float(np.max(np.abs(_arr(out["max_abs_rho_m1"]))))
    max_drho = float(np.max(np.abs(_arr(out["max_drho_dt"]))))
    mean_rho = float(_arr(out["mean_rho"])[-1])
    print(
        f"cmhd uniform rho: max|rho-1|={max_rho_m1:.6e} "
        f"hist max|rho-1|={hist_m1:.6e} max|d_t rho|={max_drho:.6e} "
        f"mean_rho={mean_rho:.12f}",
        flush=True,
    )
    # Incompressible MHD path must still be the default for mode="mhd"
    # (this file only checks the new tree). Leftover must stay tiny.
    ok = (
        out.get("rho_hat") is not None
        and np.isfinite(max_rho_m1)
        and max_rho_m1 < 1e-12
        and hist_m1 < 1e-12
        and max_drho < 1e-12
    )
    if not ok:
        print(
            f"FAIL cmhd uniform rho leftover too large: "
            f"max|rho-1|={max_rho_m1:.3e} max|d_t rho|={max_drho:.3e}",
            flush=True,
        )
        sys.exit(1)
    print("SMOKE CMHD rho OK", flush=True)


if __name__ == "__main__":
    main()
