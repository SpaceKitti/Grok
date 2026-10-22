import csv, glob, os, numpy as np, hashlib, sys
O = r"C:\Users\Akitt\Grok\jobs\cone-sims\out"
def load(p, nfilter=None):
    d = {}
    for r in csv.DictReader(open(p, encoding="utf-8")):
        if int(r["level"]) > 20: continue
        d.setdefault((int(r["n"]), float(r["kappa"]), round(float(r["alpha"]), 4)), []).append((int(r["level"]), float(r["lambda"]), float(r["grad2"])))
    return {k: sorted(v) for k, v in d.items()}
ref = load(O + r"\hp2_reduced_32_nev20\hp2_flow_reduced.csv")
def summ(v):
    l = np.array([x[1] for x in v]); l20 = l[:20]
    return dict(min=l20.min(), low=", ".join("%.3e" % x for x in l20[:4]), nz=int((abs(l20) <= 1e-3).sum()), gap=(l[20]-l[19]) if len(l) > 20 else float("nan"), g2=v[0][2])
def tipw(V, N, c=3):
    V = V.reshape(4, N, N, -1); return (V[:, :c]**2).sum((0, 1, 2)) / (V**2).sum((0, 1, 2))
for tag, folder, N in (("(a) 48", "hp2_check_48_nev20", 48), ("(b) 32/10k", "hp2_iter10k", 32)):
    p = os.path.join(O, folder, "rows.csv")
    if not os.path.exists(p): print(tag, "rows.csv missing"); continue
    new = load(p); print("==", tag, "sha8", hashlib.sha256(open(p, "rb").read()).hexdigest()[:8].upper())
    for k in sorted(new):
        a, b = summ(new[k]), summ(ref[k])
        print(k, "NEW min=%.4e nz=%d gap=%.2e g2=%.1e low=[%s] | 32/5k min=%.4e nz=%d gap=%.2e g2=%.1e low=[%s] | |min| ratio new/ref=%.3f" % (a["min"], a["nz"], a["gap"], a["g2"], a["low"], b["min"], b["nz"], b["gap"], b["g2"], b["low"], abs(a["min"])/abs(b["min"]) if b["min"] else float("nan")))
        f = os.path.join(O, folder, "evecs_n%d_k%s_a%.2f.npy" % (k[0], k[1], k[2]))
        if os.path.exists(f):
            V = np.load(f); w = np.load(f.replace("evecs", "evals")); neg = np.where(w < -1e-3)[0]
            for c in (1, 3, 5): print("   tip weight (first %d radial cells, all 4 fields) neg modes:" % c, ", ".join("L%d ?=%.3e w=%.3f" % (j, w[j], t) for j, t in zip(neg, tipw(V, N, c)[neg])) or "none")
