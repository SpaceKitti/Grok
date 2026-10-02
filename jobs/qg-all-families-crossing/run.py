"""21 separate tracks. Hybrid only after 1 and 12. Control must fail."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT))

import families as F
from protocol import EPS_EP, X_OFF, X_ON


def fmt(x) -> str:
    if x != x:
        return "nan"
    return f"{float(x):.6g}"


def write_results(rows: list[dict], path: Path) -> str:
    prefer = [r["family"] for r in rows if r["verdict"] == "prefers Γ"]
    if prefer:
        sent = "named theories that prefer the MHD wall: " + ", ".join(prefer)
    else:
        sent = "no named theory prefers the MHD wall"

    lines = []
    lines.append("# All-families crossing sweep")
    lines.append("")
    lines.append("New folder. Hive not opened. Pair A not rebuilt. P0 locked (pair A sees the wall).")
    lines.append("No letter is $n_{\\mathrm{MHD}}$ or $da=\\pi\\delta_\\Gamma$.")
    lines.append(
        f"$\\gamma_{{\\mathrm{{cross}}}}$ at $x={X_ON}$ through $\\Gamma=[-{EPS_EP},{EPS_EP}]$; "
        f"$\\gamma_{{\\mathrm{{miss}}}}$ at $x={X_OFF}$, same length."
    )
    lines.append("If a theory cannot live on this mesh without a U(1) nickname, the row is **could not define**.")
    lines.append("")
    for r in rows:
        lines.append(f"## {r['family']}")
        lines.append("")
        lines.append("```")
        lines.append(r["operator"])
        lines.append("```")
        lines.append("")
        lines.append(
            f"J_on={fmt(r['J_on'])}, J_off={fmt(r['J_off'])}, ratio={fmt(r['ratio'])}, "
            f"wall site={r['wall_site']}. verdict: **{r['verdict']}**."
        )
        lines.append("")

    lines.append("## Table")
    lines.append("")
    lines.append("| family | J_on | J_off | ratio | wall site | verdict |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for r in rows:
        lines.append(
            f"| {r['family']} | {fmt(r['J_on'])} | {fmt(r['J_off'])} | "
            f"{fmt(r['ratio'])} | {r['wall_site']} | **{r['verdict']}** |"
        )
    lines.append("")
    lines.append("## One sentence")
    lines.append("")
    lines.append(f"**{sent}**")
    lines.append("")
    lines.append("Not a theorem. No Qin, leapfrog, Hall 3×3, dynamo phenomenology.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return sent


def main() -> int:
    rows: list[dict] = []

    def go(tag, fn, *a):
        print(tag)
        r = fn(*a)
        print(" ", r["verdict"], "ratio", r["ratio"])
        rows.append(r)
        return r

    r1 = go("1 CS", F.f01_cs)
    go("2 LQG", F.f02_lqg)
    go("3 spin foam", F.f03_spinfoam)
    go("4 BF", F.f04_bf)
    go("5 GFT", F.f05_gft)
    go("6 CDT", F.f06_cdt)
    go("7 EDT", F.f07_edt)
    go("8 causal sets", F.f08_csets)
    go("9 worldsheet", F.f09_worldsheet)
    go("10 SFT", F.f10_sft)
    go("11 M-theory", F.f11_mtheory)
    r12 = go("12 holo", F.f12_holo)
    go("13 asymptotic safety", F.f13_as)
    go("14 Horava", F.f14_hl)
    go("15 twistor", F.f15_twistor)
    go("16 shape dynamics", F.f16_shape)
    go("17 NCG", F.f17_ncg)
    go("18 teleparallel", F.f18_teleparallel)
    go("19 LQC", F.f19_lqc)
    go("20 hybrid (after 1 and 12)", F.f20_hybrid, r1, r12)
    r21 = go("21 U(1) control", F.f21_u1)
    if r21["verdict"] == "prefers Γ":
        print("Control passed: sweep is broken")
        return 2

    sent = write_results(rows, ROOT / "RESULTS.md")
    (OUT / "summary.json").write_text(
        json.dumps(
            {
                "sentence": sent,
                "table": [
                    {
                        "family": r["family"],
                        "J_on": r["J_on"],
                        "J_off": r["J_off"],
                        "ratio": r["ratio"],
                        "wall_site": r["wall_site"],
                        "verdict": r["verdict"],
                    }
                    for r in rows
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    with (OUT / "all_families.csv").open("w", encoding="utf-8") as f:
        f.write("family,J_on,J_off,ratio,wall_site,verdict\n")
        for r in rows:
            f.write(
                f"{r['family']},{r['J_on']},{r['J_off']},{r['ratio']},"
                f"{r['wall_site']},{r['verdict']}\n"
            )
    print("SENTENCE:", sent)
    print("Wrote RESULTS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
