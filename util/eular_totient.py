from .prime import is_prime


# ϕ(n)
def euler_totient(n):
    if n <= 0:
        raise ValueError("Input must be a positive integer.")

    if is_prime(n):
        return n - 1

    # Initialize the result as n:
    #   Mark all numbers less than n as relatively prime to n.
    result = n

    # Start with the first prime number (2) and keep dividing 'n' by it
    #   until it's not divisible anymore.
    # For each prime factor found, reduce 'result' by (result / prime_factor).
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1

    # If 'n' is still greater than 1, it's a prime number itself.
    # So, reduce 'result' by (result / n - 1).
    if n > 1:
        result -= result // n

    return result
