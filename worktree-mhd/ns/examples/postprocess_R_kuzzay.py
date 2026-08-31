"""Pointwise leftover R = W_L + B:S on scar-off end-state.

No snapshot was on disk; this re-runs the exact scar-off kwargs
once, then postprocesses only. Sign is PLUS. Same |J| mask and
volume mean for W_L and B:S.

    python examples/postprocess_R_kuzzay.py
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from chive_ns import run_framework, DEFAULT_MHD, default_scar_centres
from chive_ns.grid import ik_cross

OUT = Path(__file__).resolve().parent / "mhd_n48_hyperkcut"


def _fields(out):
    grid = out["grid"]
    u_hat = np.array(out["u_hat"])
    B_hat = np.array(out["B_hat"])
    k = np.array(grid["k_stack"])
    axes = (1, 2, 3)
    u = np.fft.ifftn(u_hat, axes=axes).real
    B = np.fft.ifftn(B_hat, axes=axes).real
    J = np.fft.ifftn(np.array(ik_cross(out["B_hat"], grid)), axes=axes).real
    JxB = np.stack([
        J[1] * B[2] - J[2] * B[1],
        J[2] * B[0] - J[0] * B[2],
        J[0] * B[1] - J[1] * B[0],
    ])
    W_L = np.sum(u * JxB, axis=0)
    ghat = 1j * u_hat[:, None] * k[None, :]
    gu = np.fft.ifftn(ghat, axes=(2, 3, 4)).real
    S = 0.5 * (gu + np.swapaxes(gu, 0, 1))
    BS = np.einsum("i...,ij...,j...->...", B, S, B)
    R = W_L + BS
    j2 = np.sum(J**2, axis=0)
    jmag = np.sqrt(j2)
    ub = np.sum(u * B, axis=0)
    b2 = np.sum(B**2, axis=0)
    P = ub * B - 0.5 * b2 * u
    dx = float(grid["dx"])
    return dict(W_L=W_L, BS=BS, R=R, jmag=jmag, P=P, dx=dx, N=int(grid["N"]))


def _face_flux(P, mask, dx):
    """∑ P·n dA on ∂M, M = mask. Outward from M."""
    flux = 0.0
    dA = dx * dx
    for i in range(3):
        m0 = mask
        m1 = np.roll(mask, -1, axis=i)
        Pf = 0.5 * (P[i] + np.roll(P[i], -1, axis=i))
        flux += float(np.sum(Pf * (m0 & ~m1))) * dA
        flux -= float(np.sum(Pf * (~m0 & m1))) * dA
    return flux


def main():
    centres = default_scar_centres(1.0, 4, 3)
    common = dict(
        dim=3, N=48, steps=240, dt=0.0015, ic="tubes", scheme="rk2",
        force_on=False, n_scars=4, scar_centres=centres, force_amp=0.35,
        nu=5e-4, diag_every=40,
    )
    mhd = dict(DEFAULT_MHD, freeze_ext=0.0, eta_mag=1e-3,
               eta_odd=0.0, mu_eff=0.0, eta_hyper=0.0,
               posdiv=0.0, hyper_kcut=0.0)
    print("No 3-D snapshot on disk; re-running exact scar-off kwargs once.",
          flush=True)
    print(f"force_on={common['force_on']}  force_amp={common['force_amp']}",
          flush=True)
    out = run_framework(mode="mhd", viscoelastic=False, magnetic=True,
                        mhd_params=mhd, **common)
    f = _fields(out)
    W_L, BS, R = f["W_L"], f["BS"], f["R"]
    jmag = f["jmag"]
    dx = f["dx"]
    dV = dx ** 3
    M = jmag >= (0.5 * float(jmag.max()))
    nM = int(M.sum())
    nall = R.size

    g_R = float(np.mean(R))
    g_WL = float(np.mean(W_L))
    g_BS = float(np.mean(BS))
    m_WL = float(np.sum(W_L * M) / max(nM, 1))
    m_BS = float(np.sum(BS * M) / max(nM, 1))
    m_R = float(np.sum(R * M) / max(nM, 1))
    int_M_R = float(np.sum(R * M) * dV)
    flux = _face_flux(f["P"], M, dx)

    print("\n========== R = W_L + B:S   (PLUS)  scar-off t=0.36 ==========")
    print("mask M: |J| >= 0.5 max|J|   volume means (not |J|^2-weighted)")
    print(f"{'qty':<22} {'value':>14}")
    print(f"{'⟨R⟩ global':<22} {g_R:14.3e}")
    print(f"{'⟨W_L⟩ global':<22} {g_WL:14.3e}")
    print(f"{'⟨B:S⟩ global':<22} {g_BS:14.3e}")
    print(f"{'⟨W_L⟩+⟨B:S⟩':<22} {g_WL + g_BS:14.3e}")
    print(f"{'⟨W_L⟩_M':<22} {m_WL:14.3e}")
    print(f"{'⟨B:S⟩_M':<22} {m_BS:14.3e}")
    print(f"{'⟨W_L⟩_M+⟨B:S⟩_M':<22} {m_WL + m_BS:14.3e}")
    print(f"{'⟨R⟩_M':<22} {m_R:14.3e}")
    print(f"{'∫_M R':<22} {int_M_R:14.3e}")
    print(f"{'∮_∂M P·n':<22} {flux:14.3e}")
    print(f"{'∮P − ∫_M R':<22} {flux - int_M_R:14.3e}")
    print(f"cells in M: {nM} / {nall}  ({100.0 * nM / nall:.2f}%)")
    print("P = (u·B) B − (B²/2) u   (identity flux, not Ohmic current)")

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "R_identity_scar_off.csv"
    with path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["qty", "value"])
        for k, v in [
            ("force_on", 0),
            ("mask", "abs(J)>=0.5*max|J|"),
            ("mean_R_global", g_R),
            ("mean_WL_global", g_WL),
            ("mean_BS_global", g_BS),
            ("mean_WL_plus_BS_global", g_WL + g_BS),
            ("mean_WL_M", m_WL),
            ("mean_BS_M", m_BS),
            ("mean_R_M", m_R),
            ("int_M_R", int_M_R),
            ("flux_dM_P", flux),
            ("flux_minus_int_R", flux - int_M_R),
            ("n_mask", nM),
            ("n_all", nall),
        ]:
            w.writerow([k, v])
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
