# ============================================================
# @Akitti C*Hive – Vorticity + Z₇ Scar Forcing + 3D Stretching
# ============================================================

from functools import partial

import jax.numpy as jnp
from jax import jit

from .grid import ik_cross, project_div_free, _u_from_vort_2d, _u_from_vort_3d
from .clay import (
    _oldroyd_rhs_2d, _oldroyd_rhs_3d, gum_damping,
    _stress_vort_force_2d, _stress_vort_force_3d,
)
from .constants import DELTA_MIN


@jit
def modest_liar(t_norm):
    return jnp.sqrt(1.0 - jnp.clip(t_norm, 0.0, 1.0))


def _wrap(d, L):
    """Minimum-image displacement on the period-L torus."""
    return d - L * jnp.round(d / L)


def default_scar_centres(L, n_scars=1, dim=3):
    """Lattice of 1–8 (or more) scar centres on the Clay torus."""
    n = max(int(n_scars), 1)
    c = 0.5 * L
    a = 0.25 * L
    if n == 1:
        return ((c,) * dim,)
    if dim == 2:
        if n == 2:
            return ((c - a, c), (c + a, c))
        pts = []
        for k in range(n):
            ang = 2.0 * jnp.pi * k / n
            pts.append((c + a * float(jnp.cos(ang)), c + a * float(jnp.sin(ang))))
        return tuple(pts)
    if n == 2:
        return ((c - a, c, c), (c + a, c, c))
    if n == 3:
        return ((c + a, c, c), (c - 0.5 * a, c + 0.866 * a, c),
                (c - 0.5 * a, c - 0.866 * a, c))
    if n == 4:
        return ((c + a, c + a, c + a), (c + a, c - a, c - a),
                (c - a, c + a, c - a), (c - a, c - a, c + a))
    if n == 5:
        return default_scar_centres(L, 4, 3) + ((c, c, c),)
    if n == 6:
        return ((c + a, c, c), (c - a, c, c), (c, c + a, c),
                (c, c - a, c), (c, c, c + a), (c, c, c - a))
    if n == 7:
        return default_scar_centres(L, 6, 3) + ((c, c, c),)
    # n >= 8: 2×2×2 cube, then extra points on a 3³ grid
    cube = []
    for sx in (-a, a):
        for sy in (-a, a):
            for sz in (-a, a):
                cube.append((c + sx, c + sy, c + sz))
    if n <= 8:
        return tuple(cube[:n])
    extra = []
    b = L / 3.0
    for i in range(3):
        for j in range(3):
            for k in range(3):
                p = ((i + 0.5) * b, (j + 0.5) * b, (k + 0.5) * b)
                extra.append(p)
    return tuple(cube + extra)[:n]


def resolve_scar_centres(grid, n_scars=1, scar_centres=None, center=None):
    """scar_centres wins; else n_scars on the default lattice; else `center`."""
    L, dim = float(grid["L"]), int(grid["dim"])
    if scar_centres is not None:
        return tuple(tuple(map(float, c)) for c in scar_centres)
    if center is not None and int(n_scars) <= 1:
        c = tuple(center)
        if len(c) < dim:
            c = c + (L / 2,) * (dim - len(c))
        return (c[:dim],)
    return default_scar_centres(L, n_scars, dim)


def _one_scar_2d(X, Y, center, L, amplitude, phase0, sigma):
    dx, dy = _wrap(X - center[0], L), _wrap(Y - center[1], L)
    theta = jnp.arctan2(dy, dx)
    phase = jnp.cos(7 * theta + phase0) + 0.5 * jnp.sin(7 * theta - phase0)
    return amplitude * phase * jnp.exp(-(dx**2 + dy**2) / (2 * sigma**2))


def _one_scar_3d_body(X, Y, Z, center, L, amplitude, phase0, helix_sign, sigma):
    """Local helical Z₇ body force about `center` (periodic)."""
    dx = _wrap(X - center[0], L)
    dy = _wrap(Y - center[1], L)
    dz = _wrap(Z - center[2], L)
    theta = jnp.arctan2(dy, dx)
    z_ang = helix_sign * 4.0 * jnp.pi * dz / L
    phase = jnp.cos(7 * theta + z_ang + phase0) + 0.5 * jnp.sin(7 * theta - z_ang)
    env = jnp.exp(-(dx**2 + dy**2 + dz**2) / (2 * sigma**2))
    return amplitude * phase * env * jnp.stack([
        -dy,
        dx,
        0.45 * jnp.sin(z_ang) * jnp.ones_like(dx),
    ])


def z7_braid_forcing(grid, amplitude, center=None, n_scars=1,
                     scar_centres=None, sigma=None):
    """Z₇ anyonic phase + Gaussian mollifier → fractal butterfly scars.

    2D: scalar vorticity force.  3D: curl of a helical body force.
    Multi-scar: sum local braids at `scar_centres`, or at the default
    n_scars-point lattice. n_scars=1 recovers the single central scar.
    Each centre gets a 2π k / 7 phase shift and alternating helix sign.
    """
    N, L, dim = int(grid["N"]), float(grid["L"]), int(grid["dim"])
    centres = resolve_scar_centres(grid, n_scars, scar_centres, center)
    x = jnp.linspace(0.0, L, N, endpoint=False)
    if dim == 2:
        X, Y = jnp.meshgrid(x, x, indexing="ij")
        sig = 0.35 if sigma is None else sigma
        force = 0.0
        for k, c in enumerate(centres):
            force = force + _one_scar_2d(
                X, Y, c, L, amplitude, 2.0 * jnp.pi * k / 7.0, sig)
        force_hat = jnp.fft.fftn(force) * grid["dealias"]
        return force_hat

    X, Y, Z = jnp.meshgrid(x, x, x, indexing="ij")
    sig = 0.28 if sigma is None else sigma
    body = 0.0
    for k, c in enumerate(centres):
        helix = 1.0 if (k % 2 == 0) else -1.0
        body = body + _one_scar_3d_body(
            X, Y, Z, c, L, amplitude, 2.0 * jnp.pi * k / 7.0, helix, sig)
    body_hat = jnp.fft.fftn(body, axes=(1, 2, 3)) * grid["dealias"]
    return ik_cross(body_hat, grid)


@jit
def _rhs_2d(vort_hat, grid, nu, force_hat):
    dealias, k2 = grid["dealias"], grid["k2"]
    u_hat = _u_from_vort_2d(vort_hat, grid)
    u = jnp.fft.ifftn(u_hat[0]).real
    v = jnp.fft.ifftn(u_hat[1]).real
    adv = (u * jnp.fft.ifftn(1j * grid["k"][0] * vort_hat).real +
           v * jnp.fft.ifftn(1j * grid["k"][1] * vort_hat).real)
    rhs = -jnp.fft.fftn(adv) * dealias - nu * k2 * vort_hat
    return (rhs + force_hat) * dealias


@jit
def _rhs_3d(vort_hat, grid, nu, force_hat):
    """Rotational form ∇×(u×ω) = (ω·∇)u − (u·∇)ω when both fields are solenoidal."""
    dealias, k2 = grid["dealias"], grid["k2"]
    u_hat = _u_from_vort_3d(vort_hat, grid)
    u = jnp.fft.ifftn(u_hat, axes=(1, 2, 3)).real
    omega = jnp.fft.ifftn(vort_hat, axes=(1, 2, 3)).real
    cross = jnp.stack([
        u[1] * omega[2] - u[2] * omega[1],
        u[2] * omega[0] - u[0] * omega[2],
        u[0] * omega[1] - u[1] * omega[0],
    ])
    cross_hat = jnp.fft.fftn(cross, axes=(1, 2, 3)) * dealias
    rhs = ik_cross(cross_hat, grid) - nu * k2 * vort_hat
    return (rhs + force_hat) * dealias


def ns_vorticity_rhs(vort_hat, grid, nu, force_hat=0):
    """Vorticity RHS. 3D uses the rotational form that includes full stretching."""
    if vort_hat.ndim == 2:
        return _rhs_2d(vort_hat, grid, nu, force_hat)
    return _rhs_3d(vort_hat, grid, nu, force_hat)


@partial(jit, static_argnums=(5,))
def _step_2d(vort_hat, grid, nu, dt, force_hat, scheme):
    rhs = _rhs_2d
    if scheme == "euler":
        return (vort_hat + dt * rhs(vort_hat, grid, nu, force_hat)) * grid["dealias"]
    k1 = rhs(vort_hat, grid, nu, force_hat)
    k2 = rhs(vort_hat + dt * k1, grid, nu, force_hat)
    return (vort_hat + 0.5 * dt * (k1 + k2)) * grid["dealias"]


@partial(jit, static_argnums=(5,))
def _step_3d(vort_hat, grid, nu, dt, force_hat, scheme):
    rhs = _rhs_3d
    if scheme == "euler":
        out = vort_hat + dt * rhs(vort_hat, grid, nu, force_hat)
    else:
        k1 = rhs(vort_hat, grid, nu, force_hat)
        k2 = rhs(vort_hat + dt * k1, grid, nu, force_hat)
        out = vort_hat + 0.5 * dt * (k1 + k2)
    return project_div_free(out, grid)


def ns_vorticity_step(vort_hat, grid, nu, dt, force_hat=0, scheme="rk2"):
    """Classic vorticity formulation. RK2 (Heun) is the 3D default;
    forward Euler is kept for the original 2D scar runs."""
    if vort_hat.ndim == 2:
        return _step_2d(vort_hat, grid, nu, dt, force_hat, scheme)
    return _step_3d(vort_hat, grid, nu, dt, force_hat, scheme)


@partial(jit, static_argnums=(6,))
def _coupled_step_2d(omega, tau, grid, nu, dt, force, scheme, t,
                     eta_p, lambda_relax, alpha, beta_scar, stress_diff,
                     clay_gain, gum_scale, stress_couple):
    def rhs(omega, tau):
        tau_f = stress_couple * _stress_vort_force_2d(tau, grid)
        dw = _rhs_2d(omega, grid, nu, force + tau_f)
        u_hat = _u_from_vort_2d(omega, grid)
        dtau = _oldroyd_rhs_2d(tau, u_hat, grid, eta_p, lambda_relax,
                               alpha, beta_scar, stress_diff, clay_gain)
        return dw, dtau

    if scheme == "euler":
        dw, dtau = rhs(omega, tau)
        omega, tau = omega + dt * dw, tau + dt * dtau
    else:
        k1w, k1t = rhs(omega, tau)
        k2w, k2t = rhs(omega + dt * k1w, tau + dt * k1t)
        omega = omega + 0.5 * dt * (k1w + k2w)
        tau = tau + 0.5 * dt * (k1t + k2t)
    tau = 0.5 * (tau + jnp.swapaxes(tau, 0, 1))
    return omega * grid["dealias"], gum_damping(tau, t, gum_scale)


@partial(jit, static_argnums=(6,))
def _coupled_step_3d(omega, tau, grid, nu, dt, force, scheme, t,
                     eta_p, lambda_relax, alpha, beta_scar, stress_diff,
                     clay_gain, gum_scale, stress_couple):
    """NS rotational-form stretching + ∇×(∇·τ) feedback, RK2-coupled."""
    def rhs(omega, tau):
        tau_f = stress_couple * _stress_vort_force_3d(tau, grid)
        dw = _rhs_3d(omega, grid, nu, force + tau_f)
        u_hat = _u_from_vort_3d(omega, grid)
        dtau = _oldroyd_rhs_3d(tau, u_hat, grid, eta_p, lambda_relax,
                               alpha, beta_scar, stress_diff, clay_gain)
        return dw, dtau

    if scheme == "euler":
        dw, dtau = rhs(omega, tau)
        omega, tau = omega + dt * dw, tau + dt * dtau
    else:
        k1w, k1t = rhs(omega, tau)
        k2w, k2t = rhs(omega + dt * k1w, tau + dt * k1t)
        omega = omega + 0.5 * dt * (k1w + k2w)
        tau = tau + 0.5 * dt * (k1t + k2t)
    omega = project_div_free(omega, grid)
    tau = 0.5 * (tau + jnp.swapaxes(tau, 0, 1))
    return omega, gum_damping(tau, t, gum_scale)


def coupled_vorticity_stress_step(omega_hat, tau_hat, grid, nu, dt, force_hat=0,
                                  scheme="rk2", t=0.0, eta_p=0.003,
                                  lambda_relax=0.6, alpha=0.085,
                                  beta_scar=0.13, stress_diff=1e-4,
                                  clay_gain=float(DELTA_MIN),
                                  gum_scale=1.0, stress_couple=1.0):
    """One coupled (ω, τ) step: stretching NS + Oldroyd-B extra-stress."""
    args = (omega_hat, tau_hat, grid, nu, dt, force_hat, scheme, t,
            eta_p, lambda_relax, alpha, beta_scar, stress_diff, clay_gain,
            gum_scale, stress_couple)
    if omega_hat.ndim == 2:
        return _coupled_step_2d(*args)
    return _coupled_step_3d(*args)
