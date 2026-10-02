"""A2: decaying Orszag-Tang on mode=mhd only. ic=ot. No Crow, no cmhd."""
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


def _cumtrapz(y, t):
    y, t = _arr(y), _arr(t)
    if y.size < 2:
        return np.zeros_like(y)
    pieces = 0.5 * (y[1:] + y[:-1]) * (t[1:] - t[:-1])
    return np.concatenate([[0.0], np.cumsum(pieces)])


def main():
    out = run_framework(
        N=32, dim=2, steps=400, dt=0.002, diag_every=20, scheme="rk2",
        mode="mhd", ic="ot", force_on=False, viscoelastic=False, nu=1e-3,
        mhd_params=dict(
            B0=1.0, ot_u0=1.0, eta_mag=1e-3, eta_hyper=0.0, hyper_kcut=0.0,
            glm_ch=0.0, freeze_ext=0.0,
        ),
    )
    t = _arr(out["time"])
    w = _arr(out["max_vort"])
    j = _arr(out["max_j"])
    integ = _cumtrapz(w + j, t)
    print(f"A2 decaying OT  mode=mhd ic=ot  N=32 dim=2  t={t[-1]:.3f}  force_off")
    print(f"{'t':>8} {'max|ω|':>12} {'max|J|':>12} {'∫(ω+J)dt':>14} "
          f"{'log10|ω|':>10} {'log10|J|':>10}")
    for i in range(t.size):
        lw = np.log10(w[i] + 1e-30)
        lj = np.log10(j[i] + 1e-30)
        print(f"{t[i]:8.4f} {w[i]:12.6e} {j[i]:12.6e} {integ[i]:14.6e} "
              f"{lw:10.4f} {lj:10.4f}")
    print(f"end: max|ω|={w[-1]:.6e}  max|J|={j[-1]:.6e}  "
          f"∫(max|ω|+max|J|)dt={integ[-1]:.6e}")
    dw = w[-1] / (w[0] + 1e-30)
    dj = j[-1] / (j[0] + 1e-30)
    print(f"max|ω|(end)/start={dw:.4f}  max|J|(end)/start={dj:.4f}")
    if dj > 1.5 * max(dw, 1.0) and w[-1] <= 1.2 * np.max(w):
        ans = "|J| grows relative to |ω|; check whether |ω| is bounded while |J| runs."
    else:
        ans = "they climb/decay together (no |J| runaway at bounded |ω| on this window)."
    # Answer from the table, no slope fit.
    wpeak, jpeak = float(np.max(w)), float(np.max(j))
    tw, tj = float(t[int(np.argmax(w))]), float(t[int(np.argmax(j))])
    print(f"peak max|ω|={wpeak:.6e} at t={tw:.4f}; peak max|J|={jpeak:.6e} at t={tj:.4f}")
    print(ans)


if __name__ == "__main__":
    main()
