"""STAGE 5 3D blowup-watch: tiny MHD run, record max|ω|(t) and max|J|(t).

Watch only. No Clay-proof. No singularity claim. Do not interpret smear vs sheet.
Finite meters and a short table; HAVE + file. Driver already stores max_vort / max_j.
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
    return np.asarray(x, dtype=float)


def main():
    # Tiny N=8 first. dim=3 Orszag-Tang (weak uz/Bz). Force off. Few steps.
    N = 8
    dim = 3
    ic = "ot"
    steps = 8
    dt = 5e-4
    diag_every = 2
    out = run_framework(
        N=N, dim=dim, steps=steps, dt=dt, diag_every=diag_every, scheme="rk2",
        mode="mhd", ic=ic, force_on=False, viscoelastic=False, nu=1e-3,
        mhd_params=dict(
            B0=1.0, ot_u0=1.0, eta_mag=1e-3, eta_hyper=0.0, glm_ch=0.0,
        ),
    )
    t = _arr(out["time"])
    w = _arr(out["max_vort"])
    j = _arr(out["max_j"])

    print(
        f"HAVE 5 blowup-watch  N={N} dim={dim} ic={ic} mode=mhd  "
        f"force_off  steps={steps} dt={dt}  watch only, no Clay-proof, "
        f"no singularity claim",
        flush=True,
    )
    print(f"{'t':>10} {'max|w|':>14} {'max|J|':>14}", flush=True)
    for i in range(t.size):
        print(f"{t[i]:10.6f} {w[i]:14.6e} {j[i]:14.6e}", flush=True)

    failed = []

    def check(name, ok, detail):
        tag = "PASS" if ok else "FAIL"
        print(f"{tag} {name}: {detail}", flush=True)
        if not ok:
            failed.append(name)

    check("no NaN max|w|", np.all(np.isfinite(w)), f"finite={np.all(np.isfinite(w))} n={w.size}")
    check("no NaN max|J|", np.all(np.isfinite(j)), f"finite={np.all(np.isfinite(j))} n={j.size}")
    check("max|w| finite", bool(np.all(np.isfinite(w))), f"max={float(np.max(np.abs(w))):.6e}")
    check("max|J| finite", bool(np.all(np.isfinite(j))), f"max={float(np.max(np.abs(j))):.6e}")
    # Meters should be nonzero on 3D OT; N=8 is coarse but OT has current at t=0.
    check("max|w| nonzero", bool(np.max(np.abs(w)) > 0.0), f"max|w|={float(np.max(np.abs(w))):.6e}")
    check("max|J| nonzero", bool(np.max(np.abs(j)) > 0.0), f"max|J|={float(np.max(np.abs(j))):.6e}")
    check("table rows", 4 <= t.size <= 9, f"n_samples={t.size}")

    if failed:
        print("FAILED: " + ", ".join(failed), flush=True)
        sys.exit(1)
    print("SMOKE BLOWUP-WATCH OK  (watch only; no Clay-proof; no singularity claim)", flush=True)


if __name__ == "__main__":
    main()
