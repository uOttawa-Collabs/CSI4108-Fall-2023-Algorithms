#!/usr/bin/env python3
from tabulate import tabulate

from common import generate_extended_gcd_table
from util import GaloisField
from util import Polynomial


def main():
    # field = GaloisField(101)
    # a = Polynomial([1, 88, 73, 83, 51, 67], field)
    # b = Polynomial([1, 38, 41, 97], field)

    field = GaloisField(2)
    a = Polynomial([1, 0, 1, 1], field)
    b = Polynomial([1, 0, 0, 1, 1], field)
    q = a // b
    r = a - q * b

    s_1 = Polynomial([1], field)
    s_2 = Polynomial([0], field)
    s_3 = s_1 - q * s_2

    t_1 = Polynomial([0], field)
    t_2 = Polynomial([1], field)
    t_3 = t_1 - q * t_2

    print(tabulate(
        generate_extended_gcd_table(
            Polynomial([0], field),
            a, b, q, r, s_1, s_2, s_3, t_1, t_2, t_3
        ),
        headers=["a", "b", "q", "r", "s_1", "s_2", "s_3", "t_1", "t_2", "t_3"]
    ))


if __name__ == "__main__":
    main()
