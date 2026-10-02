"""Figures: matrix spectrum vs ε, monodromy, Puiseux."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update(
    {
        "font.size": 10,
        "axes.labelsize": 11,
        "figure.dpi": 140,
        "savefig.bbox": "tight",
        "axes.grid": True,
        "grid.alpha": 0.25,
    }
)


def plot_pair(name: str, sweep: dict, scored: dict, outdir: Path) -> Path:
    chk = scored["checklist"]
    fig, axes = plt.subplots(2, 2, figsize=(10.6, 8.2))

    eps = sweep["eps"]
    ev = sweep["evals"]
    ax = axes[0, 0]
    ax.plot(eps, ev[:, 0].real, color="C0", lw=1.6, label=r"$\mathrm{Re}\,\lambda_-$")
    ax.plot(eps, ev[:, 1].real, color="C1", lw=1.6, label=r"$\mathrm{Re}\,\lambda_+$")
    ax.plot(eps, ev[:, 0].imag, color="C0", ls="--", lw=1.1, label=r"$\mathrm{Im}\,\lambda_-$")
    ax.plot(eps, ev[:, 1].imag, color="C1", ls="--", lw=1.1, label=r"$\mathrm{Im}\,\lambda_+$")
    if chk.eps_ep == chk.eps_ep:
        ax.axvline(chk.eps_ep, color="k", ls=":", lw=1)
        ax.axvline(-chk.eps_ep, color="k", ls=":", lw=1)
        ax.scatter([chk.eps_ep], [chk.lam_ep.real], marker="*", s=110, c="k", zorder=5, label="EP$_2$")
    lo, hi = chk.Gamma
    ax.axhspan(lo, hi, color="0.85", zorder=0, label=r"$\Gamma$ at $\varepsilon_{\mathrm{EP}}$")
    ax.set_xlabel(r"$\varepsilon$ (shear)")
    ax.set_ylabel(r"$\lambda$")
    ax.set_title(f"{name}: spectrum vs $\\varepsilon$")
    ax.legend(fontsize=7, loc="best")

    ax = axes[0, 1]
    ax.plot(eps, sweep["gap"], color="C2", lw=1.5)
    ax.set_yscale("log")
    ax.set_xlabel(r"$\varepsilon$")
    ax.set_ylabel(r"$|\lambda_+-\lambda_-|$")
    ax.set_title("gap (EP$_2$ = 0 with Jordan block)")

    ax = axes[1, 0]
    puis = scored["puiseux"]
    if puis["delta"].size:
        ax.loglog(puis["delta"], puis["split"], "o", ms=4, color="C0", label="split")
        p = puis["exponent"]
        c = puis["c"]
        ax.loglog(puis["delta"], c * puis["delta"] ** p, color="k", lw=1.1, label=fr"$c\,\delta^{{{p:.3f}}}$")
        ax.legend(fontsize=8)
    else:
        ax.text(0.5, 0.5, "Puiseux N/A (no EP2)", ha="center", va="center", transform=ax.transAxes)
    ax.set_xlabel(r"$|\varepsilon-\varepsilon_{\mathrm{EP}}|$")
    ax.set_ylabel("eigenvalue split")
    ax.set_title("Puiseux")

    ax = axes[1, 1]
    mono = scored["mono"]
    if np.asarray(mono["theta"]).size > 2:
        th = np.asarray(mono["theta"]) / np.pi
        me = np.asarray(mono["evals"])
        ax.plot(th, me[:, 0].real, color="C0", lw=1.4)
        ax.plot(th, me[:, 1].real, color="C1", lw=1.4)
        ax.plot(th, me[:, 0].imag, color="C0", ls="--", lw=1.0)
        ax.plot(th, me[:, 1].imag, color="C1", ls="--", lw=1.0)
        ax.axvline(2, color="k", ls=":", lw=1)
        ax.axvline(4, color="k", ls=":", lw=1)
        tag = "4π EP2 YES" if mono["ep2_monodromy"] else "4π EP2 NO"
        ax.set_title(f"monodromy around EP: {tag}")
        ax.set_xlabel(r"$\theta/\pi$")
    else:
        ax.text(0.5, 0.5, "monodromy N/A (no EP2)", ha="center", va="center", transform=ax.transAxes)
        ax.set_title("monodromy")

    fig.tight_layout()
    path = outdir / f"{name}_spectrum.png"
    fig.savefig(path)
    fig.savefig(outdir / f"{name}_spectrum.pdf")
    plt.close(fig)
    return path


def plot_N_check(sweepN: dict, eps_A: float, outdir: Path) -> Path:
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    eps = sweepN["eps"]
    ev = sweepN["evals"]
    ax.plot(eps, ev[:, 0].real, color="C0", lw=1.4, label="least-damped Re")
    ax.plot(eps, ev[:, 1].real, color="C1", lw=1.4)
    ax.plot(eps, ev[:, 0].imag, color="C0", ls="--", lw=1.0, label="Im")
    ax.plot(eps, ev[:, 1].imag, color="C1", ls="--", lw=1.0)
    ax.axvline(eps_A, color="k", ls=":", lw=1, label=r"$2\times 2$ $\varepsilon_{\mathrm{EP}}$")
    ax.set_xlabel(r"$\varepsilon$")
    ax.set_ylabel(r"$\lambda$ (two least-damped of $N\times N$)")
    ax.set_title("N×N Alfvén generator: no discrete EP2 expected of the continuum")
    ax.legend(fontsize=8)
    fig.tight_layout()
    path = outdir / "A_NxN_check.png"
    fig.savefig(path)
    plt.close(fig)
    return path
