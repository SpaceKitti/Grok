"""Tiny cmhd density-tracer smoke. Helmholtz-on; not acoustics.

N=16 2D, few steps, force_off. Uniform ρ=1 leftover should be roundoff.
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
    max_abs = float(np.max(np.abs(rho - 1.0)))
    min_rho = float(np.min(rho))
    mean_rho = float(np.mean(rho))
    print(f"cmhd uniform leftover: max|rho-1|={max_abs:.6e} min_rho={min_rho:.6e} mean_rho={mean_rho:.16f}",
          flush=True)
    hist_max = float(_arr(out["max_abs_rho_m1"])[-1])
    hist_min = float(_arr(out["min_rho"])[-1])
    hist_mean = float(_arr(out["mean_rho"])[-1])
    print(f"cmhd hist: max|rho-1|={hist_max:.6e} min_rho={hist_min:.6e} mean_rho={hist_mean:.16f}",
          flush=True)
    failed = []
    if not (min_rho > 0.0):
        failed.append(f"min_rho={min_rho}")
    if abs(mean_rho - 1.0) >= 1e-12:
        failed.append(f"mean_rho={mean_rho}")
    if max_abs >= 1e-12:
        failed.append(f"max|rho-1|={max_abs}")
    if out.get("ic") is None:
        pass
    if failed:
        print("FAILED: " + ", ".join(failed), flush=True)
        sys.exit(1)
    print("SMOKE CMHD OK", flush=True)


if __name__ == "__main__":
    main()
