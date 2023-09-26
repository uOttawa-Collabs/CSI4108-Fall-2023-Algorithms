#!/usr/bin/env python3
import operator
from functools import reduce

from common import solve_crt
from util import extended_gcd


def main():
    # ax === b (mod m): [a, b, m]
    matrix = [
        [1, 3, 7],
        [1, 4, 9]
    ]

    print("Solving: ")
    print_matrix(matrix)

    # matrix = [
    #     [1, 3, 5],
    #     [1, 4, 7],
    #     [1, 1, 8]
    # ]

    # Make a = 1
    normalize(matrix)
    print("Normalized matrix: ")
    print_matrix(matrix)

    b_list = [row[1] for row in matrix]
    m_list = [row[2] for row in matrix]
    c_list = solve_crt(m_list)

    modulo = reduce(operator.mul, m_list)
    solution = sum(c * b for c, b in zip(c_list, b_list)) % modulo

    print("------------------------------")
    print(
        f"x ===",
        " + ".join([f"{c} * {b}" for c, b in zip(c_list, b_list)]),
        "(mod " + " * ".join(str(m) for m in m_list) + ")"
    )
    print(f"x === {solution} (mod {modulo})")


def normalize(matrix):
    for row in matrix:
        if row[0] == 1:
            continue
        g, inverse, _ = extended_gcd(row[0], row[2])
        if g != 1:
            raise ArithmeticError(f"Cannot find inverse of {row[0]} modulo {row[2]}")
        row[0] = 1
        row[1] = row[1] * inverse % row[2]


def print_matrix(matrix):
    for [a, b, m] in matrix:
        print(f"{a} * x === {b} (mod {m})")


if __name__ == "__main__":
    main()
