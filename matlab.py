from math import *
def f(x):
    return (3.7/(2*x**(1/2))-3.4-4*0.3*x**3)
def fp(x):
    return 27*x**8-72*x**7+3
x0 = 0.1
x1 = 0.9
for i in range(10):
    xt = x1
    x1 = x1-((f(x1)*(x1-x0))/(f(x1)-f(x0)))
    x0 = xt
    print(x0)
print(1.0043921255021844*0.5)
