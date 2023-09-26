#!/usr/bin/env python3
import sys

from util import euler_totient, prime_factorize, gcd


def main():
    print(f"Primitive roots: {find_primitive_roots(int(sys.argv[1]))}")


def find_primitive_roots(n):
    if n < 1:
        raise ValueError("Input must be a positive non-zero integer.")

    if n == 1:
        return [0]
    if n == 2:
        return [1]

    s = euler_totient(n)
    print(f"ϕ(n) = ϕ({n}) = {s}")

    factors = prime_factorize(s)
    print(f"ϕ(n) = " + " * ".join(f"{p} ^ {t}" for p, t in factors))

    candidates = [n // p for p, _ in factors]
    print(f"Candidates of powers to test: {candidates}")

    i = 2
    for i in range(2, n):
        not_found = False

        print(f"Testing {i}")
        for candidate in candidates:
            r = pow(i, candidate, n)
            print(f"{i} ^ {candidate} === {r} (mod {n})")
            if r == 1:
                not_found = True
                break

        if not not_found:
            print(f"Found least primitive root: {i}")
            break

    least_primitive_root = i
    primitive_roots = {least_primitive_root}
    for t in range(2, n):
        if gcd(t, s) == 1:
            r = pow(least_primitive_root, t, n)
            print(f"Adding {least_primitive_root} ^ {t} === {r} (mod {n}) to the primitive root set")
            primitive_roots.add(r)

    return sorted(primitive_roots)


if __name__ == "__main__":
    main()
