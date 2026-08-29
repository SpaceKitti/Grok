# ============================================================
# @Akitti C*Hive – Diagnostics (λ₂, energy, IPR, stretching, MHD)
# ============================================================

import jax.numpy as jnp
from jax import jit

from .grid import _vort_from_u_2d, _vort_from_u_3d, ik_cross


@jit
def lambda2_criterion(u, v, dx, dy):
    """Jeong–Hussain λ₂ criterion – negative regions = coherent structures / UNMI modes."""
    dudx = (jnp.roll(u, -1, 1) - jnp.roll(u, 1, 1)) / (2 * dx)
    dudy = (jnp.roll(u, -1, 0) - jnp.roll(u, 1, 0)) / (2 * dy)
    dvdx = (jnp.roll(v, -1, 1) - jnp.roll(v, 1, 1)) / (2 * dx)
    dvdy = (jnp.roll(v, -1, 0) - jnp.roll(v, 1, 0)) / (2 * dy)
    S11, S22 = dudx, dvdy
    S12 = 0.5 * (dudy + dvdx)
    O12 = 0.5 * (dudy - dvdx)
    return S11**2 + S12**2 - O12**2


@jit
def velocity_gradient(u_hat, grid):
    """∂u_i/∂x_j via ik — shape (dim, dim, *grid)."""
    k = grid["k_stack"]
    ghat = 1j * u_hat[:, None] * k[None, :]
    return jnp.fft.ifftn(ghat, axes=range(2, ghat.ndim)).real


@jit
def strain_tensor(u_hat, grid):
    """S_ij = (∂u_i/∂x_j + ∂u_j/∂x_i)/2."""
    grad = velocity_gradient(u_hat, grid)
    return 0.5 * (grad + jnp.swapaxes(grad, 0, 1))


@jit
def max_strain_rate(S):
    """max_x ||S(x)||_2 — largest singular value of the strain-rate tensor."""
    evals = jnp.linalg.eigvalsh(jnp.moveaxis(S, (0, 1), (-2, -1)))
    return jnp.max(jnp.abs(evals))


@jit
def stretching_production(u_hat, omega, grid):
    """⟨ω_i S_ij ω_j⟩ — enstrophy production by vortex stretching."""
    S = strain_tensor(u_hat, grid)
    return jnp.mean(jnp.einsum("i...,ij...,j...->...", omega, S, omega))


@jit
def lambda2_criterion_3d(u_hat, grid):
    """Full 3D Jeong–Hussain λ₂ (intermediate eigenvalue of S²+Ω²)."""
    grad = velocity_gradient(u_hat, grid)
    S = 0.5 * (grad + jnp.swapaxes(grad, 0, 1))
    O = 0.5 * (grad - jnp.swapaxes(grad, 0, 1))
    A = (jnp.einsum("ik...,kj...->ij...", S, S) +
         jnp.einsum("ik...,kj...->ij...", O, O))
    evals = jnp.linalg.eigvalsh(jnp.moveaxis(A, (0, 1), (-2, -1)))
    return evals[..., 1]


@jit
def _stress_diagnostics_2d(tau_hat, u_hat, grid):
    tau = jnp.fft.ifftn(tau_hat, axes=(2, 3)).real
    mag = jnp.sqrt(jnp.sum(tau**2, axis=(0, 1)))
    L = velocity_gradient(u_hat, grid)
    S = 0.5 * (L + jnp.swapaxes(L, 0, 1))
    return {
        "mean_tau": jnp.mean(mag),
        "max_tau": jnp.max(mag),
        "tau_s": jnp.mean(jnp.einsum("ij...,ij...->...", tau, S)),
    }


@jit
def _stress_diagnostics_3d(tau_hat, u_hat, grid):
    tau = jnp.fft.ifftn(tau_hat, axes=(2, 3, 4)).real
    mag = jnp.sqrt(jnp.sum(tau**2, axis=(0, 1)))
    L = velocity_gradient(u_hat, grid)
    S = 0.5 * (L + jnp.swapaxes(L, 0, 1))
    return {
        "mean_tau": jnp.mean(mag),
        "max_tau": jnp.max(mag),
        "tau_s": jnp.mean(jnp.einsum("ij...,ij...->...", tau, S)),
    }


def stress_diagnostics(tau_hat, u_hat, grid):
    """mean |τ|, max |τ|, and mean τ:S (viscoelastic dissipation)."""
    if tau_hat.ndim == 4:
        return _stress_diagnostics_2d(tau_hat, u_hat, grid)
    return _stress_diagnostics_3d(tau_hat, u_hat, grid)


def _zero_stress():
    z = jnp.array(0.0)
    return {"mean_tau": z, "max_tau": z, "tau_s": z}


def _zero_magnetic():
    """Placeholders so NS / clay histories share the MHD key set."""
    z = jnp.array(0.0)
    return {
        "mag_energy": z,
        "max_J": z,
        "max_divB": z,
        "mag_helicity": z,
        "cross_helicity": z,
        "j2_mean": z,
    }


@jit
def _magnetic_diagnostics_3d(B_hat, u_hat, grid):
    """Magnetic energy, current, div B, helicities.

    Magnetic helicity uses the Coulomb-gauge vector potential A with
    B = curl(A), recovered the same way velocity is recovered from vorticity:
    A-hat = (ik x B-hat) / k^2. Cross helicity is mean(u · B).
    """
    k = grid["k_stack"]
    dealias = grid["dealias"]
    B = jnp.fft.ifftn(B_hat, axes=(1, 2, 3)).real
    mag_energy = 0.5 * jnp.mean(jnp.sum(B**2, axis=0))
    divB = jnp.fft.ifftn(jnp.sum(k * B_hat, axis=0)).real
    J_hat = ik_cross(B_hat, grid) * dealias
    J = jnp.fft.ifftn(J_hat, axes=(1, 2, 3)).real
    J2 = jnp.sum(J**2, axis=0)
    A_hat = (ik_cross(B_hat, grid) / grid["k2"]) * dealias
    A = jnp.fft.ifftn(A_hat, axes=(1, 2, 3)).real
    u = jnp.fft.ifftn(u_hat, axes=(1, 2, 3)).real
    return {
        "mag_energy": mag_energy,
        "max_J": jnp.max(jnp.sqrt(J2)),
        "max_divB": jnp.max(jnp.abs(divB)),
        "mag_helicity": jnp.mean(jnp.sum(A * B, axis=0)),
        "cross_helicity": jnp.mean(jnp.sum(u * B, axis=0)),
        "j2_mean": jnp.mean(J2),
    }


def magnetic_diagnostics(B_hat, u_hat, grid):
    """Magnetic energy, max |J|, max |div B|, magnetic and cross helicity."""
    if int(grid["dim"]) != 3:
        return _zero_magnetic()
    return _magnetic_diagnostics_3d(B_hat, u_hat, grid)


@jit
def _field_diagnostics_2d(u_hat, grid):
    u = jnp.fft.ifftn(u_hat, axes=(1, 2)).real
    energy = 0.5 * jnp.mean(jnp.sum(u**2, axis=0))
    div = jnp.fft.ifftn(jnp.sum(grid["k_stack"] * u_hat, axis=0)).real
    vort_hat = _vort_from_u_2d(u_hat, grid)
    vort = jnp.fft.ifftn(vort_hat).real
    S = strain_tensor(u_hat, grid)
    dw = jnp.fft.ifftn(1j * grid["k_stack"] * vort_hat[None], axes=(1, 2)).real
    return {
        "energy": energy,
        "enstrophy": jnp.mean(vort**2),
        "ipr": jnp.sum(vort**4) / (jnp.sum(vort**2)**2 + 1e-30),
        "helicity": jnp.array(0.0),
        "max_vort": jnp.max(jnp.abs(vort)),
        "stretch": jnp.array(0.0),
        "max_div": jnp.max(jnp.abs(div)),
        "lambda2_neg_frac": jnp.array(0.0),
        "max_strain": max_strain_rate(S),
        "palinstrophy": jnp.mean(jnp.sum(dw**2, axis=0)),
    }


@jit
def _field_diagnostics_3d(u_hat, grid):
    k = grid["k_stack"]
    u = jnp.fft.ifftn(u_hat, axes=(1, 2, 3)).real
    energy = 0.5 * jnp.mean(jnp.sum(u**2, axis=0))
    div = jnp.fft.ifftn(jnp.sum(k * u_hat, axis=0)).real
    omega_hat = _vort_from_u_3d(u_hat, grid)
    omega = jnp.fft.ifftn(omega_hat, axes=(1, 2, 3)).real
    w2 = jnp.sum(omega**2, axis=0)
    grad = velocity_gradient(u_hat, grid)
    S = 0.5 * (grad + jnp.swapaxes(grad, 0, 1))
    O = 0.5 * (grad - jnp.swapaxes(grad, 0, 1))
    A = (jnp.einsum("ik...,kj...->ij...", S, S) +
         jnp.einsum("ik...,kj...->ij...", O, O))
    l2 = jnp.linalg.eigvalsh(jnp.moveaxis(A, (0, 1), (-2, -1)))[..., 1]
    gw = jnp.fft.ifftn(1j * omega_hat[:, None] * k[None, :], axes=(2, 3, 4)).real
    return {
        "energy": energy,
        "enstrophy": jnp.mean(w2),
        "ipr": jnp.sum(w2**2) / (jnp.sum(w2)**2 + 1e-30),
        "helicity": jnp.mean(jnp.sum(u * omega, axis=0)),
        "max_vort": jnp.max(jnp.sqrt(w2)),
        "stretch": jnp.mean(jnp.einsum("i...,ij...,j...->...", omega, S, omega)),
        "max_div": jnp.max(jnp.abs(div)),
        "lambda2_neg_frac": jnp.mean(l2 < 0),
        "max_strain": max_strain_rate(S),
        "palinstrophy": jnp.mean(jnp.sum(gw**2, axis=(0, 1))),
    }


def field_diagnostics(u_hat, grid, tau_hat=None, B_hat=None):
    """Energy, enstrophy, IPR, helicity, max |w|, stretching, max |div u|, tau / B stats."""
    if int(grid["dim"]) == 2:
        d = _field_diagnostics_2d(u_hat, grid)
    else:
        d = _field_diagnostics_3d(u_hat, grid)
    if tau_hat is None:
        d.update(_zero_stress())
    else:
        d.update(stress_diagnostics(tau_hat, u_hat, grid))
    if B_hat is None:
        d.update(_zero_magnetic())
    else:
        d.update(magnetic_diagnostics(B_hat, u_hat, grid))
    return d


def sample_times(n_samples, steps, dt, diag_every):
    """Physical times of the diagnostic snapshots (t=0 plus each chunk)."""
    t = jnp.arange(n_samples, dtype=jnp.float64) * (diag_every * dt)
    if n_samples > 1 and (steps % diag_every):
        t = t.at[-1].set(steps * dt)
    return t


@jit
def _time_derivative(y, t):
    """Centered d/dt; one-sided at the endpoints. Works for n>=2."""
    dt = t[1:] - t[:-1]
    interior = (y[2:] - y[:-2]) / (t[2:] - t[:-2] + 1e-30)
    left = (y[1] - y[0]) / (dt[0] + 1e-30)
    right = (y[-1] - y[-2]) / (dt[-1] + 1e-30)
    return jnp.concatenate([left[None], interior, right[None]])


@jit
def _running_trapz(y, t):
    """Running trapezoidal integral; out[0] = 0, out[i] = integral_0^{t_i} y dt."""
    pieces = 0.5 * (y[1:] + y[:-1]) * (t[1:] - t[:-1])
    return jnp.concatenate([jnp.zeros((1,), dtype=y.dtype), jnp.cumsum(pieces)])


def millennium_series(hist, time, nu, eta=0.0):
    """BKM integral, dZ/dt, dE/dt, and dissipation from a recorded history.

    Dissipation is nu Z + <tau:S> + eta <|J|^2> (Ohmic term is zero when eta=0).
    """
    energy = hist["energy"]
    enstrophy = hist["enstrophy"]
    max_vort = hist["max_vort"]
    if energy.shape[0] < 2:
        z = jnp.zeros_like(energy)
        dE_dt = z
        dZ_dt = z
        bkm = z
    else:
        dE_dt = _time_derivative(energy, time)
        dZ_dt = _time_derivative(enstrophy, time)
        bkm = _running_trapz(max_vort, time)
    ohmic = eta * hist["j2_mean"]
    dissipation = nu * enstrophy + hist["tau_s"] + ohmic
    dZ_dt_budget = 2.0 * hist["stretch"] - 2.0 * nu * hist["palinstrophy"]
    return {
        "time": time,
        "bkm_integral": bkm,
        "dZ_dt": dZ_dt,
        "dE_dt": dE_dt,
        "dissipation": dissipation,
        "ohmic": ohmic,
        "dZ_dt_budget": dZ_dt_budget,
        "max_strain": hist["max_strain"],
        "palinstrophy": hist["palinstrophy"],
    }
