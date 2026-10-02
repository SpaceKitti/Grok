"""fork vs ε, 3-region masks, P(s), r hist. No CSR on thin arms."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from unfold import P_GUE, P_POISSON


def plot_all(eps, branches, regions, arm_L, arm_R, ep, outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(eps, branches[:, 0].real, "C0-", lw=1.4, label="Re λ0")
    ax.plot(eps, branches[:, 1].real, "C1-", lw=1.4, label="Re λ1")
    ax.plot(eps, branches[:, 0].imag, "C0--", lw=1.0, label="Im λ0")
    ax.plot(eps, branches[:, 1].imag, "C1--", lw=1.0, label="Im λ1")
    ax.axvline(regions["eps_star"], color="k", ls=":", lw=1, label=r"$\varepsilon_\star$ (data)")
    ax.set_xlabel(r"$\varepsilon$")
    ax.set_ylabel(r"$\lambda$")
    ax.set_title("fork vs ε (two lowest-damped branches)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(outdir / "fork_vs_eps.png")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.4, 5.0))
    for rec, c, m in [
        (regions["pts_ep"], "C3", "o"),
    ]:
        if rec:
            z0 = np.array([p["lam0"] for p in rec])
            z1 = np.array([p["lam1"] for p in rec])
            ax.scatter(z0.real, z0.imag, c=c, marker=m, s=28, label="EP window", zorder=3)
            ax.scatter(z1.real, z1.imag, c=c, marker=m, s=28, zorder=3)
    if regions["pts_arm_L"]:
        zL = np.array([p["lam"] for p in regions["pts_arm_L"]], complex)
        ax.plot(zL.real, zL.imag, "C0.-", lw=1.2, ms=4, label="mid-arm L")
    if regions["pts_arm_R"]:
        zR = np.array([p["lam"] for p in regions["pts_arm_R"]], complex)
        ax.plot(zR.real, zR.imag, "C1.-", lw=1.2, ms=4, label="mid-arm R")
    if regions["pts_junc"]:
        zj0 = np.array([p["lam0"] for p in regions["pts_junc"]])
        zj1 = np.array([p["lam1"] for p in regions["pts_junc"]])
        ax.scatter(zj0.real, zj0.imag, c="0.5", marker="x", s=20, label="junction leftover")
        ax.scatter(zj1.real, zj1.imag, c="0.5", marker="x", s=20)
    ax.set_xlabel(r"Re $\lambda$")
    ax.set_ylabel(r"Im $\lambda$")
    ax.set_title("3-region mask (no third prong)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(outdir / "regions_mask.png")
    plt.close(fig)

    s = np.concatenate([arm_L["s"], arm_R["s"]]) if arm_L["s"].size + arm_R["s"].size else np.array([])
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    if s.size:
        bins = np.linspace(0, max(3.0, np.percentile(s, 95)), 16)
        ax.hist(s, bins=bins, density=True, color="0.75", edgecolor="k", label="arms pooled P(s)")
        xx = np.linspace(0, bins[-1], 200)
        ax.plot(xx, P_GUE(xx), "C0", lw=1.5, label="GUE Wigner")
        ax.plot(xx, P_POISSON(xx), "C1", lw=1.5, label="Poisson")
    else:
        ax.text(0.5, 0.5, "no arm spacings", ha="center", transform=ax.transAxes)
    ax.set_xlabel("unfolded s")
    ax.set_ylabel("P(s)")
    ax.set_title("mid-arm spacings (CSR not used)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(outdir / "P_s.png")
    plt.close(fig)

    r = np.concatenate([arm_L["r"], arm_R["r"]]) if arm_L["r"].size + arm_R["r"].size else np.array([])
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    if r.size:
        ax.hist(r, bins=np.linspace(0, 1, 12), density=True, color="0.75", edgecolor="k")
        ax.axvline(0.386, color="C1", ls="--", label="Poisson ⟨r⟩≈0.386")
        ax.axvline(0.603, color="C0", ls="--", label="GUE ⟨r⟩≈0.603")
    else:
        ax.text(0.5, 0.5, "no r", ha="center", transform=ax.transAxes)
    ax.set_xlabel("r")
    ax.set_title("Hermitian spacing ratio")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(outdir / "r_hist.png")
    plt.close(fig)
