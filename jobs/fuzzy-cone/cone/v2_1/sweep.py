# diagnostic: radial-penalty weight sensitivity
import sys; from fuzzy_cone_v2_1 import *
for w in (10, 100, 1000):
  for N in (21, 41):
    M=Model(N,1,wrad=w); x,E,ok,it=relax(M,M.seed_fuzzy()); o=observe(M,x)
    print(w,N,round(E/(2*np.pi),4),ok,it,{k:round(v,4) for k,v in o.items() if k!='profiles'}, round(o['profiles']['north']['r_peak'],3), flush=True)
