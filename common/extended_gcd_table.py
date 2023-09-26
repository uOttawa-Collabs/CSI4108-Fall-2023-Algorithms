def generate_extended_gcd_table(zero, a, b, q, r, s_1, s_2, s_3, t_1, t_2, t_3):
    table = []
    while True:
        table.append([str(a), str(b), str(q), str(r), str(s_1), str(s_2), str(s_3), str(t_1), str(t_2), str(t_3)])

        if r == zero:
            break

        a = b
        b = r
        q = a // b
        r = a - q * b

        s_1 = s_2
        s_2 = s_3
        s_3 = s_1 - q * s_2

        t_1 = t_2
        t_2 = t_3
        t_3 = t_1 - q * t_2

    return table
