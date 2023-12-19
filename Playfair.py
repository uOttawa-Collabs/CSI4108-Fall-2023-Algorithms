#!/usr/bin/env python3
import numpy

from util import playfair


def main():
    # Assume i = j
    key_matrix = numpy.array([
        # Key
        ["P", "L", "A", "Y", "F"],
        ["I", "R", "E", "X", "M"],
        # Pad with other unused letters
        ["B", "C", "D", "G", "H"],
        ["K", "N", "O", "Q", "S"],
        ["T", "U", "V", "W", "Z"]
    ])
    plaintext = "Hide the gold in the tree stumps"
    ciphertext = playfair(key_matrix, plaintext, show_steps=True)
    print("".join(ciphertext[i:i + 5] + " " for i in range(0, len(ciphertext), 5)).strip())


if __name__ == "__main__":
    main()
