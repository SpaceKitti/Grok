"""A2 thinning: decaying OT, mode=mhd ic=ot. Run until max|J| peaks or t=3."""
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
    N = 64
    dt = 0.002
    t_max = 3.0
    steps = int(round(t_max / dt))
    diag_every = 50
    print(f"A2 thinning  mode=mhd ic=ot  N={N} dim=2  t_max={t_max}  "
          f"dt={dt} steps={steps} force_off", flush=True)
    out = run_framework(
        N=N, dim=2, steps=steps, dt=dt, diag_every=diag_every, scheme="rk2",
        mode="mhd", ic="ot", force_on=False, viscoelastic=False, nu=1e-3,
        mhd_params=dict(
            B0=1.0, ot_u0=1.0, eta_mag=1e-3, eta_hyper=0.0, hyper_kcut=0.0,
            glm_ch=0.0, freeze_ext=0.0,
        ),
    )
    t = _arr(out["time"])
    w = _arr(out["max_vort"])
    j = _arr(out["max_j"])
    jpeak_i = int(np.argmax(j))
    wpeak_i = int(np.argmax(w))
    # Clear peak: interior max, then a drop of at least 2%.
    peaked = (0 < jpeak_i < j.size - 1) and (j[-1] < 0.98 * j[jpeak_i])
    print(f"{'t':>8} {'max|ω|':>12} {'max|J|':>12} {'log10|ω|':>10} {'log10|J|':>10}")
    for i in range(t.size):
        print(f"{t[i]:8.4f} {w[i]:12.6e} {j[i]:12.6e} "
              f"{np.log10(w[i]+1e-30):10.4f} {np.log10(j[i]+1e-30):10.4f}")
    print(f"t_end={t[-1]:.4f}  max|J| peak at t={t[jpeak_i]:.4f} "
          f"(J={j[jpeak_i]:.6e})  max|ω| peak at t={t[wpeak_i]:.4f} "
          f"(ω={w[wpeak_i]:.6e})  peaked={peaked}")
    rel = np.max(np.abs(j - w) / (w + 1e-30))
    if rel < 0.02:
        print("|J| and |ω| still decay together (no peel / no sheet on this window).")
    else:
        print("|J| peels off |ω| (current sheet).")


if __name__ == "__main__":
    main()
