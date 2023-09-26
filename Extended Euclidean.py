#!/usr/bin/env python3
import sys
from tabulate import tabulate
from common import generate_extended_gcd_table


def main():
    a = int(sys.argv[1])
    b = int(sys.argv[2])
    q = a // b
    r = a - q * b

    s_1 = 1
    s_2 = 0
    s_3 = s_1 - q * s_2

    t_1 = 0
    t_2 = 1
    t_3 = t_1 - q * t_2

    print(tabulate(
        generate_extended_gcd_table(
            0,
            a, b, q, r, s_1, s_2, s_3, t_1, t_2, t_3
        ),
        headers=["a", "b", "q", "r", "s_1", "s_2", "s_3", "t_1", "t_2", "t_3"]
    ))


if __name__ == "__main__":
    main()
