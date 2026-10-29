"""Fuzzy sphere and fuzzy orbifold S^2_F/Z_k. VENUS_FUZZY_CONE_SPEC §1, §3 Option A; FUZZ_PLAN_V2 §2.1."""
import numpy as np


def spin_matrices(N):
    """Spin-j generators, N = 2j+1 (spec §1). [L^i,L^j] = i eps^{ijk} L^k, sum L^2 = j(j+1) = (N^2-1)/4."""
    j = (N - 1) / 2.0
    m = j - np.arange(N)                       # basis |j,m>, m = j..-j
    Lz = np.diag(m).astype(complex)
    Lp = np.zeros((N, N), complex)
    for a in range(1, N):                      # L+|m> = sqrt(j(j+1)-m(m+1)) |m+1>
        Lp[a - 1, a] = np.sqrt(j * (j + 1) - m[a] * (m[a] + 1))
    Lx = (Lp + Lp.conj().T) / 2
    Ly = (Lp - Lp.conj().T) / (2j)
    return Lx, Ly, Lz


def lam_N(R, N):
    """Spec §1: lambda_N = 2R/sqrt(N^2-1)."""
    return 2.0 * R / np.sqrt(N * N - 1.0)


def R_from_lam(lam, N):
    """Inverse of spec §1 at fixed lambda (limit L2, spec §5)."""
    return lam * np.sqrt(N * N - 1.0) / 2.0


def X_matrices(R, N):
    """Spec §1: X^i = (2R/sqrt(N^2-1)) L^i, sum X^i X^i = R^2 1_N."""
    c = lam_N(R, N)
    return tuple(c * L for L in spin_matrices(N))


def g_matrix(N, k):
    """Spec §3: g = exp(2 pi i L^3/k)."""
    _, _, Lz = spin_matrices(N)
    return np.diag(np.exp(2j * np.pi * np.diag(Lz).real / k))


def invariant_mask(N, k):
    """A_k = {M : g M g^-1 = M}: entry (a,b) survives iff m_a - m_b == 0 mod k (spec §3 'block structure')."""
    j = (N - 1) / 2.0
    m = j - np.arange(N)
    d = np.rint(m[:, None] - m[None, :]).astype(int)
    return (d % k) == 0


def adjoint_laplacian(R, N):
    """FUZZ_PLAN_V2 §2.3 O-A: Delta f = sum_i [L^i,[L^i,f]] / R^2, as an N^2 x N^2 superoperator
    acting on row-major vec(f). Used only for tiny-N checks."""
    I = np.eye(N)
    D = np.zeros((N * N, N * N), complex)
    for L in spin_matrices(N):
        ad = np.kron(L, I) - np.kron(I, L.T)     # vec([L,f]) for row-major vec
        D += ad @ ad
    return D / R**2


def invariant_spectrum_counts(N, k):
    """Analytic spectrum of Delta on A_k (spec §4: eigenvalues l(l+1)/R^2; survivors m == 0 mod k,
    flagged UNCHECKED in spec and verified numerically in tests). Returns (l array, multiplicity array)."""
    ls = np.arange(N)
    mult = np.array([sum(1 for m in range(-l, l + 1) if m % k == 0) for l in ls])
    return ls, mult


def coherent_twist_overlap(N, theta, phi):
    """|<n|R_z(phi)|n>|^2 for spin-j coherent state at polar angle theta (closed form):
    <n|e^{i phi L3}|n> = (cos^2(theta/2) + sin^2(theta/2) e^{i phi})^{2j} up to a phase."""
    j2 = N - 1
    z = np.cos(theta / 2) ** 2 + np.sin(theta / 2) ** 2 * np.exp(1j * phi)
    return np.abs(z) ** (2 * j2)


def coherent_state(N, theta):
    """|n(theta, 0)> = exp(-i theta L_y)|j,j> (explicit, for tests)."""
    from scipy.linalg import expm
    _, Ly, _ = spin_matrices(N)
    e = np.zeros(N, complex); e[0] = 1
    return expm(-1j * theta * Ly) @ e
