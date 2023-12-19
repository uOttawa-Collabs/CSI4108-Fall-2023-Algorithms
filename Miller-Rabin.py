#!/usr/bin/env python3

from util import is_prime, miller_rabin


def main():
    n = 2 ** 6 + 1
    print(is_prime(n))
    print(miller_rabin(n))


if __name__ == "__main__":
    main()
