r"""Driven two-mode evolution i dpsi/dt = H_A(eps(t)) psi around the +eps_EP tip.

Model imported read-only from C:\Users\Akitt\pairA-qg-handoff (via pairA-vortices-return/vortices.py);
sheet A/B convention and eigenvalue tracking from C:\Users\Akitt\pairA-vortices-return.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # never write __pycache__ into the imported folders
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

VR = Path(r"C:\Users\Akitt\pairA-vortices-return")
if str(VR) not in sys.path:
    sys.path.insert(1, str(VR))

import vortices as VX  # noqa: E402  (pairA-vortices-return; imports handoff seed.H_A etc.)
from return_test import y_cut_gamma  # noqa: E402  (Gamma-segment cut, upper-lip reading)
from tracks import track  # noqa: E402  (continuous eigenvalue tracking)

H_A, EPS_EP, LAM_EP, A, B, V = VX.H_A, VX.EPS_EP, VX.LAM_EP, VX.A, VX.B, VX.V
GAMMA = VX.GAMMA
in_gamma = VX.in_gamma
GAM = abs(A - B) / 2.0          # gamma = |a-b|/2 (rate scale)
SHIFT = 0.5j * (A + B)          # H' = H_A + i(a+b)/2 * I removes the shared decay
R_LOOP = 0.25 * EPS_EP
EPS_START = EPS_EP - R_LOOP     # 0.75 eps_EP, inside Gamma (default)
PHASE = np.pi                   # loop phase offset: pi -> start 0.75 eps_EP (default); 0 -> start 1.25 eps_EP
I2 = np.eye(2, dtype=complex)


def Hp(eps: complex) -> np.ndarray:
    return H_A(complex(eps)) + SHIFT * I2


def expm2(H: np.ndarray, dt: float) -> np.ndarray:
    """exp(-i H dt) for 2x2 H, exact (Cayley-Hamilton)."""
    tr = np.trace(H) / 2.0
    M = H - tr * I2
    q = np.sqrt(-np.linalg.det(M) + 0j)   # M^2 = q^2 I
    x = q * dt
    s = dt * (1.0 - x * x / 6.0) if abs(x) < 1e-6 else np.sin(x) / q
    return np.exp(-1j * tr * dt) * (np.cos(x) * I2 - 1j * s * M)


def set_start(frac: float) -> None:
    """Select the loop start point: 0.75 (default, phase pi, inside Gamma) or 1.25 (phase 0, outside Gamma)."""
    global EPS_START, PHASE
    if abs(frac - 0.75) < 1e-12:
        EPS_START, PHASE = EPS_EP - R_LOOP, np.pi
    elif abs(frac - 1.25) < 1e-12:
        EPS_START, PHASE = EPS_EP + R_LOOP, 0.0
    else:
        raise ValueError("start must be 0.75 or 1.25 (points of the r = 0.25 eps_EP circle on the real axis)")


def set_swap_ab(on: bool) -> None:
    """In-memory only: swap the handoff constants a<->b used by seed.H_A (files untouched).
    eps_EP, lambda_EP, gamma and the shared-decay shift are symmetric in a,b and stay the same."""
    a0, b0 = sorted((VX._seed.A, VX._seed.B))
    VX._seed.A, VX._seed.B = (b0, a0) if on else (a0, b0)


def eps_of(theta, s: int):
    """eps(theta) = eps_EP + r e^{i(s*theta + PHASE)}; s=+1 ccw, s=-1 cw. PHASE=pi: start/end 0.75 eps_EP; PHASE=0: 1.25 eps_EP."""
    return EPS_EP + R_LOOP * np.exp(1j * (s * np.asarray(theta) + PHASE))


def sheet_basis(eps: complex):
    """Right eigenvectors ordered [sheet A, sheet B] (A = lam_EP + y/2, B = lam_EP - y/2,
    Gamma-segment cut, vortices-return convention). Returns lam[2], R (columns), Linv = R^{-1}."""
    w, R = np.linalg.eig(H_A(complex(eps)))
    y = y_cut_gamma(eps)
    lamA = LAM_EP + 0.5 * y
    if abs(w[1] - lamA) < abs(w[0] - lamA):
        w, R = w[::-1], R[:, ::-1]
    R = R / np.linalg.norm(R, axis=0, keepdims=True)
    return w, R, np.linalg.inv(R)


def decompose(eps: complex, psi: np.ndarray) -> dict:
    lam, R, Linv = sheet_basis(eps)
    c = Linv @ psi                      # c_i = <L_i|psi>/<L_i|R_i> (biorthogonal)
    wl = np.abs(c) ** 2 / np.sum(np.abs(c) ** 2)
    ov = np.array([abs(np.vdot(R[:, i], psi)) ** 2 / (np.vdot(psi, psi).real) for i in range(2)])
    wp = ov / ov.sum()
    slow = int(np.argmax(lam.imag))     # slower-decaying = larger Im lambda
    return {"lam": lam, "w": wl, "w_plain": wp, "slow_idx": slow, "hi_idx": int(np.argmax(lam.real))}


def phys(idx: int, slow_idx: int) -> str:
    return "slower-decaying" if idx == slow_idx else "faster-decaying"


def steps_per_turn(gT: float, factor: int = 1) -> int:
    # dt <= 0.01/gamma  and  >= 2000 steps per turn
    return factor * max(2000, int(np.ceil(gT / 0.01)))


def run_drive(s: int, gT: float, start: int, factor: int = 1, turns: int = 2, n_rec: int = 400) -> dict:
    T = gT / GAM
    omega = 2.0 * np.pi / T
    n1 = steps_per_turn(gT, factor)
    dt = T / n1
    lam0, R0, _ = sheet_basis(eps_of(0.0, s))
    psi = R0[:, start].copy()
    psi0 = psi.copy()
    rec_every = max(1, (n1 * turns) // n_rec)
    th_rec, wA_rec, wB_rec = [0.0], [1.0 if start == 0 else 0.0], [0.0 if start == 0 else 1.0]
    marks = {}
    for k in range(n1 * turns):
        th_mid = omega * (k + 0.5) * dt
        psi = expm2(Hp(eps_of(th_mid, s)), dt) @ psi
        psi = psi / np.linalg.norm(psi)
        kk = k + 1
        if kk % rec_every == 0 or kk % n1 == 0:
            th = omega * kk * dt
            d = decompose(eps_of(th, s), psi)
            th_rec.append(th); wA_rec.append(d["w"][0]); wB_rec.append(d["w"][1])
            if kk % n1 == 0:
                d["psi"] = psi.copy()
                d["fid"] = abs(np.vdot(psi0, psi)) / (np.linalg.norm(psi0) * np.linalg.norm(psi))
                marks[kk // n1] = d
    return {"s": s, "gT": gT, "T": T, "omega": omega, "dt": dt, "n_per_turn": n1, "start": start,
            "theta": np.array(th_rec), "wA": np.array(wA_rec), "wB": np.array(wB_rec), "marks": marks,
            "start_slow_idx": int(np.argmax(lam0.imag))}


def tracked_labels(s: int, n: int = 8000) -> dict:
    """Where the start eigenvalue of sheet A (and B) goes under continuous tracking at 2pi, 4pi."""
    th = np.linspace(0.0, 4.0 * np.pi, n + 1)
    z = eps_of(th, s)
    lam0, _, _ = sheet_basis(z[0])
    tr = track(z, first=lam0)
    out = {}
    for m, idx in ((1, n // 2), (2, n)):
        lam_m, _, _ = sheet_basis(z[idx])
        out[m] = ["AB"[int(np.argmin(np.abs(lam_m - tr["evals"][idx, j])))] for j in range(2)]
    return out  # out[m][start] = tracked label of the start sheet after m turns


def min_gap_on_loop(n: int = 4000) -> float:
    th = np.linspace(0.0, 2.0 * np.pi, n)
    return float(min(abs(np.diff(np.linalg.eigvals(H_A(complex(e)))))[0] for e in eps_of(th, 1)))


def fixed_eps_check(times_g=(1.0, 2.0, 5.0, 10.0)) -> dict:
    eps = complex(EPS_START)
    lam, R, Linv = sheet_basis(eps)
    slow = int(np.argmax(lam.imag)); fast = 1 - slow
    dG = lam[slow].imag - lam[fast].imag
    psi = R[:, 0] + R[:, 1]
    c0 = Linv @ psi
    r0 = abs(c0[fast]) ** 2 / abs(c0[slow]) ** 2
    dt = 0.01 / GAM
    U = expm2(Hp(eps), dt)
    rows, t, k = [], 0.0, 0
    for tg in times_g:
        nsteps = int(round(tg / 0.01))
        while k < nsteps:
            psi = U @ psi; psi = psi / np.linalg.norm(psi); k += 1
        t = k * dt
        c = Linv @ psi
        meas = abs(c[fast]) ** 2 / abs(c[slow]) ** 2
        exp_ = r0 * np.exp(-2.0 * dG * t)
        rows.append({"gamma_t": tg, "t": t, "measured": meas, "expected": exp_, "rel_err": abs(meas / exp_ - 1)})
    return {"eps": eps, "lam": lam, "slow": slow, "dGamma": dG, "rows": rows, "slow_sheet": "AB"[slow]}
