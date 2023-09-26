#!/usr/bin/env python3
import operator
import sys
from functools import reduce

from common import solve_crt


def main():
    m_list = [11, 13, 17]
    M_total = reduce(operator.mul, m_list)
    c_list = solve_crt(m_list)

    n = int(sys.argv[1])

    print("------------------------------")
    n_tuple = tuple(n % m for m in m_list)
    print("Integer -> Tuple:")
    print("(" + ", ".join(f"{n} mod {m}" for m in m_list) + ")", "=", n_tuple)

    print("Tuple -> Integer")
    n_prime = sum(t * c for t, c in zip(n_tuple, c_list)) % M_total
    print("(" + " + ".join(f"{t} * {c}" for t, c in zip(n_tuple, c_list)) + ")", "mod", M_total, "=", n_prime)


if __name__ == "__main__":
    main()
