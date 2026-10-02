"""Drive protocol (as in pairA-drive-return / pairA-qg-loss): loop r = 0.25 eps_EP around +eps_EP, starts 0.75 / 1.25 eps_EP."""
from __future__ import annotations

import numpy as np

import H_try as HT

E, I2 = HT.EPS_EP, HT.I2
R_LOOP = 0.25 * E
GAMMA = abs(HT.A - HT.B) / 2


def eps_of(th, s, frac):
    return E + R_LOOP * np.exp(1j * (s * th + (np.pi if frac < 1 else 0.0)))


def gamma_g(H, n=2000):
    th = np.linspace(0, 2 * np.pi, n)
    return 0.5 * max(abs(np.diff(np.linalg.eigvals(H(z)))[0].imag) for z in eps_of(th, 1, 0.75))


def expm2(Hm, dt):
    tr = np.trace(Hm) / 2.0
    M = Hm - tr * I2
    q = np.sqrt(-np.linalg.det(M) + 0j)
    x = q * dt
    s = dt * (1.0 - x * x / 6.0) if abs(x) < 1e-6 else np.sin(x) / q
    return np.exp(-1j * tr * dt) * (np.cos(x) * I2 - 1j * s * M)


def modes(H, eps):
    """index 0 = slower-decaying (larger Im), or higher-frequency if the decays are equal."""
    w, R = np.linalg.eig(H(eps))
    d = w[0] - w[1]
    by_decay = abs(d.imag) > 1e-9 * abs(d)
    key = (lambda i: -w[i].imag) if by_decay else (lambda i: -w[i].real)
    order = sorted(range(2), key=key)
    w, R = w[order], R[:, order]
    R = R / np.linalg.norm(R, axis=0, keepdims=True)
    names = ["slower-decaying", "faster-decaying"] if by_decay else ["higher-frequency", "lower-frequency"]
    return w, R, np.linalg.inv(R), names, by_decay


def run_drive(H, frac, s, gT, start, gscale, turns=2, factor=1, pert=0.0):
    T = gT / gscale
    n1 = factor * max(2000, int(np.ceil(gT / 0.01)))
    dt = T / n1
    om = 2 * np.pi / T
    Hp = (lambda z: H(z) + pert * I2) if pert else H
    _, R0, _, _, _ = modes(H, eps_of(0.0, s, frac))
    psi = R0[:, start].copy()
    out = {}
    for k in range(n1 * turns):
        psi = expm2(Hp(eps_of(om * (k + 0.5) * dt, s, frac)), dt) @ psi
        psi = psi / np.linalg.norm(psi)
        if (k + 1) % n1 == 0:
            _, R, Linv, _, _ = modes(H, eps_of(om * (k + 1) * dt, s, frac))
            c = Linv @ psi
            wv = np.abs(c) ** 2 / np.sum(np.abs(c) ** 2)
            win = int(np.argmax(wv))
            out[(k + 1) // n1] = {"wv": wv, "win": win, "w": float(wv[win]), "comp": int(np.argmax(np.abs(R[:, win]) ** 2)) + 1}
    return out


def classify(runs, speeds):
    d6, d7 = True, True
    for gT in speeds:
        for m in (1, 2):
            for st in (0, 1):
                a, b = runs[(gT, "ccw", st)][m]["win"], runs[(gT, "cw", st)][m]["win"]
                d6 &= (a == b == 0)
                d7 &= (a != b)
            for dn in ("ccw", "cw"):
                d7 &= runs[(gT, dn, 0)][m]["win"] == runs[(gT, dn, 1)][m]["win"]
    return "D6-like" if d6 else ("D7-like" if d7 else "NO")


def test(H, speeds, gscale, dt_check=True):
    out = {}
    for frac in (0.75, 1.25):
        w0, _, _, names, by_decay = modes(H, frac * E)
        runs = {}
        for gT in speeds:
            for dn, s in (("ccw", 1), ("cw", -1)):
                for st in (0, 1):
                    runs[(gT, dn, st)] = run_drive(H, frac, s, gT, st, gscale)
        dw = 0.0
        if dt_check:
            for dn, s in (("ccw", 1), ("cw", -1)):
                m2 = run_drive(H, frac, s, speeds[0], 0, gscale, factor=2)
                dw = max(dw, max(float(np.max(np.abs(m2[m]["wv"] - runs[(speeds[0], dn, 0)][m]["wv"]))) for m in (1, 2)))
        out[frac] = {"runs": runs, "cls": classify(runs, speeds), "names": names, "broken": bool(by_decay), "lam0": w0, "dw": dw}
    return out
