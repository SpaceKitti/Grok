"""L1: H_QG with i dpsi/dt = H_QG(eps) psi. Route (a): H_A written as the non-Hermitian sector of H_QG.
Route (b): lambda_EP*1 + v*[[eps, eps_EP], [-eps_EP, -eps]], the Dirac-type square root of v^2 F_JT: (H_b - lambda_EP)^2 = v^2 F_JT * 1.
Numbers a, b, v are read from the handoff seed.py. H_A itself is imported only as the comparison target."""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

HANDOFF = Path(r"C:\Users\Akitt\pairA-qg-handoff")
if str(HANDOFF) not in sys.path:
    sys.path.append(str(HANDOFF))
import seed as _seed  # noqa: E402  (numbers + comparison target only)

A_RATE, B_RATE, V = float(_seed.A), float(_seed.B), float(_seed.V)
E = abs(B_RATE - A_RATE) / (2 * abs(V))
LAM = -0.5j * (A_RATE + B_RATE)
HAVE = {"eps_EP": 0.51368066, "lam_EP": -0.308425j, "v": -0.360253, "a": 0.12337, "b": 0.49348}
I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


def H_qg_a(eps):
    """route (a): lambda_EP*1 + i(b-a)/2 sigma_z + v eps sigma_x (numbers only; equals H_A identically)."""
    e = complex(eps)
    return LAM * I2 + 0.5j * (B_RATE - A_RATE) * SZ + V * e * SX


def H_qg_b(eps):
    """route (b): lambda_EP*1 + v*[[eps, eps_EP], [-eps_EP, -eps]]."""
    e = complex(eps)
    return LAM * I2 + V * np.array([[e, E], [-E, -e]], dtype=complex)


def H_A_target(eps):
    return np.asarray(_seed.H_A(complex(eps)), dtype=complex)


def y_cut(eps):
    """sheet convention of vortices-return / probe-surface: y = 2v sqrt(eps-eps_EP) sqrt(eps+eps_EP), Gamma-segment cut, upper lip."""
    e = complex(eps)
    if abs(e.imag) < 1e-13 and abs(e.real) <= E:
        e = complex(e.real, 1e-13)
    return 2 * V * np.sqrt(e - E) * np.sqrt(e + E)


def eig_err(H1, H2, eps_list):
    err = 0.0
    for e in eps_list:
        w1 = np.linalg.eigvals(H1(e)); w2 = np.linalg.eigvals(H2(e))
        err = max(err, min(np.max(np.abs(w1 - w2)), np.max(np.abs(w1 - w2[::-1]))))
    return err


def grid():
    out = []
    for x in np.linspace(-3 * E, 3 * E, 41):
        for yy in np.linspace(-E, E, 11):
            z = complex(x, yy)
            if min(abs(z - E), abs(z + E)) > 1e-6:
                out.append(z)
    return out


def swap_count(H, tip, turns, n=8000, r=0.25):
    """continuation of both eigenvalues around a circle r*eps_EP about tip, start at tip + r (outside Gamma);
    returns [index change for start eigenvalue 0, 1] (0 = return, 1 = swap)."""
    th = np.linspace(0, 2 * np.pi * turns, n * turns + 1)
    z = tip + r * E * np.exp(1j * th) * np.sign(tip)
    w0 = np.linalg.eigvals(H(z[0])); cur = w0.copy()
    for zi in z[1:]:
        w = np.linalg.eigvals(H(zi))
        cur = w if np.sum(np.abs(w - cur)) <= np.sum(np.abs(w[::-1] - cur)) else w[::-1]
    return [int(np.argmin(np.abs(w0 - cur[j])) != j) for j in range(2)]


def ep_locations(H):
    """eps on the real axis where the two eigenvalues merge (disc of the char. polynomial = 0), by root finding."""
    from scipy.optimize import brentq
    def d(x):
        M = H(x); tr = np.trace(M); det = np.linalg.det(M)
        return (tr * tr - 4 * det).real
    xs = np.linspace(-2 * E, 2 * E, 401)
    roots = []
    for x0, x1 in zip(xs[:-1], xs[1:]):
        if d(x0) * d(x1) < 0:
            roots.append(brentq(d, x0, x1, xtol=1e-15))
    return roots


def gamma_structure(H):
    """inside Gamma: eigenvalue difference purely imaginary (shared frequency); outside: real (shared decay); mean = lambda_EP."""
    ins = [np.linalg.eigvals(H(x)) for x in np.linspace(-0.95 * E, 0.95 * E, 21)]
    out = [np.linalg.eigvals(H(x)) for x in np.concatenate([np.linspace(1.05 * E, 3 * E, 10), -np.linspace(1.05 * E, 3 * E, 10)])]
    re_in = max(abs((w[0] - w[1]).real) for w in ins)
    im_out = max(abs((w[0] - w[1]).imag) for w in out)
    shift = max(abs(0.5 * (w[0] + w[1]) - LAM) for w in ins + out)
    return re_in, im_out, shift


def similarity_test(Ha, Hb, n_check=25, seed=1):
    """find a constant S with S (Ha - lam) = (Hb - lam) S at two eps values (null space), then test it at many eps."""
    rng = np.random.default_rng(seed)
    def Ka(e): return Ha(e) - LAM * I2
    def Kb(e): return Hb(e) - LAM * I2
    rows = []
    for e in (0.3 + 0.1j, -1.1 + 0.4j):
        P, Q = Ka(e), Kb(e)
        # vec(S P - Q S) = (P^T kron I - I kron Q) vec(S)  (column-major vec)
        rows.append(np.kron(P.T, I2) - np.kron(I2, Q))
    M = np.vstack(rows)
    _, sv, Vh = np.linalg.svd(M)
    S = Vh[-1].conj().reshape(2, 2, order="F")
    res = 0.0
    for _ in range(n_check):
        e = complex(rng.normal() * 2 * E, rng.normal() * E)
        res = max(res, np.max(np.abs(S @ Ka(e) - Kb(e) @ S)) / np.max(np.abs(S)))
    return {"S": S, "cond": float(np.linalg.cond(S)), "res": float(res), "sv_min": float(sv[-1]), "sv_next": float(sv[-2])}


def su2_map():
    """explicit constant SU(2) map: S = (1/2)[1 - i(sx - sy + sz)] = exp(-i (2pi/3)/2 n.sigma), n = (1,-1,1)/sqrt3.
    S sx S^dag = sz, S sy S^dag = -sx, S sz S^dag = -sy (rotation O, det +1). H_A - lam_EP = v(-i eps_EP sz + eps sx) -> v(eps sz + i eps_EP sy) = route (b) - lam_EP."""
    S = 0.5 * (I2 - 1j * (SX - SY + SZ))
    Sd = S.conj().T
    pauli = max(np.max(np.abs(S @ SX @ Sd - SZ)), np.max(np.abs(S @ SY @ Sd + SX)), np.max(np.abs(S @ SZ @ Sd + SY)))
    O = np.array([[0, -1, 0], [0, 0, -1], [1, 0, 0]], dtype=float)   # columns: images of e_x, e_y, e_z
    form_a = max(float(np.max(np.abs((H_A_target(z) - LAM * I2) - V * (-1j * E * SZ + z * SX)))) for z in grid())
    form_b = max(float(np.max(np.abs((H_qg_b(z) - LAM * I2) - V * (z * SZ + 1j * E * SY)))) for z in grid())
    res = max(float(np.max(np.abs(S @ H_A_target(z) @ Sd - H_qg_b(z)))) for z in grid())
    return {"S": S, "det": complex(np.linalg.det(S)), "unit": float(np.max(np.abs(S @ Sd - I2))), "pauli": float(pauli),
            "detO": float(np.linalg.det(O)), "form_a": form_a, "form_b": form_b, "res": res}


def run():
    g = grid()
    out = {"numbers": {"a": A_RATE, "b": B_RATE, "v": V, "eps_EP": E, "lam_EP": LAM},
           "have_check": max(abs(E - HAVE["eps_EP"]), abs(LAM - HAVE["lam_EP"]), abs(V - HAVE["v"]), abs(A_RATE - HAVE["a"]), abs(B_RATE - HAVE["b"])),
           "n_grid": len(g)}
    for name, H in (("a", H_qg_a), ("b", H_qg_b)):
        re_in, im_out, shift = gamma_structure(H)
        out[name] = {"err": eig_err(H, H_A_target, g), "eps": ep_locations(H), "re_in": re_in, "im_out": im_out, "shift": shift,
                     "swap": {(tip, t): swap_count(H, tip * E, t) for tip in (+1, -1) for t in (1, 2)},
                     "mat_diff": max(float(np.max(np.abs(H(z) - H_A_target(z)))) for z in g),
                     "sq_res": max(float(np.max(np.abs((H(z) - LAM * I2) @ (H(z) - LAM * I2) - V ** 2 * (z * z - E * E) * I2))) for z in g)}
    out["sim_b"] = similarity_test(H_qg_a, H_qg_b)
    out["su2"] = su2_map()
    return out
