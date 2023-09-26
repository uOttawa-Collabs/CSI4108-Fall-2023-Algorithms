#!/usr/bin/env python3
import sys

from util import gcd


def main():
    n = int(sys.argv[1])
    if n < 1:
        raise ValueError("Input must be a positive non-zero integer.")

    if n == 1:
        return [0]
    if n == 2:
        return [1]

    congruence_class = []
    for i in range(1, n):
        if gcd(i, n) == 1:
            congruence_class.append(i)
    print(f"Congruence class of modulo {n}: {congruence_class}")

    table = []
    print("x\t" + "\t".join(f"x^{i}" for i in range(1, len(congruence_class) + 1)))

    for element in congruence_class:
        row = []
        for i in range(1, len(congruence_class) + 1):
            t = pow(element, i, n)
            row.append(t)
            if t == 1:
                break
        table.append((element, row))

    for key, value in table:
        print(f"{key}\t" + "\t".join(str(e) for e in value))

    print(f"Primitive roots: {[key for key, value in table if len(value) == len(congruence_class)]}")


if __name__ == "__main__":
    main()
