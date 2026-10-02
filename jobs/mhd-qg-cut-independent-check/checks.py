"""I1–I4. Γ is used only to SCORE, never to build A."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from gravity_g1 import (
    B_FIELD,
    Lattice,
    build_lattice,
    cs_density,
    scramble,
    wilson_theta_scan,
)
from mhd_letter import EPS_EP, Gamma, n_mhd_around_endpoint


@dataclass
class IRow:
    name: str
    formula: str
    number: str
    passed: bool
    note: str


def _gamma_mask(xc: np.ndarray, yc: np.ndarray, lo: float, hi: float, band: float) -> np.ndarray:
    """Plaquette centres on the slit: real axis, x∈Γ, |y| < band."""
    X, Y = np.meshgrid(xc, yc, indexing="xy")
    return (X >= lo) & (X <= hi) & (np.abs(Y) <= band)


def i1_support(lat: Lattice) -> tuple[IRow, dict]:
    lo, hi = Gamma(EPS_EP)
    band = 2.0 * lat.dy
    on = _gamma_mask(lat.xc, lat.yc, lo, hi, band)
    rho = np.abs(cs_density(lat))
    on_mean = float(np.mean(rho[on])) if np.any(on) else float("nan")
    off_mean = float(np.mean(rho[~on])) if np.any(~on) else float("nan")
    ratio = on_mean / (off_mean + 1e-16)
    # peak on Γ without being told Γ: require on/off ≫ 1
    passed = bool(ratio > 3.0)
    row = IRow(
        name="I1 support",
        formula=r"\overline{|F|/2\pi}_{\mathrm{on}\,\Gamma}\ /\ \overline{|F|/2\pi}_{\mathrm{off}\,\Gamma}",
        number=f"on={on_mean:.6g}, off={off_mean:.6g}, ratio={ratio:.4f} (need >3 to peak on Γ)",
        passed=passed,
        note="CS density of uniform-B lattice. Γ used only as a mask after A is built.",
    )
    return row, {"rho": rho, "on": on, "ratio": ratio, "lo": lo, "hi": hi, "xc": lat.xc, "yc": lat.yc}


def i2_sheet(lat: Lattice, mhd: dict) -> tuple[IRow, dict]:
    r = mhd["radius"]
    scan = wilson_theta_scan(lat, center=complex(EPS_EP, 0.0), radius=r, n_theta=mhd["theta"].size)
    i2, i4 = mhd["i2"], mhd["i4"]
    U2, U4 = scan["U"][i2], scan["U"][i4]
    d_m = abs(U2 + 1.0)
    d_p = abs(U4 - 1.0)
    # tautological cover: U(2π)=−1, U(4π)=+1
    passed = bool(d_m < 0.15 and d_p < 0.15)
    flux = lat.B * np.pi * r ** 2
    row = IRow(
        name="I2 sheet",
        formula=r"U(2\pi)\stackrel{?}{=}-1,\ U(4\pi)\stackrel{?}{=}+1",
        number=(
            f"U(2π)={U2.real:.4f}{U2.imag:+.4f}j  |U+1|={d_m:.4f}; "
            f"U(4π)={U4.real:.4f}{U4.imag:+.4f}j  |U-1|={d_p:.4f}; "
            f"enclosed flux Bπr²={flux:.4f} rad (not fitted)"
        ),
        passed=passed,
        note="Same loop family as pair-A endpoint continuation. A is uniform B, not π-flux.",
    )
    return row, {"scan": scan, "U2": U2, "U4": U4, "d_m": d_m, "d_p": d_p}


def i3_map(mhd: dict, scan: dict) -> IRow:
    """Φ from n_MHD to this U, not inserted by hand: test U vs exp(iπ n)."""
    n = mhd["n_sheet"]
    U = scan["U"]
    # resample U onto n's theta if needed — same n_theta requested
    pred = np.exp(1j * np.pi * n)
    i2, i4 = mhd["i2"], mhd["i4"]
    idx = [0, i2, i4]
    err = [abs(U[i] - pred[i]) for i in idx]
    max_err = float(np.max(err))
    # also: linear correlation of Arg(U) with n (step) vs with θ (area)
    argU = np.unwrap(np.angle(U))
    # if Φ were true, Arg(U) ≈ π n
    if np.std(n) > 0 and np.std(argU) > 0:
        corr_n = float(np.corrcoef(n, argU)[0, 1])
    else:
        corr_n = float("nan")
    corr_th = float(np.corrcoef(mhd["theta"], argU)[0, 1])
    passed = bool(max_err < 0.2)
    return IRow(
        name="I3 map",
        formula=r"\max|U-\exp(i\pi n_{\mathrm{MHD}})|\ \mathrm{at}\ (0,2\pi,4\pi)",
        number=(
            f"max|U−Φ_hand|={max_err:.4f} (need <0.2); "
            f"corr(Arg U, n_MHD)={corr_n:.3f}, corr(Arg U, θ)={corr_th:.3f}"
        ),
        passed=passed,
        note="Hand map Φ(n)=e^{iπ n} is the locked tautology. Here U comes from uniform-B holonomy.",
    )


def i4_control(lat: Lattice, mhd: dict, rng: np.random.Generator) -> tuple[IRow, dict]:
    r = mhd["radius"]
    on = wilson_theta_scan(lat, center=complex(EPS_EP, 0.0), radius=r, n_theta=181)
    off = wilson_theta_scan(lat, center=complex(0.0, 1.2), radius=r, n_theta=181)
    i2 = int(np.argmin(np.abs(on["theta"] - 2.0 * np.pi)))
    sig_on = float(abs(on["U"][i2] - 1.0))
    sig_off = float(abs(off["U"][i2] - 1.0))
    drop = sig_on / (sig_off + 1e-16)

    scr = scramble(lat, rng)
    lo, hi = Gamma(EPS_EP)
    band = 2.0 * lat.dy
    onmask = _gamma_mask(lat.xc, lat.yc, lo, hi, band)
    rho_s = np.abs(cs_density(scr))
    scr_on = float(np.mean(rho_s[onmask]))
    scr_off = float(np.mean(rho_s[~onmask]))
    scr_ratio = scr_on / (scr_off + 1e-16)

    # pass I4 only if the ON-Γ signal drops when the loop is moved off Γ
    passed = bool(drop > 3.0)
    row = IRow(
        name="I4 control",
        formula=r"|U-1|_{\mathrm{loop\ on\ endpoint}}\ /\ |U-1|_{\mathrm{loop\ off\ }\Gamma}",
        number=(
            f"shift drop-ratio={drop:.4f} (need >3); "
            f"|U-1|_on={sig_on:.4f}, |U-1|_off={sig_off:.4f}; "
            f"scramble CS on/off={scr_ratio:.4f}"
        ),
        passed=passed,
        note=(
            "Same radius, centre moved to +1.2i (off the real slit). "
            "If drop≈1 the letter is global (area law), not a cut connection. "
            "Scramble: random compact U(1) links on the same mesh."
        ),
    )
    return row, {
        "on": on, "off": off, "drop": drop,
        "scr_ratio": scr_ratio, "sig_on": sig_on, "sig_off": sig_off,
    }


def run_all(seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    lat = build_lattice(n=81, extent=2.0, B=B_FIELD)
    mhd = n_mhd_around_endpoint()
    i1, i1x = i1_support(lat)
    i2, i2x = i2_sheet(lat, mhd)
    i3 = i3_map(mhd, i2x["scan"])
    i4, i4x = i4_control(lat, mhd, rng)
    rows = [i1, i2, i3, i4]
    return {
        "rows": rows,
        "lat": lat,
        "mhd": mhd,
        "i1": i1x,
        "i2": i2x,
        "i4": i4x,
        "B": B_FIELD,
        "eps_ep": EPS_EP,
    }
