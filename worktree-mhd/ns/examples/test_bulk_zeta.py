"""Tiny Stage 4 bulk-viscosity smoke on cmhd only. Default off. Hive gamma 5/3."""
import os
import sys
from pathlib import Path

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import jax
jax.config.update("jax_enable_x64", True)

import numpy as np
from chive_ns import run_framework, GAMMA_DEFAULT, max_abs_div_u


def _arr(x):
    return np.asarray(x)


def _finite(out, keys):
    bad = []
    for k in keys:
        if k not in out:
            bad.append("missing:" + k)
            continue
        v = _arr(out[k])
        if not np.all(np.isfinite(v)):
            bad.append(k)
    return bad


def _ileak_ratio(out):
    e_kin = _arr(out["e_kin"])
    e_int = _arr(out["e_int"])
    e_mag = _arr(out["e_mag_tot"])
    e_glm = _arr(out["e_glm"])
    e_cons = e_kin + e_int + e_mag + e_glm
    ileak = _arr(out["I_leak"])
    E0 = float(e_cons[0])
    ratio = abs(float(ileak[-1])) / (abs(E0) + 1e-30)
    return ratio, float(ileak[-1]), E0, ileak


def main():
    failed = []

    def check(name, ok, detail):
        tag = "PASS" if ok else "FAIL"
        print(f"{tag} {name}: {detail}", flush=True)
        if not ok:
            failed.append(name)

    gamma = float(GAMMA_DEFAULT)
    check("hive GAMMA_DEFAULT=5/3", abs(gamma - 5.0 / 3.0) < 1e-15, f"gamma={gamma:.16f}")

    common = dict(
        N=16, dim=2, steps=16, dt=0.002, diag_every=1, scheme="rk2",
        mode="cmhd", ic="sound", force_on=False, viscoelastic=False, nu=0.001,
        ic_params=dict(sound_eps=1e-3, rho0=1.0),
    )
    mp_base = dict(
        B0=0.0, eta_mag=0.0, eta_hyper=0.0, glm_ch=0.0,
        gamma=gamma, p0=1.0,
    )
    keys = ("energy", "e_kin", "e_int", "I_leak", "mean_Q", "Q_bulk", "gamma")

    out_off = run_framework(mhd_params=dict(mp_base), **common)
    out_z0 = run_framework(mhd_params=dict(mp_base, zeta=0.0), **common)

    bad_off = _finite(out_off, keys)
    bad_z0 = _finite(out_z0, keys)
    r_off, leak_off, E0_off, ileak_off = _ileak_ratio(out_off)
    r_z0, leak_z0, E0_z0, ileak_z0 = _ileak_ratio(out_z0)
    leak_diff = float(np.max(np.abs(ileak_off - ileak_z0)))
    q_off = float(_arr(out_off["Q_bulk"])[-1])
    q_z0 = float(_arr(out_z0["Q_bulk"])[-1])
    g_off = float(_arr(out_off["gamma"])[-1])
    g_z0 = float(_arr(out_z0["gamma"])[-1])

    check("zeta omitted finite", not bad_off, f"bad={bad_off}")
    check("zeta=0 finite", not bad_z0, f"bad={bad_z0}")
    check(
        "zeta=0 leftover matches omitted control",
        leak_diff == 0.0 or leak_diff < 1e-16,
        f"max|I_leak_z0-I_leak_off|={leak_diff:.3e} "
        f"I_leak/E0_off={r_off:.6e} I_leak/E0_z0={r_z0:.6e} "
        f"I_leak_off={leak_off:.6e} I_leak_z0={leak_z0:.6e}",
    )
    check("zeta=0 Q_bulk ~ 0", abs(q_off) < 1e-30 and abs(q_z0) < 1e-30,
          f"Q_bulk_off={q_off:.6e} Q_bulk_z0={q_z0:.6e}")
    check("gamma hist 5/3 (off and z0)",
          abs(g_off - 5.0 / 3.0) < 1e-12 and abs(g_z0 - 5.0 / 3.0) < 1e-12,
          f"g_off={g_off:.16f} g_z0={g_z0:.16f}")

    crash = 1
    nan = 1
    q_on = float("nan")
    r_on = float("nan")
    leak_on = float("nan")
    max_div = float("nan")
    g_on = float("nan")
    out_on = None
    try:
        out_on = run_framework(
            mhd_params=dict(mp_base, zeta=1e-3), **common)
        crash = 0
    except Exception as exc:
        crash = 1
        print(f"CRASH zeta>0: {exc}", flush=True)

    if out_on is not None:
        bad_on = _finite(out_on, keys)
        nan = int(bool(bad_on))
        r_on, leak_on, E0_on, _ileak_on = _ileak_ratio(out_on)
        q_on = float(_arr(out_on["Q_bulk"])[-1])
        q_hist = _arr(out_on["Q_bulk"])
        q_max = float(np.max(q_hist))
        max_div = float(_arr(max_abs_div_u(out_on["u_hat"], out_on["grid"])))
        g_on = float(_arr(out_on["gamma"])[-1])
        check("zeta>0 no crash", crash == 0, f"crash={crash}")
        check("zeta>0 no NaN", not bad_on, f"bad={bad_on}")
        check("zeta>0 Q_bulk recorded", "Q_bulk" in out_on,
              f"keys_have_Q_bulk={('Q_bulk' in out_on)}")
        check("zeta>0 Q_bulk>0 (sound has div u)", q_max > 0.0,
              f"Q_bulk_last={q_on:.6e} Q_bulk_max={q_max:.6e} max|div u|={max_div:.6e}")
        check("zeta>0 gamma hist 5/3", abs(g_on - 5.0 / 3.0) < 1e-12,
              f"g_on={g_on:.16f}")
        check("zeta>0 still compressive", max_div > 1e-8,
              f"max|div u|={max_div:.6e}")
    else:
        check("zeta>0 no crash", False, "crash=1")

    print(
        "HAVE 4 bulk zeta | "
        f"gamma={gamma:.12f} "
        f"I_leak/E0_off={r_off:.6e} I_leak/E0_z0={r_z0:.6e} "
        f"leak_diff={leak_diff:.3e} "
        f"Q_bulk_off={q_off:.6e} Q_bulk_z0={q_z0:.6e} "
        f"zeta_on crash={crash} nan={nan} Q_bulk={q_on:.6e} "
        f"I_leak/E0_on={r_on:.6e} max_div={max_div:.6e} "
        "mode=cmhd default off hive-gamma-5/3",
        flush=True,
    )

    if failed:
        print("FAILED: " + ", ".join(failed), flush=True)
        sys.exit(1)
    print("SMOKE BULK ZETA OK", flush=True)


if __name__ == "__main__":
    main()
