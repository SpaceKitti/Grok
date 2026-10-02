"""Pair A handoff numbers, the handoff matrix H_A, and the three paths.

No new Hamiltonian is built: H_A is exactly the handoff 2x2 matrix.
"""
import numpy as np

# ---- handoff numbers [assumed] ----
a = 0.12337            # n=1 decay rate (handoff: pi^2/80)
b = 0.49348            # n=2 decay rate (handoff: pi^2/20)
v = -0.360253          # <sine1|x|sine2> (handoff: -32/(9 pi^2))
kappa = (b - a) / 2.0
EPS_EP_HANDOFF = 0.51368066
LAMBDA_EP_HANDOFF = -0.308425j
eps_EP = kappa / abs(v)
half_trace = -1j * (a + b) / 2.0   # tr(H)/2; common eps*L/2 diagonal NOT included


def H_A(eps):
    """Handoff matrix H_A(eps) = [[-i a, v eps], [v eps, -i b]]."""
    return np.array([[-1j * a, v * eps], [v * eps, -1j * b]], dtype=complex)


def lam_closed(eps):
    """Identity: lambda_pm = -i(a+b)/2 +- sqrt(v^2 eps^2 - kappa^2)."""
    r = np.sqrt(complex(v * v * eps * eps - kappa * kappa))
    return half_trace + r, half_trace - r


# ---- paths, t in [0, 4 pi]; one lap = 2 pi ----
R_P2 = 1.5 * eps_EP
H_P2 = 1.0 * eps_EP


def P1(t):
    """Real path along Gamma: eps = 0.5 eps_EP sin t."""
    return complex(0.5 * eps_EP * np.sin(t), 0.0)


def P2(t):
    """Lemniscate of Gerono: eps = R sin t + i h sin t cos t."""
    return complex(R_P2 * np.sin(t), H_P2 * np.sin(t) * np.cos(t))


def P3(t):
    """Circle around +eps_EP only: eps = eps_EP - 0.25 eps_EP e^{it}."""
    return eps_EP - 0.25 * eps_EP * np.exp(1j * t)


def P3b(t):
    """Same one-tip circle, starting outside Gamma: eps = eps_EP + 0.25 eps_EP e^{it}."""
    return eps_EP + 0.25 * eps_EP * np.exp(1j * t)


PATHS = {
    "P1": (P1, "eps(t) = 0.5*eps_EP*sin(t)"),
    "P2": (P2, "eps(t) = R sin(t) + i h sin(t)cos(t), R = 1.5 eps_EP, h = eps_EP"),
    "P3": (P3, "eps(t) = eps_EP - 0.25*eps_EP*exp(i t)"),
    "P3b": (P3b, "eps(t) = eps_EP + 0.25*eps_EP*exp(i t)"),
}
