import math
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

# 筛出小素数表（预处理），带进度条
def simple_sieve(limit):
    is_prime = [True] * limit
    is_prime[0:2] = [False, False]
    for i in tqdm(range(2, int(limit ** 0.5) + 1), desc="预处理素数表"):
        if is_prime[i]:
            for j in range(i * i, limit, i):
                is_prime[j] = False
    return [i for i, val in enumerate(is_prime) if val]

# 利用小素数试除加速因数分解
def get_prime_factors_fast(n, prime_list):
    factors = set()
    for p in prime_list:
        if p * p > n:
            break
        while n % p == 0:
            factors.add(p)
            n //= p
    if n > 1:
        factors.add(n)
    return list(factors)

# 计算某个质数的最小生成元
def find_min_generator(p, prime_list):
    if p <= 2:
        return None
    factors = get_prime_factors_fast(p - 1, prime_list)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return (p, g)
    return (p, None)

# 分段筛法生成所有素数，带进度
def segmented_sieve(limit):
    print(f">>> 开始分段筛选素数（上限：{limit}）")
    segment_size = int(math.sqrt(limit)) + 1
    base_primes = simple_sieve(segment_size)
    result = base_primes[:]

    for low in tqdm(range(segment_size, limit, segment_size), desc="分段筛素数"):
        high = min(low + segment_size, limit)
        is_prime = [True] * (high - low)
        for p in base_primes:
            start = max(p * p, ((low + p - 1) // p) * p)
            for j in range(start, high, p):
                is_prime[j - low] = False
        result.extend([i for i in range(low, high) if is_prime[i - low]])
    return result

# 并行计算所有素数的最小生成元
def find_all_min_generators(n):
    primes = segmented_sieve(n)
    primes = [p for p in primes if p > 2]

    print(">>> 正在构建素数因子表用于 p-1 分解...")
    prime_factors_base = simple_sieve(10**6)

    print(f">>> 启动多进程计算最小生成元，总计 {len(primes)} 个质数")
    with Pool(processes=cpu_count()) as pool:
        results = list(tqdm(pool.imap_unordered(
            lambda p: find_min_generator(p, prime_factors_base), primes
        ), total=len(primes), desc="计算最小生成元"))
    
    return {p: g for p, g in results if g is not None}

# 提取最大生成元信息
def find_max_generator_from_dict(gen_dict):
    max_value = max(gen_dict.values())
    max_keys = [p for p, g in gen_dict.items() if g == max_value]
    return max_keys, max_value

if __name__ == "__main__":
    n = int(input("Enter upper bound (建议 <= 10^7 或分批处理): "))
    generator_dict = find_all_min_generators(n)
    max_keys, max_value = find_max_generator_from_dict(generator_dict)
    print(f"\n最大生成元值为 {max_value}，对应的素数 p 为: {max_keys}")
