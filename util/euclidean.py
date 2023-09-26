def gcd(a, b):
    while b != 0:
        r = a % b
        a = b
        b = r

    return a


# Returns gcd(a, b), x, y
#   s.t. ax + by = gcd(a, b)
# Note: If gcd(a, b) = 1, x is the multiplicative inverse of a modulo b.
def extended_gcd(a, b):
    m = b
    x0, x1, y0, y1 = 1, 0, 0, 1

    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    return a, x0 % m, y0 % m
