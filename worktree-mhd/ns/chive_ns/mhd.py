# ============================================================
# @Akitti C*Hive – Spectral MHD layer
# Induction + Lorentz + odd/gyro viscosity + Qin Helmholtz
# projection + Ogilvie–Proctor / helicity monitors.
# Polymer constitutive law is untouched.
# ============================================================

import jax.numpy as jnp
from jax import jit

from .grid import (
    ik_cross, project_div_free, _vort_from_u_2d, _u_from_vort_2d,
    antiparallel_tube_vector, paper_ni_ic, paper_sigma_c,
)


# Dual regulariser to polymer stress_diff: modest Rm so residual
# dissipation stays hydro-dominated. Weak B0 keeps Alfvén CFL
# from beating the existing NS/clay step.
DEFAULT_MHD = dict(
    eta_mag=1.0e-3,
    B0=0.08,
    eta_odd=0.0,
    b_guide="z",
    # External-field freeze-out (Varnish et al.): fraction of B0 held
    # as a static back-pressure field that is NOT stretched by induction.
    freeze_ext=0.0,
    ext_profile="uniform",   # "uniform" (tension, no extra J) | "midplane"
    ext_width=0.12,          # Gaussian half-width of the midplane pile-up
    induct_ext=None,         # None → 0 if freeze_ext>0 else 1 (never stretch B_ext)
    # Clean regularisers (off by default)
    berry_gain=0.0,          # η_odd *= (1 + berry_gain |B| / <|B|>)
    mu_eff=0.0,              # additive even viscosity (scale-filter plateau)
    # PosDiv / mixed-FEM spectral analogs (off by default so NS+MHD is unchanged)
    eta_hyper=0.0,           # hyperresistivity η_h ∇⁴B — DF-preserving sheet regulariser
    posdiv=0.0,              # 1 → Helmholtz-project ω,B at the Heun midpoint
    hyper_kcut=0.0,          # optional: apply η_h only for k ≥ hyper_kcut k_max (0=all modes)
    # ES / LHDI scaffolding — OFF. Magnetic Harris seed only; E and
    # charge are zero placeholders (see es_lhdi.py for the live-layer list).
    harris=False,
    harris_width=0.08,
    harris_edge=0.0,
    es_lhdi=False,
    # Shen et al. 2025 co-located flux tubes (b_guide="flux"). Γ_m along
    # the vortex. 0 = off. tube_* default to the Crow IC if omitted.
    gamma_m=0.0,
    tube_radius=0.08,
    tube_circulation=0.7,
    tube_separation=0.24,
    tube_perturbation=0.04,
    tube_axial_wave=1,
    ot_u0=1.0,
    alfven_amp=0.01,
    # Dedner GLM (Dedner et al. 2002). glm_ch=0 disables; Qin projector remains.
    # Extra scalar psi carries div B as a damped wave; not Lorentz, not projector.
    glm_ch=0.0,
    glm_cr=0.18,
    # Hall-MHD Ohm (Stage 1; hive notes parked A4 / MHD2-04 Hall/Ohm).
    # E = -u x B + eta J + (d_i / n) J x B, n=1 default.
    # Faraday: dt B = -curl E (plus existing GLM/Dedner if glm_ch!=0).
    # d_i=0 recovers the ideal+resistive MHD induction. Hall is
    # dispersive, not heat: I_leak mill unchanged (no Hall heat term).
    # Do NOT dump Hall as a momentum body force (Venus/Russell Ohm).
    d_i=0.0,
    n_hall=1.0,
    # E2c Harris n = n_bg + harris_n1 sech^2((y-L/2)/delta). Off by default.
    # Spatial n is Hall Ohm only (d_i/n); d_i=0 still Qin MHD. No floor.
    harris_n=False,
    n_bg=0.25,
    harris_n1=0.75,
    # Two-fluid Ohm (Stage 2; Venus electron pressure; no inertia).
    # E = -u_e x B - grad(p_e)/n + eta J, u_e = u_i - (d_i/n) J, p_e = n T_e.
    # T_e=0 recovers Hall (same d_i, n). Continuity on n; no pin/floor.
    # Electron pressure is transfer/dispersive, not mill heat.
    T_e=0.0,
)


def zero_b_hat(grid, dtype=jnp.complex128):
    d, N = int(grid["dim"]), int(grid["N"])
    return jnp.zeros((d,) + (N,) * d, dtype=dtype)


def zero_psi_hat(grid, dtype=jnp.complex128):
    N, dim = int(grid["N"]), int(grid["dim"])
    return jnp.zeros((N,) * dim, dtype=dtype)


def generate_b0(grid, B0=0.08, kind="z", amp=None):
    """Divergence-free magnetic seed. Weak so hydro CFL stays dominant.

    kind:
      "z"    — uniform guide along ê_z (3D) / ê_y (2D)
      "x"    — uniform guide along ê_x (across Crow tubes)
      "tube" — alias of "x" (uniform field along the tube axis)
      "flux" / "flux_tubes" / "shen" — co-located Crow flux tubes
      "ot"   — Orszag–Tang-like seed (has current from t=0)
      "alfven" — uniform guide (ê_y in 2D / ê_z in 3D) plus a small
                transverse Alfvén δb; amp is the wave amplitude.
    For kind="flux", B0 is ignored; use mhd_params["gamma_m"] via
    generate_b_flux_tubes / split_guide_fields.
    """
    N, L, dim = int(grid["N"]), float(grid["L"]), int(grid["dim"])
    x = jnp.linspace(0.0, L, N, endpoint=False)
    B0 = float(B0)
    if amp is None:
        amp = 0.01
    if dim == 2:
        X, Y = jnp.meshgrid(x, x, indexing="ij")
        if kind == "ot":
            Bx = -B0 * jnp.sin(2 * jnp.pi * Y / L)
            By = B0 * jnp.sin(2 * jnp.pi * X / L)
        elif kind == "alfven":
            # Existing 2D guide is ê_y. δb_x = -amp sin(2π y/L) so δv=-δb
            # rides +B0 at v_A = |B0|.
            Bx = -float(amp) * jnp.sin(2 * jnp.pi * Y / L)
            By = jnp.ones_like(X) * B0
        else:
            Bx = jnp.zeros_like(X)
            By = jnp.ones_like(X) * B0
        B = jnp.stack([Bx, By])
    else:
        X, Y, Z = jnp.meshgrid(x, x, x, indexing="ij")
        z = jnp.zeros_like(X)
        if kind in ("x", "tube"):
            B = jnp.stack([jnp.ones_like(X) * B0, z, z])
        elif kind == "ot":
            Bx = B0 * (-jnp.sin(2 * jnp.pi * Y / L))
            By = B0 * jnp.sin(2 * jnp.pi * X / L)
            Bz = B0 * 0.2 * jnp.cos(2 * jnp.pi * Z / L)
            B = jnp.stack([Bx, By, Bz])
        elif kind == "alfven":
            Bx = -float(amp) * jnp.sin(2 * jnp.pi * Z / L)
            B = jnp.stack([Bx, z, jnp.ones_like(X) * B0])
        else:
            B = jnp.stack([z, z, jnp.ones_like(X) * B0])
    B_hat = jnp.fft.fftn(B, axes=range(1, dim + 1))
    return project_div_free(B_hat, grid)


def generate_u_ot(grid, U0=1.0):
    """Orszag-Tang velocity matching generate_b0(kind='ot').

    Same trigonometric skeleton as the OT magnetic seed, amplitude U0.
    3D includes a weak uz so the pair stays analogous to OT B; Qin-projected.
    """
    N, L, dim = int(grid["N"]), float(grid["L"]), int(grid["dim"])
    x = jnp.linspace(0.0, L, N, endpoint=False)
    U0 = float(U0)
    if dim == 2:
        X, Y = jnp.meshgrid(x, x, indexing="ij")
        ux = -U0 * jnp.sin(2 * jnp.pi * Y / L)
        uy = U0 * jnp.sin(2 * jnp.pi * X / L)
        u = jnp.stack([ux, uy])
    else:
        X, Y, Z = jnp.meshgrid(x, x, x, indexing="ij")
        ux = -U0 * jnp.sin(2 * jnp.pi * Y / L)
        uy = U0 * jnp.sin(2 * jnp.pi * X / L)
        uz = U0 * 0.2 * jnp.cos(2 * jnp.pi * Z / L)
        u = jnp.stack([ux, uy, uz])
    u_hat = project_div_free(jnp.fft.fftn(u, axes=range(1, dim + 1)), grid)
    return jnp.fft.ifftn(u_hat, axes=range(1, dim + 1)).real


def generate_u_alfven(grid, amp=0.01):
    """Forward Alfvén velocity matching generate_b0(kind='alfven').

    Same sin profile, δv = -δb (ρ=1): the packet propagates along +B0
    at v_A = |B0|. 2D guide is ê_y; 3D guide is ê_z. Qin-projected.
    """
    N, L, dim = int(grid["N"]), float(grid["L"]), int(grid["dim"])
    x = jnp.linspace(0.0, L, N, endpoint=False)
    amp = float(amp)
    if dim == 2:
        X, Y = jnp.meshgrid(x, x, indexing="ij")
        ux = amp * jnp.sin(2 * jnp.pi * Y / L)
        uy = jnp.zeros_like(X)
        u = jnp.stack([ux, uy])
    else:
        X, Y, Z = jnp.meshgrid(x, x, x, indexing="ij")
        z = jnp.zeros_like(X)
        ux = amp * jnp.sin(2 * jnp.pi * Z / L)
        u = jnp.stack([ux, z, z])
    u_hat = project_div_free(jnp.fft.fftn(u, axes=range(1, dim + 1)), grid)
    return jnp.fft.ifftn(u_hat, axes=range(1, dim + 1)).real


def generate_b_ext(grid, B0=0.08, kind="z", profile="midplane", width=0.12):
    """Static freeze-out field. Midplane pile-up is div-free and supplies
    magnetic pressure −∇(B_ext²/2) that opposes Crow inflow without being
    wound into a current sheet (∂t B_ext = 0, not in induction).

    uniform : constant guide (J_ext = 0 → no force until fluctuations exist)
    midplane: Gaussian in the tube-separation coordinate y
    """
    N, L, dim = int(grid["N"]), float(grid["L"]), int(grid["dim"])
    x = jnp.linspace(0.0, L, N, endpoint=False)
    B0, w = float(B0), float(width)
    if dim == 2:
        X, Y = jnp.meshgrid(x, x, indexing="ij")
        env = jnp.exp(-((Y - 0.5 * L) ** 2) / (2.0 * w * w)) if profile == "midplane" else jnp.ones_like(X)
        if kind == "ot":
            Bx = -B0 * jnp.sin(2 * jnp.pi * Y / L) * env
            By = B0 * jnp.sin(2 * jnp.pi * X / L) * env
        else:
            Bx = jnp.zeros_like(X)
            By = B0 * env
        B = jnp.stack([Bx, By])
    else:
        X, Y, Z = jnp.meshgrid(x, x, x, indexing="ij")
        z = jnp.zeros_like(X)
        env = jnp.exp(-((Y - 0.5 * L) ** 2) / (2.0 * w * w)) if profile == "midplane" else jnp.ones_like(X)
        if kind in ("x", "tube"):
            B = jnp.stack([B0 * env, z, z])
        elif kind == "ot":
            B = jnp.stack([
                -B0 * jnp.sin(2 * jnp.pi * Y / L) * env,
                B0 * jnp.sin(2 * jnp.pi * X / L) * env,
                B0 * 0.2 * jnp.cos(2 * jnp.pi * Z / L) * env,
            ])
        else:
            B = jnp.stack([z, z, B0 * env])
    B_hat = jnp.fft.fftn(B, axes=range(1, dim + 1))
    return project_div_free(B_hat, grid)


def beta_from_lambda_in(lambda_in, chi=0.5):
    """PINP map: ion–neutral coupling Λ_in → Oldroyd-B solvent fraction
    β = η_s / (η_s + η_p). Strong coupling (large Λ_in) → polymer-dominated
    (small β). chi is ionization fraction, reserved for a two-parameter map.
    """
    return 1.0 / (1.0 + float(lambda_in) / max(float(chi), 1e-6))


def generate_b_flux_tubes(grid, mhd_params, ic_params=None):
    """Co-located magnetic flux tubes on the Crow vortex centerlines.

    Shen et al. 2025: b = Γ_m f_t(r) ê_s with the same ê_s, r as ω.
    """
    icp = ic_params or {}
    gm = float(mhd_params.get("gamma_m", 0.0))
    kw = dict(
        radius=icp.get("radius", mhd_params.get("tube_radius", 0.08)),
        separation=icp.get("separation", mhd_params.get("tube_separation", 0.24)),
        perturbation=icp.get("perturbation", mhd_params.get("tube_perturbation", 0.04)),
        axial_wave=icp.get("axial_wave", mhd_params.get("tube_axial_wave", 1)),
    )
    return antiparallel_tube_vector(grid, flux=gm, **kw)


def split_guide_fields(grid, mhd_params, ic_params=None):
    """Advected B_hat + static B_ext_hat from freeze_ext ∈ [0, 1]."""
    B0 = float(mhd_params.get("B0", 0.08))
    kind = mhd_params.get("b_guide", "z")
    freeze = float(mhd_params.get("freeze_ext", 0.0))
    profile = mhd_params.get("ext_profile", "midplane")
    width = float(mhd_params.get("ext_width", 0.12))
    if kind in ("flux", "flux_tubes", "shen"):
        B_hat = generate_b_flux_tubes(grid, mhd_params, ic_params)
    else:
        B_hat = generate_b0(
            grid, B0=B0 * (1.0 - freeze), kind=kind,
            amp=float(mhd_params.get("alfven_amp", 0.01)))
    if bool(mhd_params.get("harris", False)):
        from .es_lhdi import generate_harris_sheet, generate_harris_edge_seed
        hw = float(mhd_params.get("harris_width", 0.08))
        B_hat = B_hat + generate_harris_sheet(
            grid, B0=B0, width=hw, kind=kind)
        edge = float(mhd_params.get("harris_edge", 0.0))
        if edge != 0.0:
            B_hat = B_hat + generate_harris_edge_seed(
                grid, amp=edge * B0, width=hw)
        B_hat = project_div_free(B_hat, grid)
    if freeze == 0.0:
        B_ext = zero_b_hat(grid, dtype=B_hat.dtype)
    else:
        B_ext = generate_b_ext(grid, B0=B0 * freeze, kind=kind,
                               profile=profile, width=width)
    induct = mhd_params.get("induct_ext")
    if induct is None:
        # Frozen B_ext is Lorentz-only. Advected (1-freeze)*B0 is the
        # only field induction may stretch. Midplane pile-up is a
        # gradient in incompressible vorticity form (Helmholtz kills it).
        induct = 0.0 if freeze > 0.0 else 1.0
    return B_hat, B_ext, float(induct)


def cfl_dt_mhd(u, B, dx, nu, eta_mag, cfl=0.4, d_i=0.0):
    """Advective + Alfvén + (viscous, resistive) CFL."""
    umax = jnp.max(jnp.sqrt(jnp.sum(u**2, axis=0)))
    bmax = jnp.max(jnp.sqrt(jnp.sum(B**2, axis=0)))
    hall = (jnp.pi ** 2) * jnp.abs(d_i) * bmax / (dx + 1e-30)
    return cfl * dx / (umax + bmax + 4.0 * (nu + eta_mag) / dx + hall + 1e-12)


@jit
def _curl_2d5(v_hat, grid):
    """curl of a 3-vector on a 2D grid (dz = 0). v_hat is (3, N, N).

    2.5D Hall needs Bz: in-plane-only Faraday of (J x B) is identically
    zero, so whistlers live in (Bx, By, Bz) even when hydro is 2-D.
    """
    kx, ky = grid["k"]
    dealias = grid["dealias"]
    return jnp.stack([
        1j * ky * v_hat[2],
        -1j * kx * v_hat[2],
        1j * (kx * v_hat[1] - ky * v_hat[0]),
    ]) * dealias


def _project_b_2d5(B_hat, grid):
    """Qin on in-plane B; dealias Bz. 2D k_stack cannot project 3-comp."""
    xy = project_div_free(B_hat[:2], grid)
    bz = B_hat[2] * grid["dealias"]
    return jnp.concatenate([xy, bz[None]], axis=0)


def _glm_grad_psi_for_b(psi_hat, B_hat, grid):
    """-grad psi with a zero z-row when B is 2.5D (3-comp on 2D grid)."""
    g = glm_grad_psi(psi_hat, grid)
    if B_hat.shape[0] == 3 and g.shape[0] == 2:
        return jnp.concatenate([g, jnp.zeros_like(g[:1])], axis=0)
    return g


@jit
def current_from_b(B_hat, grid):
    """Ĵ = ik × B̂  (2D returns scalar J_z)."""
    if B_hat.shape[0] == 2:
        return _vort_from_u_2d(B_hat, grid)
    if B_hat.ndim == 3:
        return _curl_2d5(B_hat, grid)
    return ik_cross(B_hat, grid) * grid["dealias"]


@jit
def _lorentz_vort_2d(B_hat, grid):
    """curl_z(J × B) in 2D: J = J_z ê_z, J×B = J (−By, Bx)."""
    Jz = jnp.fft.ifftn(current_from_b(B_hat, grid)).real
    B = jnp.fft.ifftn(B_hat, axes=(1, 2)).real
    fx = -Jz * B[1]
    fy = Jz * B[0]
    f_hat = jnp.stack([jnp.fft.fftn(fx), jnp.fft.fftn(fy)]) * grid["dealias"]
    return _vort_from_u_2d(f_hat, grid) * grid["dealias"]


@jit
def _lorentz_vort_3d(B_hat, grid):
    """curl(J × B) — vorticity source from the Lorentz force."""
    J = jnp.fft.ifftn(ik_cross(B_hat, grid), axes=(1, 2, 3)).real
    B = jnp.fft.ifftn(B_hat, axes=(1, 2, 3)).real
    L = jnp.stack([
        J[1] * B[2] - J[2] * B[1],
        J[2] * B[0] - J[0] * B[2],
        J[0] * B[1] - J[1] * B[0],
    ])
    return ik_cross(jnp.fft.fftn(L, axes=(1, 2, 3)), grid) * grid["dealias"]


@jit
def _lorentz_vort_2d5(B_hat, grid):
    """curl_z(J x B) for 2.5D B (3, N, N). Bz=0 reduces to _lorentz_vort_2d.

    This is still the ion Lorentz force, not a Hall body force.
    """
    J = jnp.fft.ifftn(_curl_2d5(B_hat, grid), axes=(1, 2)).real
    B = jnp.fft.ifftn(B_hat, axes=(1, 2)).real
    fx = J[1] * B[2] - J[2] * B[1]
    fy = J[2] * B[0] - J[0] * B[2]
    f_hat = jnp.stack([jnp.fft.fftn(fx), jnp.fft.fftn(fy)]) * grid["dealias"]
    return _vort_from_u_2d(f_hat, grid) * grid["dealias"]


def lorentz_vorticity_force(B_hat, grid):
    if B_hat.shape[0] == 2:
        return _lorentz_vort_2d(B_hat, grid)
    if B_hat.ndim == 3:
        return _lorentz_vort_2d5(B_hat, grid)
    return _lorentz_vort_3d(B_hat, grid)


def _hyper_mask(grid, hyper_kcut):
    """1 on modes with k ≥ hyper_kcut k_max. hyper_kcut=0 → all modes."""
    k2 = grid["k2"]
    kmax2 = jnp.max(k2)
    return jnp.where(k2 >= (hyper_kcut ** 2) * kmax2, 1.0, 0.0)


@jit
def _induction_2d(B_hat, u_hat, grid, eta_mag, B_cross_hat, eta_hyper, hyper_kcut):
    """∂t B = ∇×(u×B_cross) − η ∇×J(B) − η_h ∇⁴B. Freeze-out: B_cross omits B_ext."""
    u = jnp.fft.ifftn(u_hat, axes=(1, 2)).real
    B = jnp.fft.ifftn(B_cross_hat, axes=(1, 2)).real
    cross_z = u[0] * B[1] - u[1] * B[0]
    c_hat = jnp.fft.fftn(cross_z) * grid["dealias"]
    # curl(0,0,c) = (∂c/∂y, −∂c/∂x)
    rhs = jnp.stack([
        1j * grid["k"][1] * c_hat,
        -1j * grid["k"][0] * c_hat,
    ]) * grid["dealias"]
    mask = _hyper_mask(grid, hyper_kcut)
    return rhs - (eta_mag * grid["k2"] + eta_hyper * mask * grid["k2"] ** 2) * B_hat


@jit
def _induction_3d(B_hat, u_hat, grid, eta_mag, B_cross_hat, eta_hyper, hyper_kcut):
    u = jnp.fft.ifftn(u_hat, axes=(1, 2, 3)).real
    B = jnp.fft.ifftn(B_cross_hat, axes=(1, 2, 3)).real
    cross = jnp.stack([
        u[1] * B[2] - u[2] * B[1],
        u[2] * B[0] - u[0] * B[2],
        u[0] * B[1] - u[1] * B[0],
    ])
    rhs = ik_cross(jnp.fft.fftn(cross, axes=(1, 2, 3)), grid) * grid["dealias"]
    mask = _hyper_mask(grid, hyper_kcut)
    return rhs - (eta_mag * grid["k2"] + eta_hyper * mask * grid["k2"] ** 2) * B_hat


@jit
def _hall_induction_3d(B_cross_hat, grid, d_i, n_hall):
    """-curl((d_i/n) J x B). d_i=0 is the zero field (ideal+resistive MHD).

    n_hall may be a scalar (uniform n) or a real-space density array.
    Multiply (d_i/n)*(J x B) in real space before the curl so a spatial
    Harris n is not pulled out of nabla x. Scalar n recovers the old Ohm.
    """
    J = jnp.fft.ifftn(ik_cross(B_cross_hat, grid), axes=(1, 2, 3)).real
    B = jnp.fft.ifftn(B_cross_hat, axes=(1, 2, 3)).real
    JxB = jnp.stack([
        J[1] * B[2] - J[2] * B[1],
        J[2] * B[0] - J[0] * B[2],
        J[0] * B[1] - J[1] * B[0],
    ])
    invn = 1.0 / (jnp.asarray(n_hall) + 1e-30)
    E_h = d_i * invn * JxB
    return -ik_cross(jnp.fft.fftn(E_h, axes=(1, 2, 3)), grid) * grid["dealias"]


@jit
def _induction_2d5(B_hat, u_hat, grid, eta_mag, B_cross_hat, eta_hyper, hyper_kcut,
                   d_i, n_hall):
    """2.5D Faraday: dt B = -curl E, E = -u x B + eta J + (d_i/n) J x B.

    u is 2-comp (uz=0). In-plane ideal+resistive matches _induction_2d
    when Bz=0 and d_i=0; Hall then seeds Bz and whistlers.
    """
    u = jnp.fft.ifftn(u_hat, axes=(1, 2)).real
    B = jnp.fft.ifftn(B_cross_hat, axes=(1, 2)).real
    # uz = 0: u x B = (uy Bz, -ux Bz, ux By - uy Bx)
    cross = jnp.stack([
        u[1] * B[2],
        -u[0] * B[2],
        u[0] * B[1] - u[1] * B[0],
    ])
    rhs = _curl_2d5(jnp.fft.fftn(cross, axes=(1, 2)), grid)
    mask = _hyper_mask(grid, hyper_kcut)
    rhs = rhs - (eta_mag * grid["k2"] + eta_hyper * mask * grid["k2"] ** 2) * B_hat
    J = jnp.fft.ifftn(_curl_2d5(B_cross_hat, grid), axes=(1, 2)).real
    JxB = jnp.stack([
        J[1] * B[2] - J[2] * B[1],
        J[2] * B[0] - J[0] * B[2],
        J[0] * B[1] - J[1] * B[0],
    ])
    invn = 1.0 / (jnp.asarray(n_hall) + 1e-30)
    E_h = d_i * invn * JxB
    hall = -_curl_2d5(jnp.fft.fftn(E_h, axes=(1, 2)), grid)
    return rhs + hall


def induction_rhs(B_hat, u_hat, grid, eta_mag, B_cross_hat=None, eta_hyper=0.0,
                  hyper_kcut=0.0, psi_hat=None, glm_ch=0.0, d_i=0.0, n_hall=1.0):
    """dt B = -curl E (+ GLM). Hall Ohm is (d_i/n) J x B; d_i=0 is MHD.

    Keyword d_i/n_hall default so mode=cmhd callers stay resistive MHD.
    n_hall may be scalar or real-space n. d_i=0 does not rewrite Qin MHD.
    """
    if B_cross_hat is None:
        B_cross_hat = B_hat
    if B_hat.shape[0] == 2:
        dB = _induction_2d(B_hat, u_hat, grid, eta_mag, B_cross_hat, eta_hyper,
                           hyper_kcut)
        # 2-comp in-plane Hall Faraday is identically 0 (curl of JxB is ez).
    elif B_hat.ndim == 3:
        dB = _induction_2d5(B_hat, u_hat, grid, eta_mag, B_cross_hat, eta_hyper,
                            hyper_kcut, d_i, n_hall)
    else:
        dB = _induction_3d(B_hat, u_hat, grid, eta_mag, B_cross_hat, eta_hyper,
                           hyper_kcut)
        hall = _hall_induction_3d(B_cross_hat, grid, d_i, n_hall)
        dB = jnp.where(d_i != 0.0, dB + hall, dB)
    if psi_hat is not None and glm_ch != 0.0:
        dB = dB + _glm_grad_psi_for_b(psi_hat, B_hat, grid)
    return dB


@jit
def _twofluid_induction_2d(B_hat, u_hat, n_hat, grid, eta_mag, B_cross_hat,
                           eta_hyper, hyper_kcut, d_i, T_e):
    """2-comp Faraday. T_e=0 matches _induction_2d.

    In-plane Hall Faraday of (J x B) is identically 0 (caller uses 2.5D
    when d_i>0, same as hall). Electron-pressure E is in-plane, so it
    does not update in-plane B. n_hat/d_i/T_e kept for a uniform signature.
    """
    return _induction_2d(
        B_hat, u_hat, grid, eta_mag, B_cross_hat, eta_hyper, hyper_kcut)


@jit
def _twofluid_induction_2d5(B_hat, u_hat, n_hat, grid, eta_mag, B_cross_hat,
                            eta_hyper, hyper_kcut, d_i, T_e):
    """2.5D Faraday: dt B = -curl E (Qin/GLM applied by the caller).

    E = -u_e x B - grad(p_e)/n + eta J
    u_e = u_i - (d_i/n) J , p_e = n T_e (T_e const; no electron inertia).
    T_e=0 and n=const recovers hall _induction_2d5 (same d_i).
    u is 2-comp (uz=0). Ion Lorentz is not this routine.
    """
    u = jnp.fft.ifftn(u_hat, axes=(1, 2)).real
    B = jnp.fft.ifftn(B_cross_hat, axes=(1, 2)).real
    n = jnp.fft.ifftn(n_hat).real
    J = jnp.fft.ifftn(_curl_2d5(B_cross_hat, grid), axes=(1, 2)).real
    invn = 1.0 / (n + 1e-30)
    ue = jnp.stack([
        u[0] - d_i * invn * J[0],
        u[1] - d_i * invn * J[1],
        -d_i * invn * J[2],
    ])
    cross = jnp.stack([
        ue[1] * B[2] - ue[2] * B[1],
        ue[2] * B[0] - ue[0] * B[2],
        ue[0] * B[1] - ue[1] * B[0],
    ])
    rhs = _curl_2d5(jnp.fft.fftn(cross, axes=(1, 2)), grid)
    mask = _hyper_mask(grid, hyper_kcut)
    rhs = rhs - (eta_mag * grid["k2"] + eta_hyper * mask * grid["k2"] ** 2) * B_hat
    gn = jnp.fft.ifftn(1j * grid["k_stack"] * n_hat, axes=(1, 2)).real
    gpx = T_e * gn[0] * invn
    gpy = T_e * gn[1] * invn
    pe_hat = jnp.stack([
        jnp.fft.fftn(gpx),
        jnp.fft.fftn(gpy),
        jnp.zeros_like(n_hat),
    ])
    return rhs + _curl_2d5(pe_hat, grid)


@jit
def _twofluid_induction_3d(B_hat, u_hat, n_hat, grid, eta_mag, B_cross_hat,
                           eta_hyper, hyper_kcut, d_i, T_e):
    """3D Faraday for twofluid Ohm. T_e=0 and n=const recovers Hall."""
    u = jnp.fft.ifftn(u_hat, axes=(1, 2, 3)).real
    B = jnp.fft.ifftn(B_cross_hat, axes=(1, 2, 3)).real
    n = jnp.fft.ifftn(n_hat).real
    J = jnp.fft.ifftn(ik_cross(B_cross_hat, grid), axes=(1, 2, 3)).real
    invn = 1.0 / (n + 1e-30)
    ue = u - d_i * invn * J
    cross = jnp.stack([
        ue[1] * B[2] - ue[2] * B[1],
        ue[2] * B[0] - ue[0] * B[2],
        ue[0] * B[1] - ue[1] * B[0],
    ])
    rhs = ik_cross(jnp.fft.fftn(cross, axes=(1, 2, 3)), grid) * grid["dealias"]
    mask = _hyper_mask(grid, hyper_kcut)
    rhs = rhs - (eta_mag * grid["k2"] + eta_hyper * mask * grid["k2"] ** 2) * B_hat
    gn = jnp.fft.ifftn(1j * grid["k_stack"] * n_hat, axes=(1, 2, 3)).real
    gp = T_e * gn * invn
    return rhs + ik_cross(jnp.fft.fftn(gp, axes=(1, 2, 3)), grid) * grid["dealias"]


def twofluid_induction_rhs(B_hat, u_hat, n_hat, grid, eta_mag,
                           B_cross_hat=None, eta_hyper=0.0, hyper_kcut=0.0,
                           psi_hat=None, glm_ch=0.0, d_i=0.0, T_e=0.0):
    """dt B = -curl E (+ GLM). Two-fluid Ohm, no electron inertia.

    E = -u_e x B - grad(p_e)/n + eta J, u_e = u_i - (d_i/n) J, p_e = n T_e.
    T_e=0 and n=const is the Hall Ohm. d_i=0 and T_e=0 is MHD.
    mode=cmhd does not call this (induction_rhs keeps d_i=0 default).
    """
    if B_cross_hat is None:
        B_cross_hat = B_hat
    if B_hat.shape[0] == 2:
        dB = _twofluid_induction_2d(
            B_hat, u_hat, n_hat, grid, eta_mag, B_cross_hat, eta_hyper,
            hyper_kcut, d_i, T_e)
    elif B_hat.ndim == 3:
        dB = _twofluid_induction_2d5(
            B_hat, u_hat, n_hat, grid, eta_mag, B_cross_hat, eta_hyper,
            hyper_kcut, d_i, T_e)
    else:
        dB = _twofluid_induction_3d(
            B_hat, u_hat, n_hat, grid, eta_mag, B_cross_hat, eta_hyper,
            hyper_kcut, d_i, T_e)
    if psi_hat is not None and glm_ch != 0.0:
        dB = dB + _glm_grad_psi_for_b(psi_hat, B_hat, grid)
    return dB


def glm_grad_psi(psi_hat, grid):
    """-grad psi in Fourier space (Dedner hyperbolic flux)."""
    return -1j * grid["k_stack"] * psi_hat * grid["dealias"]


def glm_psi_rhs(psi_hat, B_hat, grid, glm_ch, glm_cr):
    """dt psi = -c_h^2 div B - (c_h / (c_r dx)) psi."""
    divB_hat = 1j * jnp.sum(grid["k_stack"] * B_hat, axis=0)
    ch = glm_ch
    alpha = ch / (glm_cr * grid["dx"] + 1e-30)
    return (-ch * ch * divB_hat - alpha * psi_hat) * grid["dealias"]


@jit
def _odd_vort_2d(u_hat, grid, eta_odd):
    """Work-free 2-D odd viscosity: σ:S = 0.

    σ_xx = 2 η_o S_xy, σ_xy = η_o (S_yy − S_xx), σ_yy = −2 η_o S_xy.
    On a periodic torus this force is a gradient for incompressible u
    and is therefore killed by the Helmholtz projector; kept so D₃ᵒ
    can be monitored when eta_odd ≠ 0.
    """
    k = grid["k_stack"]
    ghat = 1j * u_hat[:, None] * k[None, :]
    grad = jnp.fft.ifftn(ghat, axes=(2, 3)).real
    S = 0.5 * (grad + jnp.swapaxes(grad, 0, 1))
    sxx, sxy, syy = S[0, 0], S[0, 1], S[1, 1]
    sig = eta_odd * jnp.stack([
        jnp.stack([2.0 * sxy, syy - sxx]),
        jnp.stack([syy - sxx, -2.0 * sxy]),
    ])
    sig_hat = jnp.fft.fftn(sig, axes=(2, 3))
    f_hat = 1j * jnp.einsum("j...,ij...->i...", k, sig_hat)
    return _vort_from_u_2d(f_hat, grid) * grid["dealias"]


@jit
def _odd_vort_3d(u_hat, B_hat, grid, eta_odd, berry_gain):
    """3-D gyro/odd force η_o n̂ × ∇²u, n̂ = B/|B|.

    berry_gain > 0 scales η_o locally by (1 + berry_gain |B|/<|B|>),
    the leading magnetic-field layer of the Berry-odd tensor.
    """
    B = jnp.fft.ifftn(B_hat, axes=(1, 2, 3)).real
    bn = jnp.sqrt(jnp.sum(B**2, axis=0) + 1e-30)
    n = B / bn
    eta = eta_odd * (1.0 + berry_gain * bn / (jnp.mean(bn) + 1e-30))
    lap_u = jnp.fft.ifftn(-grid["k2"] * u_hat, axes=(1, 2, 3)).real
    f = eta * jnp.stack([
        n[1] * lap_u[2] - n[2] * lap_u[1],
        n[2] * lap_u[0] - n[0] * lap_u[2],
        n[0] * lap_u[1] - n[1] * lap_u[0],
    ])
    return ik_cross(jnp.fft.fftn(f, axes=(1, 2, 3)), grid) * grid["dealias"]


def odd_vorticity_force(u_hat, B_hat, grid, eta_odd, berry_gain=0.0):
    if u_hat.shape[0] == 2:
        return _odd_vort_2d(u_hat, grid, eta_odd)
    return _odd_vort_3d(u_hat, B_hat, grid, eta_odd, berry_gain)


@jit
def _mhd_diag_2d(B_hat, u_hat, grid, eta_mag, tau_hat, B_ext_hat, eta_hyper):
    B = jnp.fft.ifftn(B_hat, axes=(1, 2)).real
    Bext = jnp.fft.ifftn(B_ext_hat, axes=(1, 2)).real
    Btot = B + Bext
    u = jnp.fft.ifftn(u_hat, axes=(1, 2)).real
    e_kin = 0.5 * jnp.mean(jnp.sum(u**2, axis=0))
    e_mag = 0.5 * jnp.mean(jnp.sum(B**2, axis=0))
    e_mag_ext = 0.5 * jnp.mean(jnp.sum(Bext**2, axis=0))
    e_mag_tot = 0.5 * jnp.mean(jnp.sum(Btot**2, axis=0))
    Btot_hat = B_hat + B_ext_hat
    J_hat = current_from_b(Btot_hat, grid)
    J = jnp.fft.ifftn(J_hat).real
    j2 = J**2
    A = jnp.fft.ifftn(J_hat / grid["k2"]).real
    JxB_x = -J * Btot[1]
    JxB_y = J * Btot[0]
    lorentz_work = jnp.mean(u[0] * JxB_x + u[1] * JxB_y)
    Tm = jnp.mean(jnp.sum(Btot**2, axis=0))
    tau = jnp.fft.ifftn(tau_hat, axes=(2, 3)).real
    n_tau = jnp.sqrt(jnp.mean(jnp.sum(tau**2, axis=(0, 1))))
    divB = jnp.fft.ifftn(jnp.sum(grid["k_stack"] * Btot_hat, axis=0)).real
    ghat = 1j * Btot_hat[:, None] * grid["k_stack"][None, :]
    g = jnp.fft.ifftn(ghat, axes=(2, 3)).real
    smax = jnp.max(jnp.sqrt(jnp.sum(g**2, axis=(0, 1))))
    lam_min = jnp.minimum(grid["L"], 1.0 / (smax + 1e-30))
    lorentz_n = jnp.mean(jnp.sqrt(JxB_x**2 + JxB_y**2))
    lapB = jnp.fft.ifftn(grid["k2"] * Btot_hat, axes=(1, 2)).real
    hyper_ohmic = eta_hyper * jnp.mean(jnp.sum(lapB**2, axis=0))
    ughat = 1j * u_hat[:, None] * grid["k_stack"][None, :]
    gu = jnp.fft.ifftn(ughat, axes=(2, 3)).real
    Su = 0.5 * (gu + jnp.swapaxes(gu, 0, 1))
    stretch_loc = jnp.einsum("i...,ij...,j...->...", Btot, Su, Btot)
    div_u = jnp.fft.ifftn(jnp.sum(grid["k_stack"] * u_hat, axis=0)).real
    b2 = jnp.sum(Btot**2, axis=0)
    comp_loc = -0.5 * b2 * div_u
    jmag = jnp.abs(J)
    w = j2
    wsum = jnp.mean(w) + 1e-30
    b_stretch = jnp.mean(stretch_loc)
    b_comp = jnp.mean(comp_loc)
    b_stretch_j = jnp.mean(w * stretch_loc) / wsum
    b_comp_j = jnp.mean(w * comp_loc) / wsum
    wl_loc = u[0] * JxB_x + u[1] * JxB_y
    wl_j = jnp.mean(w * wl_loc) / wsum
    b2_floor = jnp.mean(b2) * 1e-8 + 1e-30
    K = jnp.zeros_like(jmag)
    K_sheet = jnp.array(0.0)
    j_w = jnp.mean(w * jmag) / wsum
    b_w = jnp.mean(w * jnp.sqrt(b2)) / wsum
    j_over_b_w = j_w / (b_w + 1e-30)
    sheet_ind = j_over_b_w
    N = B.shape[-1]
    half = N // 2
    # Half-plane fluxes: y<L/2 for Bx (Crow midplane), x<L/2 for By (transfer).
    flux_x_half = jnp.mean(Btot[0][:, :half])
    flux_y_half = jnp.mean(Btot[1][:half, :])
    flux_z_half = jnp.array(0.0)
    vort_hat = _vort_from_u_2d(u_hat, grid)
    vort = jnp.fft.ifftn(vort_hat).real
    circ_x_half = jnp.array(0.0)
    circ_y_half = jnp.mean(vort[:, :half])
    Ez = eta_mag * J - (u[0] * Btot[1] - u[1] * Btot[0])
    E_rec = jnp.max(jnp.abs(Ez))
    E_par = jnp.array(0.0)
    E_rec_sheet = jnp.mean(w * Ez) / wsum
    return {
        "e_mag": e_mag,
        "e_mag_ext": e_mag_ext,
        "e_mag_tot": e_mag_tot,
        "ohmic": eta_mag * jnp.mean(j2),
        "hyper_ohmic": hyper_ohmic,
        "max_j": jnp.max(jnp.abs(J)),
        "max_b": jnp.max(jnp.sqrt(jnp.sum(Btot**2, axis=0))),
        "H_mag": jnp.mean(A**2),
        "H_cross": jnp.mean(u[0] * Btot[0] + u[1] * Btot[1]),
        "H_current": jnp.array(0.0),
        "max_div_b": jnp.max(jnp.abs(divB)),
        "lorentz_work": lorentz_work,
        "maxwell": Tm,
        "op_ratio": n_tau / (Tm + 1e-30),
        "N_i": e_mag_tot / (e_kin + 1e-30),
        "N_i_force": lorentz_n / (jnp.mean(jnp.sum(u**2, axis=0)) + 1e-30),
        "lam_min": lam_min,
        "lam_min_dx": lam_min / grid["dx"],
        "P_back": e_mag_ext,
        "b_stretch": b_stretch,
        "b_comp": b_comp,
        "b_stretch_j": b_stretch_j,
        "b_comp_j": b_comp_j,
        "wl_j": wl_j,
        "K_sheet": K_sheet,
        "j_w": j_w,
        "j_over_b_w": j_over_b_w,
        "sheet_ind": sheet_ind,
        "flux_x_half": flux_x_half,
        "flux_y_half": flux_y_half,
        "flux_z_half": flux_z_half,
        "circ_x_half": circ_x_half,
        "circ_y_half": circ_y_half,
        "E_rec": E_rec,
        "E_par": E_par,
        "E_rec_sheet": E_rec_sheet,
    }


@jit
def _mhd_diag_3d(B_hat, u_hat, grid, eta_mag, tau_hat, B_ext_hat, eta_hyper):
    B = jnp.fft.ifftn(B_hat, axes=(1, 2, 3)).real
    Bext = jnp.fft.ifftn(B_ext_hat, axes=(1, 2, 3)).real
    Btot = B + Bext
    u = jnp.fft.ifftn(u_hat, axes=(1, 2, 3)).real
    e_kin = 0.5 * jnp.mean(jnp.sum(u**2, axis=0))
    e_mag = 0.5 * jnp.mean(jnp.sum(B**2, axis=0))
    e_mag_ext = 0.5 * jnp.mean(jnp.sum(Bext**2, axis=0))
    e_mag_tot = 0.5 * jnp.mean(jnp.sum(Btot**2, axis=0))
    Btot_hat = B_hat + B_ext_hat
    J_hat = ik_cross(Btot_hat, grid) * grid["dealias"]
    J = jnp.fft.ifftn(J_hat, axes=(1, 2, 3)).real
    j2 = jnp.sum(J**2, axis=0)
    A = jnp.fft.ifftn(J_hat / grid["k2"], axes=(1, 2, 3)).real
    JxB = jnp.stack([
        J[1] * Btot[2] - J[2] * Btot[1],
        J[2] * Btot[0] - J[0] * Btot[2],
        J[0] * Btot[1] - J[1] * Btot[0],
    ])
    lorentz_work = jnp.mean(jnp.sum(u * JxB, axis=0))
    Tm = jnp.mean(jnp.sum(Btot**2, axis=0))
    tau = jnp.fft.ifftn(tau_hat, axes=(2, 3, 4)).real
    n_tau = jnp.sqrt(jnp.mean(jnp.sum(tau**2, axis=(0, 1))))
    divB = jnp.fft.ifftn(jnp.sum(grid["k_stack"] * Btot_hat, axis=0)).real
    ghat = 1j * Btot_hat[:, None] * grid["k_stack"][None, :]
    g = jnp.fft.ifftn(ghat, axes=(2, 3, 4)).real
    smax = jnp.max(jnp.sqrt(jnp.sum(g**2, axis=(0, 1))))
    lam_min = jnp.minimum(grid["L"], 1.0 / (smax + 1e-30))
    lorentz_n = jnp.mean(jnp.sqrt(jnp.sum(JxB**2, axis=0)))
    lapB = jnp.fft.ifftn(grid["k2"] * Btot_hat, axes=(1, 2, 3)).real
    hyper_ohmic = eta_hyper * jnp.mean(jnp.sum(lapB**2, axis=0))
    ughat = 1j * u_hat[:, None] * grid["k_stack"][None, :]
    gu = jnp.fft.ifftn(ughat, axes=(2, 3, 4)).real
    Su = 0.5 * (gu + jnp.swapaxes(gu, 0, 1))
    stretch_loc = jnp.einsum("i...,ij...,j...->...", Btot, Su, Btot)
    div_u = jnp.fft.ifftn(jnp.sum(grid["k_stack"] * u_hat, axis=0)).real
    b2 = jnp.sum(Btot**2, axis=0)
    comp_loc = -0.5 * b2 * div_u
    jmag = jnp.sqrt(j2)
    w = j2
    wsum = jnp.mean(w) + 1e-30
    b_stretch = jnp.mean(stretch_loc)
    b_comp = jnp.mean(comp_loc)
    b_stretch_j = jnp.mean(w * stretch_loc) / wsum
    b_comp_j = jnp.mean(w * comp_loc) / wsum
    wl_loc = jnp.sum(u * JxB, axis=0)
    wl_j = jnp.mean(w * wl_loc) / wsum
    b2_floor = jnp.mean(b2) * 1e-8 + 1e-30
    K = jnp.sum(J * Btot, axis=0) / (b2 + b2_floor)
    K_sheet = jnp.mean(w * K) / wsum
    j_w = jnp.mean(w * jmag) / wsum
    b_w = jnp.mean(w * jnp.sqrt(b2)) / wsum
    j_over_b_w = j_w / (b_w + 1e-30)
    sheet_ind = j_over_b_w
    N = B.shape[-1]
    half = N // 2
    flux_x_half = jnp.mean(Btot[0][:, :half, :])
    flux_y_half = jnp.mean(Btot[1][:half, :, :])
    flux_z_half = jnp.mean(Btot[2][:, :, :half])
    omega = jnp.fft.ifftn(ik_cross(u_hat, grid), axes=(1, 2, 3)).real
    circ_x_half = jnp.mean(omega[0][:, :half, :])
    circ_y_half = jnp.mean(omega[1][:half, :, :])
    E_par_field = eta_mag * jnp.sum(J * Btot, axis=0) / (jnp.sqrt(b2) + 1e-30)
    E_par = jnp.max(jnp.abs(E_par_field))
    E_rec = E_par
    E_rec_sheet = jnp.mean(w * E_par_field) / wsum
    return {
        "e_mag": e_mag,
        "e_mag_ext": e_mag_ext,
        "e_mag_tot": e_mag_tot,
        "ohmic": eta_mag * jnp.mean(j2),
        "hyper_ohmic": hyper_ohmic,
        "max_j": jnp.max(jnp.sqrt(j2)),
        "max_b": jnp.max(jnp.sqrt(jnp.sum(Btot**2, axis=0))),
        "H_mag": jnp.mean(jnp.sum(A * Btot, axis=0)),
        "H_cross": jnp.mean(jnp.sum(u * Btot, axis=0)),
        "H_current": jnp.mean(jnp.sum(J * Btot, axis=0)),
        "max_div_b": jnp.max(jnp.abs(divB)),
        "lorentz_work": lorentz_work,
        "maxwell": Tm,
        "op_ratio": n_tau / (Tm + 1e-30),
        "N_i": e_mag_tot / (e_kin + 1e-30),
        "N_i_force": lorentz_n / (jnp.mean(jnp.sum(u**2, axis=0)) + 1e-30),
        "lam_min": lam_min,
        "lam_min_dx": lam_min / grid["dx"],
        "P_back": e_mag_ext,
        "b_stretch": b_stretch,
        "b_comp": b_comp,
        "b_stretch_j": b_stretch_j,
        "b_comp_j": b_comp_j,
        "wl_j": wl_j,
        "K_sheet": K_sheet,
        "j_w": j_w,
        "j_over_b_w": j_over_b_w,
        "sheet_ind": sheet_ind,
        "flux_x_half": flux_x_half,
        "flux_y_half": flux_y_half,
        "flux_z_half": flux_z_half,
        "circ_x_half": circ_x_half,
        "circ_y_half": circ_y_half,
        "E_rec": E_rec,
        "E_par": E_par,
        "E_rec_sheet": E_rec_sheet,
    }


def _mhd_diag_2d5(B_hat, u_hat, grid, eta_mag, tau_hat, B_ext_hat, eta_hyper):
    """2.5D meters: 2-comp sheet diagnostics plus full-B energy / Ohmic / divB.

    Hall energy in Bz must sit in e_mag or I_leak looks like a Hall heat term.
    """
    d = _mhd_diag_2d(B_hat[:2], u_hat, grid, eta_mag, tau_hat,
                     B_ext_hat[:2], eta_hyper)
    B = jnp.fft.ifftn(B_hat, axes=(1, 2)).real
    Bext = jnp.fft.ifftn(B_ext_hat, axes=(1, 2)).real
    Btot = B + Bext
    Btot_hat = B_hat + B_ext_hat
    u = jnp.fft.ifftn(u_hat, axes=(1, 2)).real
    d["e_mag"] = 0.5 * jnp.mean(jnp.sum(B**2, axis=0))
    d["e_mag_ext"] = 0.5 * jnp.mean(jnp.sum(Bext**2, axis=0))
    d["e_mag_tot"] = 0.5 * jnp.mean(jnp.sum(Btot**2, axis=0))
    J_hat = _curl_2d5(Btot_hat, grid)
    J = jnp.fft.ifftn(J_hat, axes=(1, 2)).real
    j2 = jnp.sum(J**2, axis=0)
    d["ohmic"] = eta_mag * jnp.mean(j2)
    d["max_j"] = jnp.max(jnp.sqrt(j2))
    d["max_b"] = jnp.max(jnp.sqrt(jnp.sum(Btot**2, axis=0)))
    divB = jnp.fft.ifftn(jnp.sum(grid["k_stack"] * Btot_hat[:2], axis=0)).real
    d["max_div_b"] = jnp.max(jnp.abs(divB))
    lapB = jnp.fft.ifftn(grid["k2"] * Btot_hat, axes=(1, 2)).real
    d["hyper_ohmic"] = eta_hyper * jnp.mean(jnp.sum(lapB**2, axis=0))
    JxB_x = J[1] * Btot[2] - J[2] * Btot[1]
    JxB_y = J[2] * Btot[0] - J[0] * Btot[2]
    d["lorentz_work"] = jnp.mean(u[0] * JxB_x + u[1] * JxB_y)
    d["maxwell"] = jnp.mean(jnp.sum(Btot**2, axis=0))
    e_kin = 0.5 * jnp.mean(jnp.sum(u**2, axis=0))
    d["N_i"] = d["e_mag_tot"] / (e_kin + 1e-30)
    return dict(d)


def mhd_field_diagnostics(B_hat, u_hat, grid, eta_mag, tau_hat=None,
                          B_ext_hat=None, eta_hyper=0.0):
    """Magnetic energy, Ohmic, |J|, helicities, Maxwell, N_i, sheet scale.

    lorentz_work = ⟨u·(J×B)⟩ is a kinetic↔magnetic transfer. It is
    recorded here but excluded from I_leak / energy_leak (E_tot identity
    is Ė_tot + ε_ν + ε_η; Lorentz cancels between the two reservoirs).
    """
    d = int(grid["dim"])
    N = int(grid["N"])
    if tau_hat is None:
        tau_hat = jnp.zeros((d, d) + (N,) * d, dtype=B_hat.real.dtype)
    if B_ext_hat is None:
        B_ext_hat = jnp.zeros_like(B_hat)
    eta_hyper = float(eta_hyper)
    if B_hat.shape[0] == 2:
        return _mhd_diag_2d(B_hat, u_hat, grid, eta_mag, tau_hat, B_ext_hat,
                            eta_hyper)
    if B_hat.ndim == 3:
        return _mhd_diag_2d5(B_hat, u_hat, grid, eta_mag, tau_hat, B_ext_hat,
                             eta_hyper)
    return _mhd_diag_3d(B_hat, u_hat, grid, eta_mag, tau_hat, B_ext_hat,
                        eta_hyper)


def _zero_mhd():
    z = jnp.array(0.0)
    return {
        "e_mag": z, "e_mag_ext": z, "e_mag_tot": z,
        "ohmic": z, "hyper_ohmic": z, "max_j": z, "max_b": z,
        "H_mag": z, "H_cross": z, "H_current": z, "max_div_b": z,
        "lorentz_work": z, "maxwell": z, "op_ratio": z,
        "N_i": z, "N_i_force": z, "ni_paper": z, "ni_paper0": z,
        "ni_li": z, "Re": z, "Rm": z, "Pr_m": z, "v_A": z,
        "lundquist": z, "plasma_beta": z,
        "lam_min": z, "lam_min_dx": z, "P_back": z,
        "b_stretch": z, "b_comp": z, "b_stretch_j": z, "b_comp_j": z,
        "wl_j": z, "K_sheet": z, "j_w": z, "j_over_b_w": z, "sheet_ind": z,
        "max_e": z, "max_charge": z, "es_energy": z, "edge_j": z,
        "flux_x_half": z, "flux_y_half": z, "flux_z_half": z,
        "circ_x_half": z, "circ_y_half": z,
        "E_rec": z, "E_par": z, "E_rec_sheet": z,
        "e_glm": z, "max_psi": z,
    }
