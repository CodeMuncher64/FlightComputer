import sympy as sp
print(dir(sp))
x = sp.symbols('x')

dx = sp.diff(1/x,x)
F = sp.integrate(1/x,x)
#symbols (such as diff(f(x), x, 0), then the result will
#Differentiate f with respect to symbols.
print(F)
print(dx)