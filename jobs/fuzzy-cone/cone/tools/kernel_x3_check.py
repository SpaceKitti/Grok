"""Basis-independent pole count: eigenvalues of x3 compressed to ker(Phi^+), Probe B R3 graded rows. Output only. Aethon 2026-11-05."""
import sys,glob,json,numpy as np
sys.path.insert(0,'/workspace/lift/fuzz/cone/v2_1')
from fuzzy_cone_v2_1 import Model
out=[]
for f in sorted(glob.glob('/workspace/lift/fuzz/cone/v2_1/sol_probeB_r3_S*_N*_seed*.npz')):
    d=np.load(f);M=Model(int(d['N']),int(d['n']),R=float(d['R']),wrad=float(d['wrad']))
    X,P,*_=M.pieces(d['x']);P=np.asarray(P);X3=np.asarray(X[2])
    w,U=np.linalg.eigh(P@P.conj().T);K=U[:,w<1e-8]
    kx3=np.real(np.einsum('ik,ij,jk->k',K.conj(),X3,K))/np.sqrt(M.c)
    lam=np.linalg.eigvalsh(K.conj().T@X3@K)/np.sqrt(M.c)
    o=dict(file=f.split('/')[-1],kernel_dim=K.shape[1],old_rank=f"{(kx3>0).sum()}/{(kx3<0).sum()}",new_rank=f"{(lam>0).sum()}/{(lam<0).sum()}",x3_eigs=np.round(lam,4).tolist())
    out.append(o);print(o)
json.dump(out,open('/workspace/lift/fuzz/cone/KERNEL_X3_CHECK_B_R3.json','w'),indent=1)
