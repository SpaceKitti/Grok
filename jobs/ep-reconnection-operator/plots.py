"""Figures (A), (B), (F) for the EP–reconnection operator test."""

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
        "axes.titlesize": 11,
        "figure.dpi": 140,
        "savefig.bbox": "tight",
        "axes.grid": True,
        "grid.alpha": 0.25,
    }
)


def plot_A_dynamo(obj0: dict, outdir: Path) -> Path:
    spec = obj0["spec"]
    puis = obj0["puis"]
    mono = obj0["mono"]
    f = spec["f"]
    ev = spec["evals"]
    f_ep = spec["f_ep"]

    fig, axes = plt.subplots(2, 2, figsize=(10.6, 8.4))

    ax = axes[0, 0]
    ax.plot(f, ev[:, 0].real, color="C0", lw=1.6, label=r"$\mathrm{Re}\,E_-$")
    ax.plot(f, ev[:, 1].real, color="C1", lw=1.6, label=r"$\mathrm{Re}\,E_+$")
    ax.plot(f, ev[:, 0].imag, color="C0", lw=1.2, ls="--", label=r"$\mathrm{Im}\,E_-$")
    ax.plot(f, ev[:, 1].imag, color="C1", lw=1.2, ls="--", label=r"$\mathrm{Im}\,E_+$")
    ax.axvline(f_ep, color="k", ls=":", lw=1.0)
    ax.axvline(-f_ep, color="k", ls=":", lw=1.0)
    ax.axvline(0.0, color="0.4", ls="--", lw=0.8)
    ax.scatter([f_ep, -f_ep], [0, 0], marker="*", s=90, c="k", zorder=5, label="EP$_2$")
    ax.scatter([0], [0], marker="D", s=40, c="0.3", zorder=5, label="diabolic")
    ax.set_xlabel(r"$f$  ($b=1$ slice)")
    ax.set_ylabel(r"eigenvalue $E$")
    ax.set_title("GSG 2004 2×2 α²-dynamo: spectrum vs $f$")
    ax.legend(fontsize=8, loc="upper right")

    ax = axes[0, 1]
    th = mono["theta"] / np.pi
    me = mono["evals"]
    ax.plot(th, me[:, 0].real, color="C0", lw=1.5, label=r"$\mathrm{Re}\,E_0$")
    ax.plot(th, me[:, 1].real, color="C1", lw=1.5, label=r"$\mathrm{Re}\,E_1$")
    ax.plot(th, me[:, 0].imag, color="C0", lw=1.1, ls="--")
    ax.plot(th, me[:, 1].imag, color="C1", lw=1.1, ls="--")
    ax.axvline(2, color="k", ls=":", lw=1)
    ax.axvline(4, color="k", ls=":", lw=1)
    ax.set_xlabel(r"loop angle $\theta/\pi$ around EP$_2$")
    ax.set_ylabel(r"$E(\theta)$ (analytically continued)")
    ax.set_title(r"sheets swap at $2\pi$, return at $4\pi$")
    ax.legend(fontsize=8)

    ax = axes[1, 0]
    ax.plot(mono["f_path"].real, mono["f_path"].imag, color="C2", lw=1.2)
    ax.scatter([f_ep], [0], marker="*", s=120, c="k", zorder=5, label="EP$_2$")
    ax.scatter([0], [0], marker="D", s=40, c="0.3", label="DP")
    ax.set_aspect("equal")
    ax.set_xlabel(r"$\mathrm{Re}\,f$")
    ax.set_ylabel(r"$\mathrm{Im}\,f$")
    ax.set_title(r"encirclement $f = f_{\mathrm{EP}} + r e^{i\theta}$")
    ax.legend(fontsize=8)

    ax = axes[1, 1]
    eps = puis["eps"]
    split_n = 0.5 * np.abs(puis["lam_num"][:, 1] - puis["lam_num"][:, 0])
    split_f = 0.5 * np.abs(puis["lam_fit"][:, 1] - puis["lam_fit"][:, 0])
    ax.loglog(eps, split_n, "o", ms=4, color="C0", label="numerical split")
    ax.loglog(eps, split_f, "-", color="k", lw=1.2, label=r"$c\sqrt{\varepsilon}$")
    ax.loglog(eps, puis["c"] * np.sqrt(eps), color="k", lw=0)  # legend already
    p, r = puis["exponent_fit"]
    ax.set_xlabel(r"$\varepsilon = f - f_{\mathrm{EP}}$")
    ax.set_ylabel(r"$|E_+ - E_-|/2$")
    ax.set_title(f"Puiseux test: fitted $p={p:.3f}$ (expect $1/2$)")
    ax.legend(fontsize=8)

    fig.tight_layout()
    path = outdir / "A_dynamo_spectrum_monodromy.png"
    fig.savefig(path)
    fig.savefig(outdir / "A_dynamo_spectrum_monodromy.pdf")
    plt.close(fig)
    return path


def plot_B_tearing(obj1: dict, outdir: Path) -> Path:
    rows = obj1["rows"]
    S_vals = obj1["S_vals"]
    k_vals = obj1["k_vals"]
    nS, nK = len(S_vals), len(k_vals)

    g = np.full((nS, nK), np.nan)
    gap = np.full((nS, nK), np.nan)
    conn = np.full((nS, nK), np.nan)
    even = np.full((nS, nK), np.nan)
    for r in rows:
        i = int(np.argmin(np.abs(S_vals - r.S)))
        j = int(np.argmin(np.abs(k_vals - r.k)))
        g[i, j] = r.gamma_re
        gap[i, j] = r.gap
        conn[i, j] = r.R_conn
        even[i, j] = r.even_frac

    fig, axes = plt.subplots(2, 2, figsize=(10.6, 8.6))

    ax = axes[0, 0]
    for i, S in enumerate(S_vals):
        ax.plot(k_vals, g[i], "-o", ms=3.5, lw=1.2, label=f"$S={S:g}$")
    ax.axhline(0.0, color="k", lw=0.8)
    ax.axvline(1.0, color="k", ls=":", lw=1, label=r"$\Delta'=0$")
    ax.set_xlabel(r"$k a$")
    ax.set_ylabel(r"$\mathrm{Re}\,\gamma\,\tau_A$ (tearing)")
    ax.set_title("tearing growth vs $k$, EP loci = defective coalescence")
    ax.legend(fontsize=7, ncol=2)
    # mark defective
    for r in rows:
        if r.defective:
            ax.scatter([r.k], [r.gamma_re], marker="*", s=80, c="k", zorder=6)

    ax = axes[0, 1]
    KK, SS = np.meshgrid(k_vals, np.log10(S_vals))
    im = ax.pcolormesh(KK, SS, g, shading="nearest", cmap="RdBu_r")
    ax.axvline(1.0, color="k", ls=":", lw=1)
    fig.colorbar(im, ax=ax, label=r"$\mathrm{Re}\,\gamma$")
    for r in rows:
        if r.defective:
            ax.scatter([r.k], [np.log10(r.S)], marker="*", s=80, c="k")
        if r.onset:
            ax.scatter([r.k], [np.log10(r.S)], marker=".", s=12, c="green", alpha=0.6)
    ax.set_xlabel(r"$k a$")
    ax.set_ylabel(r"$\log_{10} S$")
    ax.set_title(r"spectrum vs $(S,\Delta')$  (green = $R_{conn}$ onset)")

    ax = axes[1, 0]
    im = ax.pcolormesh(KK, SS, np.log10(np.maximum(gap, 1e-8)), shading="nearest", cmap="magma")
    fig.colorbar(im, ax=ax, label=r"$\log_{10}$ nearest-pair gap")
    ax.axvline(1.0, color="w", ls=":", lw=1)
    ax.set_xlabel(r"$k a$")
    ax.set_ylabel(r"$\log_{10} S$")
    ax.set_title("nearest-pair gap (dark = Alfvén-cut edge, not EP2)")

    ax = axes[1, 1]
    er = obj1["er_ref"]
    ax.plot(er.z, np.real(er.psi), color="C0", lw=1.5, label=r"$\mathrm{Re}\,\psi$")
    ax.plot(er.z, np.imag(er.psi), color="C0", lw=1.0, ls="--", label=r"$\mathrm{Im}\,\psi$")
    ax.plot(er.z, np.real(er.u), color="C1", lw=1.2, label=r"$\mathrm{Re}\,u$")
    ax.axvline(0.0, color="k", ls=":", lw=0.8)
    ax.set_xlim(-6, 6)
    ax.set_xlabel(r"$z/a$")
    ax.set_ylabel("eigenfunction")
    ax.set_title(
        f"ref tearing mode  $S={er.S:g}$, $k={er.k:g}$, "
        f"$\\gamma={er.tearing_gamma.real:.4f}$"
    )
    ax.legend(fontsize=8)

    fig.tight_layout()
    path = outdir / "B_tearing_spectrum.png"
    fig.savefig(path)
    fig.savefig(outdir / "B_tearing_spectrum.pdf")
    plt.close(fig)
    return path


def plot_F_overlay(obj1: dict, outdir: Path) -> Path:
    rows = obj1["rows"]
    S_vals = obj1["S_vals"]
    k_vals = obj1["k_vals"]
    nS, nK = len(S_vals), len(k_vals)
    CS = np.full((nS, nK), np.nan)
    MHD = np.full((nS, nK), np.nan)
    CONN = np.full((nS, nK), np.nan)
    for r in rows:
        i = int(np.argmin(np.abs(S_vals - r.S)))
        j = int(np.argmin(np.abs(k_vals - r.k)))
        CS[i, j] = r.R_CS
        MHD[i, j] = r.R_MHD
        CONN[i, j] = r.R_conn

    fig, axes = plt.subplots(1, 3, figsize=(12.2, 3.8), sharey=True)
    KK, SS = np.meshgrid(k_vals, np.log10(S_vals))
    for ax, data, title, cmap in [
        (axes[0], CONN, r"$R_{\mathrm{conn}}$", "Greens"),
        (axes[1], CS, r"$R_{\mathrm{CS}}$ (sheet holonomy)", "Blues"),
        (axes[2], MHD, r"$R_{\mathrm{MHD}}$ (Ohmic $E\cdot J$)", "Oranges"),
    ]:
        im = ax.pcolormesh(KK, SS, data, shading="nearest", cmap=cmap)
        ax.axvline(1.0, color="k", ls=":", lw=1)
        fig.colorbar(im, ax=ax, fraction=0.046)
        ax.set_xlabel(r"$k a$")
        ax.set_title(title)
    axes[0].set_ylabel(r"$\log_{10} S$")
    fig.suptitle("Object 1 overlay: connectivity vs CS holonomy vs Ohmic on the same cut", y=1.03)
    fig.tight_layout()
    path = outdir / "F_RCS_RMHD_overlay.png"
    fig.savefig(path)
    fig.savefig(outdir / "F_RCS_RMHD_overlay.pdf")
    plt.close(fig)
    return path


def plot_monodromy_obj1(obj1: dict, outdir: Path) -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.0))
    for ax, mono, title in [
        (axes[0], obj1["mono_onset"], "loop around onset $(S,k)=(500,1)$"),
        (axes[1], obj1["mono_cand"], "loop around EP candidate"),
    ]:
        th = mono["theta"] / np.pi
        ev = mono["evals"]
        ax.plot(th, ev[:, 0].real, color="C0", lw=1.4, label=r"$\mathrm{Re}\,\gamma_0$")
        ax.plot(th, ev[:, 1].real, color="C1", lw=1.4, label=r"$\mathrm{Re}\,\gamma_1$")
        ax.plot(th, ev[:, 0].imag, color="C0", ls="--", lw=1.0)
        ax.plot(th, ev[:, 1].imag, color="C1", ls="--", lw=1.0)
        ax.axvline(2, color="k", ls=":", lw=1)
        ax.axvline(4, color="k", ls=":", lw=1)
        tag = "EP2 4π YES" if mono["ep2_monodromy"] else "EP2 4π NO"
        ax.set_title(f"{title}\n{tag}")
        ax.set_xlabel(r"$\theta/\pi$")
        ax.legend(fontsize=8)
    axes[0].set_ylabel(r"continued $\gamma$")
    fig.tight_layout()
    path = outdir / "B_tearing_monodromy.png"
    fig.savefig(path)
    plt.close(fig)
    return path
