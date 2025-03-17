def is_even(n):
    return n & 1 == 0

def simple_multiply_iter(a, b):
    result = 0
    while b != 0:
        if is_even(b):
            a, b = 2*a, b >> 1
        else:
            result += a
            a, b = 2*a, b >> 1
    return result