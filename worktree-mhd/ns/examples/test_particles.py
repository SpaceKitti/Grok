"""Tiny Stage 3 test-particle smoke. Boris tracers; no deposit/back-reaction."""
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
    failed = []

    def check(name, ok, detail):
        tag = "PASS" if ok else "FAIL"
        print(f"{tag} {name}: {detail}", flush=True)
        if not ok:
            failed.append(name)

    N = 16
    L = 1.0
    dt = 0.01
    steps = 8
    n_p = 8
    m_e = 1.0 / 25.0
    crash = 1
    nan = 1
    min_x = max_x = ke_i = ke_e = float("nan")
    out = None
    try:
        out = run_framework(
            mode="twofluid",
            N=N, dim=2, steps=steps, dt=dt, diag_every=steps, scheme="rk2",
            ic="alfven", force_on=False, viscoelastic=False, nu=1e-4,
            mhd_params=dict(
                B0=1.0, alfven_amp=0.05, eta_mag=1e-4, glm_ch=0.0,
                eta_hyper=0.0, d_i=0.0, T_e=0.0, particles=True,
                n_p=n_p, m_e=m_e,
            ),
        )
        crash = 0
    except Exception as exc:
        crash = 1
        print(f"CRASH test-particles: {exc}", flush=True)

    if out is not None:
        xi = _arr(out["x_i"])
        xe = _arr(out["x_e"])
        ke_i = float(_arr(out["KE_i"])[-1])
        ke_e = float(_arr(out["KE_e"])[-1])
        x_all = np.concatenate([xi[-1].ravel(), xe[-1].ravel()])
        min_x = float(np.min(x_all))
        max_x = float(np.max(x_all))
        bad = []
        for k in ("energy", "KE_i", "KE_e", "x_i", "x_e", "v_i", "v_e"):
            v = _arr(out[k])
            if not np.all(np.isfinite(v)):
                bad.append(k)
        nan = int(bool(bad))
        check("no crash", crash == 0, f"crash={crash}")
        check("no NaN", not bad, f"bad={bad}")
        on_torus = np.all(x_all >= 0.0) and np.all(x_all < L)
        check("x on torus [0,L)", on_torus, f"min_x={min_x:.6e} max_x={max_x:.6e}")
        check("KE_i finite", np.isfinite(ke_i), f"KE_i={ke_i:.6e}")
        check("KE_e finite", np.isfinite(ke_e), f"KE_e={ke_e:.6e}")
        check("N_p=8 per species", xi.shape[-2] == n_p and xe.shape[-2] == n_p,
              f"x_i={xi.shape} x_e={xe.shape}")
        check("m_e=1/25", abs(float(out.get("m_e", m_e)) - m_e) < 1e-15,
              f"m_e={out.get('m_e', m_e)}")

    print(
        "HAVE test-particles | "
        f"crash={crash} nan={nan} min_x={min_x:.6e} max_x={max_x:.6e} "
        f"KE_i={ke_i:.6e} KE_e={ke_e:.6e} N_p={n_p}+{n_p} m_e={m_e:.6g} "
        "mode=twofluid no-deposit no-back-reaction",
        flush=True,
    )

    if failed:
        print("FAILED: " + ", ".join(failed), flush=True)
        sys.exit(1)
    print("SMOKE PARTICLES OK", flush=True)


if __name__ == "__main__":
    main()