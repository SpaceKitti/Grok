"""
EP–reconnection operator test.
Object 0 (α²-dynamo control) then Object 1 (Harris tearing).
Object 2 is not run unless Object 1 locks as a dictionary.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

sys.path.insert(0, str(ROOT))

from object0_dynamo import run_object0
from object1_tearing import run_object1
from plots import plot_A_dynamo, plot_B_tearing, plot_F_overlay, plot_monodromy_obj1


def _fmt(x, nd=5):
    if x is None:
        return "nan"
    try:
        if x != x:
            return "nan"
    except Exception:
        return str(x)
    if isinstance(x, (bool, np.bool_)):
        return "1" if x else "0"
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    try:
        return f"{float(x):.{nd}g}"
    except Exception:
        return str(x)


def write_table(rows, path_csv: Path, path_md: Path) -> None:
    cols = [
        "S",
        "k",
        "Delta_prime",
        "R_EP",
        "R_Puiseux",
        "R_conn",
        "R_rate",
        "pred_FKR",
        "pred_SP",
        "pred_Hall",
        "pred_plasmoid",
        "best_branch",
        "gamma_re",
        "gamma_im",
        "gap",
        "petermann",
        "defective",
        "R_CS",
        "R_MHD",
        "R_mono",
        "n_sheet",
        "Gamma_lo",
        "Gamma_hi",
        "onset",
        "even_frac",
    ]
    with path_csv.open("w", encoding="utf-8") as f:
        f.write(",".join(cols) + "\n")
        for r in rows:
            f.write(",".join(_fmt(getattr(r, c)) for c in cols) + "\n")

    lines = []
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("| " + " | ".join("---" for _ in cols) + " |")
    for r in rows:
        lines.append("| " + " | ".join(_fmt(getattr(r, c), 4) for c in cols) + " |")
    path_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_results(obj0: dict, obj1: dict | None, path: Path) -> None:
    lines = []
    lines.append("# EP–reconnection operator  —  Object 0 then Object 1")
    lines.append("")
    lines.append("New session, new folder. Dynamo control + tearing operator + scoring table only.")
    lines.append("Source control: Günther–Stefani–Gerbeth, arXiv:math-ph/0407015.")
    lines.append("")
    lines.append("## (A) Object 0 — 2×2 α²-dynamo toy")
    lines.append("")
    p = obj0["puiseux"]
    m = obj0["monodromy"]
    lines.append(
        f"- Square-root Puiseux: **{'PASS' if p['passed'] else 'FAIL'}**  "
        f"(fitted exponent $p={p['exponent']:.4f}$, $r={p['exponent_r']:.4f}$, "
        f"max rel residual {p['max_rel_residual']:.3e})."
    )
    lines.append(
        f"- EP$_2$ 4π monodromy: **{'PASS' if m['ep2_monodromy'] else 'FAIL'}**  "
        f"(swap at 2π={m['swapped_at_2pi']}, return-4π eval distance={m['return_4pi_eval']:.3e}, "
        f"RP angle 2π={m['rp_angle_2pi']:.3f}, 4π={m['rp_angle_4pi']:.3f}, "
        f"2π-cross={m['rp_angle_2pi_cross']:.3f})."
    )
    lines.append(
        f"- Diabolic contrast (Hermitian loop around origin): min gap "
        f"{obj0['diabolic_contrast_min_gap']:.4f} (no branching)."
    )
    lines.append(
        "- Locations: branching EP$_2$ on the cone $f^2-|b|^2=0$, $|b|\\neq 0$ "
        "(algebraic 2, geometric 1). Diabolic point at the origin (algebraic=geometric=2)."
    )
    lines.append(f"- Object 0 overall: **{'PASS' if obj0['passed'] else 'FAIL — STOP'}**.")
    lines.append("")
    if not obj0["passed"]:
        lines.append("Object 0 did not show a square-root Puiseux split with 4π EP$_2$ monodromy. STOP.")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return

    lines.append("## (B) Object 1 — Harris tearing / reconnection operator")
    lines.append("")
    chk = obj1["check"]
    lines.append(
        f"- Operator self-check: **{'PASS' if chk['ok'] else 'FAIL'}**  "
        f"$\\gamma(S=200,k=0.5)={chk['gamma_unstable']}$, "
        f"$\\gamma(S=200,k=1.3)={chk['gamma_stable']}$, "
        f"even-frac unstable={chk['even_unstable']:.3f}."
    )
    res = chk["resolved"]
    lines.append(
        f"- Inner layer: $dz_\\min={res['dz_min']:.4g}$, "
        f"$\\delta_\\mathrm{{SP}}={res['delta_SP']:.4g}$, "
        f"$\\delta_\\mathrm{{FKR}}={res['delta_FKR']:.4g}$, "
        f"resolved SP={res['resolved_SP']}, FKR={res['resolved_FKR']}."
    )
    hunt = obj1["hunt"]
    lines.append(
        f"- EP hunt: source={hunt['source']}, n_defective={hunt['n_defective']}, "
        f"min gap={hunt['min_gap']:.4g} at {hunt['min_gap_at']}, "
        f"R_EP global={hunt['R_EP_global']}."
    )
    puis = hunt["puiseux"]
    lines.append(
        f"- Puiseux along $k$ at candidate: p={puis.get('exponent')}, "
        f"residual={puis.get('residual')}, passed={puis.get('passed')}."
    )
    mo = obj1["mono_onset"]
    mc = obj1["mono_cand"]
    lines.append(
        f"- Monodromy around onset (500,1): swap2π={mo['swapped_at_2pi']}, "
        f"4π-return={mo['returned_4pi']}, EP2={mo['ep2_monodromy']}."
    )
    lines.append(
        f"- Monodromy around candidate ({mc['S0']},{mc['k0']}): swap2π={mc['swapped_at_2pi']}, "
        f"4π-return={mc['returned_4pi']}, EP2={mc['ep2_monodromy']}."
    )
    lines.append(f"- Lock reasons: {obj1['lock_reason']}")
    sf = obj1.get("scale_fit", {})
    lines.append(
        f"- Measured $\\gamma(S)$ exponent at $ka=0.55$: $p={sf.get('p')}$ "
        f"(FKR $-3/5=-0.6$, Sweet-Parker $-1/2$, Coppi $-1/3$). $r={sf.get('r')}$."
    )
    lines.append("")
    lines.append("## (C) Scoring table")
    lines.append("")
    lines.append("See `outputs/C_scoring_table.md` and `outputs/C_scoring_table.csv`.")
    lines.append("Columns: $(S,\\Delta', R_\\mathrm{EP}, R_\\mathrm{Puiseux}, R_\\mathrm{conn}, "
                 "\\mathrm{rate}, \\mathrm{FKR}/\\mathrm{SP}/\\mathrm{Hall}/\\mathrm{plasmoid})$.")
    lines.append("")
    lines.append("## (D) One sentence")
    lines.append("")
    lines.append(f"**{obj1['verdict']}**")
    lines.append("")
    lines.append("## (E) Object 2")
    lines.append("")
    if obj1["verdict"] == "dictionary" and obj1["lock"]:
        lines.append("Object 1 passed as dictionary — Object 2 would run next (Hall + guide field).")
    else:
        lines.append("Object 1 did not lock. Object 2 is **not** run.")
    lines.append("")
    lines.append("## (F) R_CS vs R_MHD overlay")
    lines.append("")
    lines.append("See `outputs/F_RCS_RMHD_overlay.png`.")
    # do they light on the same interval as R_conn?
    rows = obj1["rows"]
    conn_on = [r for r in rows if r.R_conn > 0.5]
    if conn_on:
        cs_on = np.mean([r.R_CS for r in conn_on])
        cs_off = np.mean([r.R_CS for r in rows if r.R_conn < 0.5]) if any(r.R_conn < 0.5 for r in rows) else np.nan
        mhd_on = np.mean([r.R_MHD for r in conn_on])
        mhd_off = np.mean([r.R_MHD for r in rows if r.R_conn < 0.5]) if any(r.R_conn < 0.5 for r in rows) else np.nan
        lines.append(
            f"- Mean $R_\\mathrm{{CS}}$ on/off $R_\\mathrm{{conn}}$: {cs_on:.4g} / {cs_off:.4g}."
        )
        lines.append(
            f"- Mean $R_\\mathrm{{MHD}}$ on/off $R_\\mathrm{{conn}}$: {mhd_on:.4g} / {mhd_off:.4g}."
        )
        same = (cs_on > cs_off) and (mhd_on > mhd_off)
        if same:
            lines.append(
                "- $R_\\mathrm{CS}$ and $R_\\mathrm{MHD}$ both rise on the $R_\\mathrm{conn}$ interval; "
                "this is the resistive layer, not a spin-foam theorem. No black-hole claim."
            )
        else:
            lines.append(
                "- $R_\\mathrm{CS}$ and $R_\\mathrm{MHD}$ do **not** light on the same interval as "
                "$R_\\mathrm{conn}$. Keep CS orthogonal. No black-hole or spin-foam theorem."
            )
    lines.append("")
    lines.append("Hive-slot exports (0-forms, not written into any Qin/leapfrog): "
                 "`n_sheet`, `Gamma_lo`, `Gamma_hi`, `R_EP`, `R_conn` in the CSV.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    print("=== OBJECT 0 : GSG 2004 2x2 alpha^2-dynamo toy ===")
    obj0 = run_object0(OUT)
    plot_A_dynamo(obj0, OUT)
    print(
        f"  Puiseux passed={obj0['puiseux']['passed']}  p={obj0['puiseux']['exponent']:.4f}  "
        f"rel={obj0['puiseux']['max_rel_residual']:.3e}"
    )
    print(
        f"  Monodromy EP2={obj0['monodromy']['ep2_monodromy']}  "
        f"swap2pi={obj0['monodromy']['swapped_at_2pi']}  "
        f"needs_4pi={obj0['monodromy']['needs_4pi']}"
    )
    print(f"  OBJECT 0: {'PASS' if obj0['passed'] else 'FAIL'}")
    if not obj0["passed"]:
        write_results(obj0, None, ROOT / "RESULTS.md")
        print("Object 0 failed square-root Puiseux / 4pi test. STOP.")
        return 1

    print("=== OBJECT 1 : Harris tearing operator ===")
    obj1 = run_object1(OUT, n=181)
    print(f"  self-check ok={obj1['check']['ok']}  gamma_u={obj1['check']['gamma_unstable']}")
    print(f"  EP hunt: {obj1['hunt']['source']}  n_def={obj1['hunt']['n_defective']}  "
          f"min_gap={obj1['hunt']['min_gap']:.4g}  R_EP={obj1['hunt']['R_EP_global']}")
    print(f"  Puiseux: {obj1['hunt']['puiseux']}")
    print(f"  mono onset EP2={obj1['mono_onset']['ep2_monodromy']}  "
          f"cand EP2={obj1['mono_cand']['ep2_monodromy']}")
    print(f"  verdict: {obj1['verdict']}")
    print(f"  reasons: {obj1['lock_reason']}")

    plot_B_tearing(obj1, OUT)
    plot_F_overlay(obj1, OUT)
    plot_monodromy_obj1(obj1, OUT)
    write_table(obj1["rows"], OUT / "C_scoring_table.csv", OUT / "C_scoring_table.md")
    write_results(obj0, obj1, ROOT / "RESULTS.md")

    # compact JSON summary (no eigenfunctions)
    summary = {
        "object0_passed": obj0["passed"],
        "object0_puiseux_p": obj0["puiseux"]["exponent"],
        "object0_ep2_monodromy": obj0["monodromy"]["ep2_monodromy"],
        "object1_selfcheck": obj1["check"]["ok"],
        "object1_verdict": obj1["verdict"],
        "object1_lock": obj1["lock"],
        "object1_lock_reason": obj1["lock_reason"],
        "object1_n_defective": obj1["hunt"]["n_defective"],
        "object1_min_gap": obj1["hunt"]["min_gap"],
        "object1_R_EP": obj1["hunt"]["R_EP_global"],
        "object1_puiseux": obj1["hunt"]["puiseux"],
        "object2_run": False,
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print("Wrote outputs/ and RESULTS.md")
    if obj1["verdict"] != "dictionary":
        print("STOP after Object 1. Object 2 not run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
