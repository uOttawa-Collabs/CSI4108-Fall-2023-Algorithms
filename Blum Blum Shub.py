#!/usr/bin/env python3
import random

from util import blum_blum_shub_prng, is_prime


def main():
    p = generate_prime(12)
    while p % 4 != 3:
        p = generate_prime(12)

    q = generate_prime(12)
    while q % 4 != 3:
        q = generate_prime(12)

    s = generate_prime(24)

    print(f"p = {p} = {bin(p)}")
    print(f"q = {q} = {bin(q)}")
    print(f"s = {s}")
    print(f"p % 4 = {p % 4}")
    print(f"q % 4 = {q % 4}")

    generator = blum_blum_shub_prng(p, q, s)
    for _ in range(15):
        print(next(generator))


def generate_prime(bit_length):
    while True:
        p = random.getrandbits(bit_length)
        p |= (1 << bit_length - 1) | 1
        if p % 2 != 0 and is_prime(p):
            return p


if __name__ == "__main__":
    main()
