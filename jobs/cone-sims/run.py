# cone-sims run.py — built by Aethon against CONE_SIM_SPECS 58429B51 (rev 15; Venus-confirmed).
# NOT FROZEN: thresholds/predictions are placeholders tied to Helios's next hash. Graded mode refuses to run.
# Modes: --smoke (tiny scratch, H5) | --full (blocked until FINAL_SPEC_HASH set and matches).
import sys, os, csv, time, hashlib, json, math, tracemalloc
import numpy as np
from scipy.integrate import solve_bvp
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC_HASH_BUILT = "CA9D5CBC"  # rev 17, confirmed by Venus (CHANGES EBA72AF3)
VENUS_DIFF_HASH = "62983822"  # REV9 diff
FINAL_SPEC_HASH = "CA9D5CBC"    # pinned 15 Oct 2026 ~19:25 BST (rev 17); --full still needs NanoRibbon go (instanton run first)
NCY = "NOT COMPUTED (YET)"
PLACEHOLDER_GAP = 100.0  # [assumed] placeholder
PENDING = "PENDING FINAL HASH"
# Thresholds: every value [assumed]; frozen only against the final hash.
THR = {
  "C1_R_tol": 1e-6,              # spec l.92 [assumed]; read-out only
  "C1_normal_phi2": 1e-6,        # column test max_phi2 < 1e-6 drops normal-state
  "C2_mesh_conv_rel": 1e-4,      # reported only [assumed]
  "GB_rel_finest": 1e-4,         # [solver check only, not a test] [assumed]
  "C3_tol": "10 x Richardson E_K, E_T [assumed]; computed in richardson_k1/out (0DCA572A): p_T 1.965-2.112, p_K 2.0000-2.0001, max E_T 9.83e-4 (rel 1.56e-4), max E_K 1.61e-5 (rel 1.28e-6)",
  "C4_zero_rule": "|lam|/lam_gap -> 0, trend over >=3 grids [assumed]; report-only (rev 7); l.175 |lam|<1e-8 dropped",
  "C5_angle_tol": 1e-3,          # n = 2 rows only (Venus: n = 1 by construction)
  "C4_gap_split": PLACEHOLDER_GAP, # used ONLY by the rev-10 5v10 guard's count; C4 counting uses tau0 (Venus ruling 2)
  "C4_near_zero": PENDING,       # mesh-convergence cutoff on |lam|/lam_gap, set from >=3 grids at final hash
  "HP2_overlap": 0.99,           # [assumed]
  "XI_FACTOR": 10.0,             # gauge penalty xi = XI_FACTOR/lambda_min(G^T G) [assumed; H3 deviation, accepted: Venus] (spec: xi = 1; checked by xi_check.py)
  "LANCZOS_TOL": 1e-9,           # [assumed]
  "GRAD_TARGET": 1e-8,           # Venus ruling 1: polish target for |grad|_2 [assumed]
  "POLISH_STEPS": 12,
  "RATE_LOG_FRAC": 0.5,          # rev 16: fitted order p_i >= 0.5 p_c over grids 48/64/80/96
  "RATE_MIN_FALL": 2.0,          # rev 16: and total fall >= 2 over the whole 48->96 span (not per step)
  "ZERO_FLOOR": 1e-13,           # ruling: solver floor for zero-mode eigenvalues
  "FLOOR_NEAR": 10.0,            # ruling: control zero mode within 10x of ZERO_FLOOR on any grid => fall test undecided
  "GRAD_FLOOR": 1e-13,           # |grad|_2 below this counts as the solver floor (or: no further Newton progress)
  "STAT_FACTOR": 10.0,           # stationary iff |grad|_2 <= min|lambda_reported| / 10 (Venus ruling 1)
  "TAU0_FACTOR": 10.0,           # Venus ruling 2: tau0 = 10 x max|lambda| of the alpha=1 control known zero modes
  "UNDECIDED_BAND": 3.0,         # any eigenvalue within factor 3 of tau0 => count undecided
  "GAUGE_MIX_REL": 1e-6,         # mu(xi) spread above this => flag gauge-physical mixing [assumed]
  "C5_penalty": 10.0,            # FROZEN 15 Oct ~18:45 BST, tuned on alpha=1 control only (24x24, R=8): E/E_ref 1.0001 (d=2), 1.0000 (d=4) [assumed]
  "C5_target": "seed moment",    # FROZEN: target M = sum (1-|Phi|^2) r^2 cos 2phi dA of the product-ansatz seed at d
}
SCRATCH = "--smoke" in sys.argv
WORKERS = int(sys.argv[sys.argv.index("--workers")+1]) if "--workers" in sys.argv else 1
STAGE = sys.argv[sys.argv.index("--stage")+1] if "--stage" in sys.argv else None
OUT = os.path.join(HERE, "out_scratch" if SCRATCH else "out")
os.makedirs(OUT, exist_ok=True)
_EIGSH = None  # test hook; default scipy.sparse.linalg.eigsh

def _eigsh_call(*a, **k):
    fn = _EIGSH
    if fn is None:
        from scipy.sparse.linalg import eigsh as fn
    return fn(*a, **k)

def _log_solve(n, k, al, extra=""):
    print(f"solve n={n} kappa={k} alpha={al}{extra}", flush=True)

def _worker_fail(n, k, al, exc):
    msg = f"n={n} kappa={k} alpha={al}: {type(exc).__name__}: {exc}"
    print("FAIL " + msg, flush=True)
    raise RuntimeError(msg) from None

def _lanczos_sa(op, nev, tol):
    """SA eigsh with one ncv/maxiter retry; keep converged subset on second failure."""
    partial = False
    try:
        w, V = _eigsh_call(op, k=nev, which="SA", tol=tol, ncv=max(3*nev, 40), maxiter=20000)
    except Exception as e:
        if not hasattr(e, "eigenvalues"):
            raise
        try:
            w, V = _eigsh_call(op, k=nev, which="SA", tol=tol, ncv=max(4*nev, 80), maxiter=60000)
        except Exception as e2:
            if not hasattr(e2, "eigenvalues"):
                raise
            w = np.atleast_1d(np.asarray(getattr(e2, "eigenvalues"), dtype=float).reshape(-1))
            V = np.asarray(getattr(e2, "eigenvectors"))
            nd = op.shape[0]
            if V.size == 0 or w.size == 0:
                w = np.array([], dtype=float)
                V = np.zeros((nd, 0), dtype=float)
            elif V.ndim == 1:
                V = V.reshape(nd, -1)
            nconv = int(min(w.size, V.shape[1]))
            w, V = w[:nconv], V[:, :nconv]
            partial = True
    return w, V, partial

def tag():
    return "[SCRATCH H5 — not a result]" if SCRATCH else ""

def wcsv(name, hdr, rows):
    p = os.path.join(OUT, name)
    with open(p, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(hdr); w.writerows(rows)
    return p

def num(x):
    try: return float(x)
    except Exception: return None

# ---------------- C1: READ-OUT of signed run-2 data (not a test) ----------------
def c1():
    rows = list(csv.DictReader(open(os.path.join(HERE, "nc_scan.csv"), encoding="utf-8")))
    base = {}
    for r in rows:
        mu, p2 = num(r["mu_matter"]), num(r["max_phi2"])
        if mu is None or p2 is None or p2 < THR["C1_normal_phi2"]: continue
        key = (r["row"], r["layout"], r["eps"], r["alpha"], r["kappa"])
        base.setdefault(key, {})[int(r["n"])] = (mu, p2)
    out = []
    for key, d in sorted(base.items()):
        k = float(key[4])
        for n, (mu, p2) in sorted(d.items()):
            if n < 2: continue
            if 1 not in d:
                out.append([n, key[4], *key[:4], mu, NCY, p2, "NOT COMPUTED (YET): no n=1 on same background"]); continue
            R = mu / (n * d[1][0])
            if k == 1.0: st = "not graded (kappa=1 BPS identity)"
            else: st = "read-out |R-1|<=tol" if abs(R-1) <= THR["C1_R_tol"] else "read-out |R-1|>tol"
            out.append([n, key[4], *key[:4], mu, R, p2, st])
    wcsv("c1_ratios.csv", ["n","kappa","row","layout","eps","alpha","mu","R","max_phi2","status"], out)
    return out

# ---------------- C2: axisymmetric 2-tip solver + Luo–Tian inequality ----------------
# metric ds^2 = ds^2 + f(s)^2 dphi^2, s in [0, L]; tips: f'(0)=alpha_N, f'(L)=-alpha_S; K = -f''/f.
def c2_profile(aN, aS, N, J):
    s = np.linspace(0, math.pi, N)
    # f = A sin s + sum_j c_j sin(j s)/j^2 ... enforce tip slopes exactly via two coefficients
    def build(c):
        A = 0.5*(aN + aS); B = 0.5*(aN - aS)
        # g(s) = sin(s)(A + B cos s): f'(0)=A+B=aN, f'(pi)=-(A-B)=-aS
        f = np.sin(s)*(A + B*np.cos(s))
        for j, cj in enumerate(c, start=2):
            f = f + cj*np.sin(s)**2*np.sin((j-1)*s)   # zero value and zero slope at both tips
        return f
    def K_of(f):
        h = s[1]-s[0]
        fpp = np.gradient(np.gradient(f, h), h)
        return -fpp/np.where(np.abs(f) > 1e-300, f, np.nan), fpp
    def obj(c):
        f = build(c)
        if np.any(f[1:-1] <= 0): return 1e6
        K, _ = K_of(f); i = slice(2, -2)
        w = f[i]; Kb = np.sum(K[i]*w)/np.sum(w)
        return float(np.sum((K[i]-Kb)**2*w)/np.sum(w))/Kb**2
    res = minimize(obj, np.zeros(J), method="Nelder-Mead" if J <= 2 else "BFGS",
                   options={"maxiter": 2000})
    f = build(res.x); K, fpp = K_of(f)
    h = s[1]-s[0]
    # Gauss–Bonnet [solver check only, not a test]: int K dA = 2pi int -f'' ds (trapezoid) + deficits = 4pi
    intK = 2*math.pi*np.trapezoid(-fpp, s)
    gb = intK + 2*math.pi*(1-aN) + 2*math.pi*(1-aS)
    return math.sqrt(max(res.fun, 0.0)), gb, 4*math.pi

def luo_tian(al):
    d = [1-a for a in al]
    ok = sum(d) < 2 and all(d[i] < sum(d)-d[i] for i in range(len(d)))
    return ok

def c2(grids, J, alphas):
    rows, gbrows = [], []
    for aN in alphas:
        for aS in alphas:
            if aS < aN: continue
            for N in grids:
                nonu, gb, ref = c2_profile(aN, aS, N, J)
                rows.append([aN, aS, N, "2-tip: football iff equal (theorem; reported)", nonu, "reported, not graded"])
                gbrows.append([aN, aS, N, gb, abs(gb-ref)/ref])
    tri = []
    for a in alphas:
        for b in alphas:
            for c in alphas:
                if a <= b <= c: tri.append([a, b, c, luo_tian([a, b, c]), "theorem-forced, reported only"])
    wcsv("c2_balance.csv", ["alpha_N","alpha_S","grid","case","||K-Kbar||/Kbar","status"], rows)
    wcsv("c2_luo_tian_3tip.csv", ["a1","a2","a3","inequality_holds","status"], tri)
    wcsv("c2_gauss_bonnet_SOLVER_CHECK.csv", ["alpha_N","alpha_S","grid","intK+sum_delta","rel_resid  [solver check only, not a test]"], gbrows)
    return rows, gbrows, tri

# ---------------- C3: conditional rows ----------------
def c3():
    rows = [["Law-GR [GR control] (alpha = 1 - 4G mu appears only here)", NCY, "needs core Einstein solve; control only"],
            ["Law-hers", NCY, "no T<->K law found in X_COPY"],
            ["Law-HP [hive proposal, untested]", NCY, "E_K, E_T from richardson_k1/ job; observed order reported there"]]
    wcsv("c3_strain.csv", ["law_row","result","note"], rows); return rows

# ---------------- Vortex on cone (shared background for C4/C5/HP2) ----------------
# metric dr^2 + alpha^2 r^2 dphi^2; phi = f(r) e^{i n phi}, A_phi = n a(r).  Convention (e=v=1), BPS at kappa=1:
# f'' + f'/r - n^2 (1-a)^2 f/(alpha^2 r^2) + (kappa/2)(1-f^2) f = 0 ;  a'' - a'/r + f^2 (1-a) = 0
def vortex_on_cone(n, kappa, alpha, R=12.0, N=200):
    r = np.linspace(1e-4, R, N)
    m = n/alpha
    def F(r, y):
        f, fp, a, ap = y
        return np.vstack([fp, -fp/r + m*m*(1-a)**2*f/r**2 - 0.5*kappa*(1-f*f)*f, ap, ap/r - f*f*(1-a)])
    def bc(y0, y1):
        return np.array([y0[0], y0[2], y1[0]-1, y1[2]-1])
    f0 = np.tanh(r)**m; a0 = np.tanh(r/2)**2
    y0 = np.vstack([f0, np.gradient(f0, r), a0, np.gradient(a0, r)])
    sol = solve_bvp(F, bc, r, y0, tol=1e-6, max_nodes=20000)
    f, fp, a, ap = sol.sol(r)
    e = 0.5*(fp**2 + m*m*(1-a)**2*f**2/r**2 + (m*ap/r)**2 + 0.25*kappa*(1-f*f)**2)
    mu = 2*math.pi*alpha*np.trapezoid(e*r, r)
    return sol.status, mu, float(np.max(np.abs(sol.rms_residuals)))

# ---------------- Polar lattice abelian-Higgs on the cone (C4, HP2, C5) ----------------
# Cone metric dr^2 + alpha^2 r^2 dphi^2, phi in [0, 2pi). Sites r_i=(i+1/2)h, i<Nr; phi_j=2pi j/Np.
# dof: Re/Im Phi at sites; theta_r links (i->i+1); theta_p links (j->j+1). Non-compact U(1), e=v=1.
# Energy density 1/2|D Phi|^2 + 1/2 B^2 + (kappa/8)(1-|Phi|^2)^2 (same convention as vortex_on_cone).
# Outer ring i=Nr is a fixed boundary Phi = e^{i n phi} (finite box: translations are only near-zero).
# The tip r=0 is not a site; the central disc carries flux sum_j theta_p(0,j) (tip excluded — disclosed).
import jax, jax.numpy as jnp
jax.config.update("jax_enable_x64", True)
from scipy.optimize import minimize as _min

class ConeLattice:
    def __init__(s, Nr, Np, R, alpha, kappa, n):
        s.Nr, s.Np, s.R, s.al, s.k, s.n = Nr, Np, R, alpha, kappa, n
        s.h = R/(Nr+0.5); s.dp = 2*math.pi/Np
        s.r = (np.arange(Nr)+0.5)*s.h
        s.rl = (np.arange(Nr)+1.0)*s.h                    # radius of radial-link midpoint / plaquette centre
        s.ns = Nr*Np; s.nr = Nr*Np; s.np_ = Nr*Np        # radial links include link to the fixed outer ring
        s.ndof = 2*s.ns + s.nr + s.np_
        ph = np.arange(Np)*s.dp
        s.bnd = np.exp(1j*n*ph)
    def unpack(s, x):
        Nr, Np = s.Nr, s.Np
        re = x[:s.ns].reshape(Nr, Np); im = x[s.ns:2*s.ns].reshape(Nr, Np)
        tr = x[2*s.ns:2*s.ns+s.nr].reshape(Nr, Np); tp = x[2*s.ns+s.nr:].reshape(Nr, Np)
        return re + 1j*im, tr, tp
    def pack(s, P, tr, tp):
        return np.concatenate([P.real.ravel(), P.imag.ravel(), tr.ravel(), tp.ravel()])
    def energy(s, x):
        P, tr, tp = s.unpack(x)
        h, dp, al = s.h, s.dp, s.al
        r = jnp.asarray(s.r)[:, None]; rl = jnp.asarray(s.rl)[:, None]
        Pout = jnp.concatenate([P[1:], jnp.asarray(s.bnd)[None, :]], 0)       # site i+1 (outer ring fixed)
        Dr = (Pout*jnp.exp(-1j*tr) - P)/h                                     # radial covariant difference
        Pj = jnp.roll(P, -1, 1)
        Dp = (Pj*jnp.exp(-1j*tp) - P)/(al*r*dp)
        Er = 0.5*jnp.sum(jnp.abs(Dr)**2*al*rl*h*dp)                           # radial link area ~ alpha r_l h dphi
        Ep = 0.5*jnp.sum(jnp.abs(Dp)**2*al*r*h*dp)
        Eu = jnp.sum(s.k/8*(1-jnp.abs(P)**2)**2*al*r*h*dp)
        # plaquettes between rings i and i+1 (i < Nr-1) and between ring Nr-1 and fixed outer ring (theta_p = n dphi there)
        tp_out = jnp.concatenate([tp[1:], jnp.full((1, s.Np), s.n*dp)], 0)
        flux = tr + tp_out - jnp.roll(tr, -1, 1) - tp
        Ap = al*rl*h*dp
        Eb = 0.5*jnp.sum(flux**2/Ap)
        disc = jnp.sum(tp[0]); Ad = 0.5*al*s.r[0]**2*2*math.pi
        Eb = Eb + 0.5*disc**2/Ad
        return Er + Ep + Eu + Eb
    def seed(s, centres):
        # product ansatz of unit vortices at cone points (rho, phi0); sum of windings must equal n
        Pg = np.ones((s.Nr, s.Np), complex)
        R2, PH = np.meshgrid(s.r, np.arange(s.Np)*s.dp, indexing="ij")
        X, Y = R2*np.cos(PH), R2*np.sin(PH)
        tp = np.zeros((s.Nr, s.Np))
        for (rho, p0, w) in centres:
            dx, dy = X-rho*np.cos(p0), Y-rho*np.sin(p0)
            d = np.hypot(dx, dy); Pg *= (np.tanh(d)*np.exp(1j*np.arctan2(dy, dx)))**w
        # link phases from the scalar phase so D Phi ~ 0 far out
        ph = np.angle(Pg)
        tp = np.angle(np.exp(1j*(np.roll(ph, -1, 1) - ph)))*np.tanh(R2/2)**2
        return s.pack(Pg, np.zeros((s.Nr, s.Np)), tp)
    def sep_moment(s, x):
        P, _, _ = s.unpack(x)
        r = jnp.asarray(s.r)[:, None]; ph = jnp.asarray(np.arange(s.Np)*s.dp)[None, :]
        return jnp.sum((1-jnp.abs(P)**2)*r**2*jnp.cos(2*ph)*s.al*r*s.h*s.dp)
    def relax(s, x0, iters, efun=None):
        efun = efun or s.energy
        E = jax.jit(efun); G = jax.jit(jax.grad(efun))
        r = _min(lambda x: float(E(x)), x0, jac=lambda x: np.asarray(G(x)), method="L-BFGS-B",
                 options={"maxiter": iters, "gtol": 1e-13, "ftol": 1e-22, "maxcor": 30})
        return r.x, float(r.fun), float(np.max(np.abs(G(r.x)))), r.nit
    def polish(s, x, steps=None):
        # Venus ruling 1: Newton-Krylov polish to stationarity. Solve (H + xi G G^T) dx = -g by MINRES (g is gauge-orthogonal
        # by gauge invariance, so the penalty only regularises gauge directions); accept a step only if |g|_2 drops.
        from scipy.sparse.linalg import LinearOperator, minres
        steps = steps or THR["POLISH_STEPS"]
        gfun = jax.jit(jax.grad(s.energy)); hist = []
        for _ in range(steps):
            g = np.asarray(gfun(x)); gn = float(np.linalg.norm(g)); hist.append(gn)
            if gn <= THR["GRAD_TARGET"]: break
            Gs = s.gauge_sparse(x); GT = Gs.T.tocsr(); xj = jnp.asarray(x)
            hvp = jax.jit(lambda v: jax.jvp(jax.grad(s.energy), (xj,), (v,))[1])
            from scipy.sparse.linalg import eigsh
            gmin = float(eigsh((GT @ Gs).tocsc(), k=1, sigma=0, which="LM", return_eigenvectors=False)[0])
            xi = THR["XI_FACTOR"]/gmin
            op = LinearOperator((s.ndof, s.ndof), dtype=float, matvec=lambda v: np.asarray(hvp(jnp.asarray(np.ravel(v)))) + xi*(Gs @ (GT @ np.ravel(v))))
            dx, _ = minres(op, -g, rtol=1e-12, maxiter=4000)
            t = 1.0; acc = False
            while t > 1e-3:
                gn2 = float(np.linalg.norm(np.asarray(gfun(x + t*dx))))
                if gn2 < gn: x = x + t*dx; acc = True; break
                t *= 0.5
            if not acc: break
        g = np.asarray(gfun(x))
        return x, float(np.linalg.norm(g)), float(np.max(np.abs(g))), hist
    def gauge_basis(s, x):
        # generator of local gauge transforms eps_s: dPhi = i eps Phi; dtheta_link = eps_end - eps_start
        P, tr, tp = s.unpack(x); ns = s.ns
        Gm = np.zeros((s.ndof, ns))
        idx = np.arange(ns).reshape(s.Nr, s.Np)
        for i in range(s.Nr):
            for j in range(s.Np):
                q = idx[i, j]
                Gm[q, q] = -P[i, j].imag; Gm[ns+q, q] = P[i, j].real
                Gm[2*ns+q, q] -= 1.0                                    # radial link starting here
                if i > 0: Gm[2*ns+idx[i-1, j], q] += 1.0               # radial link ending here
                Gm[2*ns+ns+q, q] -= 1.0                                 # phi link starting here
                Gm[2*ns+ns+idx[i, (j-1) % s.Np], q] += 1.0              # phi link ending here
        return Gm
    def gauge_sparse(s, x):
        # sparse local gauge generator (ndof x nsites), same entries as gauge_basis
        import scipy.sparse as sps
        P, _, _ = s.unpack(x); ns = s.ns; Nr, Np = s.Nr, s.Np
        idx = np.arange(ns).reshape(Nr, Np); q = idx.ravel()
        ii, jj = np.meshgrid(np.arange(Nr), np.arange(Np), indexing="ij"); ii, jj = ii.ravel(), jj.ravel()
        m = ii > 0
        rows = [q, ns+q, 2*ns+q, 3*ns+q, 2*ns+idx[ii[m]-1, jj[m]], 3*ns+idx[ii, (jj-1) % Np]]
        cols = [q, q, q, q, q[m], q]
        vals = [-P.imag.ravel(), P.real.ravel(), -np.ones(ns), -np.ones(ns), np.ones(m.sum()), np.ones(ns)]
        return sps.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(s.ndof, ns))
    def spectrum(s, x, nev):
        # Lanczos (ARPACK eigsh 'SA') on jax Hessian-vector products + background-gauge penalty xi*G G^T.
        # xi = XI_FACTOR / lambda_min(G^T G): every pure-gauge direction is lifted to >= XI_FACTOR [assumed].
        from scipy.sparse.linalg import LinearOperator, eigsh
        G = s.gauge_sparse(x); GT = G.T.tocsr()
        gfun = jax.grad(s.energy); xj = jnp.asarray(x)
        hvp = jax.jit(lambda v: jax.jvp(gfun, (xj,), (v,))[1])
        GtG = (GT @ G).tocsc()
        gmin = float(_eigsh_call(GtG, k=1, sigma=0, which="LM", return_eigenvectors=False)[0])
        xi = THR["XI_FACTOR"]/max(gmin, 1e-12)
        op = LinearOperator((s.ndof, s.ndof), dtype=float,
                            matvec=lambda v: np.asarray(hvp(jnp.asarray(np.ravel(v)))) + xi*(G @ (GT @ np.ravel(v))))
        w, V, partial = _lanczos_sa(op, nev, THR["LANCZOS_TOL"])
        s.spectrum_partial = partial
        s.spectrum_tag = "report-only (Lanczos did not fully converge; kept subset)" if partial else None
        if w.size:
            o = np.argsort(w); w, V = w[o], V[:, o]
            s.gauge_leak = float(np.max(np.linalg.norm(GT @ V, axis=0)))
        else:
            s.gauge_leak = float("nan")
        return w, V, xi
    def gauge_sector(s, x, xi_code, ng=5):
        # [hive proposal, untested] REPORT-ONLY: mu = lambda_gauge/xi on pure-gauge directions v = G eps (Rayleigh quotients)
        from scipy.sparse.linalg import eigsh
        G = s.gauge_sparse(x); GT = G.T.tocsr()
        mu, eps = eigsh((GT @ G).tocsc(), k=ng, sigma=0, which="LM"); o = np.argsort(mu); mu, eps = mu[o], eps[:, o]
        gfun = jax.grad(s.energy); xj = jnp.asarray(x)
        hvp = jax.jit(lambda v: jax.jvp(gfun, (xj,), (v,))[1])
        eff = {}
        for lab, xi in (("1", 1.0), ("5/lmin", 5.0/mu[0]), ("10/lmin", 10.0/mu[0])):
            r = []
            for j in range(ng):
                v = G @ eps[:, j]; v = v/np.linalg.norm(v)
                r.append(float(v @ (np.asarray(hvp(jnp.asarray(v))) + xi*(G @ (GT @ v))))/xi)
            eff[lab] = r
        mixing = any(max(abs(eff[p][j]-eff[q][j]) for p in eff for q in eff)/mu[j] > THR["GAUGE_MIX_REL"] for j in range(ng))
        return float(mu[0]), eff, mixing
    def classify(s, x, v):
        P, _, _ = s.unpack(x); dP, _, _ = s.unpack(v)
        drho = 2*np.real(np.conj(P)*dP)                                 # gauge-invariant delta|Phi|^2
        c = np.abs(np.fft.fft(drho, axis=1)).sum(0)
        l = int(np.argmax(c[:s.Np//2+1]))
        return "scale-like (l=0)" if l == 0 else f"position-like (l={l})"

def known_zero_count(n, k):
    # alpha = 1 control: kappa = 1 -> 2n position moduli [standard: Weinberg 1979]; kappa != 1 -> 2 translations
    return 2*n if k == 1.0 else 2

def reach(L, x, target):
    # one gradient cut: L-BFGS stopped as soon as |grad|_2 <= target (so cuts come in ~decades); Newton polish only if L-BFGS stalls
    E = jax.jit(L.energy); Gf = jax.jit(jax.grad(L.energy)); best = {"x": x}
    def cb(xk):
        best["x"] = xk
        if float(np.linalg.norm(np.asarray(Gf(xk)))) <= target: raise StopIteration
    try:
        _min(lambda z: float(E(z)), x, jac=lambda z: np.asarray(Gf(z)), method="L-BFGS-B", callback=cb,
             options={"maxiter": 20000, "gtol": 1e-14, "ftol": 1e-22, "maxcor": 30})
    except StopIteration:
        pass
    x = best["x"]; g2 = float(np.linalg.norm(np.asarray(Gf(x))))
    if g2 > target:
        keep = THR["GRAD_TARGET"]; THR["GRAD_TARGET"] = target
        x, g2, gmax, hist = L.polish(x, steps=1); THR["GRAD_TARGET"] = keep
    return x, g2

def control_stop(L, x, K, nev):
    # Venus/NanoRibbon rule: relax the alpha=1 control until a >=10x cut in |grad|_2 changes the largest of its K zero
    # modes by < 2x; only then freeze tau0. Returns (x, w, V, xi, steps[(g2, zmax)], converged).
    steps = []; g2 = float(np.linalg.norm(np.asarray(jax.grad(L.energy)(x))))
    target = g2
    while True:
        w, V, xi = L.spectrum(x, nev)
        if w.size == 0:
            steps.append((g2, float("nan")))
            return x, w, V, xi, steps, "stopped at Lanczos non-convergence"
        z = float(sorted(np.abs(w))[min(K, w.size)-1]); steps.append((g2, z))
        if len(steps) >= 2:
            (ga, za), (gb, zb) = steps[-2], steps[-1]
            if ga/gb >= 10.0 and max(za/zb, zb/za) < 2.0:
                return x, w, V, xi, steps, "stopped (10x grad cut, zmax change < 2x)"
        if g2 < THR["GRAD_FLOOR"]:
            return x, w, V, xi, steps, "stopped at solver floor"
        target = g2/10.0
        x, g2n = reach(L, x, target)
        if g2n >= g2:          # no further progress: this |grad|_2 is the solver floor (Helios: rule always ends)
            return x, w, V, xi, steps, "stopped at solver floor"
        g2 = g2n

def track(L, x, nev):
    # alpha<1: relax by 10x gradient cuts to the solver floor (no spectra on the way), then ONE spectrum
    g2 = float(np.linalg.norm(np.asarray(jax.grad(L.energy)(x))))
    while g2 >= THR["GRAD_FLOOR"]:
        x, g2n = reach(L, x, g2/10.0)
        if g2n >= g2: break
        g2 = g2n
    w, V, xi = L.spectrum(x, nev)
    return x, w, V, xi

def _order(Ns, z):
    # least-squares observed order of fall: slope of -log z vs log N over all grids
    lx = np.log(np.asarray(Ns, float)); ly = -np.log(np.asarray(z, float))
    return float(np.polyfit(lx, ly, 1)[0])

def fall_test(grids, zc, za, cnt):
    # rev 16 ruling (replaces gradient-cut test): fall over grid refinement on the run's own grids, tau0 per grid from that
    # grid's own alpha=1 control. Mode i passes iff fitted order p_i >= RATE_LOG_FRAC * p_c (p_c = control's fitted order on
    # the same grids) AND total fall |lam|_first/|lam|_last >= RATE_MIN_FALL over the whole span (not per step).
    # Control zero mode within FLOOR_NEAR x ZERO_FLOOR on any grid => undecided. Returns (status, lifted, p_c).
    Ns = [g[0] for g in grids]
    pc = _order(Ns, [zc[g] for g in grids])
    if len(grids) < 3: return "undecided (fewer than three grids)", [], pc
    if min(zc[g] for g in grids) <= THR["FLOOR_NEAR"]*THR["ZERO_FLOOR"]:
        return "undecided (control zero mode within %gx of solver floor %.0e)" % (THR["FLOOR_NEAR"], THR["ZERO_FLOOR"]), [], pc
    lifted = []
    for i in range(cnt):
        z = [za[g][i] for g in grids]; pi = _order(Ns, z); F = z[0]/z[-1]
        if not (pi >= THR["RATE_LOG_FRAC"]*pc and F >= THR["RATE_MIN_FALL"]):
            lifted.append((i, pi, F, pc))
    return ("undecided (candidate lifted modes: %s)" % ";".join(f"#{i} order {a:.3g} vs control {c:.3g}, total fall {b:.3g}" for i, a, b, c in lifted)
            if lifted else "count (grid-refinement fall test passed)"), lifted, pc

def _c4_group(args):
    (n, k), alphas, grids, R, nev, iters = args
    al = None
    try:
        return _c4_group_body(n, k, alphas, grids, R, nev, iters)
    except RuntimeError:
        raise
    except Exception as e:
        _worker_fail(n, k, al, e)

def _c4_group_body(n, k, alphas, grids, R, nev, iters):
    rows = []; ctrl = []; global LIFTED; LIFTED = []
    K = known_zero_count(n, k); zc = {}; za = {}; pend = {}
    for (Nr, Np) in grids:
        tau0, tau_status, floor = None, NCY, None
        for al in sorted(alphas, reverse=True):          # alpha = 1 control first: tau0 fixed before alpha < 1
            try:
                t0 = time.perf_counter()
                L = ConeLattice(Nr, Np, R, al, k, n)
                x, E, gm, it = L.relax(L.seed([(0.0, 0.0, n)]), iters)
                _log_solve(n, k, al, extra=f" Nr={Nr} Np={Np}")
                if al == 1.0:
                    x, w, V, xi, steps, conv = control_stop(L, x, K, nev); csteps = steps
                    zmax = steps[-1][1]
                    t = THR["TAU0_FACTOR"]*zmax
                    repro = int(np.sum(np.abs(w) <= t)) == K and not any(t/THR["UNDECIDED_BAND"] <= abs(v) <= t*THR["UNDECIDED_BAND"] for v in w)
                    floor = steps[-1][0] if conv == "stopped at solver floor" else None
                    if repro:
                        zc[(Nr, Np)] = zmax          # rev 17: only a control that reproduces K feeds p_c / the fall test
                        tau0, tau_status = t, "frozen; " + conv + (" [floor-limited]" if floor is not None else "")
                    else:
                        tau0, tau_status, floor = None, NCY + " (control does not reproduce its known count %d; %s)" % (K, conv)
                    ctrl.append([n, k, Nr, Np, K, ";".join(f"{a:.2e}/{b:.3e}" for a, b in steps), conv, repro, tau0 if tau0 else tau_status,
                                 steps[-1][0] if conv == "stopped at solver floor" else "not reached"])
                else:
                    x, w, V, xi = track(L, x, nev)
                g2 = float(np.linalg.norm(np.asarray(jax.grad(L.energy)(x))))
                E = float(L.energy(x))
                if tau0 is not None:
                    cnt = int(np.sum(np.abs(w) <= tau0))
                    und = any(tau0/THR["UNDECIDED_BAND"] <= abs(v) <= tau0*THR["UNDECIDED_BAND"] for v in w)
                    cnt_ok = g2 <= tau0/THR["STAT_FACTOR"]
                    cstat = "undecided (eigenvalue within 3x of tau0)" if und else ("count" if cnt_ok else "report-only (grad > tau0/10)")
                    if cstat == "count" and al == 1.0:
                        cstat = "control (known count %d reproduced)" % K
                    elif cstat == "count":
                        if (Nr, Np) == grids[-1]: cstat = "count pending grid-refinement fall test"; pend[al] = cnt
                        else: cstat = "count on this grid (fall test applied on finest grid only)"
                    if floor is not None: cstat += " [floor-limited, floor |grad|2=%.2e]" % floor
                else:
                    cnt, cstat = NCY, "report-only (tau0 " + tau_status + ")"
                mu0, eff, mix = L.gauge_sector(x, xi)
                gsec = [mu0, eff["1"][0], eff["5/lmin"][0], eff["10/lmin"][0], "MIXING" if mix else "ok"]
                dt = time.perf_counter()-t0
                if al != 1.0: za.setdefault(al, {})[(Nr, Np)] = sorted(np.abs(w)) if w.size else []
                partial = getattr(L, "spectrum_partial", False)
                ptag = getattr(L, "spectrum_tag", None)
                n_write = max(len(w), nev)
                for m in range(n_write):
                    if m < len(w):
                        lv = w[m]
                        typ = L.classify(x, V[:, m]) + (" [hive proposal, untested]" if (al < 1.0 and lv < 0) else "")
                        near = tau0 is not None and abs(lv) <= tau0
                        need = (tau0/THR["STAT_FACTOR"]) if near else abs(lv)/THR["STAT_FACTOR"]
                        stn = "row ok" if g2 <= need else "report-only (grad > %s/10)" % ("tau0" if near else "|lambda|")
                        if partial: stn = ptag if stn == "row ok" else (stn + "; " + ptag)
                        rows.append([n, k, al, Nr, Np, m, lv, (lv/tau0 if tau0 else NCY), typ, E, g2, it, xi, L.gauge_leak,
                                     stn, tau0 if tau0 else tau_status, cnt, cstat, dt] + gsec)
                    else:
                        rows.append([n, k, al, Nr, Np, m, NCY, NCY, NCY, E, g2, it, xi, getattr(L, "gauge_leak", NCY),
                                     "report-only (Lanczos subset; mode not converged)",
                                     tau0 if tau0 else tau_status, cnt, cstat, dt] + gsec)
            except RuntimeError:
                raise
            except Exception as e:
                _worker_fail(n, k, al, e)
    # grid-refinement fall test, applied after all grids; status overwrites the pending finest-grid count status
    fin = grids[-1]; FT = []
    for al in sorted(a for a in alphas if a != 1.0):
        have = all(g in zc for g in grids) and all(g in za.get(al, {}) for g in grids)
        if al in pend and have:
            try:
                st, lf, pc = fall_test(grids, zc, za[al], pend[al])
            except Exception as e:
                st, lf, pc = "not applied (Lanczos subset too short for fall test: %s)" % e, [], float("nan")
        else:
            st, lf, pc = "not applied (finest-grid status not 'count' or a grid's control tau0 missing)", [], (
                _order([g[0] for g in grids], [zc[g] for g in grids]) if all(g in zc for g in grids) else float("nan"))
        for r in rows:
            if r[2] == al and (r[3], r[4]) == fin and str(r[17]).startswith("count pending"):
                r[17] = st + str(r[17])[len("count pending grid-refinement fall test"):]
        LIFTED.extend([[n, k, al, i, a, fi, fc] for i, a, fi, fc in lf])
        FT.append([n, k, al, ";".join(f"{g[0]}" for g in grids), ";".join(f"{zc.get(g, float('nan')):.4e}" for g in grids),
                   f"{pc:.3f}", pend.get(al, NCY), st])
    return rows, ctrl, LIFTED, FT

def pmap(fn, items):
    if WORKERS <= 1:
        return [fn(i) for i in items]
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=WORKERS) as ex:
        return list(ex.map(fn, items))      # order preserved

def guard(scr):
    # rev 10 GUARD (runs before anything is graded): grid 48 (scratch 16), penalties 5 and 10 /lambda_min must give the same
    # near-zero count and the same 24-mode window at 4 s.f. Fail => C4/HP2 count rows report-only.
    Ng = 16 if scr else 48; nev = 12 if scr else 24; ok = True; rows = []
    for (n, k, al) in [(1, 2.0, 0.75), (2, 1.0, 0.5)]:
        L = ConeLattice(Ng, Ng, 6.0 if scr else 10.0, al, k, n)
        x, E, g, it = L.relax(L.seed([(0.0, 0.0, n)]), 300 if scr else 5000)
        res = {}
        for f in (5.0, 10.0):
            keep = THR["XI_FACTOR"]; THR["XI_FACTOR"] = f
            w, V, xi = L.spectrum(x, nev); THR["XI_FACTOR"] = keep
            gap = next((lv for lv in w if abs(lv) > THR["C4_gap_split"]*max(abs(w[0]), 1e-300)), float("nan"))
            res[f] = (w, int(np.sum(np.abs(w) < gap)))
        same = res[5.0][1] == res[10.0][1] and all(f"{a:.3e}" == f"{b:.3e}" for a, b in zip(res[5.0][0], res[10.0][0]))
        ok &= same; rows.append([n, k, al, Ng, res[5.0][1], res[10.0][1], same])
    wcsv("guard_5v10.csv", ["n","kappa","alpha","grid","nz_count_5","nz_count_10","pass"], rows)
    return ok

def c4_hp2(scr):
    T0 = time.perf_counter()
    grids = [(12, 12), (16, 16), (20, 20)] if scr else [(48, 48), (64, 64), (80, 80), (96, 96)]   # Lanczos on HVPs
    R = 6.0 if scr else 10.0
    nev = 12 if scr else 24
    cases = [(1, 2.0, 0.75)] if scr else [(n, k, a) for n in (1, 2) for k in (0.5, 1.0, 2.0) for a in (0.5, 0.75, 0.9, 1.0)]
    groups = sorted({(c[0], c[1]) for c in cases})
    res = pmap(_c4_group, [((n, k), sorted({c[2] for c in cases if (c[0], c[1]) == (n, k)} | {1.0}), grids, R, nev, 300 if scr else 5000) for (n, k) in groups])
    rows = [r for rr, _, _, _ in res for r in rr]; ctrl = [c for _, cc, _, _ in res for c in cc]
    wcsv("c4_candidate_lifted_modes.csv", ["n","kappa","alpha","mode_index","fitted_order","total_fall_first_to_last_grid","control_fitted_order_p_c"], [l for _, _, ll, _ in res for l in ll])
    wcsv("c4_grid_fall_test.csv", ["n","kappa","alpha","grids","control_zmax_per_grid","control_fitted_order_p_c","count_finest_grid","status"], [f for _, _, _, ff in res for f in ff])
    wcsv("c4_control_stop.csv", ["n","kappa","Nr","Nphi","K_known","steps |grad|2/zmax","stop_reason","reproduces_K","tau0","solver_floor_grad2"], ctrl)
    ref = {(r[0], r[1], r[3]): r[19] for r in rows if r[2] == 1.0}
    for r in rows:
        r.append("report-only: " + str(r[19]/ref[(r[0], r[1], r[3])]) if (r[0], r[1], r[3]) in ref else NCY + " (no alpha=1 on same grid)")
    T = time.perf_counter()-T0
    wcsv("c4_modes.csv", ["n","kappa","alpha","Nr","Nphi","mode","lambda","lambda/tau0","type","E","grad2","iters","xi_gauge_penalty","gauge_leak","row_stationarity","tau0","count(|lam|<=tau0)","count_status","case_seconds",
                          "GAUGE-SECTOR [hive proposal, untested; report-only, never in count] mu_min(G^T G)","mu_eff xi=1","mu_eff xi=5/lmin","mu_eff xi=10/lmin","mixing_flag","mu_min/mu_min(alpha=1)"], rows)
    return rows, T

def _hp2_series(args):
    n, k, alphas, Nr, Np, R, iters, nev = args
    al = None
    try:
        return _hp2_series_body(n, k, alphas, Nr, Np, R, iters, nev)
    except RuntimeError:
        raise
    except Exception as e:
        _worker_fail(n, k, al, e)

def _hp2_series_body(n, k, alphas, Nr, Np, R, iters, nev):
    prev = None; rows = []
    for al in alphas:
        try:
            L = ConeLattice(Nr, Np, R, al, k, n)
            x, E, g, it = L.relax(L.seed([(0.0, 0.0, n)] if n else []), iters)
            x, g2 = reach(L, x, THR["GRAD_TARGET"])
            w, V, _ = L.spectrum(x, nev)
            _log_solve(n, k, al, extra=f" Nr={Nr} Np={Np}")
            nconv = len(w)
            if prev is not None and nconv and prev.shape[1] and V.shape[1]:
                nc = min(prev.shape[1], V.shape[1])
                ov = np.full(max(nconv, nev), np.nan)
                ov[:nc] = np.max(np.abs(prev[:, :nc].T @ V[:, :nc]), 0)
            else:
                ov = np.full(max(nconv, nev), np.nan)
            partial = getattr(L, "spectrum_partial", False)
            ptag = getattr(L, "spectrum_tag", None)
            n_write = max(nconv, nev)
            for m in range(n_write):
                if m < nconv:
                    stn = "row ok" if g2 <= abs(w[m])/THR["STAT_FACTOR"] else "report-only (grad > |lambda|/10)"
                    if partial: stn = ptag if stn == "row ok" else (stn + "; " + ptag)
                    rows.append([n, k, al, m, w[m], ov[m], "track" if (ov[m] >= THR["HP2_overlap"]) else "no-track/first", g2, stn])
                else:
                    rows.append([n, k, al, m, NCY, NCY, "no-track/first", g2,
                                 "report-only (Lanczos subset; mode not converged)"])
            prev = V if nconv else prev
        except RuntimeError:
            raise
        except Exception as e:
            _worker_fail(n, k, al, e)
    return rows

def hp2(scr):
    T0 = time.perf_counter()
    alphas = list(np.linspace(1.0, 0.5, 3 if scr else 26))
    Nr, Np = (12, 12) if scr else (64, 64)
    ser = [(n, k) for n in ((1,) if scr else (0, 1, 2)) for k in ((1.0,) if scr else (0.5, 1.0, 2.0))]
    rows = [r for rr in pmap(_hp2_series, [(n, k, alphas, Nr, Np, 6.0 if scr else 10.0, 300 if scr else 5000, 8 if scr else 20) for (n, k) in ser]) for r in rr]
    wcsv("hp4_richardson.csv", ["[hive proposal, untested] HP4","status"], [["dmu/dalpha vs 10 x Richardson error", NCY + " (error estimate from richardson_k1/)"]])
    wcsv("hp2_flow.csv", ["n","kappa","alpha","level","lambda","max_overlap_prev","tracking  [hive proposal, untested]","grad2","row_stationarity"], rows)
    return rows, time.perf_counter()-T0

def c5(scr):
    # n = 2 at kappa = 1, configurations symmetric about the tip: vortices at (d/2, 0) and (d/2, pi) in cone coords.
    # F(d) = |P_perp dX/dd|^2 (gauge-orthogonal tangent norm); h(d) = |P_perp dX/dTheta|^2 for a rigid phi-rotation.
    # Inherited conical angle near d->0: A = Theta_period * d sqrt(h)/ds, Theta_period = pi (identical vortices).
    T0 = time.perf_counter()
    Nr, Np = (14, 16) if scr else (64, 64)
    ds_ = [0.6, 1.0, 1.4] if scr else list(np.round(np.arange(0.2, 6.01, 0.2), 3))
    alphas = [0.75] if scr else [0.5, 0.75, 1.0]
    rows = []
    for al in alphas:
        L = ConeLattice(Nr, Np, 6.0 if scr else 10.0, al, 1.0, 2)
        def config(d):
            # separation constraint: quadratic penalty pinning M(x) = sum (1-|Phi|^2) r^2 cos(2phi) dA to the seed's value
            x0 = L.seed([(d/2, 0.0, 1), (d/2, math.pi, 1)])
            Mt = float(L.sep_moment(x0))
            Ef = lambda x: L.energy(x) + THR["C5_penalty"]*(L.sep_moment(x) - Mt)**2
            x, E, g, it = L.relax(x0, 2000 if scr else 3000, Ef)
            return x, float(L.energy(x)), g
        dd = 0.05
        for d in ds_:
            xp, _, _ = config(d+dd); xm, E, g = config(d-dd); x0 = 0.5*(xp+xm)
            Gm = L.gauge_basis(x0); U, sv, _ = np.linalg.svd(Gm, full_matrices=False)
            Ug = U[:, sv > 1e-10*sv[0]]
            t = (xp-xm)/(2*dd); t = t - Ug @ (Ug.T @ t)
            P, tr, tp = L.unpack(x0)
            rot = lambda Z: (np.roll(Z, -1, 1) - np.roll(Z, 1, 1))/(2*L.dp)
            tq = L.pack(rot(P), rot(tr), rot(tp)); tq = tq - Ug @ (Ug.T @ tq)
            F = float(t @ t)*L.al*L.h*L.dp; Hh = float(tq @ tq)*L.al*L.h*L.dp   # crude dof-measure [assumed]
            rows.append([2, al, d, F, Hh, E, g])
    # inherited angle estimate from the two smallest d: A ~ pi * (sqrt(h2)-sqrt(h1)) / (s2-s1)
    out = []
    for al in alphas:
        rr = [x for x in rows if x[1] == al]
        s = np.concatenate([[0.0], np.cumsum([math.sqrt(max(rr[i][3], 0))*(rr[i+1][2]-rr[i][2]) for i in range(len(rr)-1)])])
        A = math.pi*(math.sqrt(rr[1][4])-math.sqrt(rr[0][4]))/(s[1]-s[0]) if len(rr) > 1 and s[1] > s[0] else float("nan")
        for i, x in enumerate(rr):
            out.append(x + [s[i], A, "graded row (n=2, alpha<1; threshold PENDING FINAL HASH)" if al < 1 else "alpha=1 reported only"])
    wcsv("c5_moduli.csv", ["n","alpha","d_sep","F(d)","h(d)","E","max_grad","geodesic_s","inherited_angle_est","status"], out)
    return out, time.perf_counter()-T0

def c7():
    import sympy as sp
    t, a, b = sp.symbols("theta a b", positive=True)
    r = a*sp.exp(b*t); dr = sp.diff(r, t); d2 = sp.diff(r, t, 2)
    kc = sp.simplify((r**2 + 2*dr**2 - r*d2)/(r**2+dr**2)**sp.Rational(3, 2))
    grok = -b**2/(r**2*(1+b**2))
    diff = sp.simplify(grok + b**2*kc**2)
    with open(os.path.join(OUT, "c7_spiral.md"), "w", encoding="utf-8") as fh:
        fh.write(f"kappa_c = {kc}\nGrok K + b^2 kappa_c^2 = {diff}\nRECORDED (Venus V6): G6 FAIL as stated; not run as a test.\n")
    return str(kc), str(diff)

def _test_eigsh_fail():
    """Forced ArpackNoConvergence: first call fails, retry succeeds; then both fail and subset is kept."""
    from scipy.sparse.linalg import LinearOperator, eigsh as real_eigsh
    try:
        from scipy.sparse.linalg import ArpackNoConvergence
    except ImportError:
        from scipy.sparse.linalg._eigen.arpack import ArpackNoConvergence
    n = 24; nev = 4
    rng = np.random.default_rng(0)
    A = rng.normal(size=(n, n)); A = (A + A.T) / 2
    op = LinearOperator((n, n), matvec=lambda v: A @ np.ravel(v), dtype=float)
    global _EIGSH
    calls = {"n": 0}

    def fail_then_ok(*a, **k):
        calls["n"] += 1
        if calls["n"] == 1:
            raise ArpackNoConvergence("forced first fail", np.array([]), np.zeros((n, 0)))
        return real_eigsh(*a, **k)

    _EIGSH = fail_then_ok
    w, V, partial = _lanczos_sa(op, nev, 1e-8)
    assert not partial and w.size == nev, (partial, w.size)
    print("test-eigsh-fail retry-ok: PASS", flush=True)

    def fail_twice(*a, **k):
        w0, V0 = real_eigsh(op, k=2, which="SA")
        raise ArpackNoConvergence("forced both fail", w0, V0)

    _EIGSH = fail_twice
    w, V, partial = _lanczos_sa(op, nev, 1e-8)
    assert partial and 0 < w.size <= nev, (partial, w.size)
    print("test-eigsh-fail keep-subset: PASS nconv=%d tagged report-only" % w.size, flush=True)
    _EIGSH = None
    import pickle
    try:
        _worker_fail(1, 1.0, 0.5, ValueError("boom"))
    except RuntimeError as e:
        pickle.loads(pickle.dumps(e))
        assert "n=1" in str(e) and "kappa=1.0" in str(e) and "alpha=0.5" in str(e), str(e)
        print("test-worker-fail pickle: PASS", flush=True)
    return 0

def main():
    spec = os.path.join(HERE, "spec", "CONE_SIM_SPECS.md")
    h = hashlib.sha256(open(spec, "rb").read()).hexdigest()[:8].upper() if os.path.exists(spec) else "MISSING"
    if "--test-eigsh-fail" in sys.argv:
        print(tag(), f"spec hash file={h} built_against={SPEC_HASH_BUILT}")
        sys.exit(_test_eigsh_fail())
    if not SCRATCH and "--full" not in sys.argv:
        print("REFUSED: pass --smoke (scratch) or --full (graded, needs NanoRibbon go)."); sys.exit(2)
    if not SCRATCH:
        if FINAL_SPEC_HASH is None or h != FINAL_SPEC_HASH:
            print(f"REFUSED: graded run needs FINAL_SPEC_HASH (now {FINAL_SPEC_HASH}); spec file hash {h}."); sys.exit(2)
    tracemalloc.start(); T = {}
    if STAGE == "HP2":
        print(tag(), f"stage=HP2 spec hash file={h} built_against={SPEC_HASH_BUILT} (C1–C4 reused, not rewritten)")
        rh, T["HP2"] = hp2(SCRATCH)
        peak = tracemalloc.get_traced_memory()[1]/2**20
        for x in rh: print(tag(), f"HP2 [hive proposal, untested] n={x[0]} kappa={x[1]} alpha={x[2]:.3f} level={x[3]} lam={x[4]} overlap={x[5]}")
        print(tag(), "timings_s=" + json.dumps({k: round(v, 3) for k, v in T.items()}), f"peak_py_MiB={peak:.1f}")
        json.dump({"timings_s": T, "peak_py_MiB": peak, "scratch": SCRATCH, "stage": STAGE}, open(os.path.join(OUT, "timing.json"), "w"))
        return
    t0 = time.perf_counter(); r1 = c1(); T["C1"] = time.perf_counter()-t0
    grids = [41, 81, 161] if SCRATCH else [201, 401, 801, 1601]
    alphas = [0.5, 0.9] if SCRATCH else [0.5, 0.6, 0.7, 0.8, 0.9, 0.95]
    t0 = time.perf_counter(); r2, gb, tri = c2(grids, 2 if SCRATCH else 4, alphas); T["C2"] = time.perf_counter()-t0
    c3()
    cases = [(1, 1.0, 1.0), (1, 1.0, 0.5)] if SCRATCH else [(n, k, a) for n in (1, 2) for k in (0.5, 1.0, 2.0) for a in (0.5, 0.75, 0.9, 1.0)]
    t0 = time.perf_counter(); vb = [[n, k, a, *vortex_on_cone(n, k, a)] for (n, k, a) in cases]; T["vortex"] = time.perf_counter()-t0
    wcsv("vortex_background.csv", ["n","kappa","alpha","bvp_status","mu","max_rms_resid"], vb)
    t0 = time.perf_counter(); GUARD_OK = guard(SCRATCH); T["guard"] = time.perf_counter()-t0
    print(tag(), "GUARD 5v10:", "PASS" if GUARD_OK else "FAIL => C4/HP2 count rows report-only")
    r4, T["C4"] = c4_hp2(SCRATCH)
    rh, T["HP2"] = hp2(SCRATCH)
    r5, T["C5"] = c5(SCRATCH)
    t0 = time.perf_counter(); kc, d7 = c7(); T["C7"] = time.perf_counter()-t0
    peak = tracemalloc.get_traced_memory()[1]/2**20
    print(tag(), f"spec hash file={h} built_against={SPEC_HASH_BUILT} venus_diff={VENUS_DIFF_HASH}")
    print(tag(), f"C1 read-out rows={len(r1)}  graded=0 (read-out)")
    for g in gb: print(tag(), f"GB [solver check only, not a test] aN={g[0]} aS={g[1]} N={g[2]} rel={g[4]:.3e}")
    for x in r2: print(tag(), f"C2 aN={x[0]} aS={x[1]} N={x[2]} ||K-Kbar||/Kbar={x[4]:.3e} (reported)")
    print(tag(), f"C2 3-tip Luo–Tian rows={len(tri)} holds={sum(1 for t in tri if t[3])}")
    for v in vb: print(tag(), f"vortex n={v[0]} kappa={v[1]} alpha={v[2]} status={v[3]} mu={v[4]:.6f} mu/(pi n)={v[4]/(math.pi*v[0]):.6f} resid={v[5]:.2e}")
    for x in r4: print(tag(), f"C4 n={x[0]} kappa={x[1]} alpha={x[2]} grid={x[3]}x{x[4]} mode={x[5]} lam={x[6]:.4e} {x[8]} grad2={x[10]:.1e} {x[14]} tau0={x[15]} count={x[16]} {x[17]} t={x[18]:.1f}s")
    for x in rh: print(tag(), f"HP2 [hive proposal, untested] n={x[0]} kappa={x[1]} alpha={x[2]:.3f} level={x[3]} lam={x[4]:.4e} overlap={x[5]:.3f}")
    for x in r5: print(tag(), f"C5 n={x[0]} alpha={x[1]} d={x[2]} F={x[3]:.4e} h={x[4]:.4e} s={x[7]:.3f} angle_est={x[8]:.4f} E={x[5]:.4f}")
    print(tag(), f"C7 kappa_c={kc}; Grok K + b^2 kappa_c^2 = {d7}")
    print(tag(), "timings_s=" + json.dumps({k: round(v, 3) for k, v in T.items()}), f"peak_py_MiB={peak:.1f}")
    json.dump({"timings_s": T, "peak_py_MiB": peak, "scratch": SCRATCH}, open(os.path.join(OUT, "timing.json"), "w"))

if __name__ == "__main__":
    main()
