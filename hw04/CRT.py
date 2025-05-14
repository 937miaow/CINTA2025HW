import sympy
from Crypto.Util.number import long_to_bytes
import time
import random
import math

def generate_large_prime(bits):
    while True:
        p = sympy.randprime(2**(bits-1), 2**bits)
        if sympy.isprime(p):
            return p
            
def extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        g, x, y = extended_gcd(b, a % b)
        return (g, y, x - (a // b) * y)

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

def mod_exp(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if (exp % 2) == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

def CRT(a1, a2, m1, m2):
    M = m1 * m2
    M1 = M // m1
    M2 = M // m2
    inv_M1 = modinv(M1, m1)
    inv_M2 = modinv(M2, m2)
    x = (a1 * M1 * inv_M1 + a2 * M2 * inv_M2) % M
    return x

# Generate two large prime numbers
bits = 1024
p = generate_large_prime(bits)
q = generate_large_prime(bits)
n = p * q
m = 2024
e = 2**255 - 19

# Calculate m^e mod n without CRT
start_time = time.time()
result_without_CRT = mod_exp(m, e, n)
end_time = time.time()
time_without_CRT = end_time - start_time
print("Result without CRT:", result_without_CRT)

# Calculate m^e mod n with CRT
start_time = time.time()
a1 = mod_exp(m, e, p)
a2 = mod_exp(m, e, q)
result_with_CRT = CRT(a1, a2, p, q)
end_time = time.time()
time_with_CRT = end_time - start_time
print("Result with CRT:", result_with_CRT)

# Check if the results are the same
assert result_without_CRT == result_with_CRT, "Results do not match!"
print("Results match!")

# Compare the time taken
print("Time without CRT:", time_without_CRT)
print("Time with CRT:", time_with_CRT)