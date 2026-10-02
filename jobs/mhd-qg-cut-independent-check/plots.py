from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update(
    {"font.size": 10, "figure.dpi": 140, "savefig.bbox": "tight", "axes.grid": True, "grid.alpha": 0.22}
)


def plot_cs_map(bundle: dict, outdir: Path) -> Path:
    i1 = bundle["i1"]
    rho = i1["rho"]
    xc, yc = i1["xc"], i1["yc"]
    lo, hi = i1["lo"], i1["hi"]
    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    vmax = max(float(np.max(rho)) * 3.0, 1e-3)
    im = ax.pcolormesh(xc, yc, rho, shading="nearest", cmap="magma", vmin=0.0, vmax=vmax)
    fig.colorbar(im, ax=ax, label=r"$|F|/2\pi$")
    ax.plot([lo, hi], [0, 0], color="cyan", lw=2.5, label=r"$\Gamma$ (score mask only)")
    ax.set_aspect("equal")
    ax.set_xlabel("Re")
    ax.set_ylabel("Im")
    ax.set_title("I1: CS density of uniform-B lattice (A has no cut source)")
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    path = outdir / "I1_cs_density.png"
    fig.savefig(path)
    plt.close(fig)
    return path


def plot_loops(bundle: dict, outdir: Path) -> Path:
    mhd = bundle["mhd"]
    on = bundle["i2"]["scan"]
    off = bundle["i4"]["off"]
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.8))

    ax = axes[0]
    th = on["theta"] / np.pi
    ax.plot(th, on["U"].real, color="C0", lw=1.5, label=r"$\mathrm{Re}\,U$ on endpoint")
    ax.plot(th, on["U"].imag, color="C0", ls="--", lw=1.1, label=r"$\mathrm{Im}\,U$")
    ax.plot(off["theta"] / np.pi, off["U"].real, color="C1", lw=1.2, label=r"$\mathrm{Re}\,U$ off $\Gamma$")
    ax.plot(off["theta"] / np.pi, off["U"].imag, color="C1", ls="--", lw=1.0)
    ax.axhline(-1, color="k", ls=":", lw=0.8)
    ax.axhline(1, color="0.5", ls=":", lw=0.8)
    ax.axvline(2, color="k", ls=":", lw=0.8)
    ax.axvline(4, color="k", ls=":", lw=0.8)
    ax.set_xlabel(r"$\theta/\pi$")
    ax.set_ylabel("Wilson $U$")
    ax.set_title("I2/I4: holonomy on endpoint vs off $\\Gamma$")
    ax.legend(fontsize=7)

    ax = axes[1]
    pred = np.exp(1j * np.pi * mhd["n_sheet"])
    ax.plot(mhd["theta"] / np.pi, mhd["n_sheet"], color="C0", lw=1.5, label=r"$n_{\mathrm{MHD}}$")
    ax.plot(on["theta"] / np.pi, np.unwrap(np.angle(on["U"])) / np.pi, color="C1", lw=1.3, label=r"$\mathrm{Arg}\,U/\pi$")
    ax.plot(mhd["theta"] / np.pi, np.real(pred), color="C2", ls="--", lw=1.0, label=r"hand $\mathrm{Re}\,e^{i\pi n}$")
    ax.set_xlabel(r"$\theta/\pi$")
    ax.set_title("I3: independent $U$ vs hand $\\Phi(n)$")
    ax.legend(fontsize=7)

    fig.tight_layout()
    path = outdir / "I2_I3_I4_loops.png"
    fig.savefig(path)
    plt.close(fig)
    return path
