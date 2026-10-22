# [SCRATCH H5] Venus guard: penalty XI_FACTOR = 5 vs 10 (xi = XI_FACTOR/lambda_min(G^T G)), grid 48, box only.
# PASS RULE (fixed before running): per case, (1) near-zero count identical at both penalties, where near-zero = modes
# below lambda_gap and lambda_gap = first |lambda| > C4_gap_split x |lambda_0| (run.py placeholder rule); (2) every mode
# in the 24-mode window matches to 4 significant figures ("%.3e"). The tiny negative modes are thereby allowed a
# 5th-digit difference. (3) gauge leakage |G^T v| <= 1e-5 at both penalties.
import sys, os; sys.argv = ["x", "--smoke"]
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "run.py"), encoding="utf-8").read().replace('if __name__ == "__main__":\n    main()', ''))
NEV, FACS = 24, (5.0, 10.0)
def nz(w):
    gap = next((lv for lv in w if abs(lv) > THR["C4_gap_split"]*max(abs(w[0]), 1e-300)), float("nan"))
    return int(np.sum(np.abs(w) < gap)), gap
ok_all = True
for (n, k, al) in [(1, 2.0, 0.75), (2, 1.0, 0.5)]:
    L = ConeLattice(48, 48, 10.0, al, k, n)
    x, E, g, it = L.relax(L.seed([(0.0, 0.0, n)]), 5000)
    res = {}
    for f in FACS:
        THR["XI_FACTOR"] = f
        w, V, xi = L.spectrum(x, NEV)
        res[f] = (w, xi, L.gauge_leak, *nz(w))
    (w5, xi5, lk5, c5, g5), (w10, xi10, lk10, c10, g10) = res[5.0], res[10.0]
    s5, s10 = [f"{v:.3e}" for v in w5], [f"{v:.3e}" for v in w10]
    mism = [i for i in range(NEV) if s5[i] != s10[i]]
    ok = (c5 == c10) and not mism and lk5 <= 1e-5 and lk10 <= 1e-5
    ok_all &= ok
    print(f"[SCRATCH H5] n={n} kappa={k} alpha={al} grid=48 |grad|={g:.1e}")
    print(f"  xi(5/lmin)={xi5:.2f} xi(10/lmin)={xi10:.2f}  near-zero count {c5} vs {c10}  lambda_gap {g5:.4e} vs {g10:.4e}  leak {lk5:.1e} vs {lk10:.1e}")
    print(f"  mode | 5/lmin | 10/lmin | |diff|")
    for i in range(NEV):
        print(f"  {i:2d} | {w5[i]: .4e} | {w10[i]: .4e} | {abs(w5[i]-w10[i]):.1e}{'  MISMATCH' if i in mism else ''}")
    print(f"  case {'PASS' if ok else 'FAIL'} (mismatches at 4 s.f.: {len(mism)})")
print("XI_GUARD", "PASS" if ok_all else "FAIL")
