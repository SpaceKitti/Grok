"""E/(pi|n|) for the 8 main rows with cone_v1_4b (self-dual energy). Cheap: single grid DR=w_N/20."""
import json, numpy as np, cone_v1_4b as b
rows = []
for al in (0.9, 0.75, 0.5, 1/3):
    for n in (1, 2):
        s = b.solve(al, n, b.W_N / 20); rows.append(dict(alpha=al, n=n, E_over_pin=s["E"]/(np.pi*n), ok=s["ok"])); print(rows[-1], flush=True)
json.dump(dict(code="cone_v1_4b.py", dr="w_N/20", rows=rows), open("CONE_ENERGY_V1_4b.json", "w"), indent=1)
