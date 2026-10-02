"""A.2 first. Writes RESULTS.md + outputs/. Stop when those exist."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT))

from diagnostics import arm_stats, ep_stats, verdict_letter
from plots import plot_all
from regions import opening_metric, split_regions, track_two_lowest_damped
from spectrum_dewar import REASON as DEWAR_REASON
from spectrum_dewar import STUB as DEWAR_STUB
from spectrum_slab import ETA, REQUIRED_EPS, n2_check, save_sweep, sweep


def eps_grid() -> np.ndarray:
    dense = np.linspace(0.18, 1.02, 85)
    g = np.unique(np.sort(np.concatenate([dense, REQUIRED_EPS])))
    return g


def write_results(path: Path, payload: dict) -> None:
    n2 = payload["n2"]
    v = payload["verdict"]
    reg = payload["regions"]
    sw = payload["sw"]
    om = payload["opening"]
    arm_L, arm_R, ep = payload["arm_L"], payload["arm_R"], payload["ep"]
    n_sel = 2 * sw["eps"].size
    n_tot = sw["N"] * sw["eps"].size
    lines = []
    lines.append(
        f"N={sw['N']}  η={sw['eta']}  ε’s={sw['eps'].size}  "
        f"n_arm={reg['n_arm']}  n_ep={reg['n_ep']}  n_junc={reg['n_junc']}  "
        f"R_pair={om['max_re_split']:.4g}"
    )
    lines.append(
        f"selection: two lowest-damped non-spurious modes per ε, matched in ε; "
        f"n_selected/n_total={n_sel}/{n_tot}; "
        f"drop highly damped Dirichlet tail n_bar>2N/3; "
        f"keep thin locus of that pair (off ideal Γ=[-|ε|,|ε|] in the sense Im<0 resistive)"
    )
    lines.append(f"verdict {v['letter']}  {v['have']}")
    lines.append("4d metric / JT dual: NOT IN THIS FOLDER")
    lines.append("")
    lines.append("# Alfvén fork measure")
    lines.append("")
    lines.append("Dirichlet slab. Alfvén only. Not tearing. Dewar A.1 stubbed.")
    lines.append("")
    lines.append("## N=2 check")
    lines.append(
        f"a={n2['a']:.6g} b={n2['b']:.6g} v={n2['v']:.6g}  "
        f"max abs err vs pair_A refs = {n2['max_abs_err']:.3e}  "
        f"{'PASS' if n2['pass'] else 'STOP'}"
    )
    lines.append("")
    lines.append("## A.2 operator")
    lines.append("A = ε x + i η ∂_xx on [-1,1], Dirichlet.")
    lines.append("Square Galerkin in φ_n=sin(nπ(x+1)/2), n=1..N. M=I, ∂_xx diagonal.")
    lines.append("Rectangular (N+3)×N: not used (no larger basis to truncate).")
    lines.append(
        f"N={sw['N']}. η={sw['eta']}. ε grid includes {[float(x) for x in REQUIRED_EPS]}."
    )
    lines.append(f"A.1 Dewar: STUB={DEWAR_STUB}. {DEWAR_REASON}")
    lines.append("")
    lines.append("## Fork selection")
    lines.append(
        "Track two lowest-damped (largest Im) non-spurious eigenvalues vs ε, "
        "nearest-neighbour matched. Isolated highly damped Dirichlet modes dropped "
        f"(n_bar>2N/3). has_fork={om['has_fork']} (max Re split={om['max_re_split']:.4g})."
    )
    if not om["has_fork"]:
        lines.append("No ε-opening (vertical Im stack only) = no fork; histograms not used for class.")
    lines.append("")
    lines.append("## Regions")
    lines.append(
        f"data-driven ε★={reg['eps_star']:.6g}, z_EP={reg['z_ep']}, min_gap={reg['min_gap']:.4g}."
    )
    lines.append("EP window = contiguous un-opened block around min-gap (not gated on Pair A λ_EP).")
    lines.append("mid-arm = opened 1-D loci L/R in Re.")
    lines.append(reg["third_prong_note"])
    lines.append(
        f"n_arm={reg['n_arm']} n_ep={reg['n_ep']} n_junc={reg['n_junc']} "
        f"(junction leftover points={len(reg['pts_junc'])})."
    )
    lines.append("")
    lines.append("## Unfold / diagnostics")
    lines.append("mid-arm: spline polyline → arc length ℓ; N_bar from 1-D KDE ρ≥0 (monotone). s=ΔN_bar, ⟨s⟩=1.")
    lines.append("No global polynomial. No |z-z_NN|√ρ. CSR not applied (thin arms).")
    lines.append("EP: Airy zoom ζ∝(z-z_EP)^{2/3} is a microscope, not arm unfolding. No default AI†/AII†.")
    lines.append(
        f"arm L: n_sp={arm_L['n_spacings']} class={arm_L['class']} "
        f"KS_GUE={arm_L['ks_GUE']:.3g} KS_Pois={arm_L['ks_Poisson']:.3g} ⟨r⟩={arm_L['mean_r']:.3g}"
    )
    lines.append(
        f"arm R: n_sp={arm_R['n_spacings']} class={arm_R['class']} "
        f"KS_GUE={arm_R['ks_GUE']:.3g} KS_Pois={arm_R['ks_Poisson']:.3g} ⟨r⟩={arm_R['mean_r']:.3g}"
    )
    lines.append(
        f"EP: n={ep['n']} kind={ep['kind']} gap_p={ep['gap_p']:.3g} (√ germ ~ 0.5; not defaulted to Airy)"
    )
    lines.append(f"algebraic residual max={payload['max_res']:.3e} (Galerkin eigenpairs).")
    lines.append("")
    lines.append("## Verdict")
    lines.append(f"**{v['letter']}**  {v['have']}")
    lines.append(v["why"])
    lines.append("Never: we found QG. Never: JT is dual.")
    lines.append("4d metric / JT dual: NOT IN THIS FOLDER")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    print("N=2 check")
    n2 = n2_check()
    print(f"  a={n2['a']:.6g} b={n2['b']:.6g} v={n2['v']:.6g} maxerr={n2['max_abs_err']:.3e}")
    if not n2["pass"]:
        Path(ROOT / "RESULTS.md").write_text(
            "N=? η=0.05 ε’s=? n_arm=0 n_ep=0 n_junc=0 R_pair=nan\n"
            "selection: aborted\n"
            "verdict FAILED FAILED\n"
            "4d metric / JT dual: NOT IN THIS FOLDER\n\n"
            f"N=2 check STOP max abs err={n2['max_abs_err']}\n"
        )
        print("STOP N=2")
        return 1

    grid = eps_grid()
    print("A.2 N=64")
    sw = sweep(64, grid, ETA)
    save_sweep(sw, OUT)
    print("  eig done", sw["evals"].shape, "max res", np.nanmax(sw["residual"]))

    print("A.2 N=128")
    sw128 = sweep(128, grid, ETA)
    save_sweep(sw128, OUT)
    print("  eig done", sw128["evals"].shape, "max res", np.nanmax(sw128["residual"]))
    # use 128 for the measure
    sw = sw128

    branches = track_two_lowest_damped(sw["evals"], sw["spurious"])
    om = opening_metric(branches)
    print("  has_fork", om["has_fork"], "max Re split", om["max_re_split"])
    reg = split_regions(sw["eps"], branches)
    print("  n_arm", reg["n_arm"], "n_ep", reg["n_ep"], "n_junc", reg["n_junc"], "ε★", reg["eps_star"])

    arm_L = arm_stats(reg["pts_arm_L"])
    arm_R = arm_stats(reg["pts_arm_R"])
    ep = ep_stats(reg["pts_ep"], reg["z_ep"], reg["eps_star"], om["gap"], sw["eps"])
    verd = verdict_letter(om["has_fork"], arm_L, arm_R, ep, reg["n_junc"], True)
    print("  verdict", verd)

    plot_all(sw["eps"], branches, reg, arm_L, arm_R, ep, OUT)

    payload = {
        "n2": n2,
        "sw": sw,
        "opening": om,
        "regions": reg,
        "arm_L": arm_L,
        "arm_R": arm_R,
        "ep": ep,
        "verdict": verd,
        "max_res": float(np.nanmax(sw["residual"])),
    }
    write_results(ROOT / "RESULTS.md", payload)
    (OUT / "summary.json").write_text(
        json.dumps(
            {
                "N": sw["N"],
                "eta": sw["eta"],
                "n_eps": int(sw["eps"].size),
                "n_arm": reg["n_arm"],
                "n_ep": reg["n_ep"],
                "n_junc": reg["n_junc"],
                "has_fork": om["has_fork"],
                "eps_star": reg["eps_star"],
                "gap_p": ep["gap_p"],
                "arm_L_class": arm_L["class"],
                "arm_R_class": arm_R["class"],
                "verdict": verd,
            },
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )
    print("Wrote RESULTS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
