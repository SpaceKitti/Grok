"""Tiny MHD B-E smoke: energy identity, OT, GLM, Harris flux monitors."""
import os
import sys
from pathlib import Path

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import jax
jax.config.update("jax_enable_x64", True)

import numpy as np
from chive_ns import run_framework, generate_u_alfven, make_grid


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

    rg, ileakg, e0g = _leak_ratio(out_glm)
    print(f"D GLM leak: I_leak/E0={rg:.6e} I_leak={ileakg:.6e} E0={e0g:.6e}", flush=True)
    check("D GLM leak", rg < 1e-6, f"I_leak/E0={rg:.3e}")

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

    # F Alfven: small transverse wiggle on the incompressible toy, Qin (glm_ch=0).
    B0 = 1.0
    amp = 0.05
    L = 1.0
    N = 16
    dt = 0.01
    steps = 20
    out_a = run_framework(
        N=N, dim=2, steps=steps, dt=dt, diag_every=steps, scheme="rk2",
        mode="mhd", ic="alfven", force_on=False, viscoelastic=False, nu=1e-4,
        mhd_params=dict(
            B0=B0, alfven_amp=amp, eta_mag=1e-4, glm_ch=0.0, eta_hyper=0.0,
        ),
    )
    u = np.fft.ifftn(np.asarray(out_a["u_hat"]), axes=(1, 2)).real
    grid0 = make_grid(N, L=L, dim=2)
    u0 = np.asarray(generate_u_alfven(grid0, amp=amp))

    def _phase_y(fx):
        profile = np.mean(np.asarray(fx), axis=0)
        return float(np.angle(np.fft.fft(profile)[1]))

    phi0 = _phase_y(u0[0])
    phi1 = _phase_y(u[0])
    dphi = float(np.unwrap(np.array([phi0, phi1]))[1] - phi0)
    T = steps * dt
    k = 2.0 * np.pi / L
    v_A = abs(B0)
    v_phase = -dphi / (k * T + 1e-30)
    ratio = v_phase / (v_A + 1e-30)
    print(
        f"F Alfven: v_phase={v_phase:.6f} v_A={v_A:.6f} v_phase/v_A={ratio:.6f} "
        f"dphi={dphi:.6f} T={T:.4f} b_guide={out_a['mhd_params'].get('b_guide')}",
        flush=True,
    )
    check("F Alfven phase speed", abs(ratio - 1.0) < 0.1,
          f"v_phase={v_phase:.4f} v_A={v_A:.4f} ratio={ratio:.4f}")
    check("F Alfven ic wiring", out_a.get("ic") == "alfven"
          and out_a["mhd_params"].get("b_guide") == "alfven",
          f"ic={out_a.get('ic')} b_guide={out_a['mhd_params'].get('b_guide')}")

    if failed:
        print("FAILED: " + ", ".join(failed), flush=True)
        sys.exit(1)
    print("SMOKE MHD B-E OK", flush=True)


if __name__ == "__main__":
    main()
