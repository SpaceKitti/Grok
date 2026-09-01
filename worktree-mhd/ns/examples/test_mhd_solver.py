"""Tiny MHD B-E smoke: energy identity, OT, GLM, Harris flux monitors."""
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


def _leak_ratio(out):
    e0 = float(_arr(out["e_tot"])[0])
    ileak = float(_arr(out["I_leak"])[-1])
    return abs(ileak) / (abs(e0) + 1e-30), ileak, e0


def main():
    failed = []

    def check(name, ok, detail):
        tag = "PASS" if ok else "FAIL"
        print(f"{tag} {name}: {detail}", flush=True)
        if not ok:
            failed.append(name)

    mp0 = dict(eta_hyper=0.0, glm_ch=0.0)
    common2 = dict(
        N=16, dim=2, steps=8, dt=5e-4, diag_every=8, scheme="rk2",
        mode="mhd", force_on=False, viscoelastic=False,
    )

    # B energy identity (hydro off, Qin projector)
    out_b2 = run_framework(mhd_params=dict(mp0), **common2)
    r2, ileak2, e02 = _leak_ratio(out_b2)
    print(f"B energy 2D: I_leak/E0={r2:.6e} I_leak={ileak2:.6e} E0={e02:.6e}", flush=True)
    check("B energy 2D", r2 < 1e-6, f"I_leak/E0={r2:.3e}")

    out_b3 = run_framework(
        N=8, dim=3, steps=4, dt=5e-4, diag_every=4, scheme="rk2",
        mode="mhd", force_on=False, viscoelastic=False,
        mhd_params=dict(mp0),
    )
    r3, ileak3, e03 = _leak_ratio(out_b3)
    print(f"B energy 3D: I_leak/E0={r3:.6e} I_leak={ileak3:.6e} E0={e03:.6e}", flush=True)
    check("B energy 3D", r3 < 1e-6, f"I_leak/E0={r3:.3e}")

    # C Orszag-Tang (ic=ot sets b_guide=ot)
    out_ot = run_framework(ic="ot", mhd_params=dict(mp0), **common2)
    rc, ileakc, e0c = _leak_ratio(out_ot)
    divc = float(_arr(out_ot["max_div_b"])[-1])
    print(f"C OT: I_leak/E0={rc:.6e} max_div_b[-1]={divc:.6e}", flush=True)
    check("C OT leak", rc < 1e-6, f"I_leak/E0={rc:.3e}")
    check("C OT finite", np.isfinite(divc), f"max_div_b={divc:.3e}")

    # D GLM: Qin projector vs Dedner psi
    out_glm = run_framework(
        ic="ot",
        mhd_params=dict(eta_hyper=0.0, glm_ch=0.5, glm_cr=0.18),
        **common2,
    )
    div0 = float(_arr(out_ot["max_div_b"])[-1])
    div1 = float(_arr(out_glm["max_div_b"])[-1])
    print(
        f"D GLM: max_div_b glm_ch=0 -> {div0:.6e}; "
        f"glm_ch=0.5 glm_cr=0.18 -> {div1:.6e}",
        flush=True,
    )
    check("D GLM finite", np.isfinite(div0) and np.isfinite(div1),
          f"div0={div0:.3e} div1={div1:.3e}")

    # E Harris sheet (default/smooth IC). Do not interpret smear vs ribbon.
    out_h = run_framework(
        mhd_params=dict(eta_hyper=0.0, glm_ch=0.0, harris=True),
        **common2,
    )
    fx = float(_arr(out_h["flux_x_half"])[-1])
    fy = float(_arr(out_h["flux_y_half"])[-1])
    rr = float(_arr(out_h["rec_rate_flux"])[-1])
    er = float(_arr(out_h["E_rec"])[-1])
    print(
        f"E Harris: flux_x_half={fx:.6e} flux_y_half={fy:.6e} "
        f"rec_rate_flux={rr:.6e} E_rec={er:.6e}",
        flush=True,
    )
    ok_h = all(np.isfinite(v) for v in (fx, fy, rr, er))
    check("E Harris finite", ok_h,
          f"flux_x={fx:.4e} flux_y={fy:.4e} rec_rate={rr:.4e} E_rec={er:.4e}")

    if failed:
        print("FAILED: " + ", ".join(failed), flush=True)
        sys.exit(1)
    print("SMOKE MHD B-E OK", flush=True)


if __name__ == "__main__":
    main()
