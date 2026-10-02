"""
One operator per family. Not one QG object.
Undefined theories are not given a U(1) nickname.
"""

from __future__ import annotations

import numpy as np

from protocol import DELTA, EPS_EP, X_OFF, X_ON, ratio, undef, verdict

# ---------------------------------------------------------------------------
# Defined on this mesh
# ---------------------------------------------------------------------------


def f01_cs() -> dict:
    op = (
        "Chern–Simons / 3d gravity\n"
        "    S = (k/4π)∫ Tr(A dA + 2/3 A^3), k=8, G=SU(2) or U(1)\n"
        "    2d spatial lattice, CS vacuum F=0, A_ℓ=0\n"
        "    J = |∫_γ A|"
    )
    j_on, j_off = 0.0, 0.0
    r = ratio(j_on, j_off)
    return _row("1 Chern–Simons / 3d gravity", op, j_on, j_off, r, "vacuum A=0", False)


def f03_spinfoam() -> dict:
    op = (
        "Spin foam (2d)\n"
        "    Z = ∑_{j_f} ∏_faces dim(j)  with flatness: only j compatible with F=0\n"
        "    on this mesh every face amplitude is 1 (no curvature)\n"
        "    J = |Z_path − 1| = 0"
    )
    j_on, j_off = 0.0, 0.0
    r = ratio(j_on, j_off)
    return _row("3 Spin foam", op, j_on, j_off, r, "flat foam", False)


def f04_bf() -> dict:
    op = (
        "BF theory\n"
        "    S = ∫ B ∧ F\n"
        "    eom F=0, B free; no δ_Γ source\n"
        "    J = |∮ F along the short path| = 0"
    )
    j_on, j_off = 0.0, 0.0
    r = ratio(j_on, j_off)
    return _row("4 BF theory", op, j_on, j_off, r, "F=0", False)


def f06_cdt() -> dict:
    op = (
        "Causal dynamical triangulations (2d strip)\n"
        "    S = λ N_2, regular causal ladder (diamonds), T=8 slices\n"
        "    J = number of dual edges that meet the vertical probe\n"
        "    no Γ in the action"
    )
    # one dual edge per slice, independent of x
    t_slices = 8
    j_on = float(t_slices)
    j_off = float(t_slices)
    r = ratio(j_on, j_off)
    return _row("6 Causal dynamical triangulations", op, j_on, j_off, r, "uniform ladder", False)


def f07_edt() -> dict:
    op = (
        "Euclidean dynamical triangulations (2d)\n"
        "    S = λ N_2, regular triangulation of the rectangle\n"
        "    J = number of edges dual-crossing the vertical probe\n"
        "    no Γ in the action"
    )
    j_on = 8.0
    j_off = 8.0
    r = ratio(j_on, j_off)
    return _row("7 Euclidean dynamical triangulations", op, j_on, j_off, r, "uniform triangulation", False)


def f08_csets() -> dict:
    op = (
        "Causal sets\n"
        "    sprinkle N=250 points in [-2,2]², Minkowski t=Im, x=Re\n"
        "    link if timelike; J = mean number of links that meet the probe (12 sprinklings)"
    )
    def crosses(x1, t1, x2, t2, xv: float) -> bool:
        if (x1 - xv) * (x2 - xv) > 0:
            return False
        if abs(x2 - x1) < 1e-15:
            return False
        s = (xv - x1) / (x2 - x1)
        if s < 0.0 or s > 1.0:
            return False
        tt = t1 + s * (t2 - t1)
        return abs(tt) <= DELTA + 1e-12

    n = 250
    n_spr = 12
    acc_on = 0.0
    acc_off = 0.0
    for seed in range(n_spr):
        rng = np.random.default_rng(seed)
        x = rng.uniform(-2, 2, n)
        t = rng.uniform(-2, 2, n)
        jon = joff = 0
        for i in range(n):
            for j in range(i + 1, n):
                dt = abs(t[j] - t[i])
                dx = abs(x[j] - x[i])
                if dt <= dx + 1e-15:
                    continue
                if crosses(x[i], t[i], x[j], t[j], X_ON):
                    jon += 1
                if crosses(x[i], t[i], x[j], t[j], X_OFF):
                    joff += 1
        acc_on += jon
        acc_off += joff
    j_on = acc_on / n_spr
    j_off = acc_off / n_spr
    r = ratio(j_on, j_off)
    return _row("8 Causal sets", op, j_on, j_off, r, f"mean of {n_spr} sprinklings", False)


def f09_worldsheet() -> dict:
    op = (
        "Worldsheet string\n"
        "    S_Nambu = ∫ dλ √(ẋ²) = 2δ on both probes\n"
        "    no wall weight"
    )
    j_on = 2.0 * DELTA
    j_off = 2.0 * DELTA
    r = ratio(j_on, j_off)
    return _row("9 Worldsheet string", op, j_on, j_off, r, "equal length", False)


def f12_holo() -> dict:
    op = (
        "AdS/CFT holographic defect\n"
        "    3-layer bulk ds²=dr²+(1+r)² dx²\n"
        "    boundary field χ=βx, β=1/3, no slit in χ\n"
        "    J=|χ(x+iδ)−χ(x−iδ)|"
    )
    j_on, j_off = 0.0, 0.0  # χ depends only on x
    r = ratio(j_on, j_off)
    return _row("12 AdS/CFT holographic defect", op, j_on, j_off, r, "smooth χ=βx", False)


def f18_teleparallel() -> dict:
    op = (
        "Teleparallel / gauge gravity\n"
        "    Weitzenböck: ω=0, e^a=dx^a, torsion T=de=0\n"
        "    J=|∫_γ T|"
    )
    j_on, j_off = 0.0, 0.0
    r = ratio(j_on, j_off)
    return _row("18 Teleparallel / gauge gravity", op, j_on, j_off, r, "T=0", False)


def f20_hybrid(cs: dict, holo: dict) -> dict:
    op = (
        "Akitti hybrid\n"
        "    J_h = hypot(J_CS, J_holo) on the same meridian\n"
        "    after family 1 and family 12 already have rows\n"
        "    not n_MHD"
    )
    j_on = float(np.hypot(cs["J_on"], holo["J_on"]))
    j_off = float(np.hypot(cs["J_off"], holo["J_off"]))
    r = ratio(j_on, j_off)
    return _row("20 Akitti hybrid (CS + holo)", op, j_on, j_off, r, "hypot(1,12)", False)


def f21_u1() -> dict:
    op = (
        "Uniform U(1) control\n"
        "    A=(−By/2, Bx/2), B=1\n"
        "    J=|B x δ|  (larger off the slit)"
    )
    j_on = abs(1.0 * X_ON * DELTA)
    j_off = abs(1.0 * X_OFF * DELTA)
    r = ratio(j_on, j_off)
    return _row("21 Uniform U(1) control", op, j_on, j_off, r, "x=0.25 vs 1.2", False)


# ---------------------------------------------------------------------------
# Could not define on this mesh without faking a nickname
# ---------------------------------------------------------------------------


def f02_lqg() -> dict:
    return undef(
        "2 Ashtekar–Barbero / canonical LQG",
        "Needs a 3d spatial graph, SU(2) spin networks, densitized triad, "
        "Hamiltonian constraint. This slit is a 2d label plane, not a 3-geometry. "
        "No fake holonomy.",
    )


def f05_gft() -> dict:
    return undef(
        "5 Group field theory",
        "Needs a field on G^d (typically SU(2)^4) and a combinatorially nonlocal "
        "action. Not a 2d mesh theory. No fake holonomy.",
    )


def f10_sft() -> dict:
    return undef(
        "10 String field theory",
        "Cubic/closed SFT lives on the string Hilbert space, not on this slit mesh. "
        "No fake holonomy.",
    )


def f11_mtheory() -> dict:
    return undef(
        "11 Supergravity / M-theory reduction",
        "11d / 10d SUGRA plus compactification. No 2d-mesh reduction here without "
        "inventing a U(1) nickname.",
    )


def f13_as() -> dict:
    return undef(
        "13 Asymptotic safety (truncation)",
        "FRG in theory space (g, λ, …). No local lattice letter on γ_cross. "
        "No fake holonomy.",
    )


def f14_hl() -> dict:
    return undef(
        "14 Hořava–Lifshitz",
        "Anisotropic z=3 gravity on a spacetime foliation. Not defined on this "
        "2d MHD-label mesh. No fake holonomy.",
    )


def f15_twistor() -> dict:
    return undef(
        "15 Twistor / ambitwistor",
        "CP^3 incidence / ambitwistor string. The ε-plane is not twistor space. "
        "No fake holonomy.",
    )


def f16_shape() -> dict:
    return undef(
        "16 Shape dynamics",
        "Conformal 3-geometry, York time, refoliation-invariant Hamiltonian. "
        "No 3-geometry here. No fake holonomy.",
    )


def f17_ncg() -> dict:
    return undef(
        "17 Noncommutative geometry",
        "Connes triple (A,H,D) or Moyal plane. No spectral triple for this slit "
        "without putting Γ into D by hand. No fake holonomy.",
    )


def f19_lqc() -> dict:
    return undef(
        "19 Loop quantum cosmology letter on this slit",
        "LQC is holonomy-corrected FRW (μ-bar, volume operator on a cosmological "
        "cell). This slit is not a minisuperspace. No fake holonomy.",
    )


def _row(name, op, j_on, j_off, r, wall_site, inserted) -> dict:
    return {
        "family": name,
        "operator": op,
        "J_on": float(j_on),
        "J_off": float(j_off),
        "ratio": float(r),
        "wall_site": wall_site,
        "verdict": verdict(True, inserted, r, j_on, j_off),
        "defined": True,
        "inserted": inserted,
    }
