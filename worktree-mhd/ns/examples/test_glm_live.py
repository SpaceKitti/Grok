"""F3 live-psi: glm_ch=0 vs glm_ch>0 with a div-B kick. mode=mhd. Textbook OT seed unchanged."""
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


def _run(glm_ch):
    return run_framework(
        N=32, dim=2, steps=100, dt=0.002, diag_every=20, scheme="rk2",
        mode="mhd", ic="ot", force_on=False, viscoelastic=False, nu=1e-3,
        mhd_params=dict(
            B0=1.0, ot_u0=1.0, eta_mag=1e-3, eta_hyper=0.0, hyper_kcut=0.0,
            glm_ch=glm_ch, glm_cr=0.18, freeze_ext=0.0, divb_kick=0.05,
        ),
    )


def main():
    print("F3 live-psi  mode=mhd ic=ot + divb_kick=0.05  N=32  (OT By=sin 2x untouched)")
    outs = {}
    for ch in (0.0, 0.5):
        out = _run(ch)
        outs[ch] = out
        t = _arr(out["time"])
        divb = _arr(out["max_div_b"])
        eglm = _arr(out["e_glm"])
        etot = _arr(out["e_tot"])
        econs = etot + eglm
        e0 = float(econs[0])
        ileak = _arr(out["I_leak"])
        print(f"\nglm_ch={ch:g}  glm_cr=0.18")
        print(f"{'t':>8} {'max|div B|':>14} {'e_glm':>14} {'I_leak/E0':>14}")
        for i in range(t.size):
            print(f"{t[i]:8.4f} {divb[i]:14.6e} {eglm[i]:14.6e} "
                  f"{abs(ileak[i]) / (abs(e0) + 1e-30):14.6e}")
        print(f"  t0 max|div B|={divb[0]:.6e}  tend={divb[-1]:.6e}  "
              f"e_glm tend={eglm[-1]:.6e}  I_leak/E0 tend="
              f"{abs(ileak[-1]) / (abs(e0) + 1e-30):.6e}")


if __name__ == "__main__":
    main()
