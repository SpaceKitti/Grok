#!/usr/bin/env python3
"""Re-grade Probe B R3 per Y_JUNCTION_B_R3_GRADER_FIX_ADDENDUM.md decabc9d (G1 basis-free rank, G2 DEGENERATE, G3 literal peaks).
Saved npz only, no solves. Venus 2026-11-09."""
import json, os, sys, hashlib, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); CONE=os.path.abspath(os.path.join(HERE,'..','fuzz','cone'))
sys.path.insert(0,os.path.join(CONE,'v2_1')); from fuzzy_cone_v2_1 import Model
sha=lambda p: hashlib.sha256(open(p,'rb').read()).hexdigest()[:8]
SW=os.path.join(CONE,'SWEEP_probe_B_r3.json'); OLD=os.path.join(CONE,'RESULT_PROBE_B_R3.json')
sweep=json.load(open(SW)); rows=[r for r in sweep['rows'] if r.get('status')=='ok']
def rank(npz):
    d=np.load(npz); M=Model(int(d['N']),int(d['n']),R=float(d['R']),wrad=float(d['wrad']))
    X,P,*_=M.pieces(d['x']); P=np.asarray(P); X3=np.asarray(X[2])
    w,U=np.linalg.eigh(P@P.conj().T); K=U[:,w<1e-8]
    lam=np.linalg.eigvalsh(K.conj().T@X3@K)/np.sqrt(M.c)
    return int((lam>0).sum()), int((lam<0).sum()), K.shape[1], np.round(lam,4).tolist()
out=[]
for r in rows:
    rN,rS,kd,lam=rank(r['npz'])
    out.append(dict(start=r['start'],b=float(r['b']),N=int(r['N']),seed=int(r['kick_seed']),conv=bool(r['convergence']['converged']),
        rank_N=rN,rank_S=rS,kernel_dim=kd,x3_eigs=lam,peaks_N=int(r['probe_B']['peaks_north']['n_peaks']),peaks_S=int(r['probe_B']['peaks_south']['n_peaks']),
        A3=float(r['probe_B']['A3']),E=float(r['E']),absQ6=float(r['flux'].get('abs_Q_minus_6',abs(r['flux']['Q_total']-6)))))
g=[o for o in out if o['start']=='S1' and o['b']==2.0 and o['N'] in (61,81)]
und=[f"S1 N={o['N']} s{o['seed']} nonconv" for o in g if not o['conv']]
brk=[f"S1 N={o['N']} s{o['seed']} rank {o['rank_N']}/{o['rank_S']}" for o in g if o['conv'] and (o['rank_N'],o['rank_S'])!=(3,3)]
brk+=[f"S1 N={o['N']} s{o['seed']} |Q-6|" for o in g if o['conv'] and o['absQ6']>3e-2]
E=lambda s,N,sd: next(o['E'] for o in out if o['start']==s and o['b']==2.0 and o['N']==N and o['seed']==sd)
grid=abs(E('S1',81,0)-E('S1',61,0))
b2=[o for o in out if o['b']==2.0 and o['N'] in (61,81)]
dE=max(abs(E('S1',N,sd)-E('S2',N,sd)) for N in (61,81) for sd in (0,1,2))
degen=len(b2)==12 and all(o['conv'] for o in b2) and dE<=grid
three=len(g)==6 and all(o['peaks_N']==3 and o['peaks_S']==3 and o['A3']>0.1 for o in g)
merge=len(g)==6 and all(o['peaks_N']==1 and o['peaks_S']==1 and o['A3']<0.02 for o in g)
v='UNDECIDED' if und else 'BROKEN' if brk else 'DEGENERATE' if degen else 'THREE-LEG' if three else 'MERGE' if merge else 'UNDECIDED'
res=dict(tool='grade_probe_b_r3_fix.py',addendum_sha8=sha(os.path.join(CONE,'Y_JUNCTION_B_R3_GRADER_FIX_ADDENDUM.md')),sweep_sha8=sha(SW),
    supersedes_verdict_of=sha(OLD),grader_sha8=sha(__file__),verdict=v,undecided=und,broken=brk,
    degenerate_check=dict(max_dE_S1_S2=dE,grid_error=grid),graded_rows=g,output_only_rows=[o for o in out if o not in g])
p=os.path.join(CONE,'RESULT_PROBE_B_R3_REGRADE.json'); json.dump(res,open(p,'w'),indent=1)
print(v,res['degenerate_check'],brk,und,'sha',sha(p),'grader',res['grader_sha8'])
print(sorted(set((o['peaks_N'],o['peaks_S']) for o in g)),sorted(set(o['rank_N'] for o in out)))
