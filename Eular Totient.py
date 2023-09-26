#!/usr/bin/env python3
import sys

from util import euler_totient
from util import gcd
from util import prime_factorize


def main():
    n = int(sys.argv[1])
    print(prime_factorize(n))
    print(euler_totient(n))


if __name__ == "__main__":
    main()
