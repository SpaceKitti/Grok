"""Tiny twofluid smoke: Te=0 vs hall, Te>0 positivity. Stage 2 only."""
import os
import sys
from pathlib import Path

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import jax
jax.config.update("jax_enable_x64", True)

import numpy as np
from chive_ns import run_framework, generate_u_alfven, make_grid, generate_b0
from chive_ns.compressible import uniform_rho_hat
from chive_ns.mhd import induction_rhs, twofluid_induction_rhs


def _arr(x):
    return np.asarray(x)


def _finite(out, keys):
    bad = []
    for k in keys:
        v = _arr(out[k])
        if not np.all(np.isfinite(v)):
            bad.append(k)
    return bad


def _min_n(out):
    ni = np.fft.ifftn(np.asarray(out["n_i_hat"])).real
    ne = np.fft.ifftn(np.asarray(out["n_e_hat"])).real
    return float(ni.min()), float(ne.min()), float(ni.mean()), float(ne.mean())


def _leak(out):
    e0 = float(_arr(out["e_tot"])[0])
    ileak = float(_arr(out["I_leak"])[-1])
    return abs(ileak) / (abs(e0) + 1e-30), ileak, e0


def _ohm_close(grid, d_i, T_e=0.0):
    """T_e=0 twofluid Faraday must be the Hall Ohm (same d_i, n=1)."""
    B = generate_b0(grid, B0=1.0, kind="alfven", amp=0.05)
    if d_i != 0.0 and B.shape[0] == 2:
        z = np.zeros_like(np.asarray(B[0]))
        B = np.concatenate([np.asarray(B), z[None]], axis=0)
    B_hat = np.asarray(B)
    u = generate_u_alfven(grid, amp=0.05)
    u_hat = np.fft.fftn(np.asarray(u), axes=(1, 2))
    n_hat = np.asarray(uniform_rho_hat(grid, rho0=1.0))
    eta = 1e-4
    dB_h = np.asarray(induction_rhs(
        B_hat, u_hat, grid, eta, B_hat, 0.0, 0.0, None, 0.0, d_i, 1.0))
    dB_t = np.asarray(twofluid_induction_rhs(
        B_hat, u_hat, n_hat, grid, eta, B_hat, 0.0, 0.0, None, 0.0, d_i, T_e))
    rel = np.max(np.abs(dB_h - dB_t)) / (np.max(np.abs(dB_h)) + 1e-30)
    return float(rel), float(np.max(np.abs(dB_h))), float(np.max(np.abs(dB_t)))


def main():
    failed = []

    def check(name, ok, detail):
        tag = "PASS" if ok else "FAIL"
        print(f"{tag} {name}: {detail}", flush=True)
        if not ok:
            failed.append(name)

    B0 = 1.0
    amp = 0.05
    N = 16
    dt = 0.01
    steps = 20
    keys = ("energy", "e_tot", "I_leak", "max_div_b", "e_mag_tot",
            "min_n_i", "min_n_e")
    common = dict(
        N=N, dim=2, steps=steps, dt=dt, diag_every=steps, scheme="rk2",
        ic="alfven", force_on=False, viscoelastic=False, nu=1e-4,
    )
    mp0 = dict(B0=B0, alfven_amp=amp, eta_mag=1e-4, glm_ch=0.0, eta_hyper=0.0,
               d_i=0.0, T_e=0.0)

    grid0 = make_grid(N, L=1.0, dim=2)
    rel0, ah0, at0 = _ohm_close(grid0, d_i=0.0, T_e=0.0)
    print(f"Ohm Te=0 di=0  rel={rel0:.3e} |dB|_hall={ah0:.3e} |dB|_tf={at0:.3e}",
          flush=True)
    check("Ohm Te=0 di=0 matches hall", rel0 < 1e-12, f"rel={rel0:.3e}")
    relh, ahh, ath = _ohm_close(grid0, d_i=0.05, T_e=0.0)
    print(f"Ohm Te=0 di=0.05 rel={relh:.3e} |dB|_hall={ahh:.3e} |dB|_tf={ath:.3e}",
          flush=True)
    check("Ohm Te=0 di=0.05 matches hall", relh < 1e-10, f"rel={relh:.3e}")

    crash = {}
    out = {}
    try:
        out["mhd"] = run_framework(mode="mhd", mhd_params=dict(mp0), **common)
        crash["mhd"] = 0
    except Exception as exc:
        crash["mhd"] = 1
        print(f"CRASH mhd: {exc}", flush=True)
        out["mhd"] = None
    try:
        out["hall"] = run_framework(mode="hall", mhd_params=dict(mp0), **common)
        crash["hall"] = 0
    except Exception as exc:
        crash["hall"] = 1
        print(f"CRASH hall: {exc}", flush=True)
        out["hall"] = None
    try:
        out["tf00"] = run_framework(mode="twofluid", mhd_params=dict(mp0), **common)
        crash["tf00"] = 0
    except Exception as exc:
        crash["tf00"] = 1
        print(f"CRASH twofluid Te=0 di=0: {exc}", flush=True)
        out["tf00"] = None

    bad_m = _finite(out["mhd"], ("energy", "e_tot", "I_leak")) if out["mhd"] else ["crash"]
    bad_h = _finite(out["hall"], ("energy", "e_tot", "I_leak")) if out["hall"] else ["crash"]
    bad_00 = _finite(out["tf00"], keys) if out["tf00"] else ["crash"]
    check("mhd no crash", crash["mhd"] == 0 and not bad_m, f"crash={crash['mhd']} bad={bad_m}")
    check("hall Te=0 di=0 no crash", crash["hall"] == 0 and not bad_h,
          f"crash={crash['hall']} bad={bad_h}")
    check("twofluid Te=0 di=0 no crash", crash["tf00"] == 0 and not bad_00,
          f"crash={crash['tf00']} bad={bad_00}")

    min_ni_00 = min_ne_00 = float("nan")
    ileak_00 = div_00 = float("nan")
    if out["tf00"] is not None:
        min_ni_00, min_ne_00, mean_ni_00, mean_ne_00 = _min_n(out["tf00"])
        r00, ileak_00, e0_00 = _leak(out["tf00"])
        div_00 = float(_arr(out["tf00"]["max_div_b"])[-1])
        print(
            f"Te=0 di=0 twofluid: min n_i={min_ni_00:.6e} min n_e={min_ne_00:.6e} "
            f"mean n_i={mean_ni_00:.6e} I_leak={ileak_00:.6e} max|divB|={div_00:.6e}",
            flush=True,
        )
        check("twofluid Te=0 di=0 min n_i>0", min_ni_00 > 0.0, f"min n_i={min_ni_00:.3e}")
        check("twofluid Te=0 di=0 min n_e>0", min_ne_00 > 0.0, f"min n_e={min_ne_00:.3e}")
        if out["hall"] is not None:
            eh = float(_arr(out["hall"]["e_tot"])[-1])
            et = float(_arr(out["tf00"]["e_tot"])[-1])
            rel_e = abs(et - eh) / (abs(eh) + 1e-30)
            print(f"Te=0 di=0 e_tot hall={eh:.6e} twofluid={et:.6e} rel={rel_e:.3e}",
                  flush=True)
            check("Te=0 di=0 twofluid close to hall e_tot", rel_e < 1e-8, f"rel={rel_e:.3e}")

    dt_h = 5e-4
    steps_h = 40
    common_h = dict(common, steps=steps_h, dt=dt_h, diag_every=steps_h)
    try:
        out["tf05"] = run_framework(
            mode="twofluid",
            mhd_params=dict(mp0, d_i=0.05, T_e=0.0),
            **common_h,
        )
        crash["tf05"] = 0
    except Exception as exc:
        crash["tf05"] = 1
        print(f"CRASH twofluid Te=0 di=0.05: {exc}", flush=True)
        out["tf05"] = None
    try:
        out["hall05"] = run_framework(
            mode="hall",
            mhd_params=dict(mp0, d_i=0.05),
            **common_h,
        )
        crash["hall05"] = 0
    except Exception as exc:
        crash["hall05"] = 1
        print(f"CRASH hall di=0.05: {exc}", flush=True)
        out["hall05"] = None

    bad_05 = _finite(out["tf05"], keys) if out["tf05"] else ["crash"]
    check("twofluid Te=0 di=0.05 no crash", crash["tf05"] == 0 and not bad_05,
          f"crash={crash['tf05']} bad={bad_05}")
    min_ni_05 = min_ne_05 = float("nan")
    ileak_05 = div_05 = float("nan")
    if out["tf05"] is not None:
        min_ni_05, min_ne_05, mean_ni_05, mean_ne_05 = _min_n(out["tf05"])
        r05, ileak_05, e0_05 = _leak(out["tf05"])
        div_05 = float(_arr(out["tf05"]["max_div_b"])[-1])
        print(
            f"Te=0 di=0.05 twofluid: min n_i={min_ni_05:.6e} min n_e={min_ne_05:.6e} "
            f"I_leak={ileak_05:.6e} I_leak/E0={r05:.6e} max|divB|={div_05:.6e}",
            flush=True,
        )
        check("twofluid Te=0 di=0.05 min n_i>0", min_ni_05 > 0.0, f"min n_i={min_ni_05:.3e}")
        check("twofluid Te=0 di=0.05 min n_e>0", min_ne_05 > 0.0, f"min n_e={min_ne_05:.3e}")
        check("twofluid Te=0 di=0.05 I_leak finite", np.isfinite(ileak_05),
              f"I_leak={ileak_05:.3e}")
        if out["hall05"] is not None:
            eh = float(_arr(out["hall05"]["e_tot"])[-1])
            et = float(_arr(out["tf05"]["e_tot"])[-1])
            rel_e = abs(et - eh) / (abs(eh) + 1e-30)
            print(f"Te=0 di=0.05 e_tot hall={eh:.6e} twofluid={et:.6e} rel={rel_e:.3e}",
                  flush=True)
            check("Te=0 di=0.05 twofluid close to hall e_tot", rel_e < 1e-4,
                  f"rel={rel_e:.3e}")

    try:
        out["tfT"] = run_framework(
            mode="twofluid",
            mhd_params=dict(mp0, d_i=0.0, T_e=0.01, n_eps=0.01),
            **common,
        )
        crash["tfT"] = 0
    except Exception as exc:
        crash["tfT"] = 1
        print(f"CRASH twofluid Te=0.01: {exc}", flush=True)
        out["tfT"] = None
    bad_T = _finite(out["tfT"], keys) if out["tfT"] else ["crash"]
    check("twofluid Te=0.01 no crash", crash["tfT"] == 0 and not bad_T,
          f"crash={crash['tfT']} bad={bad_T}")
    min_ni_T = min_ne_T = float("nan")
    ileak_T = div_T = float("nan")
    if out["tfT"] is not None:
        min_ni_T, min_ne_T, mean_ni_T, mean_ne_T = _min_n(out["tfT"])
        rT, ileak_T, e0_T = _leak(out["tfT"])
        div_T = float(_arr(out["tfT"]["max_div_b"])[-1])
        print(
            f"Te=0.01 di=0 twofluid: min n_i={min_ni_T:.6e} min n_e={min_ne_T:.6e} "
            f"mean n_i={mean_ni_T:.6e} I_leak={ileak_T:.6e} max|divB|={div_T:.6e}",
            flush=True,
        )
        check("twofluid Te=0.01 min n_i>0", min_ni_T > 0.0, f"min n_i={min_ni_T:.3e}")
        check("twofluid Te=0.01 min n_e>0", min_ne_T > 0.0, f"min n_e={min_ne_T:.3e}")
        check("twofluid Te=0.01 I_leak finite", np.isfinite(ileak_T),
              f"I_leak={ileak_T:.3e}")

    print(
        "HAVE twofluid | "
        f"Te=0 di=0 crash={crash.get('tf00', 1)} nan={int(bool(bad_00))} "
        f"min_n_i={min_ni_00:.6e} min_n_e={min_ne_00:.6e} T_e=0 d_i=0 mode=twofluid "
        f"I_leak={ileak_00:.3e} max|divB|={div_00:.3e} | "
        f"Te=0 di=0.05 crash={crash.get('tf05', 1)} nan={int(bool(bad_05))} "
        f"min_n_i={min_ni_05:.6e} min_n_e={min_ne_05:.6e} T_e=0 d_i=0.05 mode=twofluid "
        f"I_leak={ileak_05:.3e} max|divB|={div_05:.3e} | "
        f"Te=0.01 crash={crash.get('tfT', 1)} nan={int(bool(bad_T))} "
        f"min_n_i={min_ni_T:.6e} min_n_e={min_ne_T:.6e} T_e=0.01 d_i=0 mode=twofluid "
        f"I_leak={ileak_T:.3e} max|divB|={div_T:.3e}",
        flush=True,
    )

    if failed:
        print("FAILED: " + ", ".join(failed), flush=True)
        sys.exit(1)
    print("SMOKE TWOFLUID OK", flush=True)


if __name__ == "__main__":
    main()
