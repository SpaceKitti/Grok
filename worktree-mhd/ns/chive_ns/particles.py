# ============================================================
# @Akitti C*Hive – Stage 3 test-particle tracers (Boris)
# Passive: fluid Ohm E + spectral B. No deposit, no back-reaction.
# Not PIC, not MMS. Hive e=1. Default m_e/m_i = 1/25 (not 1/1836).
# ============================================================

import jax.numpy as jnp

from .grid import velocity_from_vorticity
from .mhd import current_from_b


M_I = 1.0
Q_I = 1.0
Q_E = -1.0
M_E_DEFAULT = 1.0 / 25.0
N_P_DEFAULT = 8  # per species; 8 ions + 8 electrons


def _as_3vec(field):
    """Pad a 2-comp field with a zero z-row. Already-3 is unchanged."""
    if field.shape[0] == 3:
        return field
    z = jnp.zeros_like(field[0])
    return jnp.concatenate([field, z[None]], axis=0)


def _cross_last(a, b):
    return jnp.stack([
        a[..., 1] * b[..., 2] - a[..., 2] * b[..., 1],
        a[..., 2] * b[..., 0] - a[..., 0] * b[..., 2],
        a[..., 0] * b[..., 1] - a[..., 1] * b[..., 0],
    ], axis=-1)


def ohm_E(u, B, J, n, d_i, eta, T_e, grad_n=None):
    """Two-fluid / Hall Ohm in physical space. Hive e=1.

    E = -u_e x B - grad(p_e)/n + eta J
    u_e = u_i - (d_i/n) J , p_e = n T_e (T_e const; no electron inertia).

    u, B, J are (2 or 3, *grid). n is scalar or (*grid). T_e=0 recovers Hall.
    If grad_n is None the electron-pressure term is 0 (const n or T_e=0).
    Does not deposit particle current. Fluid is the field.
    """
    u3 = _as_3vec(u)
    B3 = _as_3vec(B)
    J3 = _as_3vec(J)
    invn = 1.0 / (n + 1e-30)
    ue = u3 - d_i * invn * J3
    E = -jnp.stack([
        ue[1] * B3[2] - ue[2] * B3[1],
        ue[2] * B3[0] - ue[0] * B3[2],
        ue[0] * B3[1] - ue[1] * B3[0],
    ]) + eta * J3
    if grad_n is not None:
        E = E - T_e * _as_3vec(grad_n) * invn
    return E


def ohm_fields(u_hat, B_hat, n_hat, grid, d_i, eta, T_e, n0=1.0):
    """Physical E, B from fluid hats via twofluid Ohm. No particle J."""
    axes = tuple(range(1, u_hat.ndim))
    u = jnp.fft.ifftn(u_hat, axes=axes).real
    B = jnp.fft.ifftn(B_hat, axes=axes).real
    J_hat = current_from_b(B_hat, grid)
    if J_hat.ndim == B.ndim:
        J = jnp.fft.ifftn(J_hat, axes=axes).real
    else:
        Jz = jnp.fft.ifftn(J_hat).real
        z = jnp.zeros_like(Jz)
        J = jnp.stack([z, z, Jz])
    if n_hat is None:
        n = jnp.full_like(B[0], n0)
        gn = None
    else:
        n = jnp.fft.ifftn(n_hat).real
        gn = jnp.fft.ifftn(1j * grid["k_stack"] * n_hat, axes=axes).real
    E = ohm_E(u, B, J, n, d_i, eta, T_e, grad_n=gn)
    return E, _as_3vec(B)


def gather_at(field, x, grid):
    """Periodic bilinear (2D) / trilinear (3D) interpolate at x.

    field: (ncomp, N, N) or (ncomp, N, N, N)
    x: (N_p, dim)  (wrapped internally)
    returns (N_p, ncomp)
    """
    N = field.shape[-1]
    L = grid["L"]
    dim = x.shape[-1]
    xi = x * (N / L)
    i0 = jnp.floor(xi).astype(jnp.int32)
    f = xi - jnp.floor(xi)
    i0 = i0 % N
    i1 = (i0 + 1) % N
    if dim == 2:
        ix0, iy0 = i0[:, 0], i0[:, 1]
        ix1, iy1 = i1[:, 0], i1[:, 1]
        fx, fy = f[:, 0], f[:, 1]
        v00 = field[:, ix0, iy0]
        v10 = field[:, ix1, iy0]
        v01 = field[:, ix0, iy1]
        v11 = field[:, ix1, iy1]
        val = ((1.0 - fx) * (1.0 - fy) * v00
               + fx * (1.0 - fy) * v10
               + (1.0 - fx) * fy * v01
               + fx * fy * v11)
        return val.T
    ix0, iy0, iz0 = i0[:, 0], i0[:, 1], i0[:, 2]
    ix1, iy1, iz1 = i1[:, 0], i1[:, 1], i1[:, 2]
    fx, fy, fz = f[:, 0], f[:, 1], f[:, 2]
    c000 = field[:, ix0, iy0, iz0]
    c100 = field[:, ix1, iy0, iz0]
    c010 = field[:, ix0, iy1, iz0]
    c110 = field[:, ix1, iy1, iz0]
    c001 = field[:, ix0, iy0, iz1]
    c101 = field[:, ix1, iy0, iz1]
    c011 = field[:, ix0, iy1, iz1]
    c111 = field[:, ix1, iy1, iz1]
    wx0, wy0, wz0 = 1.0 - fx, 1.0 - fy, 1.0 - fz
    val = (wx0 * wy0 * wz0 * c000 + fx * wy0 * wz0 * c100
           + wx0 * fy * wz0 * c010 + fx * fy * wz0 * c110
           + wx0 * wy0 * fz * c001 + fx * wy0 * fz * c101
           + wx0 * fy * fz * c011 + fx * fy * fz * c111)
    return val.T


def boris_push(x, v, q, m, E, B, dt):
    """Boris velocity kick: m dv/dt = q (E + v x B). Hive e=1.

    x, v: x is (N_p, dim) unused here (x is updated by wrap_x);
    v, E, B are (N_p, 3). Returns v_new.
    """
    del x
    qdt_2m = (q * dt) / (2.0 * m)
    v_minus = v + qdt_2m * E
    t = qdt_2m * B
    t2 = jnp.sum(t * t, axis=-1, keepdims=True)
    s = 2.0 * t / (1.0 + t2)
    v_prime = v_minus + _cross_last(v_minus, t)
    v_plus = v_minus + _cross_last(v_prime, s)
    return v_plus + qdt_2m * E


def wrap_x(x, v, dt, grid):
    """x = (x + v dt) mod L on the torus. v may be 3-comp; uses first dim axes."""
    L = grid["L"]
    dim = x.shape[-1]
    return jnp.mod(x + v[:, :dim] * dt, L)


def kinetic_energy(v, m):
    """KE = sum 0.5 m |v|^2 over particles."""
    return 0.5 * m * jnp.sum(v * v)


def init_particle_arrays(grid, n_p=N_P_DEFAULT):
    """8 ions + 8 electrons on a tiny 2x4 lattice. v=0."""
    L = float(grid["L"])
    dim = int(grid["dim"])
    n_p = int(n_p)
    xs = jnp.array([0.125, 0.375, 0.625, 0.875]) * L
    ys = jnp.array([0.25, 0.75]) * L
    xx, yy = jnp.meshgrid(xs, ys, indexing="ij")
    xy = jnp.stack([xx.ravel()[:n_p], yy.ravel()[:n_p]], axis=1)
    if dim == 2:
        x = xy
    else:
        z = jnp.full((n_p, 1), 0.5 * L)
        x = jnp.concatenate([xy, z], axis=1)
    v = jnp.zeros((n_p, 3), dtype=x.dtype)
    return x, v, jnp.array(x), jnp.array(v)


def step_from_fluid(x_i, v_i, x_e, v_e, u_hat, B_hat, n_hat, grid, dt,
                    mhd_params, m_e=M_E_DEFAULT):
    """One passive Boris step in fluid Ohm E and spectral B. No deposit."""
    d_i = float(mhd_params.get("d_i", 0.0))
    eta = float(mhd_params.get("eta_mag", 0.0))
    T_e = float(mhd_params.get("T_e", 0.0))
    n0 = float(mhd_params.get("n", mhd_params.get("n_hall", 1.0)))
    E, B = ohm_fields(u_hat, B_hat, n_hat, grid, d_i, eta, T_e, n0=n0)
    Ei = gather_at(E, x_i, grid)
    Bi = gather_at(B, x_i, grid)
    Ee = gather_at(E, x_e, grid)
    Be = gather_at(B, x_e, grid)
    v_i = boris_push(x_i, v_i, Q_I, M_I, Ei, Bi, dt)
    v_e = boris_push(x_e, v_e, Q_E, m_e, Ee, Be, dt)
    x_i = wrap_x(x_i, v_i, dt, grid)
    x_e = wrap_x(x_e, v_e, dt, grid)
    return x_i, v_i, x_e, v_e


def with_passive_particles(advance, snapshot, state0, grid, dt, mhd_params,
                           n_from="hall"):
    """Wrap a fluid advance: tracers see Ohm E after each step. No deposit.

    Fluid advance is unchanged. Particle current is not added to Ampere/Faraday.
    n_from="twofluid" reads n_i_hat from the fluid state; "hall" uses n_hall.
    """
    n_p = int(mhd_params.get("n_p", N_P_DEFAULT))
    m_e = float(mhd_params.get("m_e", M_E_DEFAULT))
    x_i0, v_i0, x_e0, v_e0 = init_particle_arrays(grid, n_p=n_p)
    twofluid = n_from == "twofluid"

    def advance_p(state, idx):
        fluid, x_i, v_i, x_e, v_e = state
        fluid = advance(fluid, idx)
        if twofluid:
            omega_hat, _tau_hat, B_hat, _psi_hat, n_i_hat = fluid
        else:
            omega_hat, _tau_hat, B_hat, _psi_hat = fluid
            n_i_hat = None
        u_hat = velocity_from_vorticity(omega_hat, grid)
        x_i, v_i, x_e, v_e = step_from_fluid(
            x_i, v_i, x_e, v_e, u_hat, B_hat, n_i_hat, grid, dt,
            mhd_params, m_e=m_e)
        return (fluid, x_i, v_i, x_e, v_e)

    def snapshot_p(state):
        fluid, x_i, v_i, x_e, v_e = state
        d = snapshot(fluid)
        d["KE_i"] = kinetic_energy(v_i, M_I)
        d["KE_e"] = kinetic_energy(v_e, m_e)
        d["x_i"] = x_i
        d["x_e"] = x_e
        d["v_i"] = v_i
        d["v_e"] = v_e
        return d

    return advance_p, snapshot_p, (state0, x_i0, v_i0, x_e0, v_e0)