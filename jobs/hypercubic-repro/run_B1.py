"""B1 round: G0 on the open kernel, B0 clamp gate, then (if B0 passes) G1 static at L=24 and L=20. No flow."""
import json, time, hashlib, numpy as np, hc_open as O, hc_kernel as H, test_open as TO
h = lambda f: hashlib.sha256(open(f, 'rb').read()).hexdigest()[:8].upper()
SPEC = '/workspace/lift/HYPERCUBIC_REPRO_GATES_FINAL.md'; B1 = '/workspace/lift/HYPERCUBIC_BOUNDARY_FIX_B1.md'
assert h(SPEC) == '1A723DCE' and h(B1) == '2BA983A1'
R = dict(spec=h(SPEC), boundary_fix=h(B1), files={f: h(f) for f in ('hc_open.py', 'test_open.py', 'hc_kernel.py', 'test_hc.py', 'run.py', 'kernels.py', 'lattice.py', 'run_B1.py')},
         setup=dict(box='open, no wrap', clamp='links touching site layers 0,1 from each face', interior_gauge='regular (B1 unspecified)', centre='cell centre (L-1)/2', rho=3.0, nsub=16, cooling='none'))
dump = lambda: json.dump(R, open('out/B1.json', 'w'), indent=1, default=float)
T0 = time.time(); t = time.time(); R['G0'] = TO.G0_open_full(24, 3); R['G0']['seconds'] = round(time.time()-t, 1); print('G0', R['G0'], flush=True); dump()
EIGHTPI2 = 8*np.pi**2; rho = 3.0
def static(L, eps):
    hc = O.HCOpen(L, eps); U = O.bpst_regular(hc, rho); out = {}
    S, dens = hc.action(U, per_site=True); d = hc.dist.reshape(-1); rb = L/2-3; tail = H.bpst_tail(rb, rho)
    cont_site = O.continuum_density(d, rho)
    # B0a: loops containing a clamped link, lattice minus continuum (c_s s^4 x plane density at loop centre; BPST: each plane = density/6)
    lm = hc.clamp_loop_mask(U); Sc = hc.action(U, loop_mask=lm); Cc = 0.0
    for s, cs in hc.loops():
        for mu in range(4):
            for nu in range(mu+1, 4):
                ctr = hc.X.copy(); ctr[..., mu] += s/2; ctr[..., nu] += s/2
                dc = np.sqrt(((ctr-hc.centre)**2).sum(-1)); Cc += float((hc.valid(mu, nu, s)*lm(mu, nu, s)*cs*s**4*O.continuum_density(dc, rho)/6).sum())
    out['B0_clamp_loops'] = dict(S_lat_over_8pi2=Sc/EIGHTPI2, S_cont_over_8pi2=Cc/EIGHTPI2, excess_over_8pi2=(Sc-Cc)/EIGHTPI2)
    sl = (hc.layer.reshape(-1) <= 2)
    out['B0_clamp_sites_layer_le2'] = dict(S_lat_over_8pi2=float(dens[sl].sum())/EIGHTPI2, S_cont_over_8pi2=float(cont_site[sl].sum())/EIGHTPI2,
                                         excess_over_8pi2=float((dens[sl]-cont_site[sl]).sum())/EIGHTPI2)
    ball = d <= rb; Sb = float(dens[ball].sum())
    out.update(S_total_over_8pi2=S/EIGHTPI2, S_ball_over_8pi2=Sb/EIGHTPI2, S_outside_over_8pi2=(S-Sb)/EIGHTPI2, rball=rb, continuum_tail=tail,
               boundary_excess_over_8pi2=(S-Sb)/EIGHTPI2-tail, continuum_in_box_outside_ball_over_8pi2=float(cont_site[~ball].sum())/EIGHTPI2,
               eq19=H.eq19(eps, rho), G1_target=H.eq19(eps, rho)*(1-tail))
    out['G1_rel_dev'] = out['S_ball_over_8pi2']/out['G1_target'] - 1; out['G1_pass'] = bool(abs(out['G1_rel_dev']) <= 0.01)
    out['rho_0'] = hc.rho_moment(U); out['Q_interior_t0'] = hc.interior_charge(U); return out
t = time.time(); R['L24'] = {str(e): static(24, e) for e in (1, -1)}; R['L24_seconds'] = round(time.time()-t, 1); print('L24', R['L24'], flush=True)
b0 = max(abs(R['L24'][k]['B0_clamp_loops']['excess_over_8pi2']) for k in R['L24']); R['B0'] = dict(max_abs_excess_over_8pi2=b0, limit=0.01, pass_=bool(b0 <= 0.01)); dump()
if R['B0']['pass_']:
    t = time.time(); R['L20'] = {str(e): static(20, e) for e in (1, -1)}; R['L20_seconds'] = round(time.time()-t, 1)
    R['G1'] = {e: dict(dev24=R['L24'][e]['G1_rel_dev'], dev20=R['L20'][e]['G1_rel_dev'], box_err=abs(R['L24'][e]['G1_rel_dev']-R['L20'][e]['G1_rel_dev']),
                       pass24=R['L24'][e]['G1_pass'], pass20=R['L20'][e]['G1_pass']) for e in ('1', '-1')}
    print('G1', R['G1'], flush=True)
R['total_seconds'] = round(time.time()-T0, 1); R['finished'] = time.strftime('%Y-%m-%d %H:%M:%S %Z'); dump(); print('DONE', flush=True)
