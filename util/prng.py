def blum_blum_shub_prng(p, q, s):
    n = p * q
    x_0 = pow(s, 2, n)
    x = x_0

    while True:
        x = pow(x, 2, n)
        yield x % 2, {"n": n, "seed": x_0, "x": x}
