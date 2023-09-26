from .euclidean import extended_gcd
from .prime import is_prime


class Field:
    def reduce(self, a):
        raise NotImplementedError()

    def sum(self, a, b):
        raise NotImplementedError()

    def get_additive_inverse(self, a):
        raise NotImplementedError()

    def subtract(self, a, b):
        return self.sum(a, self.get_additive_inverse(b))

    def multiply(self, a, b):
        raise NotImplementedError()

    def get_multiplicative_inverse(self, a):
        raise NotImplementedError()

    def divide(self, a, b):
        return self.multiply(a, self.get_multiplicative_inverse(b))

    def __eq__(self, other):
        raise NotImplementedError()


class TestField(Field):
    def reduce(self, a):
        return a

    def sum(self, a, b):
        return a + b

    def get_additive_inverse(self, a):
        return -a

    def multiply(self, a, b):
        return a * b

    def __eq__(self, other):
        return type(other) == TestField


class GaloisField(Field):
    def __init__(self, order):
        if not is_prime(order):
            raise ValueError("Order of Galois Field must be a prime")
        self.order = order

    def reduce(self, a):
        return a % self.order

    def sum(self, a, b):
        return (a + b) % self.order

    def get_additive_inverse(self, a):
        return (-a) % self.order

    def multiply(self, a, b):
        return a * b % self.order

    def get_multiplicative_inverse(self, a):
        _, inverse, _ = extended_gcd(a, self.order)
        return inverse

    def __eq__(self, other):
        if type(other) != GaloisField:
            return False
        return self.order == other.order

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"GaloisField({self.order})"
