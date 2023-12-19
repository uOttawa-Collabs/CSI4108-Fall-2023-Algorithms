import sys


def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True

    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6

    return True


def miller_rabin(n):
    # If the number is less than 3, it is prime only if it is 2.
    if n < 3:
        return n == 2

    # If the number is even, it is composite.
    if n % 2 == 0:
        return False

    if n >= 2 ** 64:
        print("Miller-Rabin may not give confident result when n is greater or equal than 2 ^ 64", file=sys.stderr)

    # List of base values used for the Miller-Rabin test.
    A = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]

    # Compute d and r such that n - 1 = d * 2 ^ r.
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    # Perform Miller-Rabin test for each base value in A.
    for a in A:
        v = pow(a, d, n)

        # If a ^ d === 0 (mod n), then n | a.
        # If a ^ d === 1 or a ^ d == -1 === n - 1 (mod n), then all following number in the series are 1, pass.
        if v <= 1 or v == n - 1:
            continue

        for i in range(r):
            v = pow(v, 2, n)
            # If a ^ (d * 2 ^ i) = -1 === n - 1 (mod n) and this is not the last number in the series, pass.
            if v == n - 1 and i != r - 1:
                v = 1
                break

            # Got 1 in the middle but did not go through -1: composite number
            if v == 1:
                return False

    # v is not 1 in the end: composite number
    if v != 1:
        return False

    # If all tests pass, the number is likely prime.
    return True


def prime_generator():
    n = 2
    yield n

    n = 3
    while True:
        if is_prime(n):
            yield n
        n += 2


def prime_factorize(n):
    if n < 1:
        return []

    if n == 1:
        return [(1, 1)]

    factors = []
    generator = prime_generator()

    for p in generator:
        t = 0

        while n % p == 0:
            n /= p
            t += 1

        if t > 0:
            factors.append((p, t))

        if p >= n:
            break

    return factors
