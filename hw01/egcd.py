def egcd_iter(a, b):
    r0, r1 = 1, 0   # |r0 s0 a|
    s0, s1 = 0, 1   # |r1 s1 b|
    while b != 0:
        c = a // b
        r0, r1 = r1, r0 - c * r1
        s0, s1 = s1, s0 - c * s1
        a, b = b, a % b
    return a, r0, s0
