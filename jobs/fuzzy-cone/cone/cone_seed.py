"""C-1 fuzzy cone seed on the Z_k cap (CONE_SPEC_V1 §3; b0a62591 + ADDENDUM_P1 3150c48b). Aethon 2026-10-29.
Fuzzy-native pieces only on the S^2 factor (R0): monopole projectors P_+- = (1 +- Lam)/2,
Lam = (2 L.sigma + 1)/N (exact projectors, from it1b/venus_v1_2_check_charge.py 0530de3b). No sampled continuum
field on S^2_F. The x3,x4 dependence is a profile F(r) and the winding e^{i n theta}:
  g = P_+ + e^{i n theta} P_-   (exact unitary; P_- rank N-1)
  B_i = L_i + F(r) (g L_i g^+ - L_i),    U_mu = exp(-i n Phi_mu P_-) with Phi_mu = int_link F dtheta (exact: P_- projector)
F -> 1 for r >> r_c, so the far field is an exact fuzzy pure gauge (B = g L g^+, U = g-transport) at every N.
Cone tip law (Akitti framework core, C^1 matched): u(r) = (r/r_c)^p, p = |n|/alpha, F = 1 - exp(-u)  (F ~ r^p at the tip; 1 - F < 1e-6 for u > 14).
Fuzzy tip (default, graded): u_fuzzy = u * r^2/(r^2 + w_N^2), w_N = 2R/sqrt(N+1) (coherent-state width).
Sharp tip (side only): w = 0.
FLAG (spec ambiguity S1): the tip radius r is read in the x3,x4 plane (where the winding lives); w_N is a sphere width
carried over to the plane. FLAG S2: p = |n|/alpha is put in by hand through F, so P2 checks the construction, not dynamics."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "it1b"))
from fuzzy_instanton import spin_matrices
SIG = [np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], complex)]

def w_of(R, N): return 2 * R / np.sqrt(N + 1)

def profile(r, n, alpha, r_c, w):
    p = abs(n) / alpha; u = (r / r_c) ** p
    if w > 0: u = u * r**2 / (r**2 + w**2)
    return -np.expm1(-u)          # F = 1 - exp(-u): F ~ u ~ r^p at the tip, F -> 1 (pure gauge) beyond ~2 r_c

def projectors(N):
    Ls = spin_matrices(N)
    Lam = (2 * sum(np.kron(Ls[a], SIG[a]) for a in range(3)) + np.eye(2 * N)) / N
    return (np.eye(2 * N) + Lam) / 2, (np.eye(2 * N) - Lam) / 2

def build(m, n, r_c, tip="fuzzy", ns=16, sgn=1):
    """m = it1b Model (any k; seed is Z_k invariant since Lam commutes with G = g(x)h). alpha = 1/m.k (D2)."""
    N = m.N; alpha = 1.0 / m.k; w = w_of(m.R, N) if tip == "fuzzy" else 0.0
    Pp, Pm = projectors(N); Lf = m.Lfull; M = 2 * N
    B = np.zeros((3, m.L3, m.L4, M, M), complex); U = np.zeros((2, m.L3, m.L4, M, M), complex)
    F = lambda rr: profile(rr, n, alpha, r_c, w)
    for p in range(m.L3):
        for q in range(m.L4):
            x3, x4 = m.x3[p], m.x4[q]; rr = np.hypot(x3, x4); th = sgn * np.arctan2(x4, x3)
            g = Pp + np.exp(1j * n * th) * Pm
            for i in range(3): B[i, p, q] = Lf[i] + F(rr) * (g @ Lf[i] @ g.conj().T - Lf[i])
            for mu in range(2):
                tot = 0.0
                for s in range(ns):
                    t0, t1 = s / ns * m.a, (s + 1) / ns * m.a
                    P0 = (x3 + (t0 if mu == 0 else 0), x4 + (t0 if mu == 1 else 0))
                    P1 = (x3 + (t1 if mu == 0 else 0), x4 + (t1 if mu == 1 else 0))
                    dth = np.angle(np.exp(1j * sgn * (np.arctan2(P1[1], P1[0]) - np.arctan2(P0[1], P0[0]))))
                    tot += F(np.hypot((P0[0] + P1[0]) / 2, (P0[1] + P1[1]) / 2)) * dth
                U[mu, p, q] = np.eye(M) + (np.exp(-1j * n * tot) - 1) * Pm     # exact exp(-i n tot P_-)
    return B, U

def tip_holonomy(n, k):
    """Frozen rule (build file §3): tip holonomy m = n mod k of the Z_k cap (winding n seen through the k-fold cap
    weight w_cap = 4 pi R^2/(kN)); Q_pred = n/k (in Z/k, = m/k mod 1)."""
    return n % k, n / k
