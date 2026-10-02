"""L3: loss on the 'gravity side' = the anti-Hermitian part of H_QG (route a), which is H_A's loss copied into H_QG.
Driven evolution i dpsi/dt = H_QG(eps(t)) psi around +eps_EP, written in this folder (no H_A / drive.py call at runtime).
Same convention as pairA-drive-return: eps(theta) = eps_EP + r e^{i(s theta + phi0)}, r = 0.25 eps_EP, phi0 = pi (start 0.75) or 0 (start 1.25),
T = gammaT / gamma, gamma = |a-b|/2, exact 2x2 midpoint propagator, gamma dt <= 0.01 and >= 2000 steps per turn, left-eigenvector weights."""
from __future__ import annotations

import numpy as np

import H_QG as HQ

E, LAM = HQ.E, HQ.LAM
GAM = abs(HQ.A_RATE - HQ.B_RATE) / 2
I2 = HQ.I2
R_LOOP = 0.25 * E


def loss_part(H, eps):
    """anti-Hermitian part (H - H^dagger)/2i of H_QG at eps: the loss operator."""
    M = H(eps)
    return (M - M.conj().T) / 2j


def expm2(Hm, dt):
    tr = np.trace(Hm) / 2.0
    M = Hm - tr * I2
    q = np.sqrt(-np.linalg.det(M) + 0j)
    x = q * dt
    s = dt * (1.0 - x * x / 6.0) if abs(x) < 1e-6 else np.sin(x) / q
    return np.exp(-1j * tr * dt) * (np.cos(x) * I2 - 1j * s * M)


def sheet_basis(H, eps):
    w, R = np.linalg.eig(H(eps))
    lamA = LAM + 0.5 * HQ.y_cut(eps)
    if abs(w[1] - lamA) < abs(w[0] - lamA):
        w, R = w[::-1], R[:, ::-1]
    R = R / np.linalg.norm(R, axis=0, keepdims=True)
    return w, R, np.linalg.inv(R)


def weights(H, eps, psi):
    lam, R, Linv = sheet_basis(H, eps)
    c = Linv @ psi
    return np.abs(c) ** 2 / np.sum(np.abs(c) ** 2), lam


def run_drive(H, start_frac, s, gT, start, turns=2):
    phase = np.pi if start_frac < 1 else 0.0
    def eps_of(th):
        return E + R_LOOP * np.exp(1j * (s * th + phase))
    T = gT / GAM
    n1 = max(2000, int(np.ceil(gT / 0.01)))
    dt = T / n1
    om = 2 * np.pi / T
    _, R0, _ = sheet_basis(H, eps_of(0.0))
    psi = R0[:, start].copy()
    marks = {}
    for k in range(n1 * turns):
        psi = expm2(H(eps_of(om * (k + 0.5) * dt)), dt) @ psi
        psi = psi / np.linalg.norm(psi)
        if (k + 1) % n1 == 0:
            w, lam = weights(H, eps_of(om * (k + 1) * dt), psi)
            marks[(k + 1) // n1] = {"w": w, "lam": lam}
    return marks


def classify(runs, speeds):
    same, opp, indep = True, True, True
    for sp in speeds:
        for m in (1, 2):
            for st in "AB":
                a, b = runs[(sp, "ccw", st)][m]["win"], runs[(sp, "cw", st)][m]["win"]
                same &= a == b; opp &= a != b
            for dn in ("ccw", "cw"):
                indep &= runs[(sp, dn, "A")][m]["win"] == runs[(sp, dn, "B")][m]["win"]
    if same and indep:
        return "D6-like"
    if opp and indep:
        return "D7-like"
    return "MIXED"


def run(H=HQ.H_qg_a, speeds=(20.0, 40.0, 100.0)):
    out = {}
    for frac in (0.75, 1.25):
        eps0 = frac * E
        lam0, _, _ = sheet_basis(H, eps0)
        slow = int(np.argmax(lam0.imag)); hi = int(np.argmax(lam0.real))
        runs = {}
        for gT in speeds:
            for dn, s in (("ccw", 1), ("cw", -1)):
                for st in (0, 1):
                    mk = run_drive(H, frac, s, gT, st)
                    rec = {}
                    for m in (1, 2):
                        w = mk[m]["w"]; k = int(np.argmax(w))
                        name = ("slower-decaying" if k == slow else "faster-decaying") if frac < 1 else ("higher-frequency" if k == hi else "lower-frequency")
                        rec[m] = {"win": "AB"[k], "phys": name, "w": float(w[k]), "wv": w}
                    runs[(gT, dn, "AB"[st])] = rec
        out[frac] = {"runs": runs, "cls": classify(runs, speeds), "lam0": lam0, "slow": "AB"[slow], "hi": "AB"[hi]}
    return out
