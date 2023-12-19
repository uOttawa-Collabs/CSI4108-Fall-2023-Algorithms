import typing

import numpy


def normalize_plaintext(plaintext: str) -> typing.List[str]:
    # To upper case and replace all spaces
    plaintext = plaintext.upper().replace(" ", "")

    # Remove all characters outside the alphabet
    alphabet = [chr(ord("A") + i) for i in range(0, 26)]
    plaintext = [c for c in plaintext if c in alphabet]

    return plaintext


def slice_matrix(matrix: numpy.ndarray, a: typing.Tuple[int, int], b: typing.Tuple[int, int]) \
        -> (numpy.ndarray, typing.Tuple[int, int], typing.Tuple[int, int]):
    a_x, a_y = a
    b_x, b_y = b

    # Calculate coordinates for left-upper corner and right-lower corner
    x_1 = min(a_x, b_x)
    y_1 = min(a_y, b_y)
    x_2 = max(a_x, b_x)
    y_2 = max(a_y, b_y)

    # New coordinate for point a and b in the sliced matrix
    a_sliced = (a_x - x_1, a_y - y_1)
    b_sliced = (b_x - x_1, b_y - y_1)

    return matrix[x_1:x_2 + 1, y_1:y_2 + 1], a_sliced, b_sliced


def playfair(key_matrix: numpy.ndarray, plaintext: str, show_steps=False) -> str:
    plaintext_character_list = normalize_plaintext(plaintext)
    if show_steps:
        print(f"Normalized plaintext: {''.join(plaintext_character_list)}")

    ciphertext_character_list = []

    if show_steps:
        print("Key matrix:")
        print(key_matrix)

    row_count, column_count = key_matrix.shape
    if row_count != 5 or column_count != 5:
        raise ValueError("Key matrix must be a 5 * 5 matrix")

    coordinate_map = {
        key_matrix[i, j]: (i, j)
        for i in range(row_count)
        for j in range(column_count)
    }

    i = 0
    while i < len(plaintext_character_list):
        b0, b1 = plaintext_character_list[i:i + 2]
        if show_steps:
            print(f"Processing digram {b0}{b1}")

        if b0 == b1:
            if show_steps:
                print(f"Found digram consisting of the same letter")
                print(f"Add an X in between and continue")
            plaintext_character_list.insert(i + 1, "X")
            continue

        b0_coordinate, b1_coordinate = coordinate_map[b0], coordinate_map[b1]
        if show_steps:
            print(f"Coordinate for {b0}: {b0_coordinate}")
            print(f"Coordinate for {b1}: {b1_coordinate}")

        key_matrix_sliced, b0_coordinate_sliced, b1_coordinate_sliced \
            = slice_matrix(key_matrix, b0_coordinate, b1_coordinate)

        if show_steps:
            print("Sliced key matrix:")
            print(key_matrix_sliced)
            print(f"New coordinate for {b0}: {b0_coordinate_sliced}")
            print(f"New coordinate for {b1}: {b1_coordinate_sliced}")

        b0_encrypted = ""
        b1_encrypted = ""
        if b0_coordinate[0] == b1_coordinate[0]:
            if show_steps:
                print("Row shaped matrix, performing circular shift right")
            b0_encrypted = key_matrix[b0_coordinate[0], (b0_coordinate[1] + 1) % column_count]
            b1_encrypted = key_matrix[b1_coordinate[0], (b1_coordinate[1] + 1) % column_count]
        elif b0_coordinate[1] == b1_coordinate[1]:
            if show_steps:
                print("Column shaped matrix, performing circular shift down")
            b0_encrypted = key_matrix[(b0_coordinate[0] + 1) % row_count, b0_coordinate[1]]
            b1_encrypted = key_matrix[(b1_coordinate[0] + 1) % row_count, b1_coordinate[1]]
        else:
            if show_steps:
                print("Normal matrix, picking opposite corner")
            row_count_sliced, column_count_sliced = key_matrix_sliced.shape
            b0_encrypted = key_matrix_sliced[
                b0_coordinate_sliced[0], column_count_sliced - b0_coordinate_sliced[1] - 1
            ]
            b1_encrypted = key_matrix_sliced[
                b1_coordinate_sliced[0], column_count_sliced - b1_coordinate_sliced[1] - 1
            ]

        if show_steps:
            print(f"Encrypted digram: {b0_encrypted}{b1_encrypted}")
        ciphertext_character_list.append(b0_encrypted)
        ciphertext_character_list.append(b1_encrypted)

        i += 2
        if len(plaintext_character_list) - i == 1:
            if show_steps:
                print("One character left, appending an X and continue")
            plaintext_character_list.append("X")

        if show_steps:
            print()

    return "".join(ciphertext_character_list)
