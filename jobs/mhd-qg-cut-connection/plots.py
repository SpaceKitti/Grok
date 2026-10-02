"""Track 0 picture of Γ + two sheets; C4 overlay on the slit."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle

plt.rcParams.update(
    {
        "font.size": 10,
        "figure.dpi": 140,
        "savefig.bbox": "tight",
        "axes.grid": True,
        "grid.alpha": 0.22,
    }
)


def plot_gamma_sheets(eps: float, jump: dict, outdir: Path) -> Path:
    lo, hi = -abs(eps), abs(eps)
    fig, axes = plt.subplots(1, 3, figsize=(12.4, 3.9))

    # --- (a) slit in the spectral plane, two faces ---
    ax = axes[0]
    ax.axhline(0, color="0.75", lw=0.8)
    ax.axvline(0, color="0.75", lw=0.8)
    ax.plot([lo, hi], [0.04, 0.04], color="C0", lw=4.0, solid_capstyle="butt", label="upper face $n=0$")
    ax.plot([lo, hi], [-0.04, -0.04], color="C1", lw=4.0, solid_capstyle="butt", label="lower face $n=1$")
    ax.scatter([lo, hi], [0, 0], s=40, c="k", zorder=5)
    ax.annotate(r"branch pt", xy=(hi, 0), xytext=(hi + 0.15 * abs(eps), 0.35),
                fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.set_xlim(lo - 0.6 * abs(eps), hi + 0.8 * abs(eps))
    ax.set_ylim(-1.0, 1.0)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel(r"$\mathrm{Re}\,\lambda$")
    ax.set_ylabel(r"$\mathrm{Im}\,\lambda$")
    ax.set_title(r"(0) $\Gamma=[−|ε|,|ε|]$ two faces glued")
    ax.legend(fontsize=7, loc="upper left")

    # --- (b) sqrt covering: spiral / two sheets ---
    ax = axes[1]
    th = np.linspace(0, 4 * np.pi, 800)
    r = 0.15 + 0.12 * (th / (4 * np.pi))
    zs = r * np.exp(1j * th)
    w = np.sqrt(zs)  # principal then continuation via exp(iθ/2)
    w = np.sqrt(r) * np.exp(1j * th / 2.0)
    c = th / (2 * np.pi)
    ax.scatter(w.real, w.imag, c=c, s=6, cmap="coolwarm", linewidths=0, vmin=0, vmax=2)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$\mathrm{Re}\sqrt{z}$")
    ax.set_ylabel(r"$\mathrm{Im}\sqrt{z}$")
    ax.set_title(r"two sheets: $4\pi$ garage around one end")
    cb = fig.colorbar(ax.collections[0], ax=ax, fraction=0.046)
    cb.set_label(r"$\theta/2\pi$ (sheet index)")

    # --- (c) n_sheet MHD vs QG on the same loop ---
    ax = axes[2]
    thp = jump["theta"] / np.pi
    ax.step(thp, jump["n_sheet"], where="post", color="C0", lw=1.6, label=r"$n_{\mathrm{MHD}}$")
    nq = np.floor(np.unwrap(jump["theta"]) / (2.0 * np.pi) + 1e-12)
    nq = nq - nq[0]
    ax.step(thp, nq, where="post", color="C1", lw=1.3, ls="--", label=r"$n_{\mathrm{QG}}$")
    ax.axvline(2, color="k", ls=":", lw=0.9)
    ax.axvline(4, color="k", ls=":", lw=0.9)
    ax.set_xlabel(r"loop angle $\theta/\pi$ around branch point")
    ax.set_ylabel("sheet index")
    ax.set_title(r"$\Delta n$ shared; matrices not")
    ax.legend(fontsize=8)

    fig.tight_layout()
    path = outdir / "0_gamma_two_sheets.png"
    fig.savefig(path)
    fig.savefig(outdir / "0_gamma_two_sheets.pdf")
    plt.close(fig)
    return path


def plot_c4(c4: dict, outdir: Path) -> Path:
    s, rm, rq = c4["s"], c4["R_mhd"], c4["R_qg"]
    lo, hi = c4["lo"], c4["hi"]
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.plot(s, rm, color="C0", lw=1.8, label=r"$R_{\mathrm{MHD}}$ (Alfvén occupancy)")
    ax.plot(s, rq, color="C1", lw=1.6, ls="--", label=r"$R_{\mathrm{QG}}$ (CS density)")
    ax.axvspan(lo, hi, color="0.85", zorder=0, label=r"$\Gamma$")
    ax.set_xlabel(r"arc length $s$ along the real line (one $\varepsilon$)")
    ax.set_ylabel("residual density")
    ax.set_title(r"C4: both light on $\Gamma$,  $R_{\mathrm{MHD}}=2\,R_{\mathrm{QG}}$  on the slit")
    ax.legend(fontsize=8)
    fig.tight_layout()
    path = outdir / "4_C4_overlay.png"
    fig.savefig(path)
    fig.savefig(outdir / "4_C4_overlay.pdf")
    plt.close(fig)
    return path
