import sympy
from Crypto.Util.number import long_to_bytes

n = 4608698932612205094380746525651403
e = 65537
c = 787448046610690384536113698384269

print("n is prime?:", sympy.isprime(n))

factors = sympy.factorint(n)
print("factors of n:", factors)

p = list(factors.keys())[0]
q = list(factors.keys())[1]

print("p:", p)
print("q:", q)

phi = (p - 1) * (q - 1)

def extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        g, x, y = extended_gcd(b, a % b)
        return (g, y, x - (a // b) * y)
    
g,x,y = extended_gcd(e, phi)
d = x % phi

print("d:", d)

m = pow(c, d, n)
print("m:", m)

print(long_to_bytes(m))