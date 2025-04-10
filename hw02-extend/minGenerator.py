import math

def sieve_primes(limit):
    # 埃氏筛法
    is_prime = [True] * limit
    is_prime[0:2] = [False, False]
    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[i]:
            for j in range(i * i, limit, i):
                is_prime[j] = False
    return [i for i, val in enumerate(is_prime) if val]

def get_prime_factors(n):
    factors = set()
    # 先除以2
    while n % 2 == 0:
        factors.add(2)
        n //= 2
    # 再试奇数因子
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            factors.add(i)
            n //= i
    # 最后剩下的是一个大质因子
    if n > 2:
        factors.add(n)
    return list(factors)

def find_min_generator(p):
    if p <= 2:
        return None
    factors = get_prime_factors(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    return None

def find_all_min_generators(n):
    result = {}
    primes = sieve_primes(n)
    for p in primes:
        if p > 2:
            g = find_min_generator(p)
            if g:
                result[p] = g
    return result

def find_max_generator_from_dict(gen_dict):
    max_value = max(gen_dict.values())
    max_keys = [p for p, g in gen_dict.items() if g == max_value]
    return max_keys, max_value

if __name__ == "__main__":
    n = int(input("Enter a number: "))
    generator_dict = find_all_min_generators(n)
    max_keys, max_value = find_max_generator_from_dict(generator_dict)
    print(f"\n最大生成元值为 {max_value}，对应的素数 p 为: {max_keys}")
