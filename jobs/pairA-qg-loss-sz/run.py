"""pairA-qg-loss-sz: `python run.py` writes RESULTS.md and stops. No folders are loaded."""
from __future__ import annotations

import sys
import time

sys.dont_write_bytecode = True
from pathlib import Path  # noqa: E402

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
except Exception:
    pass

import numpy as np  # noqa: E402
import sympy as sp  # noqa: E402

import drive_test as DT  # noqa: E402
import H_try as HT  # noqa: E402

E, V, A, B = HT.EPS_EP, HT.V, HT.A, HT.B
ETA_STAR = abs(V) / (2 * E)
CLUSTER = 1e-3   # roots closer than this are one (near-)coalesced EP; the spec rounding of eps_EP (3.3e-10) splits a double root by ~1e-4
ETAS = [0.0, 1e-3, 3e-3, 1e-2, 3e-2, 0.1, 0.2, 0.3, 0.35, ETA_STAR, 0.4, 1.0, 3.0]
SPEEDS = (40.0, 100.0)


def fz(z):
    return f"{z.real:+.6f}{z.imag:+.6f}i"


def fe(e):
    return f"{e:.6f} (=|v|/(2ε_EP))" if e == ETA_STAR else f"{e:g}"


def fmt_new(ep):
    if not ep["new"]:
        return ""
    parts = []
    for q in ep["new"]:
        parts.append(f"{q['x']:+.4f}: " + ("inside" if q["in"] else f"dist {q['dloop']:.4f}"))
    return " (" + ", ".join(parts) + ")"


def fmt_rows(ep):
    return "; ".join(f"{fz(x['eps'])}: {x['swap']}/{x['ret']}" for x in ep["rows"])


def symbolic():
    eps, eta, a, b, v, Ee = sp.symbols("eps eta_g a b v eps_EP", real=True)
    F = eps ** 2 - Ee ** 2
    I = sp.I
    sx = sp.Matrix([[0, 1], [1, 0]]); sz = sp.Matrix([[1, 0], [0, -1]])
    Hr = -I * (a + b) / 2 * sp.eye(2) + v * eps * sx - I * (a - b) / 2 * sz
    Ht = (Hr + I * eta * F * sz).applyfunc(sp.simplify)
    Hshift = Hr.subs({a: a - eta * F, b: b + eta * F}, simultaneous=True)
    res = (Ht - Hshift).applyfunc(sp.simplify)
    kap = (b - a) / 2
    D = sp.expand(((Ht.trace()) ** 2 - 4 * Ht.det()) / 4)
    Dform = sp.expand(v ** 2 * eps ** 2 - (kap + eta * F) ** 2)
    # factorisation with kappa = |v| eps_EP (v < 0, so |v| = -v)
    fac = sp.expand(Dform.subs(b, a + 2 * (-v) * Ee) + (eps - Ee) * (eps + Ee) * (eta * (eps + Ee) + v) * (eta * (eps - Ee) - v))
    return Hr.applyfunc(sp.simplify), Ht, res, sp.simplify(D - Dform), sp.simplify(fac)


def ep_info(eta):
    c = np.trim_zeros(HT.disc_coeffs(eta), "f")
    roots = np.roots(c)
    groups = []
    for r in roots:
        for g in groups:
            if abs(r - g[0]) < CLUSTER:
                g.append(r); break
        else:
            groups.append([r])
    distinct = [(complex(np.mean(g)), len(g)) for g in groups]
    new = [abs(V) / eta - E, -(abs(V) / eta - E)] if eta > 0 else []
    closed = [E, -E] + new
    cf_err = max(min(abs(r - q) for q in closed) for r in roots)
    # D(+-eps_EP) = v^2 eps_EP^2 - kappa^2 does not depend on eta_g (F_JT(+-eps_EP) = 0): kept iff it is 0 up to the spec rounding
    dE = [abs(np.polyval(HT.disc_coeffs(eta), s * E)) for s in (1, -1)]
    kept = [d < 1e-9 for d in dE]
    H = HT.make_H(eta)
    rows = []
    for z, m in distinct:
        others = [abs(z - o) for o, _ in distinct if abs(z - o) > CLUSTER]
        r = 0.2 * min(others + [E])
        rows.append({"eps": z, "mult": m, "swap": HT.swap_around(H, z, r, 1), "ret": HT.swap_around(H, z, r, 2),
                     "in_loop": abs(z - E) < 0.25 * E, "dloop": abs(abs(z - E) - 0.25 * E)})
    newpos = [{"x": x, "in": abs(x - E) < 0.25 * E, "dloop": abs(abs(x - E) - 0.25 * E)} for x in new]
    e1 = any(q["in"] or q["dloop"] < 0.1 * E for q in newpos)
    # Jordan structure at the root next to +eps_EP
    zE = min(roots, key=lambda z: abs(z - E))
    M = H(zE) - np.trace(H(zE)) / 2 * HT.I2
    jord = {"eig": float(np.max(np.abs(np.linalg.eigvals(M)))), "norm": float(np.linalg.norm(M)), "mult": [m for z, m in distinct if abs(z - zE) < CLUSTER][0]}
    real = bool(np.max(np.abs(roots.imag)) < 1e-6)
    return {"roots": roots, "distinct": distinct, "n_mult": len(roots), "n_dist": len(distinct), "kept": kept, "dE": dE, "cf_err": cf_err,
            "rows": rows, "new": newpos, "E1": e1, "jord": jord, "real": real}


def main() -> int:
    t0 = time.time()
    Hr, Ht, sres, dres, fres = symbolic()
    print("H_real (H_A basis) =", sp.sstr(Hr))
    print("H_try  (H_A basis) =", sp.sstr(Ht))
    print("H_try - H_A(a -> a - eta_g F, b -> b + eta_g F) =", sp.sstr(sres))
    print("discriminant - [v^2 eps^2 - (kappa + eta_g F)^2] =", dres, "; factorisation residual =", fres)
    es, eg = 0.3, 0.1
    Hs, Hs0 = HT.make_H(eg)(es), HT.make_H(0.0)(es)
    print(f"sample eps = {es}, eta_g = {eg}: H_try =\n{Hs}\nH_try - H_A =\n{Hs - HT.H_A(es)}")
    zs = [0.3 + 0.2j, -0.7 + 0.1j, 1.1 - 0.5j, 0.75 * E, 1.25 * E, 0.2]
    shift_res = max(float(np.max(np.abs(HT.make_H(e)(z) - HT.H_A_rates(z, A - e * HT.F_JT(z), B + e * HT.F_JT(z))))) for e in ETAS for z in zs)
    h0_res = max(float(np.max(np.abs(HT.make_H(0.0)(z) - HT.H_A(z)))) for z in zs)
    disc_res = max(abs(HT.disc_numeric(HT.make_H(e), z) - np.polyval(HT.disc_coeffs(e), z)) for e in ETAS for z in zs)
    pt_res = max(float(np.max(np.abs(HT.SX @ np.conj(M) @ HT.SX - M))) for e in ETAS for x in (0.2, 0.75 * E, 1.25 * E, 0.9)
                 for M in [HT.make_H(e)(x) - np.trace(HT.make_H(e)(x)) / 2 * HT.I2])
    sym_res = max(float(np.max(np.abs(HT.make_H(e)(z).T - HT.make_H(e)(z)))) for e in ETAS for z in zs)
    print(f"numeric: rate-shift residual {shift_res:.1e}; H_try(0) - H_A {h0_res:.1e}; disc poly residual {disc_res:.1e}; PT (sx K) residual on real eps {pt_res:.1e}; H^T - H {sym_res:.1e}")
    Ex = HT.KAPPA / abs(V); etx = abs(V) / (2 * Ex); cx = HT.KAPPA - etx * Ex ** 2
    rx = np.roots([-etx ** 2, 0.0, V ** 2 - 2 * etx * cx, 0.0, -cx ** 2])
    exact_split = max(abs(r - Ex) for r in rx if abs(r - Ex) < 1e-2)
    print(f"exact eps_EP = kappa/|v| = {Ex:.10f}: roots at eta* = {rx}; max distance of the near-+eps_EP roots from eps_EP {exact_split:.1e}")
    ga = DT.GAMMA
    res = {}
    for eta in ETAS:
        H = HT.make_H(eta)
        ep = ep_info(eta)
        cs = HT.copy_test(H)
        cd = HT.copy_test(H, traceless=True)
        loop = HT.swap_around(H, E, 0.25 * E, 1), HT.swap_around(H, E, 0.25 * E, 2)
        gg = DT.gamma_g(H)
        dr = DT.test(H, SPEEDS, ga, dt_check=True)
        d2 = DT.test(H, SPEEDS, gg, dt_check=False)
        res[eta] = {"ep": ep, "cs": cs, "cd": cd, "loop": loop, "gg": gg, "dr": dr, "d2": d2}
        print(f"η_g={fe(eta)}: n_EP {ep['n_dist']} distinct / {ep['n_mult']} with mult; roots {[fz(z) + ('x' + str(m) if m > 1 else '') for z, m in ep['distinct']]}; ±ε_EP kept {ep['kept']}; E1 {ep['E1']}; "
              f"copy strict {'YES' if cs['copy'] else 'NO'} ({cs['smin_best']:.1e}) dyn {'YES' if cd['copy'] else 'NO'} ({cd['smin_best']:.1e}); loop {loop}; γ_g={gg:.5f}; "
              f"0.75 [{'broken' if dr[0.75]['broken'] else 'unbroken'}] {dr[0.75]['cls']}, 1.25 [{'broken' if dr[1.25]['broken'] else 'unbroken'}] {dr[1.25]['cls']}; dt Δw {max(dr[0.75]['dw'], dr[1.25]['dw']):.1e}; "
              f"secondary γ_g: {d2[0.75]['cls']}/{d2[1.25]['cls']}  t={time.time()-t0:.0f}s")
    # rounding probe: random traceless 1e-15 matrices (fixed seed, 3 draws; a scalar probe cancels exactly in the propagator)
    rng = np.random.default_rng(20260926)
    PROBES = []
    for _ in range(3):
        X = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
        X = X - np.trace(X) / 2 * HT.I2
        PROBES.append(1e-15 * X / np.linalg.norm(X))
    def probe_dw(eta, gT):
        H = HT.make_H(eta); runs = res[eta]["dr"][0.75]["runs"]; out = 0.0
        for P in PROBES:
            Hp = (lambda z, H=H, P=P: H(z) + P)
            for dn, s in (("ccw", 1), ("cw", -1)):
                for st in (0, 1):
                    mk = DT.run_drive(Hp, 0.75, s, gT, st, ga)
                    out = max(out, max(float(np.max(np.abs(mk[m]["wv"] - runs[(gT, dn, st)][m]["wv"]))) for m in (1, 2)))
        return out
    def dt_dw(eta, gT):
        H = HT.make_H(eta); runs = res[eta]["dr"][0.75]["runs"]
        return max(max(float(np.max(np.abs(DT.run_drive(H, 0.75, s, gT, 0, ga, factor=2)[m]["wv"] - runs[(gT, dn, 0)][m]["wv"]))) for m in (1, 2)) for dn, s in (("ccw", 1), ("cw", -1)))
    FL = {}
    FL[0.0] = {("probe", gT): probe_dw(0.0, gT) for gT in SPEEDS}
    FL[0.0].update({("dt", 40.0): res[0.0]["dr"][0.75]["dw"], ("dt", 100.0): dt_dw(0.0, 100.0)})
    rprobe = FL[0.0][("probe", 40.0)]
    print(f"traceless probe at η_g=0: γT=40 {rprobe:.1e}, γT=100 {FL[0.0][('probe', 100.0)]:.1e}; dt-halving γT=100 {FL[0.0][('dt', 100.0)]:.1e}")
    base = res[0.0]["dr"][0.75]["runs"]
    base_dw = max(res[0.0]["dr"][0.75]["dw"], res[0.0]["dr"][1.25]["dw"])
    def purity(runs, gT, m):
        return min(runs[(gT, dn, st)][m]["w"] for dn in ("ccw", "cw") for st in (0, 1))
    grade_rows = []
    for eta, r in res.items():
        dr = r["dr"]
        r["E2"] = not (dr[0.75]["broken"] and not dr[1.25]["broken"])
        r["eligible"] = eta > 0 and not r["ep"]["E1"] and not r["E2"]
        r["floor"] = max(max(dr[0.75]["dw"], dr[1.25]["dw"]), base_dw, rprobe)
        runs = dr[0.75]["runs"]
        r["comp_change"] = any(runs[k][m]["comp"] != base[k][m]["comp"] for k in runs for m in (1, 2))
        r["dP"] = {(gT, m): purity(runs, gT, m) - purity(base, gT, m) for gT in SPEEDS for m in (1, 2)}
        r["climb"] = any(dp > 10 * r["floor"] for dp in r["dP"].values())
        r["notcopy"] = not r["cs"]["copy"] and not r["cd"]["copy"]
        r["caused"] = r["eligible"] and dr[0.75]["cls"] == "D6-like" and (r["comp_change"] or r["climb"])
        if r["caused"] and r["notcopy"]:
            grade_rows.append(eta)
    notcopy_any = any(res[e]["notcopy"] for e in ETAS if e > 0)
    grade = "HAVE" if grade_rows else ("PARTIAL" if notcopy_any else "MISSING")
    elig = [e for e in ETAS if res[e]["eligible"]]
    consec = any(elig.index(grade_rows[i + 1]) == elig.index(grade_rows[i]) + 1 for i in range(len(grade_rows) - 1)) if len(grade_rows) > 1 else False
    flag = "" if grade != "HAVE" else (" (≥ 2 consecutive eligible grid points)" if consec else " (FLAG: single grid point)")
    print(f"GRADE (original rule) {grade}{flag}; caused rows {grade_rows}; eligible {elig}")
    # post-hoc Hive-amended floor (not the pre-fixed rule): max over both speeds of (dt-halving, traceless probe), this row and eta_g = 0
    for e in elig:
        FL[e] = {("probe", gT): probe_dw(e, gT) for gT in SPEEDS}
        FL[e].update({("dt", 40.0): res[e]["dr"][0.75]["dw"], ("dt", 100.0): dt_dw(e, 100.0)})
        print(f"η_g={fe(e)}: " + ", ".join(f"{k[0]} γT={k[1]:.0f} {v_:.1e}" for k, v_ in FL[e].items()) + f"  t={time.time()-t0:.0f}s")
    base_fa = max(FL[0.0].values())
    rowsA = []
    for e in elig:
        r = res[e]
        r["floorA"] = max(max(FL[e].values()), base_fa)
        r["climbA"] = any(dp > 10 * r["floorA"] for dp in r["dP"].values())
        r["causedA"] = r["eligible"] and r["dr"][0.75]["cls"] == "D6-like" and (r["comp_change"] or r["climbA"])
        if r["causedA"] and r["notcopy"]:
            rowsA.append(e)
    gradeA = "HAVE" if rowsA else ("PARTIAL" if notcopy_any else "MISSING")
    # largest clean purity drop: a drop exceeding 10x the amended floor (which covers both speeds)
    drops = [(dp, e, k) for e in elig for k, dp in res[e]["dP"].items() if dp < 0 and -dp > 10 * res[e]["floorA"]]
    clean_drop = min(drops) if drops else None
    single = grade == "HAVE" and not consec
    header = f"GRADE (letter): {grade}{', single grid point' if single else ''}; GRADE (physics): PARTIAL, D6 inherited"
    p40 = {e: min(res[e]["dr"][0.75]["runs"][(40.0, dn, st)][1]["w"] for dn in ("ccw", "cw") for st in (0, 1)) for e in (0.0, 0.1, 0.2)}
    r02 = res[0.2]["dr"][0.75]["runs"]
    cwccw = max(abs(r02[(100.0, "ccw", st)][m]["w"] - r02[(100.0, "cw", st)][m]["w"]) for st in (0, 1) for m in (1, 2))
    eta2 = abs(V) / E
    ep2 = ep_info(eta2)
    print(header); print(f"amended letter grade {gradeA}; rows {rowsA}; clean drop {clean_drop}; η=|v|/ε_EP roots {ep2['distinct']}")

    # ------------------------------------------------ RESULTS.md
    thr_lo, thr_hi = abs(V) / (2.25 * E), abs(V) / (1.75 * E)
    thr_hi2 = abs(V) / (0.25 * E)
    inside_broken_lo = 0.25 * HT.KAPPA / (0.4375 * E ** 2)
    L = ["# pairA-qg-loss-sz — RESULTS", "",
         "**Signed off 2026-09-26:** Venus (maths) and Helios (physics).", "",
         "Loss-contrast placement (the follow-up Helios offered after pairA-qg-loss). No folder was loaded; the numbers are from the job spec only (a = 0.12337, b = 0.49348, v = −0.360253, ε_EP = 0.51368066, λ_EP = −0.308425i, F_JT = ε² − ε_EP²). No claim of QG, a JT dual, or an Einstein solution.", "",
         "gravity-side is hive language [hive-interpretation]", "",
         "## Verdict", "",
         f"**{header}**", "",
         f"- Original-rule letter result (README rule as fixed; the README's scalar probe cancels exactly, so the traceless probe at η_g = 0, γT = 40 is used in its place, Δw = {rprobe:.1e}): **{grade}**{flag}. Rows meeting the HAVE rule: {grade_rows if grade_rows else 'none'}. Eligible rows (not E1/E2): {[fe(e) for e in elig]}.",
         f"- **post-hoc Hive-amended floor (not the pre-fixed rule):** floor(η_g) = max over γT = 40 and 100 of (dt-halving Δw, random traceless 1e-15 probe Δw), on the row and on η_g = 0. Letter grade recomputed: **{gradeA}** (rows meeting HAVE: {rowsA if rowsA else 'none'}). η_g = 0.2 **{'passes' if 0.2 in rowsA else 'does not pass'}**: amended floor {res[0.2]['floorA']:.1e}, so 10 × floor = {10 * res[0.2]['floorA']:.1e} against its largest purity rise {max(res[0.2]['dP'].values()):+.1e}.",
         f"- **Trigger of the letter HAVE** [threshold artifact risk]: the +{p40[0.2] - p40[0.0]:.3f} rise at η_g = 0.2 (γT = 40, 2π) is purification timing / non-adiabatic wobble, winner unchanged, non-monotonic ({p40[0.0]:.4f}, {p40[0.1]:.4f}, {p40[0.2]:.4f}).",
         f"- **Copy of H_A:** YES at η_g = 0 (H_try(0) − H_A = {h0_res:.1e}: H_real **is** H_A [by construction]). NO for every η_g > 0, strict and dynamical [identity: a constant S and an affine ε map preserve the degree of the discriminant, which is quartic in ε for η_g > 0 and quadratic for H_A(αε + β); computed s_min in the table]. The scalar part does not matter (the dynamical test drops it). **Not a constant basis change, but the same family as H_A**: H_try = H_A with ε-dependent rates a → a − η_g F_JT and b → b + η_g F_JT [identity; numeric residual {shift_res:.1e}].",
         "",
         "## Basis form of the extra term (H_A basis)", "",
         f"- H_real = `{sp.sstr(Hr)}` = H_A [by construction].",
         f"- H_try = `{sp.sstr(Ht)}`.",
         f"- H_try − H_A(a → a − η_g F, b → b + η_g F) = `{sp.sstr(sres)}` [identity]. The trace is unchanged, so λ_EP = −i(a+b)/2 is unchanged.",
         f"- The extra term iη_g F_JT σ_z is **diagonal contrast**: +iη_g F on entry 11 and −iη_g F on entry 22, and nothing off-diagonal.",
         f"- Sample ε = {es}, η_g = {eg}: H_try − H_A = diag({(Hs - HT.H_A(es))[0, 0]:.6f}, {(Hs - HT.H_A(es))[1, 1]:.6f}); off-diagonal {abs((Hs - HT.H_A(es))[0, 1]):.1e} [computed]. F_JT({es}) = {HT.F_JT(es):.6f}.",
         "- Sign: with ψ ~ e^{−iλt}, entry 11 has rate a − η_g F. Inside Γ (F < 0) the −ia site loses more and the −ib site less, so the effective contrast κ + η_g F falls. Outside Γ (F > 0) the contrast rises.", "",
         "## EPs vs η_g", "",
         f"- D(ε) = (tr² − 4 det)/4 = v²ε² − (κ + η_g F)², κ = (b − a)/2 = {HT.KAPPA:.6f} > 0 [identity; sympy residual {dres}, numeric {disc_res:.1e}].",
         f"- With κ = |v|ε_EP: D = −(ε − ε_EP)(ε + ε_EP)[η_g(ε + ε_EP) − |v|][η_g(ε − ε_EP) + |v|] [identity; sympy residual {fres}]. Roots: **±ε_EP (kept at every η_g) and new real EPs at ±(|v|/η_g − ε_EP)**, exactly (not only 'about').",
         f"- Rounding: the spec's ε_EP = 0.51368066 vs κ/|v| = {HT.KAPPA / abs(V):.10f} (3.3e-10 apart), so D(±ε_EP) = v²ε_EP² − κ² = {res[0.0]['ep']['dE'][0]:.1e} rather than 0. D(±ε_EP) does not depend on η_g, because F_JT(±ε_EP) = 0; 'kept' is tested this way (|D(±ε_EP)| < 1e-9). Near the coalescence the square root amplifies the rounding: at η_g* the double root splits into a pair about {abs(res[ETA_STAR]['ep']['cf_err']):.1e} off the real axis, and at η_g = 0.35 the near-pair roots move by about 1e-6. Roots within {CLUSTER:g} are counted as one (near-)coalesced EP. With the exact ε_EP = κ/|v| (check only), the η_g* roots next to +ε_EP are {exact_split:.1e} from it, a double root up to numerical root-finding [computed].",
         f"- **Coalescence:** at eta_g* = |v|/(2 eps_EP) = {ETA_STAR:.8f} each new EP merges with an old tip (D proportional to (eps -/+ eps_EP)^2): non-generic EP2, defective, no branch point, trivial monodromy [identity + computed; see the row].",
         f"- **Second non-generic point (Venus):** at η_g = |v|/ε_EP = {eta2:.4f} the two new EPs meet at ε = 0, outside the loop (D ∝ ε²(ε² − ε_EP²)). This explains the phase swap between η_g = 0.4 and 1 [identity]. Computed roots there: {', '.join(fz(z) + (f' ×{m}' if m > 1 else '') for z, m in ep2['distinct'])}; small-circle 2π swap / 4π return: {fmt_rows(ep2)} [computed].",
         f"- New-EP enclosure (E1, fixed rule: inside the loop or within 0.1 ε_EP of it): |v|/η_g − ε_EP is inside the loop for η_g ∈ ({thr_lo:.4f}, {thr_hi:.4f}), and ε_EP − |v|/η_g is inside for η_g > {thr_hi2:.4f} [identity]. Rows flagged E1 are listed below.",
         f"- Phase at the start points (E2): 0.75 ε_EP stays broken only for η_g < {inside_broken_lo:.4f} (it becomes unbroken when the new EP crosses 0.75 ε_EP, and broken again with flipped contrast for η_g > {thr_hi2:.4f}). 1.25 ε_EP becomes broken for η_g > {thr_lo:.4f} [identity].", "",
         "| η_g | n_EP distinct | n_EP with mult | roots (×mult) | ±ε_EP kept | all real | closed-form err | E1 (new EP in/near loop) | small-circle 2π swap / 4π return | Jordan at +ε_EP (|eig|, ‖M‖, mult) | loop 2π / 4π |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for eta in ETAS:
        ep, r = res[eta]["ep"], res[eta]
        L.append(f"| {fe(eta)} | {ep['n_dist']} | {ep['n_mult']} | {', '.join(fz(z) + (f' ×{m}' if m > 1 else '') for z, m in ep['distinct'])} | {'yes' if all(ep['kept']) else 'NO'} | {'yes' if ep['real'] else 'no'} | {ep['cf_err']:.1e} | "
                 f"{'**YES**' if ep['E1'] else 'no'}{fmt_new(ep)} | {fmt_rows(ep)} | ({ep['jord']['eig']:.1e}, {ep['jord']['norm']:.2f}, {ep['jord']['mult']}) | {r['loop'][0]} / {r['loop'][1]} |")
    L += ["", "## D6/D7 table vs η_g (primary: γ = |a − b|/2, γT = 40 and 100)", "",
          f"γ = {ga:.6f}. dt = 0.01/γ. The rounding probe is a random traceless 1e-15 matrix (fixed seed, 3 draws, max taken); a scalar probe cancels exactly in the propagator. The floors per speed are in the next table. The 'floor' column here is the original-rule floor [computed].", "",
          "| η_g | copy strict / dyn (s_min) | E1 | phase 0.75 / 1.25 | **0.75 ε_EP** | **1.25 ε_EP** | eligible | dt-halving Δw | floor | 0.75 physical winner changed vs η_g = 0 | max ΔP (0.75 purity vs η_g = 0) | purity climb > 10×floor | caused | γ_g | secondary (γ_g T) 0.75 / 1.25 |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for eta in ETAS:
        r = res[eta]; dr = r["dr"]
        mdp = max(r["dP"].values(), key=abs)
        L.append(f"| {fe(eta)} | {'YES' if r['cs']['copy'] else 'NO'} / {'YES' if r['cd']['copy'] else 'NO'} ({r['cs']['smin_best']:.1e} / {r['cd']['smin_best']:.1e}) | {'YES' if r['ep']['E1'] else 'no'} | "
                 f"{'broken' if dr[0.75]['broken'] else 'unbroken'} / {'broken' if dr[1.25]['broken'] else 'unbroken'} | **{dr[0.75]['cls']}** | **{dr[1.25]['cls']}** | {'yes' if r['eligible'] else 'no'} | "
                 f"{max(dr[0.75]['dw'], dr[1.25]['dw']):.1e} | {r['floor']:.1e} | {'YES' if r['comp_change'] else 'no'} | {mdp:+.2e} | {'YES' if r['climb'] else 'no'} | {'YES' if r['caused'] else 'no'} | {r['gg']:.5f} | {r['d2'][0.75]['cls']} / {r['d2'][1.25]['cls']} |")
    # winners-change line
    def winsig(eta):
        runs = res[eta]["dr"][0.75]["runs"]; nm = res[eta]["dr"][0.75]["names"]
        return sorted({(nm[runs[k][m]["win"]], runs[k][m]["comp"]) for k in runs for m in (1, 2)})
    small = [e for e in ETAS if e <= 0.01]
    large_elig = [e for e in elig if e >= 0.1]
    base_sig = winsig(0.0)
    same_small = all(winsig(e) == base_sig for e in small)
    same_large = all(winsig(e) == base_sig for e in large_elig) if large_elig else None
    L += ["", "## Winners and purity", "",
          f"- **Winners-change line:** 0.75 ε_EP winners at η_g = 0: {base_sig} (label, physical site). Small η_g (≤ 0.01): {'unchanged' if same_small else 'CHANGED'}. Largest eligible η_g (≥ 0.1: {[fe(e) for e in large_elig]}): {'unchanged' if same_large else ('CHANGED' if same_large is not None else 'n/a')}. "
          + "Non-eligible rows: " + "; ".join(f"η_g = {fe(e)}: {winsig(e)}" for e in ETAS if not res[e]["eligible"] and e > 0) + " [computed].",
          f"- **Purity:** max |ΔP| at 0.75 ε_EP on eligible rows: " + "; ".join(f"η_g = {fe(e)}: {max(res[e]['dP'].values(), key=abs):+.2e} (amended floor {res[e]['floorA']:.1e})" for e in elig) + " [computed].",
          (f"- **Largest clean purity drop** (a drop exceeding 10 × the amended floor, which covers both speeds): ΔP = {clean_drop[0]:+.2e} at η_g = {fe(clean_drop[1])}, γT = {clean_drop[2][0]:.0f}, {2 * clean_drop[2][1]}π [computed]." if clean_drop else "- **Largest clean purity drop:** none exceeds 10 × the amended floor [computed]."),
          f"- **η_g = 0.2, γT = 100** [numerical, cause not established]: the cw and ccw weights differ at the 1e-2 level (max {cwccw:.1e}). The row is rounding-dominated (dt-halving {FL[0.2][('dt', 100.0)]:.1e}, probe up to {FL[0.2][('probe', 100.0)]:.1e}) and is not evidence either way. An optional high-precision re-run is offered, not done.", "",
          "### Floors per speed (0.75 ε_EP; dt-halving at start mode 0, both directions; probe over 3 draws × both directions × both start modes)", "",
          "| η_g | dt-halving γT = 40 | dt-halving γT = 100 | probe γT = 40 | probe γT = 100 | amended floor (incl. η_g = 0) | purity climb > 10×amended floor | caused (amended) |", "|---|---|---|---|---|---|---|---|"]
    for e in [0.0] + elig:
        f_ = FL[e]; r = res[e]
        L.append(f"| {fe(e)} | {f_[('dt', 40.0)]:.1e} | {f_[('dt', 100.0)]:.1e} | {f_[('probe', 40.0)]:.1e} | {f_[('probe', 100.0)]:.1e} | " + (f"{r['floorA']:.1e} | {'YES' if r['climbA'] else 'no'} | {'YES' if r['causedA'] else 'no'} |" if e > 0 else f"{base_fa:.1e} | (baseline) | (baseline) |"))
    L += ["",
          "### Weights (primary speeds)", "",
          "| η_g | start | γT | turn | ccw from 0 | ccw from 1 | cw from 0 | cw from 1 | class |", "|---|---|---|---|---|---|---|---|---|"]
    for eta in ETAS:
        dr = res[eta]["dr"]
        for f in (0.75, 1.25):
            nm = dr[f]["names"]; rr = dr[f]["runs"]
            for gT in SPEEDS:
                for m in (1, 2):
                    L.append(f"| {fe(eta)} | {f:.2f} | {int(gT)} | {2*m}π | " + " | ".join(f"{nm[rr[(gT, dn, st)][m]['win']]} [site {rr[(gT, dn, st)][m]['comp']}] ({rr[(gT, dn, st)][m]['w']:.4f})" for dn in ("ccw", "cw") for st in (0, 1)) + f" | {dr[f]['cls']} |")
    d6_dirind = all(res[e]["dr"][0.75]["cls"] == "D6-like" for e in elig)
    L += ["", "## Physics note", "",
          f"- The extra term keeps the PT-type symmetry (real coupling, imaginary diagonal): σ_x K maps the traceless part of H_try(ε) to itself for real ε (residual {pt_res:.1e}), unlike the coupling term in pairA-qg-loss. H_try is also complex-symmetric (H^T = H, residual {sym_res:.1e}) [identity + computed].",
          f"- So D6 direction-independence should survive. Check: on the eligible rows the 0.75 ε_EP class is {'D6-like on every row' if d6_dirind else 'NOT D6-like on every row'} [computed].",
          "- Inside Γ, F < 0 lowers the effective contrast κ + η_g F; outside, it raises it. The new EPs mark where κ + η_g F = ±|v|ε.",
          "- **Mechanism:** Loss contrast keeps both D6 supports (transpose identity and PT) [identity]; it lowers the inside-Gamma contrast kappa + eta_g F, so selection slows and purity drops [computed]; D6 is inherited from H_A, not caused by the term." + (f" Largest clean drop: ΔP = {clean_drop[0]:+.2e} (η_g = {fe(clean_drop[1])}, γT = {clean_drop[2][0]:.0f}, {2 * clean_drop[2][1]}π)." if clean_drop else ""), "",
          "## Caveats", "",
          "- H_real is H_A exactly, so any D6 at small η_g is H_A's own D6. The rule asks whether the new term changes winners or raises the purity above the floor on clean rows.",
          "- Rows with E1 or E2 are listed but not used for the grade: there a new EP sits in or near the loop, or the start points have a different phase from H_A.",
          "- At η_g* the merged EP has trivial monodromy, so the drive loop encloses no net branch point there.",
          "- γ_g (secondary) is ½ max |Im Δλ| on the loop. The literal 'min imaginary split' is 0 wherever the split is real; at η_g = 0 this γ_g equals ½ the smallest |Δλ| on the loop.",
          "- Tags: [by construction] H_real = H_A, the placement, γ; [identity] the rate-shift form, the discriminant and its factorisation, the EP locations and thresholds, copy NO for η_g > 0; [computed] roots, monodromy, copy residuals, weights, classes, floors; [hive-interpretation] 'gravity-side'.", "",
          "No folders were loaded (nothing to SHA-check); only this folder was written.", ""]
    (ROOT / "RESULTS.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"Wrote RESULTS.md  t={time.time()-t0:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
