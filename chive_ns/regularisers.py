# ============================================================
# @Akitti C*Hive – Controllable hybrid regularisation dials
# Voigt / Fréchet / J-mollify / high-De kernel / LB second-moment
# ============================================================

import jax.numpy as jnp
from jax import jit


def mollify_hat(field_hat, grid, soft_J):
    """Jaracz–Lee velocity / stress mollification: exp(-soft_J k²)."""
    return field_hat * jnp.exp(-soft_J * grid["k2"])


@jit
def _sheet_order_from_S(S):
    """s = 1 - |λ₂| / ||λ|| from strain-rate eigenvalues (Set 3 VGT)."""
    evals = jnp.linalg.eigvalsh(jnp.moveaxis(S, (0, 1), (-2, -1)))
    nrm = jnp.linalg.norm(evals, axis=-1) + 1e-12
    mid = evals[..., evals.shape[-1] // 2]
    return 1.0 - jnp.abs(mid) / nrm


@jit
def kinematic_lambda(work, nu, enstrophy):
    """Self-consistent λ = |W| / (|W| + ν Z) (Set 1 closed dial)."""
    aw = jnp.abs(work)
    return aw / (aw + nu * enstrophy + 1e-30)


@jit
def _voigt_rhs_2d(tau_hat, vort, grid, alpha_par, alpha_perp, gamma_s):
    """2D Voigt: t = e_z, so A is isotropic in-plane with α_perp."""
    k = grid["k_stack"]
    kappa = alpha_perp**2 * (1.0 + gamma_s * 0.0)
    return -kappa * grid["k2"] * tau_hat * grid["dealias"]


@jit
def _voigt_rhs_3d_sheet(tau_hat, omega, S, grid, alpha_par, alpha_perp, gamma_s):
    k = grid["k_stack"]
    w2 = jnp.sum(omega**2, axis=0)
    tdir = omega / jnp.sqrt(w2 + 1e-12)
    s = _sheet_order_from_S(S)
    a_par = alpha_par * (1.0 - gamma_s * jnp.clip(s, 0.0, 1.0))
    a_perp = alpha_perp * (1.0 + gamma_s * jnp.clip(s, 0.0, 1.0))
    A = ((a_par**2 - a_perp**2) * tdir[:, None] * tdir[None, :]
         + (a_perp**2) * jnp.broadcast_to(
             jnp.eye(3)[:, :, None, None, None], (3, 3) + w2.shape))
    gtau = jnp.fft.ifftn(
        1j * tau_hat[:, :, None] * k[None, None, :], axes=(3, 4, 5)).real
    flux = jnp.einsum("pq...,ijq...->ijp...", A, gtau)
    flux_hat = jnp.fft.fftn(flux, axes=(3, 4, 5))
    return 1j * jnp.einsum("p...,ijp...->ij...", k, flux_hat) * grid["dealias"]


@jit
def frechet_stress_rhs(tau_hat, tau, grid, epsilon):
    """Cheap Fréchet-style diffusion: core-weighted Laplacian of τ (Set 2).

    More diffusion where |τ| is large so peak polymer work is spread out
    without raising bulk η_p.
    """
    mag = jnp.sqrt(jnp.sum(tau**2, axis=(0, 1)) + 1e-30)
    w = 1.0 + mag / (jnp.mean(mag) + 1e-12)
    gtau = jnp.fft.ifftn(
        1j * tau_hat[:, :, None] * grid["k_stack"][None, None, :],
        axes=range(3, tau_hat.ndim + 1)).real
    flux = w * gtau
    flux_hat = jnp.fft.fftn(flux, axes=range(3, flux.ndim))
    return epsilon * 1j * jnp.einsum(
        "p...,ijp...->ij...", grid["k_stack"], flux_hat) * grid["dealias"]


@jit
def high_de_blend(tau, omega, S, eta_p, lambda_relax, high_de):
    """Blend continuum τ toward a bounded high-De plateau in |ω| cores (Set 3)."""
    wabs = jnp.sqrt(jnp.sum(omega**2, axis=0) + 1e-30)
    thresh = 0.7 * jnp.max(wabs)
    phi = high_de / (1.0 + jnp.exp(-(wabs - thresh) / (0.05 * thresh + 1e-12)))
    De = lambda_relax * jnp.sqrt(jnp.sum(S**2, axis=(0, 1)) + 1e-30)
    tau_core = (eta_p / (lambda_relax + 1e-12)) * S / (1.0 + De)
    return (1.0 - phi) * tau + phi * tau_core, phi


@jit
def lb_filtered_div(tau_hat, grid, soft_lb):
    """Fluctuating-LB second-moment proxy: ∇·(filtered τ) (Set 4)."""
    Pi_hat = mollify_hat(tau_hat, grid, soft_lb)
    return 1j * jnp.einsum("j...,ij...->i...", grid["k_stack"], Pi_hat)


def regularise_constitutive(tau_hat, u_hat, omega, S, grid, p):
    """Apply J-mollify on constitutive velocity + Voigt + Fréchet on τ RHS."""
    u_c = mollify_hat(u_hat, grid, float(p.get("soft_J", 0.0)))
    extra = jnp.zeros_like(tau_hat)
    ap = float(p.get("alpha_par", 0.0))
    aq = float(p.get("alpha_perp", 0.0))
    gs = float(p.get("gamma_s", 2.0))
    if (ap > 0.0 or aq > 0.0) and tau_hat.ndim == 5:
        extra = extra + _voigt_rhs_3d_sheet(
            tau_hat, omega, S, grid, ap, aq, gs)
    elif aq > 0.0 and tau_hat.ndim == 4:
        extra = extra + _voigt_rhs_2d(tau_hat, None, grid, ap, aq, gs)
    eps = float(p.get("epsilon_frechet", 0.0))
    if eps > 0.0:
        tau = jnp.fft.ifftn(tau_hat, axes=range(2, tau_hat.ndim)).real
        extra = extra + frechet_stress_rhs(tau_hat, tau, grid, eps)
    return u_c, extra
