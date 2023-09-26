#!/usr/bin/env python3
from util import prime_generator


def main():
    g = prime_generator()
    while True:
        p = next(g)
        if p > 300:
            break
        print(p, pow(2, (p - 1) // 2, p), p % 8)


if __name__ == "__main__":
    main()
