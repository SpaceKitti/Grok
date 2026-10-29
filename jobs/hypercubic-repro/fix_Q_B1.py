"""Recompute interior Q in out/B1.json with the corrected 1/(2pi^2) normalisation (static t=0 config; no flow), update hashes."""
import json, time, hashlib, hc_open as O
h = lambda f: hashlib.sha256(open(f, 'rb').read()).hexdigest()[:8].upper()
R = json.load(open('out/B1.json'))
for L in (24, 20):
    hc = O.HCOpen(L, 1); U = O.bpst_regular(hc, 3.0); Q = hc.interior_charge(U)    # config is eps-independent
    for e in ('1', '-1'):
        R[f'L{L}'][e]['Q_interior_t0_superseded_2x_bug'] = R[f'L{L}'][e]['Q_interior_t0']; R[f'L{L}'][e]['Q_interior_t0'] = Q
R['files_at_run'] = R.pop('files'); R['files_final'] = {f: h(f) for f in ('hc_open.py', 'test_open.py', 'hc_kernel.py', 'test_hc.py', 'run.py', 'kernels.py', 'lattice.py', 'run_B1.py', 'fix_Q_B1.py')}
R['Q_fix'] = 'interior_charge normalisation 1/pi^2 -> 1/(2pi^2) after run; only Q changed (G0/B0/G1/rho_0 do not use it); recomputed ' + time.strftime('%Y-%m-%d %H:%M:%S %Z')
json.dump(R, open('out/B1.json', 'w'), indent=1); print({L: R[f'L{L}']['1']['Q_interior_t0'] for L in (24, 20)})
