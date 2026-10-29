"""PRIMARY test B observable: pole LDOS (FUZZ_PLAN_V4 §3).
K_N(t;pole) = sum_{l<=N-1} |<pole|psi_l>|^2 exp(-t l(l+1)/R^2), psi_l normalised Z_k-invariant eigenfunctions,
<pole|.|pole> = Berezin (coherent-state) symbol at the tip. Compared with classical cone K_inf(t;pole).
Derivation (README A8): only m=0 modes are nonzero at the pole (m=0 is Z_k-invariant for every k).
Fuzzy normalised harmonic Y_l0 = sqrt(kN/(4 pi R^2)) T_l0 (T Hilbert-Schmidt unit; fuzzy integral (4 pi R^2/(kN)) Tr on A_k,
area 4 pi R^2/k as in V2 §2.3). Wigner-Eckart: <j j|T_l0|j j> = sqrt((2l+1)/N) <j j; l 0|j j>, and
<j j; l 0|j j>^2 = c_l = ((N-1)!)^2 N / ((N+l)! (N-1-l)!).  Hence
  K_N = k/(4 pi R^2) sum_{l=0}^{N-1} (2l+1) c_l e^{-t l(l+1)/R^2},   K_inf = k/(4 pi R^2) sum_{l>=0} (2l+1) e^{-t l(l+1)/R^2}."""
import numpy as np
from scipy.special import gammaln

def cg_sq(N):
    """c_l for l = 0..N-1 (closed form above; verified against explicit matrices in tests)."""
    l = np.arange(N)
    return np.exp(2 * gammaln(N) + np.log(N) - gammaln(N + l + 1) - gammaln(N - l))

def K_fuzzy(R, N, k, t):
    l = np.arange(N); t = np.atleast_1d(t)
    return k / (4 * np.pi * R**2) * ((2 * l + 1) * cg_sq(N) * np.exp(-np.outer(t, l * (l + 1)) / R**2)).sum(1)

def K_classical(R, k, t, exp_cut):
    """Classical S^2/Z_k pole kernel; series cut where t l(l+1)/R^2 > exp_cut (config; error < e^{-exp_cut} relative)."""
    t = np.atleast_1d(t)
    lmax = int(np.ceil(np.sqrt(exp_cut * R**2 / t.min()))) + 1
    l = np.arange(lmax + 1)
    return k / (4 * np.pi * R**2) * ((2 * l + 1) * np.exp(-np.outer(t, l * (l + 1)) / R**2)).sum(1)

def ldos_width(R, N, k, cfg):
    """V4 §3: t* = first t (scanning upward from t_lo) where |K_N/K_inf - 1| drops to <= threshold (frozen 0.10);
    log-linear interpolation between grid points. w = sqrt(t*). Grid t/R^2 in [ldos_t_lo, ldos_t_hi] (config)."""
    t = R**2 * np.geomspace(cfg["ldos_t_lo"], cfg["ldos_t_hi"], cfg["ldos_n_t"])
    dev = np.abs(K_fuzzy(R, N, k, t) / K_classical(R, k, t, cfg["ldos_exp_cut"]) - 1)
    thr = cfg["ldos_threshold"]
    below = np.flatnonzero(dev <= thr)
    out = {"N": N, "k": k, "R": float(R), "monotone": bool(np.all(np.diff(dev) <= 0))}
    if len(below) == 0 or below[0] == 0:
        out.update(t_star=None, w_over_R=None, reason="no crossing inside t grid")
        return out
    i = below[0]
    x0, x1 = np.log(t[i - 1]), np.log(t[i]); y0, y1 = dev[i - 1] - thr, dev[i] - thr
    ts = float(np.exp(x0 - y0 * (x1 - x0) / (y1 - y0)))
    out.update(t_star=ts, t_star_over_Rlam=ts / (R * 2 * R / np.sqrt(N * N - 1.0)), w_over_R=float(np.sqrt(ts) / R))
    return out
