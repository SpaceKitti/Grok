# Venus small algebra checks for CONE_SPEC_V1 (no sims)
import sympy as sp
r,al,n,c=sp.symbols('r alpha n c',positive=True)
f=r**(n/al)
lap=sp.simplify(sp.diff(f,r,2)+sp.diff(f,r)/r-n**2*f/(al**2*r**2))   # cone metric dr^2+al^2 r^2 dphi^2, field f e^{i n phi}
dens=sp.simplify(sp.diff(f,r)**2+n**2*f**2/(al**2*r**2))
print('Laplace residual:',lap); print('energy density:',sp.factor(dens))
E=sp.integrate(dens*al*r,(r,0,1),conds='none'); print('core energy (r<1):',sp.simplify(E))
print('12 pentagons alpha=5/6 total deficit/(2pi):',12*(1-sp.Rational(5,6)),'(chi=2 needs 2)')
print('tip exponent n=1 alpha=5/6:',sp.Rational(1)/sp.Rational(5,6))
print('Zk cap alpha=1/k exponents n=1:',[k for k in (1,2,3)])
