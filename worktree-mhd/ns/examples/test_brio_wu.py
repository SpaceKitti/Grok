"""Tiny Brio-Wu smoke: cmhd 1D MHD Riemann. Spectral ringing expected.

No WENO/TVD/limiter. mode=mhd / Alfven untouched.
"""
import os
import sys
from pathlib import Path

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import jax
jax.config.update("jax_enable_x64", True)

import numpy as np
from chive_ns import run_framework, GAMMA_DEFAULT


def _arr(x):
    return np.asarray(x)


def main():
    N, dt, steps = 64, 0.001, 16
    T = steps * dt
    gamma = float(GAMMA_DEFAULT)
    out = run_framework(
        N=N, dim=2, steps=steps, dt=dt, diag_every=steps, scheme="rk2",
        mode="cmhd", ic="brio_wu", force_on=False, viscoelastic=False, nu=0.001,
        mhd_params=dict(
            eta_mag=1.0e-3, eta_hyper=0.0, glm_ch=0.0,
            gamma=gamma, B0=0.75,
        ),
    )
    rho = np.fft.ifftn(_arr(out["rho_hat"])).real
    p = np.fft.ifftn(_arr(out["p_hat"])).real
    B = np.fft.ifftn(_arr(out["B_hat"]), axes=(1, 2)).real
    rho_x = np.mean(rho, axis=1)
    p_x = np.mean(p, axis=1)
    Bx_x = np.mean(B[0], axis=1)
    min_rho, max_rho = float(np.min(rho)), float(np.max(rho))
    min_p, max_p = float(np.min(p)), float(np.max(p))
    min_Bx, max_Bx = float(np.min(B[0])), float(np.max(B[0]))
    samples = [0, N // 8, N // 4, N // 2, 3 * N // 4]
    print(
        f"cmhd brio_wu: N={N} t={T:.4f} dt={dt} ic={out.get('ic')} "
        f"min/max rho={min_rho:.6e}/{max_rho:.6e} "
        f"min/max p={min_p:.6e}/{max_p:.6e} "
        f"min/max Bx={min_Bx:.6e}/{max_Bx:.6e}",
        flush=True,
    )
    for i in samples:
        print(
            f"  sample x={i / N:.4f} rho={rho_x[i]:.6e} "
            f"p={p_x[i]:.6e} Bx={Bx_x[i]:.6e}",
            flush=True,
        )
    d = np.diff(rho_x)
    flips = int(np.sum((d[1:] * d[:-1]) < 0))
    overshoot = (max_rho > 1.0 + 1e-3) or (min_rho < 0.125 - 1e-3)
    ringing = bool(overshoot or flips >= 4)
    print(
        f"  ringing={ringing} overshoot={overshoot} deriv_sign_flips={flips}",
        flush=True,
    )
    failed = []
    if out.get("ic") != "brio_wu":
        failed.append(f"ic={out.get('ic')}")
    if not all(np.isfinite(v) for v in (min_rho, max_rho, min_p, max_p, min_Bx)):
        failed.append("nonfinite rho/p/Bx")
    if not ringing:
        failed.append("ringing not visible (do not smooth it away)")
    if failed:
        print("FAIL cmhd brio_wu: " + ", ".join(failed), flush=True)
        return False
    print("SMOKE CMHD Brio-Wu OK (spectral ringing present)", flush=True)
    return True


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
