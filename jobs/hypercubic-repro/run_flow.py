"""B1 flow runs G2/G3/G4 on open box (hc_open A08C51E2 unchanged). Flow = unchanged Loops.flow (RK3), called in 25-step chunks
for checkpoint/resume and rho(t) diagnostic every 25 steps (diagnostic only, not a gate). Usage: run_flow.py G2|G3|G4"""
import sys, os, json, time, hashlib, numpy as np, hc_open as O
h8 = lambda f: hashlib.sha256(open(f, 'rb').read()).hexdigest()[:8].upper()
assert h8('/workspace/lift/HYPERCUBIC_REPRO_GATES_FINAL.md') == '1A723DCE' and h8('/workspace/lift/HYPERCUBIC_BOUNDARY_FIX_B1.md') == '2BA983A1'
assert h8('hc_open.py') == 'A08C51E2'
G = sys.argv[1]; cfg = dict(G2=(-1, 0.002, 300, 2.8778), G3=(1, 0.002, 300, 2.9447), G4=(-1, 0.001, 600, 2.8778))[G]
eps, hstep, N, rho0_ref = cfg; L = 24; CH = 25
hc = O.HCOpen(L, eps); ck = f'out/{G}_ckpt.npz'; js = f'out/{G}.json'
if os.path.exists(ck):
    z = np.load(ck, allow_pickle=True); U = z['U']; R = json.loads(str(z['R'])); print('resume at step', R['steps_done'], flush=True)
else:
    U = O.bpst_regular(hc, 3.0); r0 = hc.rho_moment(U)
    R = dict(gate=G, eps=eps, h=hstep, steps=N, T=hstep*N, L=L, rho_init=3.0, cooling='none', rho0=r0, rho0_ref=rho0_ref,
             Q_interior_t0=hc.interior_charge(U), S0=hc.action(U)/(8*np.pi**2), steps_done=0, rho_t=[[0.0, r0]], S_t=[[0.0, hc.action(U)/(8*np.pi**2)]],
             files={f: h8(f) for f in ('hc_open.py', 'hc_kernel.py', 'kernels.py', 'lattice.py', 'run_flow.py')},
             spec='1A723DCE', boundary_fix='2BA983A1', started=time.strftime('%Y-%m-%d %H:%M:%S %Z'), wall_s=0.0)
    assert abs(r0 - rho0_ref) < 1e-3, r0
while R['steps_done'] < N:
    t = time.time(); U, _ = hc.flow(U, h=hstep, max_steps=CH, record=CH)
    R['steps_done'] += CH; tt = R['steps_done']*hstep; S = hc.action(U)/(8*np.pi**2)
    if S > R['S_t'][-1][1]: R['WARN_S_rose'] = R.get('WARN_S_rose', []) + [tt]
    R['rho_t'].append([tt, hc.rho_moment(U)]); R['S_t'].append([tt, S]); R['wall_s'] += time.time()-t
    np.savez(ck, U=U, R=json.dumps(R, default=float)); json.dump(R, open(js, 'w'), indent=1, default=float)
    print(time.strftime('%H:%M:%S'), G, 'step', R['steps_done'], 'rho', R['rho_t'][-1][1], 'S', S, flush=True)
rf = R['rho_t'][-1][1]; R['rho_flowed'] = rf; R['ratio'] = rf/R['rho0']; R['signed_shift'] = R['ratio']-1; R['Q_interior_T'] = hc.interior_charge(U)
if G == 'G2': R['pass'] = bool(R['ratio'] >= 0.95)
if G == 'G3': R['pass'] = bool(R['ratio'] < 1)
if G == 'G4':
    g2 = json.load(open('out/G2.json')); R['G2_ratio'] = g2['ratio']; R['delta_vs_G2'] = R['ratio']-g2['ratio']
    R['delta_rho_shift_abs'] = (rf-3)/3 - (g2['rho_flowed']-3)/3; R['pass'] = bool(abs(R['delta_vs_G2']) <= 0.01)
R['finished'] = time.strftime('%Y-%m-%d %H:%M:%S %Z'); json.dump(R, open(js, 'w'), indent=1, default=float); print('DONE', R['pass'], flush=True)
