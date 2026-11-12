import json, datetime, hashlib
from continuum_two_pole import cap_flux
rows = [dict(n=n, h=h, cap=cap_flux(n, h=h)[0], hemisphere=cap_flux(n, h=h)[1]) for n in (1, 2) for h in (1e-3, 5e-4)]
d = {n: abs(rows[2*i+1]["cap"] - rows[2*i]["cap"]) for i, n in enumerate((1, 2))}
out = dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(), solver="continuum_two_pole.py " + hashlib.sha256(open("continuum_two_pole.py","rb").read()).hexdigest()[:8],
           R=3.0, r_c=1.5, rows=rows, cap_change_on_halving=d, limit=0.002, verdict="PASS" if max(d.values()) < 0.002 else "FAIL")
json.dump(out, open("CONTINUUM_GRID_CHECK.json", "w"), indent=1); print(json.dumps(out, indent=1))
