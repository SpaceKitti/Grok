# ============================================================
# @Akitti C*Hive – Diagnostics (λ₂, energy, IPR, stretching)
# ============================================================

import jax.numpy as jnp
from jax import jit

from .grid import _vort_from_u_2d, _vort_from_u_3d
from .regularisers import _sheet_order_from_S


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
        "sheet_order": jnp.mean(_sheet_order_from_S(S)),
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
        "sheet_order": jnp.mean(_sheet_order_from_S(S)),
    }


def field_diagnostics(u_hat, grid, tau_hat=None):
    """Energy, enstrophy, IPR, helicity, max |ω|, stretching, max |div u|, τ stats."""
    if int(grid["dim"]) == 2:
        d = _field_diagnostics_2d(u_hat, grid)
    else:
        d = _field_diagnostics_3d(u_hat, grid)
    if tau_hat is None:
        d.update(_zero_stress())
    else:
        d.update(stress_diagnostics(tau_hat, u_hat, grid))
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
    """Running trapezoidal integral; out[0] = 0, out[i] = ∫_0^{t_i} y dt."""
    pieces = 0.5 * (y[1:] + y[:-1]) * (t[1:] - t[:-1])
    return jnp.concatenate([jnp.zeros((1,), dtype=y.dtype), jnp.cumsum(pieces)])


def millennium_series(hist, time, nu):
    """BKM integral, dZ/dt, dE/dt, and dissipation from a recorded history."""
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
    ohmic = hist.get("ohmic", jnp.zeros_like(enstrophy))
    hyper_ohmic = hist.get("hyper_ohmic", jnp.zeros_like(enstrophy))
    eps_nu = nu * enstrophy
    # ε_η = η⟨|J|²⟩ + η_h⟨|∇²B|²⟩. Lorentz work is a kin↔mag
    # transfer and MUST NOT enter this meter (it cancels in E_tot).
    eps_eta = ohmic + hyper_ohmic
    dissipation = eps_nu + hist["tau_s"] + eps_eta
    e_mag = hist.get("e_mag_tot", hist.get("e_mag", jnp.zeros_like(energy)))
    e_tot = energy + e_mag
    if energy.shape[0] < 2:
        dE_tot_dt = jnp.zeros_like(energy)
        I_nu = jnp.zeros_like(energy)
        I_eta = jnp.zeros_like(energy)
        I_tau = jnp.zeros_like(energy)
    else:
        dE_tot_dt = _time_derivative(e_tot, time)
        I_nu = _running_trapz(eps_nu, time)
        I_eta = _running_trapz(eps_eta, time)
        I_tau = _running_trapz(hist["tau_s"], time)
    # Instantaneous residual of Ė_tot + ε_ν + ε_η (+τ:S). Lorentz excluded.
    energy_leak = dE_tot_dt + dissipation
    # Integrated: ∫(Ė + ε) dt = ΔE_tot + ∫ε. Old (E0-E)+∫ε was a
    # hidden sign error (≈2∫ε when the identity holds).
    I_leak = (e_tot - e_tot[0]) + I_nu + I_eta + I_tau
    dZ_dt_budget = 2.0 * hist["stretch"] - 2.0 * nu * hist["palinstrophy"]
    work = hist.get("work", hist["tau_s"])
    sheet = hist.get("sheet_order", jnp.zeros_like(max_vort))
    weight = 1.0 + 0.15 * jnp.abs(work) + 0.08 * (1.0 - sheet)
    if energy.shape[0] < 2:
        I_bkm_w = jnp.zeros_like(energy)
        I_sigma = jnp.zeros_like(energy)
    else:
        I_bkm_w = _running_trapz(max_vort / weight, time)
        I_sigma = _running_trapz(hist.get("sigma_inf", jnp.zeros_like(max_vort)), time)
    return {
        "time": time,
        "bkm_integral": bkm,
        "dZ_dt": dZ_dt,
        "dE_dt": dE_dt,
        "dissipation": dissipation,
        "dZ_dt_budget": dZ_dt_budget,
        "max_strain": hist["max_strain"],
        "palinstrophy": hist["palinstrophy"],
        "I_bkm_w": I_bkm_w,
        "I_sigma": I_sigma,
        "sheet_order": sheet,
        "work": work,
        "lambda_kin": hist.get("lambda_kin", jnp.zeros_like(energy)),
        "eps_ratio": hist.get("eps_ratio", jnp.zeros_like(energy)),
        "Gamma": hist.get("Gamma", jnp.zeros_like(energy)),
        "ohmic": ohmic,
        "e_mag": hist.get("e_mag", jnp.zeros_like(energy)),
        "e_tot": e_tot,
        "dE_tot_dt": dE_tot_dt,
        "eps_nu": eps_nu,
        "I_nu": I_nu,
        "I_eta": I_eta,
        "I_tau": I_tau,
        "energy_leak": energy_leak,
        "I_leak": I_leak,
        "rec_rate_flux": (
            -_time_derivative(hist["flux_x_half"], time)
            if energy.shape[0] >= 2 and "flux_x_half" in hist
            else jnp.zeros_like(energy)
        ),
    }
