import operator
from functools import reduce

from util import gcd, extended_gcd


def solve_crt(m_list):
    print("Solving with CRT: ")
    check(m_list)

    M_total = reduce(operator.mul, m_list)

    print("M:")
    M_list = [M_total // m for m in m_list]
    print_M_list(m_list, M_list)

    print("d:")
    d_list = [M % m for M, m in zip(M_list, m_list)]
    print_d_list(m_list, M_list, d_list)

    print("d^(-1):")
    d_reverse_list = [extended_gcd(d, m)[1] for d, m in zip(d_list, m_list)]
    print_d_reverse_list(m_list, d_reverse_list)

    print("c:")
    c_list = [d_reverse * M for d_reverse, M in zip(d_reverse_list, M_list)]
    print_c_list(d_reverse_list, M_list, c_list)

    return c_list


def check(m_list):
    for i in range(len(m_list)):
        for j in range(i + 1, len(m_list)):
            if gcd(m_list[i], m_list[j]) != 1:
                raise ArithmeticError("Moduli must be pairwise coprime")


def print_M_list(m_list, M_list):
    for i, M in enumerate(M_list):
        print(f"M_{i + 1} = {' * '.join(str(m) for m in m_list)} / {m_list[i]} = {M_list[i]}")


def print_d_list(m_list, M_list, d_list):
    for i, (m, M, d) in enumerate(zip(m_list, M_list, d_list)):
        print(f"d_{i + 1} = M_{i + 1} mod m_{i + 1} = {M} mod {m} = {d}")


def print_d_reverse_list(m_list, d_reverse_list):
    for i, (m, d_reverse) in enumerate(zip(m_list, d_reverse_list)):
        print(f"d_{i + 1}^(-1) === {d_reverse} (mod {m})")


def print_c_list(d_reverse_list, M_list, c_list):
    for i, (d_reverse, M, c) in enumerate(zip(d_reverse_list, M_list, c_list)):
        print(f"c_{i + 1} = d_{i + 1}^(-1) * M_{i + 1} = {d_reverse} * {M} = {c}")
