#!/usr/bin/env python3
import operator
import sys
from functools import reduce

from common import solve_crt
from util import euler_totient


def main():
    m_list = [11, 13, 17]
    M_total = reduce(operator.mul, m_list)
    c_list = solve_crt(m_list)

    n = int(sys.argv[1])
    exponent = int(sys.argv[2])
    modulo = int(sys.argv[3])

    print("------------------------------")
    n_tuple = tuple(n % m for m in m_list)
    print("Integer -> Tuple:")
    print("(" + ", ".join(f"{n} mod {m}" for m in m_list) + ")", "=", n_tuple)

    print("Totients:")
    totients = [euler_totient(m) for m in m_list]
    print_totient_list(m_list, totients)

    print("Tuple exponents:")
    tuple_exponents = [exponent % totient for totient in totients]
    for totient, tuple_exponent in zip(totients, tuple_exponents):
        print(f"{exponent} mod {totient} = {tuple_exponent}")

    print(f"{n} ^ {exponent} mod {modulo}")
    print("-> (" + ", ".join(
        f"{t} ^ {tuple_exponent} mod {m}" for t, tuple_exponent, m in zip(n_tuple, tuple_exponents, m_list)) + ")")
    r_tuple = tuple(t ** tuple_exponent % m for t, tuple_exponent, m in zip(n_tuple, tuple_exponents, m_list))
    print("=", r_tuple)

    print("Tuple -> Integer")
    n_prime = sum(t * c for t, c in zip(r_tuple, c_list)) % M_total
    print("(" + " + ".join(f"{t} * {c}" for t, c in zip(r_tuple, c_list)) + ")", "mod", M_total, "=", n_prime)


def print_totient_list(m_list, totient_list):
    for i, (m, totient) in enumerate(zip(m_list, totient_list)):
        print(f"φ(m_{i + 1}) = φ({m}) = {totient}")


if __name__ == "__main__":
    main()
