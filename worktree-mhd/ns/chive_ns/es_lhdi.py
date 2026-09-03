# ============================================================
# @Akitti C*Hive – Electrostatic / LHDI scaffolding (NOT live)
#
# Placeholders only. es_lhdi=False everywhere in the stepper.
# Harris sheet is an optional *magnetic* seed; charge and E are
# stored as zeros so a future ES layer can attach without a
# rewrite of the spectral core.
# ============================================================
"""Electrostatic LHDI groundwork.

What is *not* implemented (do not treat as solved)
-------------------------------------------------
A true electrostatic Lower-Hybrid Drift layer needs a Poisson /
Darwin field that the present incompressible MHD stepper does not
carry. The dual-role physics in Thatikonda et al. is:

  * ES regime (low β_e, thicker sheets): E×B transport at density /
    pressure *edges* flattens ∇n, ∇p (anomalous viscosity).
  * EM regime (higher β_e, L ∼ ρ_i): δB, current bifurcation, low-k
    kinking, anomalous resistivity.

We still have no charge, no E, no Harris-edge electrostatic seed that
feeds back. This module is the socket.

Equation changes required for a live ES-LHDI layer
--------------------------------------------------
Keep unmollified u in induction / Lorentz / odd. Add, do not replace:

  1. Electrostatic potential (periodic torus, zero mean):
       −∇² φ = ρ_c / ε₀          (spectral: φ̂ = ρ̂_c / k²)
       E_es  = −∇φ

  2. Momentum / vorticity residual — extra body force
       f_es = ρ_c E_es
     injected as curl(f_es) next to curl(J×B) and curl(div τ).
     In the incompressible projection this force is *not* a gradient
     unless ρ_c is uniform, so it survives Helmholtz and is the
     actual ES back-reaction.

  3. Induction must *not* see a mollified velocity. Faraday:
       ∂t B = −∇×E_tot
       E_tot = −u_raw × B + η J − ∇φ
     The −∇φ term has zero curl, so *ideal Faraday is unchanged*.
     The ES field affects B only indirectly, through u (E×B drift
     in momentum). That is why a naive “add E to induction” is
     wrong in the electrostatic limit.

  4. Charge continuity (or quasi-neutrality closure):
       ∂t ρ_c + ∇·J = 0
     with J = J_MHD + σ_es E_es  or a two-fluid Hall/electron
     current. Quasi-neutral alternative: ρ_c ≈ 0 and φ from
     ∇·(n ∇φ) = ∇·(n u×B) (Boltzmann / gyrokinetic).

  5. Harris equilibrium + edge seed (magnetic part is below):
       B_x = B_0 tanh((y − y_0)/δ)
       n   ∝ sech²((y − y_0)/δ) + n_bg     (needs compressibility
                                             or a passive tracer)
     LHDI grows at the *edges* (|y − y_0| ∼ δ), not the current
     peak. A magnetic-only Harris seed without ρ_c will not produce
     the ES branch.

  6. Diagnostics that must exist before turning the layer on:
       max|E|, max|ρ_c|, edge |J| width, low-k kink energy,
       η_LHDI proxy (must be additive resistivity, never a
       velocity filter — see the J-mollify leak).

Do not add anomalous η_LHDI until Ohmic can be split
η|J|² vs η_LHDI|J|², or the late-Ohmic audit is poisoned.
"""

import jax.numpy as jnp
from jax import jit

from .grid import project_div_free


def zero_e_hat(grid, dtype=jnp.complex128):
    """Placeholder electric field (Fourier). Always zero until ES is live."""
    d, N = int(grid["dim"]), int(grid["N"])
    return jnp.zeros((d,) + (N,) * d, dtype=dtype)


def zero_charge_hat(grid, dtype=jnp.complex128):
    """Placeholder charge density (Fourier). Always zero until ES is live."""
    N, dim = int(grid["N"]), int(grid["dim"])
    return jnp.zeros((N,) * dim, dtype=dtype)


def generate_harris_sheet(grid, B0=0.08, width=0.08, kind="x"):
    """Harris reconnecting sheet, div-free.

    B = B0 tanh((y − L/2)/δ) ê_x  (kind 'x' / 'tube')
      or ê_z (kind 'z'). Current peaks at the Crow midplane.
    This is a *magnetic* equilibrium seed, not the ES edge mode.
    """
    N, L, dim = int(grid["N"]), float(grid["L"]), int(grid["dim"])
    B0, w = float(B0), max(float(width), 1e-8)
    x = jnp.linspace(0.0, L, N, endpoint=False)
    if dim == 2:
        X, Y = jnp.meshgrid(x, x, indexing="ij")
        prof = B0 * jnp.tanh((Y - 0.5 * L) / w)
        z = jnp.zeros_like(X)
        B = jnp.stack([prof, z]) if kind in ("x", "tube") else jnp.stack([z, prof])
    else:
        X, Y, Z = jnp.meshgrid(x, x, x, indexing="ij")
        z = jnp.zeros_like(X)
        prof = B0 * jnp.tanh((Y - 0.5 * L) / w)
        if kind in ("x", "tube"):
            B = jnp.stack([prof, z, z])
        else:
            B = jnp.stack([z, z, prof])
    B_hat = jnp.fft.fftn(B, axes=range(1, dim + 1))
    return project_div_free(B_hat, grid)


def generate_harris_n(grid, n_bg=0.25, n1=0.75, width=0.08):
    """Venus Harris density: n = n_bg + n1 sech^2((y - L/2)/delta). No floor.

    n_bg=0.25, n1=0.75 keeps min n >= n_bg > 0 on the periodic box.
    Same delta as generate_harris_sheet (caller passes harris_width).
    Returns real-space n (not Fourier).
    """
    N, L, dim = int(grid["N"]), float(grid["L"]), int(grid["dim"])
    n_bg, n1, w = float(n_bg), float(n1), max(float(width), 1e-8)
    x = jnp.linspace(0.0, L, N, endpoint=False)
    if dim == 2:
        _X, Y = jnp.meshgrid(x, x, indexing="ij")
    else:
        _X, Y, _Z = jnp.meshgrid(x, x, x, indexing="ij")
    eta = (Y - 0.5 * L) / w
    return n_bg + n1 / jnp.cosh(eta) ** 2


def generate_harris_edge_seed(grid, amp=0.02, width=0.08, k_edge=4):
    """Small solenoidal perturbation localised at the Harris *edges*.

    Envelope ∼ sech²(η) |η| with η = (y−L/2)/δ, so the seed sits where
    LHDI would grow, not at the current peak. Amplitude is in Alfvén
    units of the parent B0 (caller scales). k_edge is the integer
    streamwise wavenumber along x.
    """
    N, L, dim = int(grid["N"]), float(grid["L"]), int(grid["dim"])
    amp, w = float(amp), max(float(width), 1e-8)
    k_edge = int(k_edge)
    x = jnp.linspace(0.0, L, N, endpoint=False)
    if dim == 2:
        X, Y = jnp.meshgrid(x, x, indexing="ij")
        eta = (Y - 0.5 * L) / w
        env = (1.0 / jnp.cosh(eta)) ** 2 * jnp.abs(eta)
        phase = jnp.sin(2.0 * jnp.pi * k_edge * X / L)
        bx, by = amp * env * phase, jnp.zeros_like(X)
        B = jnp.stack([bx, by])
    else:
        X, Y, Z = jnp.meshgrid(x, x, x, indexing="ij")
        eta = (Y - 0.5 * L) / w
        env = (1.0 / jnp.cosh(eta)) ** 2 * jnp.abs(eta)
        phase = jnp.sin(2.0 * jnp.pi * k_edge * X / L)
        z = jnp.zeros_like(X)
        # δB_z at the edges — a seed for the out-of-plane ES/EM branch
        B = jnp.stack([z, z, amp * env * phase])
    B_hat = jnp.fft.fftn(B, axes=range(1, dim + 1))
    return project_div_free(B_hat, grid)


@jit
def _es_placeholders_3d(u_hat, B_hat, grid):
    """Zero E and ρ_c plus dummy monitors. No back-reaction."""
    z = jnp.array(0.0)
    return {
        "max_e": z,
        "max_charge": z,
        "es_energy": z,
        "edge_j": z,
    }


def es_placeholder_diagnostics():
    z = jnp.array(0.0)
    return {
        "max_e": z,
        "max_charge": z,
        "es_energy": z,
        "edge_j": z,
    }


def es_equation_notes():
    """Return the Faraday / momentum change list as a string."""
    return __doc__
