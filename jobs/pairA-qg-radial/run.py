"""pairA-qg-radial: `python run.py` writes RESULTS.md and stops. No folders are loaded. match.py is imported only after all roots are computed and logged."""
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

import mpmath as mp  # noqa: E402
import sympy as sp  # noqa: E402

import families as FA  # noqa: E402
import inputs as IN  # noqa: E402
import roots as RT  # noqa: E402

FAMS = list(IN.FAMILY_KEYS)


def nz(z, d=12):
    z = mp.mpc(z)
    if abs(mp.im(z)) < mp.mpf(10) ** -100 * max(1, abs(z)):
        return mp.nstr(mp.re(z), d)
    return f"{mp.nstr(mp.re(z), d)} {'+' if mp.im(z) >= 0 else '-'} {mp.nstr(abs(mp.im(z)), d)}i"


def inputs_block(fam):
    rows = [f"| {k} | {('computed: ' + mp.nstr(IN.val(k), 12)) if IN.INPUTS[k][1] == 'extremality' else IN.val(k)} | {IN.INPUTS[k][1]} |" for k in IN.FAMILY_KEYS[fam]]
    return ["| input | value | fixing rule |", "|---|---|---|"] + rows + ["", f"Free scales: **{IN.free_count(fam)}** (each 'free' set to its neutral convention)."]


def roots_block(rts):
    return ["| root | multiplicity | physical | label | note |", "|---|---|---|---|---|"] + [f"| {nz(x['v'])} | {x['mult']} | {'yes' if x['phys'] else 'no'} | {x['label']} | {x['note']} |" for x in rts]


def main() -> int:
    t0 = time.time()
    assert "match" not in sys.modules
    bad, hits, nforb = IN.scan()
    print(f"inputs: rule problems {bad}; forbidden hits {hits} (scanned against {nforb} values)")
    if bad or hits:
        raise SystemExit("forbidden input or missing rule: stop")
    r1, i1 = RT.fam1()
    r2, i2 = RT.fam2()
    r3 = RT.fam3()
    r40, r4e, i4 = RT.fam4()
    bad2, hits2, _ = IN.scan()          # re-scan with the extremality-computed Q
    print(f"re-scan after roots: rule problems {bad2}; hits {hits2}")
    if bad2 or hits2:
        raise SystemExit("forbidden input after computing Q: stop")
    ALL = {FAMS[0]: r1, FAMS[1]: r2, FAMS[2]: r3[FAMS[2]][0], FAMS[3]: r3[FAMS[3]][0], FAMS[4]: r3[FAMS[4]][0], FAMS[5]: r40 + r4e}
    for k, v in ALL.items():
        print(k, [(nz(x["v"], 8), x["mult"], x["phys"]) for x in v])

    rs = FA.rescaling_check()
    print(f"rescaling check: {rs}")
    Lam1, Q1, rN = i1["Lam"], i1["Q"], i1["rNc"]
    MN_formula = Q1 ** 2 / rN + Lam1 * rN ** 3 / 3
    L = ["# pairA-qg-radial — RESULTS", "",
         "**Signed off 2026-09-26:** Venus (maths) and Helios (physics).", "",
         "Does a standard gravity family give a radial equation whose root lands on Pair A's tip, with no Pair A input and no tuned scale? No folders loaded. Conventions: Planck units G = c = ħ = 4πε₀ = 1; each free scale is set to 1 in its own units (the Liouville V amplitude is set to −1 so that a real horizon exists) [by construction].", "",
         f"Firewall: every input carries a fixing rule (rule problems: {len(bad)}), and the forbidden-input scan found **{len(hits)}** hits against {nforb} Pair A numbers and combinations (re-scan after computing the extremal Q: {len(hits2)} hits) [computed]. The target appears only in match.py, which is imported after this section was built.", "",
         "**Global caveat:** eps is a dimensionless drive parameter; every gravity root is a length, so the comparison needs a unit (Planck units here, itself a convention). Even an exact hit would be [by construction: unit choice].", "",
         "## Raw roots (computed before any matching)", ""]
    # F1
    L += ["### F1 Einstein–Maxwell–Λ", "",
          f"Equation: f(r) = `{FA.F1_f}` = 0, i.e. r² f = `{FA.F1_poly}` = 0 [standard].",
          f"Extremal / Nariai conditions: {FA.F1_EXTREMAL} [standard + identity].", ""] + inputs_block(FAMS[0]) + ["", *roots_block(r1), "",
          f"- Checks: polynomial relative residual {mp.nstr(i1['res'], 3)}; deflation remainders {mp.nstr(i1['rem'], 3)}; cold-branch formula vs extremal root {mp.nstr(i1['rcold_vs_re'], 3)} [computed].",
          f"- Extremal Q = {mp.nstr(i1['Q'], 15)} (from M and Λ). Nariai at this Λ: Q = 0 needs M_N = 1/(3√Λ) = {mp.nstr(i1['MN0'], 6)}, r_N = 1/√Λ = {mp.nstr(i1['rN0'], 6)}; charged Nariai for this Q has r_N = {mp.nstr(rN, 6)} with **M = Q²/r_N + Λr_N³/3 = {mp.nstr(MN_formula, 6)}** (≈ r_N/3 = {mp.nstr(rN / 3, 6)}; cross-check r_N − (2/3)Λr_N³ = {mp.nstr(i1['MNc'], 6)}). Not realised at M = 1 [computed].",
          "- Helios: at r ~ 1 Planck length, Λ's effect is ~1e-122, so F1 is Reissner–Nordström in practice (extremal Q = M). The only real scale is M, which is free, so PARTIAL [by construction]. Planck 2018 Λ is the honest external choice [standard].", ""]
    # F2
    r2_main = [x for x in r2 if "k = 0" not in x["label"]]
    r2_ind = [x for x in r2 if "k = 0" in x["label"]]
    for x in r2_ind:
        x["note"] = "[indicative only; outside linear validity] (m2 r = " + mp.nstr(i2["m2"] * mp.re(x["v"]), 3) + ")"
    L += ["### F2 Stelle / quadratic gravity", "",
          FA.F2_CONV,
          f"Equation used: linearised static metric h(r) = `{FA.F2_h}` = 0 (Stelle 1978, α = 0), m₂ = 1/√(2β_W) [standard]. **A full numerical LPPS shooting solve was not done**: the non-Schwarzschild branch is represented by its characteristic radii (the Yukawa radius 1/m₂ and the bifurcation radius 0.876/m₂) and by the zeros of the linearised h. Zeros: r = 2M + W_k(z)/m₂, z = −(4m₂M/3)e^{{−2m₂M}} = {nz(i2['z'], 10)} [identity], with infinitely many complex branches (k = −3…3 listed).",
          "Whether β in mass-scale units is theory-fixed: **free** (a coupling of the theory; nothing in the theory fixes it) [standard].",
          "Dimensional argument [identity]: with G = 1 and α = 0 the only scales are M (a length) and m₂ = 1/√(2β_W) (an inverse length), so r_h = g(m₂M)/m₂. Also, r = 2M solves the full Stelle equations for every β_W (Ricci-flat metrics solve quadratic gravity) [standard], so M alone can place a root anywhere, and a full LPPS solve could only reproduce PARTIAL [by construction]. The LPPS branch only exists near m₂r_h ≲ 0.876 [standard].", ""] + inputs_block(FAMS[1]) + ["", *roots_block(r2_main), "",
          "Linearised zero, listed separately (not on a par with the roots above):", "", *roots_block(r2_ind), "",
          f"- Checks: max |h| at the Lambert-W zeros {mp.nstr(i2['res'], 3)} [computed]. Caveat: the linearised h is not reliable at r ~ 2M (strong field); its zero is indicative only.", ""]
    # F3
    L += ["### F3 2D dilaton gravity (Killing norm ξ = 0)", "",
          "General solution: ξ(X) = e^{Q(X)}(w(X) − C), with Q = ∫U dX and w = −2∫e^{Q}V dX, for S = ∫√−g [XR − U(X)(∇X)² − 2V(X)] [standard form, Grumiller–Kummer–Vassilevich 2002 review; normalisation by construction so that SRG gives 1 − 2C/r].", ""]
    for key, nm in ((FAMS[2], "SRG"), (FAMS[3], "CGHS"), (FAMS[4], "Liouville")):
        mdl = FA.F3_MODELS[nm]; rts, inf = r3[key]
        L += [f"#### {key}", "",
              f"U = `{mdl['U']}`, V = `{mdl['V']}` (parameters: {mdl['params_U']} in U, {mdl['params_V']} in V, plus the mass Casimir C). Coordinate: {mdl['coord']}.",
              f"ξ(X) = `{inf['K']}`" + (f"; in r: `{inf['Kr']}`" if "Kr" in inf else "") + f" [computed]. |ξ| at the real root: {inf['chk']:.1e}.",
              {"SRG": "Root set by: C (= M) only.", "CGHS": "Root set by: λ and C (X_h = C/(4λ²)).", "Liouville": "Root set by: p, q, s and C (e^{(p+s)X_h} = −C(p+s)/(2q)). V amplitude −1: the same sign as SRG and CGHS in this action convention, and it allows a real Killing horizon; a consistent convention [by construction]. Caveat: X is the dilaton, not an areal radius, so comparing X_h with eps_EP depends even more on the coordinate."}[nm], ""] + inputs_block(key) + ["", *roots_block(rts), ""]
    # F4
    L += ["### F4 R1-like product chart AdS₂ × S² (Einstein–Maxwell–Λ, ε as the radial coordinate)", "",
          "Ansatz: ds² = −h(ε)dt² + dε²/h(ε) + r(ε)² dΩ², electric field F_tε = Q/r² (Maxwell solved). Equations E^μ_ν = G^μ_ν + Λδ^μ_ν − 8πT^μ_ν = 0 [standard].",
          f"- Normalisation check: RNdS (r = ε, h = f) gives residuals {i4['rnds']} [computed].",
          f"- E^t_t − E^ε_ε = G^t_t − G^ε_ε = `{i4['diff']}` [computed]. G^t_t − G^eps_eps = +2h r''/r (mostly-plus) [sign corrected; r'' = 0 unaffected], so **r'' = 0** along ε: r = αε + r₀. α ≠ 0 is F1 again (r = ε after a shift). r = const [by construction of the AdS2xS2 ansatz; alpha != 0 is F1].",
          f"- Product (r = r₀): `{i4['eqs_p'][0]}` = 0 and `{i4['eqs_p'][2]}` = 0, so Λr₀⁴ − r₀² + Q² = 0 (the same quartic as F1's extremal condition [identity]) and h'' = 2(Q²/r₀⁴ − Λ) = 2/l². General solution h = ε²/l² + c₁ε + c₀. After the ε-shift isometry, h = (ε² − ε_h²)/l², with **ε_h a free integration constant** (the AdS₂ black-hole temperature) [computed + standard].",
          f"- r(ε) has no zeros at all: it is constant. The zeros of h sit at ±ε_h, a ± pair by construction, but their location is not fixed by the field equations. l² = {mp.nstr(i4['l2'], 12)} on the AdS₂ branch [computed].",
          f"- **Rescaling check (sympy):** under ε = ε_h u, t = τ/ε_h the metric becomes g_ττ = `{rs['g_tautau']}`, g_uu = `{rs['g_uu']}`, F_τu = `{rs['F']}`. ε_h removed: **{rs['eps_h_removed']}**. Zeros of h at u = {rs['zeros_u']} [computed].", ""] + inputs_block(FAMS[5]) + ["", "r₀ roots:", "", *roots_block(r40), "", "zeros of h(ε) (neutral ε_h = 1):", "", *roots_block(r4e), ""]

    # ---------------- matching (only now)
    import match as MT  # noqa: E402
    Lsym, xs = sp.symbols("L x", positive=True)
    I_ov = sp.simplify(2 / Lsym * sp.integrate(xs * sp.sin(sp.pi * xs / Lsym) * sp.sin(2 * sp.pi * xs / Lsym), (xs, 0, Lsym)))
    I_c = sp.simplify(2 / Lsym * sp.integrate((xs - Lsym / 2) * sp.sin(sp.pi * xs / Lsym) * sp.sin(2 * sp.pi * xs / Lsym), (xs, 0, Lsym)))
    num = sp.N(I_ov.subs(Lsym, 2), 12)
    ov = {"I": I_ov, "I_c": I_c, "eq": sp.simplify(I_ov + 16 * Lsym / (9 * sp.pi ** 2)) == 0, "num": num,
          "rel_v": f"{float(abs(abs(num) - sp.Rational('0.360253')) / sp.Rational('0.360253')):.1e}",
          "eps": sp.N(27 * sp.pi ** 4 / 5120, 12), "eps_id": sp.simplify((3 * sp.pi ** 2 / 80) / (2 * 32 / (9 * sp.pi ** 2)) - 27 * sp.pi ** 4 / 5120)}
    eta_s = sp.symbols("eta", positive=True)
    kap = 3 * eta_s * sp.pi ** 2 / (2 * Lsym ** 2)
    eps_gen = sp.simplify(kap / (16 * Lsym / (9 * sp.pi ** 2)))
    ov["eps_gen"] = eps_gen
    ov["eps_gen_ok"] = sp.simplify(eps_gen - 27 * eta_s * sp.pi ** 4 / (32 * Lsym ** 3)) == 0
    ov["eps_gen_box"] = sp.simplify(eps_gen.subs({eta_s: sp.Rational(1, 20), Lsym: 2}) - 27 * sp.pi ** 4 / 5120) == 0
    ov["kap_ok"] = sp.simplify(kap - (eta_s * (2 * sp.pi / Lsym) ** 2 - eta_s * (sp.pi / Lsym) ** 2) / 2) == 0
    ov["foot_L2"] = sp.simplify(sp.Rational(1, 2) * (8 / (3 * sp.pi)) ** 2 - 16 * 2 / (9 * sp.pi ** 2))
    ov["foot_Lpi"] = sp.simplify(16 * sp.pi / (9 * sp.pi ** 2))
    print(f"overlap check: {ov}")
    print("match.py imported after roots")
    hyp = MT.hypotheticals(i1, i2)
    hyp[FAMS[5]] = ["F4: the +-eps_h pair exists by construction of the AdS2 black-hole chart, but eps_h is removable by a coordinate rescaling (diffeomorphism) eps = eps_h u, t = tau/eps_h [standard], so gravity cannot fix its location: MISSING. Only eps_h>0 (black-hole patch) vs eps_h=0 (Poincare patch) is physical; the pair always sits at u = +-1 in the chart's own units, so matching it to +-eps_EP is exactly the unit choice in the global caveat." + f" [sympy check: eps_h removed = {rs['eps_h_removed']}]"]
    L += ["## Match test (match.py, run after the raw roots above)", "",
          f"r = eps_EP is a match test, not an input. Relative error of the closest physical root to {mp.nstr(MT.TARGET, 9)} (taken from match.py), with the free scales at their neutral convention. Hypothetical values that WOULD hit are information only; nothing was tuned.", "",
          "| family | free scales | closest physical root | rel. error | closest over all roots | ± pair? | L6-type r² ≈ 0.453 root? | tag | grade |", "|---|---|---|---|---|---|---|---|---|"]
    summary = {}
    for fam in FAMS:
        rts = ALL[fam]
        b, e = MT.closest(rts)
        ba, ea = MT.closest(rts, phys_only=False)
        l6 = MT.l6_hits(rts)
        free = IN.free_count(fam)
        closes = not fam.startswith("F4")
        g = MT.grade(fam, e, free, bool(hits), closes_without_pairA=closes)
        tag = "[by construction]" if g.startswith("PARTIAL [by") else ("[computed]" if g != "HAVE" else "[predicted]")
        summary[fam] = g
        L.append(f"| {fam} | {free} | {nz(b['v'], 10) if b else '—'} | {mp.nstr(e, 4) if e is not None else '—'} | {nz(ba['v'], 8)} ({mp.nstr(ea, 3)}) | {MT.PM[fam]} | {'YES: ' + ', '.join(nz(x['v'], 8) for x in l6) if l6 else 'no'} | {tag} | **{g}** |")
    L += ["", "### Hypothetical placements (information only, not tuned) [PARTIAL, by construction]", ""]
    for fam in FAMS:
        L += [f"- **{fam}:** " + " ".join(hyp[fam])]
    L += ["", "## Extra roots (logged, never hidden)", "",
          "- F1: besides the extremal (double) horizon, a cosmological horizon at r ≈ √(3/Λ) ~ 1e61 and a negative root of r²f at about −1e61 (unphysical). No Nariai root is realised at M = 1, and nothing near r² ≈ 0.453. Pair A has a single ± pair; F1 has three distinct roots (four with multiplicity) and no ± pair.",
          "- F2: two characteristic radii, plus the linearised-h zeros: one physical real zero (k = 0), one negative real zero (k = −1, unphysical), and infinitely many complex Lambert-W zeros (k = ±1, ±2, …; seven branches listed).",
          "- F3: SRG has one root. CGHS has one root in X; the complex r-copies are log-branch artefacts of X = e^{2λr}. Liouville has one real root and infinitely many complex ones, X_k = X_0 + 2πik/(p+s).",
          "- F4: four r₀ roots: one physical AdS₂ × S² (r₀ = +1), its negative (unphysical), and a charged-Nariai dS₂ × S² pair at |r₀| ≈ 1/√Λ (dS₂, not AdS₂: the extra Nariai-type root, at ~6e60, not at 0.453). h(ε) has the ± pair ±ε_h.", "",
          "- F2's linearised zero (listed separately) has relative error " + ", ".join(f"{mp.nstr(MT.rel(x['v']), 4)} (r = {nz(x['v'], 8)})" for x in r2_ind) + " [indicative only; outside linear validity].", "",
          "## Side observations (notes only; not inputs)", "",
          f"- π² note: a = π²/80 = {mp.nstr(mp.pi ** 2 / 80, 10)} and b = π²/20 = {mp.nstr(mp.pi ** 2 / 20, 10)} match the given a = 0.12337 and b = 0.49348 to all 5 digits given (relative differences {mp.nstr(abs(mp.pi ** 2 / 80 - mp.mpf('0.12337')) / mp.mpf('0.12337'), 2)} and {mp.nstr(abs(mp.pi ** 2 / 20 - mp.mpf('0.49348')) / mp.mpf('0.49348'), 2)}), and b = 4a exactly (4 × 0.12337 = {mp.nstr(4 * mp.mpf('0.12337'), 6)}). So eps_EP = (b − a)/(2|v|) = 3π²/(160|v|) (relative difference from the match target: {mp.nstr(abs(3 * mp.pi ** 2 / (160 * mp.mpf('0.360253'))) / MT.TARGET - 1, 2)}, computed after matching). A ratio of 4 with π² fits the n = 1 and n = 2 decay rates of a diffusing box (γ_n ~ n²π²) [confirmed by Akitti 2026-09-26: Dirichlet slab, eta=0.05, L=2, n=1,2 modes]. Not used anywhere as an input.",
          f"- v = <sine_1|x|sine_2> on the L=2 Dirichlet slab = -16L/(9 pi^2) = -32/(9 pi^2) [confirmed by Akitti 2026-09-26; post-hoc]; the whole Pair A triple (a, b, v) is the 2-mode Galerkin of A = eps x + i eta d_xx; eps_EP = 27 pi^4/5120 is fixed by eta, L only. Sympy check [computed]: (2/L)∫₀^L x sin(πx/L) sin(2πx/L) dx = `{ov['I']}` (equals −16L/(9π²): {ov['eq']}); with x − L/2: `{ov['I_c']}`; at L = 2: {ov['num']} (|value| vs 0.360253: relative difference {ov['rel_v']}). 27π⁴/5120 = {ov['eps']} (relative difference from the match target: {mp.nstr(abs(mp.mpf(ov['eps']) / MT.TARGET - 1), 2)}; identity check (3π²/80)/(2·32/(9π²)) − 27π⁴/5120 = {ov['eps_id']}).",
          f"- General form [identity, given the 2-mode Galerkin]: eps_EP = kappa/|v| = (3 eta pi^2/(2L^2)) / (16L/(9 pi^2)) = 27 eta pi^4/(32 L^3), which gives 27 pi^4/5120 at eta = 0.05, L = 2. Sympy [computed]: κ = (b − a)/2 = 3ηπ²/(2L²): {ov['kap_ok']}; κ/|v| = `{ov['eps_gen']}`, equals 27ηπ⁴/(32L³): {ov['eps_gen_ok']}; at η = 1/20, L = 2 equals 27π⁴/5120: {ov['eps_gen_box']}. The tip is where the linear drive eps x just matches the diffusion contrast between the two modes; it moves in proportion to eta and falls as 1/L^3.",
          "- Post-hoc (2026-09-26): eps_EP = 3pi^2/(160|v|) is an MHD box number (eta, L, v); gravity families with generic couplings cannot produce it without feeding the box in, consistent with NOT HAVE. The source of v is still open.", "",
          f"- Footnote: |v| = 1/2 (8/(3pi))^2 [numerical coincidence: holds only at L = 2, where 16L/(9 pi^2) = 1/2 (8/(3pi))^2; on L = pi the real coupling is 16/(9 pi)]. Sympy: ½(8/(3π))² − 32/(9π²) = {ov['foot_L2']}; 16L/(9π²) at L = π = `{ov['foot_Lpi']}` [computed].", "",
          "## Summary", ""]
    for fam in FAMS:
        L.append(f"- {fam}: **{summary[fam]}**")
    have_any = any(g == "HAVE" for g in summary.values())
    L += ["", f"**Overall: {'HAVE' if have_any else 'NOT HAVE'}**: {'some family is HAVE with no tuned scale' if have_any else 'no family is HAVE; the best outcome is PARTIAL [by construction] (one free scale can always be placed), and F4 is MISSING (the ±eps_h pair exists by construction, but eps_h is removable by a coordinate rescaling, so gravity cannot fix its location)'} [computed].", "",
          "## Conventions chosen", "",
          "- Planck units G = c = ħ = 4πε₀ = 1; Λ from Planck 2018 times l_P².",
          "- F1: Q fixed by extremality (cold branch) for the given M and Λ; M free = 1.",
          "- F2: LPPS sign convention (L = R − β_W C² + αR², m₂ = 1/√(2β_W)); the spec's +βC² is β = −β_W. α drops out for static black holes. Linearised metric used instead of a full shooting solve.",
          "- F3: GKV-type action and general solution; U, V normalised so that SRG gives 1 − 2C/r; CGHS radial coordinate from X = e^{2λr}; Liouville V amplitude −1.",
          "- F4: ε_h (integration constant) set to 1 as the neutral value; the chart's ε origin fixed by the shift isometry.", "",
          "## Final lines", "",
          "RADIAL EQUATION FROM GRAVITY: HAVE only if some family is HAVE with no tuned scale.",
          "r = eps_EP is a match test, not an input.",
          "No claim that Pair A is a quantum-gravity result, that it has a JT dual, or that it is an Einstein solution. The standard solutions used here are textbook solutions of their own theories; matching or not matching a number says nothing about Pair A's physics.",
          "gravity-side is hive language [hive-interpretation]", ""]
    (ROOT / "RESULTS.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"summary {summary}; overall {'HAVE' if have_any else 'NOT HAVE'}; wrote RESULTS.md t={time.time()-t0:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
