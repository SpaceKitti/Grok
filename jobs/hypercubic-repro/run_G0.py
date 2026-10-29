import json, time, hashlib, numpy as np, hc_kernel as H, test_hc as T
h=lambda f: hashlib.sha256(open(f,'rb').read()).hexdigest()[:8].upper()
spec='/workspace/lift/HYPERCUBIC_REPRO_GATES.md'; assert h(spec)=='FDF44325'
res=dict(gate='G0', spec=h(spec), hc_kernel=h('hc_kernel.py'), test_hc=h('test_hc.py'), run_py=h('run.py'), kernels=h('kernels.py'), lattice=h('lattice.py'), L=24, seed=3, tol=1e-12)
t0=time.time(); res.update(T.G0_full(24,3)); res['G0_seconds']=round(time.time()-t0,1); print(res, flush=True)
t1=time.time(); t0d={}
for eps in (1,-1):
    hc=H.HCLoops(24,eps); U=H.bpst_links(hc,3.0); ia=hc.interior_action(U); tail=H.bpst_tail(ia['rball'],3.0)
    t0d[str(eps)]=dict(rho_t0=hc.rho_moment(U), S_over_8pi2=ia['S']/(8*np.pi**2), S_ball_over_8pi2=ia['S_ball']/(8*np.pi**2),
        S_out_over_8pi2=ia['S_outside']/(8*np.pi**2), continuum_tail=tail, boundary_excess=ia['S_outside']/(8*np.pi**2)-tail,
        eq19=H.eq19(eps,3.0), eq19_times_1mtail=H.eq19(eps,3.0)*(1-tail), Q_t0=hc.charge(U))
    print(eps, t0d[str(eps)], flush=True)
res['t0']=t0d; res['t0_seconds']=round(time.time()-t1,1); res['finished']=time.strftime('%Y-%m-%d %H:%M:%S %Z')
json.dump(res, open('out/G0.json','w'), indent=1)
