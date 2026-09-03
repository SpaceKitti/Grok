"""A2c 3D textbook-B OT: wire-check + tiny blowup-watch.

Watch only. No Clay-proof. No singularity claim. No Crow, no merge.
"""
import os
import sys
from pathlib import Path

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import jax
jax.config.update("jax_enable_x64", True)

import numpy as np
from chive_ns import run_framework, generate_u_ot, generate_b0, make_grid


def _arr(x):
    return np.asarray(x, dtype=float)


def print_formulas():
    print("Venus 3D textbook-B OT formulas:", flush=True)
    print("  x=2πX/L, y=2πY/L, z=2πZ/L", flush=True)
    print("  u = U0 (-sin y, sin x, 0.2 cos z)", flush=True)
    print("  B = B0 (-sin y, sin 2x, 0.2 cos z)", flush=True)
    print("  Qin-project B (the Bz term is not div-free).", flush=True)
    print("  Keep u; double the harmonic on By like 2D.", flush=True)
    print(
        "  Matching seed is u=B up to amplitude — that's the diagonal. "
        "This seed is NOT a copy of u.",
        flush=True,
    )


def seed_check(N=16):
    g = make_grid(N, L=1.0, dim=3)
    L = float(g["L"])
    u = np.asarray(generate_u_ot(g, U0=1.0))
    Bhat = generate_b0(g, B0=1.0, kind="ot")
    B = np.asarray(jax.numpy.fft.ifftn(Bhat, axes=(1, 2, 3)).real)
    x = np.linspace(0.0, L, N, endpoint=False)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    xx = 2.0 * np.pi * X / L
    yy = 2.0 * np.pi * Y / L
    zz = 2.0 * np.pi * Z / L
    u_raw = np.stack([-np.sin(yy), np.sin(xx), 0.2 * np.cos(zz)])
    B_raw = np.stack([-np.sin(yy), np.sin(2.0 * xx), 0.2 * np.cos(zz)])
    B_match = np.stack([-np.sin(yy), np.sin(xx), 0.2 * np.cos(zz)])
    # After Qin, By should still track sin 2x, not sin x.
    corr_by_2x = float(np.corrcoef(B[1].ravel(), B_raw[1].ravel())[0, 1])
    corr_by_x = float(np.corrcoef(B[1].ravel(), B_match[1].ravel())[0, 1])
    corr_uy_x = float(np.corrcoef(u[1].ravel(), u_raw[1].ravel())[0, 1])
    corr_uy_by = float(np.corrcoef(u[1].ravel(), B[1].ravel())[0, 1])
    k_stack = np.asarray(g["k_stack"])
    divB = float(np.max(np.abs(np.fft.ifftn(1j * np.sum(k_stack * np.asarray(Bhat), axis=0)).real)))
    print(
        f"SEED N={N}  corr(By, sin 2x)={corr_by_2x:.4f}  "
        f"corr(By, sin x)={corr_by_x:.4f}  corr(uy, sin x)={corr_uy_x:.4f}  "
        f"corr(uy, By)={corr_uy_by:.4f}  max|div B|={divB:.3e}",
        flush=True,
    )
    ok = (
        corr_by_2x > 0.95
        and corr_by_x < 0.5
        and corr_uy_x > 0.95
        and abs(corr_uy_by) < 0.5
        and divB < 1e-10
    )
    print(f"{'PASS' if ok else 'FAIL'} 3D textbook-B seed (By=sin 2x, u not a copy of B)", flush=True)
    return ok


def peel_decision(t, w, j):
    """Say peel from the table only. Do not invent."""
    rel = np.max(np.abs(j - w) / (np.maximum(w, j) + 1e-30))
    wmax, jmax = float(np.max(w)), float(np.max(j))
    tw, tj = float(t[int(np.argmax(w))]), float(t[int(np.argmax(j))])
    # |J| runs away at bounded |ω|: J peak clearly above W peak AND
    # columns not identical, and ω does not track J's growth.
    j_over_w = jmax / (wmax + 1e-30)
    w_bounded = w[-1] <= 1.2 * wmax
    j_run = jmax > 1.15 * wmax and jmax > 1.15 * j[0]
    cols_same = rel < 0.02
    if cols_same:
        peel = False
        why = (
            f"columns nearly identical (max rel |J-ω|={rel:.3f}); "
            "no peel on this window"
        )
    elif j_run and w_bounded:
        peel = True
        why = (
            f"columns not identical (max rel |J-ω|={rel:.3f}); "
            f"|J| runs (peak {jmax:.4e} at t={tj:.4f}) at bounded |ω| "
            f"(peak {wmax:.4e} at t={tw:.4f}, end/peak={w[-1]/(wmax+1e-30):.3f})"
        )
    else:
        peel = False
        why = (
            f"columns differ (max rel |J-ω|={rel:.3f}, |J|_peak/|ω|_peak={j_over_w:.3f}) "
            "but |J| does not run away at bounded |ω| on this window"
        )
    return peel, why


def main():
    print_formulas()
    if not seed_check(N=16):
        print("FAILED seed check", flush=True)
        sys.exit(1)

    N = 16
    dim = 3
    ic = "ot"
    dt = 0.005
    steps = 100
    diag_every = 10
    print(
        f"A2c blowup-watch  N={N} dim={dim} ic={ic} mode=mhd  "
        f"force_off  steps={steps} dt={dt}  t={steps*dt:.3f}  "
        f"watch only, no Clay-proof, no singularity claim",
        flush=True,
    )
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
    print(f"{'t':>10} {'max|w|':>14} {'max|J|':>14}", flush=True)
    for i in range(t.size):
        print(f"{t[i]:10.6f} {w[i]:14.6e} {j[i]:14.6e}", flush=True)

    failed = []

    def check(name, ok, detail):
        tag = "PASS" if ok else "FAIL"
        print(f"{tag} {name}: {detail}", flush=True)
        if not ok:
            failed.append(name)

    check("no NaN max|w|", np.all(np.isfinite(w)), f"n={w.size}")
    check("no NaN max|J|", np.all(np.isfinite(j)), f"n={j.size}")
    check("max|w| nonzero", bool(np.max(np.abs(w)) > 0.0), f"max|w|={float(np.max(np.abs(w))):.6e}")
    check("max|J| nonzero", bool(np.max(np.abs(j)) > 0.0), f"max|J|={float(np.max(np.abs(j))):.6e}")

    peel, why = peel_decision(t, w, j)
    print(f"PEEL={'yes' if peel else 'no'}: {why}", flush=True)
    print("watch only; no Clay-proof; no singularity claim", flush=True)

    if failed:
        print("FAILED: " + ", ".join(failed), flush=True)
        sys.exit(1)
    print("HAVE A2c 3D textbook-B OT (By=sin 2x; watch max|w| vs max|J|).", flush=True)


if __name__ == "__main__":
    main()
