class Polynomial:
    def __init__(self, coefficients, coefficient_field, big_endian=True):
        self.coefficient_field = coefficient_field

        if len(coefficients) == 0:
            self.coefficients = [0]
            return

        if big_endian:
            # Big endian is more intuitive for humans,
            #   but we store the coefficients as little endian, so that order of each term matches the index.
            self.coefficients = [0] * len(coefficients)
            for index, coefficient in enumerate(coefficients):
                self.coefficients[len(coefficients) - index - 1] = coefficient_field.reduce(coefficient)
        else:
            self.coefficients = [coefficient_field.reduce(c) for c in coefficients]

    def __pre_operate_check(self, other):
        if self.coefficient_field != other.coefficient_field:
            raise ArithmeticError("Cannot operate on two polynomials whose coefficients are in different field")

    def __sum(self, other, operator):
        return Polynomial(
            sum_coefficient_list(self.coefficients, other.coefficients, operator),
            self.coefficient_field, big_endian=False
        )

    def __isum(self, other, operator):
        sum_coefficient_list_inplace(self.coefficients, other.coefficients, operator)
        return self

    # Arithmetics
    def __add__(self, other):
        self.__pre_operate_check(other)
        return self.__sum(other, lambda a, b: self.coefficient_field.sum(a, b))

    def __iadd__(self, other):
        self.__pre_operate_check(other)
        self.__isum(other, lambda a, b: self.coefficient_field.sum(a, b))
        return self

    def __sub__(self, other):
        self.__pre_operate_check(other)
        return self.__sum(other, lambda a, b: self.coefficient_field.subtract(a, b))

    def __isub__(self, other):
        self.__pre_operate_check(other)
        self.__isum(other, lambda a, b: self.coefficient_field.subtract(a, b))
        return self

    def __neg__(self):
        return Polynomial([], self.coefficient_field) - self

    def __lshift__(self, n):
        if n < 0:
            return self.__copy__()
        return Polynomial(
            shift_coefficient_list(self.coefficients, "left", n),
            self.coefficient_field, big_endian=False
        )

    def __ilshift__(self, n):
        if n < 0:
            return self
        self.coefficients = shift_coefficient_list(self.coefficients, "left", n)
        return self

    def __rshift__(self, n):
        if n < 0:
            return self.__copy__()
        return Polynomial(
            shift_coefficient_list(self.coefficients, "right", n),
            self.coefficient_field, big_endian=False
        )

    def __irshift__(self, n):
        if n < 0:
            return self
        self.coefficients = shift_coefficient_list(self.coefficients, "right", n)
        return self

    def __mul__(self, other):
        if type(other) == int:
            return Polynomial(
                multiply_coefficient_list(self.coefficients, other, lambda a, b: self.coefficient_field.multiply(a, b)),
                self.coefficient_field, big_endian=False
            )
        if type(other) != Polynomial:
            raise ArithmeticError("Unsupported operand")

        self.__pre_operate_check(other)
        return Polynomial(convolute_coefficient_list(
            self.coefficients, other.coefficients,
            lambda a, b: self.coefficient_field.sum(a, b),
            lambda a, b: self.coefficient_field.multiply(a, b)
        ),
            self.coefficient_field,
            big_endian=False
        )

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        if type(other) == int:
            multiply_coefficient_list_inplace(self.coefficients, other,
                                              lambda a, b: self.coefficient_field.multiply(a, b))
            return self
        if type(other) != Polynomial:
            raise ArithmeticError("Unsupported operand")

        self.__pre_operate_check(other)
        self.coefficients = convolute_coefficient_list(
            self.coefficients, other.coefficients,
            lambda a, b: self.coefficient_field.sum(a, b),
            lambda a, b: self.coefficient_field.multiply(a, b)
        )
        return self

    def __pow__(self, power, modulo=None):
        multiplicand = self.__copy__()
        while True:
            power -= 1
            if power <= 0:
                break
            multiplicand.__imul__(self)
            if modulo is not None:
                self.__pre_operate_check(modulo)
                raise NotImplementedError("TODO")
        return multiplicand

    def __ipow__(self, power):
        multiplicand = self.__copy__()
        while True:
            power -= 1
            if power <= 0:
                break
            self.__imul__(multiplicand)
        return self

    def __divmod__(self, other):
        self.__pre_operate_check(other)
        r = self.__copy__()
        q = Polynomial([], self.coefficient_field)
        while len(r) >= len(other):
            power = len(r) - len(other)
            coefficient = other.coefficient_field.divide(r.coefficients[-1], other.coefficients[-1])
            t = Polynomial(
                shift_coefficient_list([coefficient], "left", power),
                self.coefficient_field,
                big_endian=False
            )
            r -= t * other
            q += t
        return q, r

    def __mod__(self, other):
        self.__pre_operate_check(other)
        _, r = divmod(self, other)
        return r

    def __floordiv__(self, other):
        self.__pre_operate_check(other)
        q, _ = divmod(self, other)
        return q

    def __len__(self):
        return len(self.coefficients)

    def __str__(self):
        # Use big endian mode for intuitiveness
        terms = []

        for index, coefficient in enumerate(self.coefficients):
            if coefficient == 0:
                continue

            if index == 0:
                terms.append(f"{self.coefficients[index]}")
                continue

            string = ""
            if coefficient == 1:
                string += "x"
            elif coefficient == -1:
                string += "-x"
            else:
                string += f"{coefficient}x"

            if index > 1:
                string += f"^{index}"

            terms.append(string)
        terms.reverse()

        if len(terms) == 0:
            return "0"
        return " + ".join(terms)

    def __repr__(self):
        # Use big endian mode for intuitiveness
        return f"Polynomial({list(reversed(self.coefficients))}, {self.coefficient_field})"

    def __eq__(self, other):
        if self.coefficient_field != other.coefficient_field:
            return False
        if self.coefficients != other.coefficients:
            return False
        return True

    def __copy__(self):
        return Polynomial(self.coefficients, self.coefficient_field, big_endian=False)


# Internal utils
def shift_coefficient_list(a, direction, n):
    if direction == "left":
        return [0] * n + a
    if direction == "right":
        coefficients = a[n:]
        if len(coefficients) == 0:
            coefficients = [0]
        return coefficients


def sum_coefficient_list(a, b, operator):
    padding = len(b) - len(a)
    if padding < 0:
        padding = 0

    coefficients = a.copy()
    coefficients.extend([0] * padding)
    for index, coefficient in enumerate(b):
        coefficients[index] = operator(coefficients[index], coefficient)

    return trim_coefficient_list(coefficients)


def sum_coefficient_list_inplace(a, b, operator):
    padding = len(b) - len(a)
    if padding < 0:
        padding = 0

    a.extend([0] * padding)
    for index, coefficient in enumerate(b):
        a[index] = operator(a[index], coefficient)

    trim_coefficient_list_in_place(a)


def multiply_coefficient_list(a, n, operator):
    return [operator(c, n) for c in a]


def multiply_coefficient_list_inplace(a, n, operator):
    for i in range(len(a)):
        a[i] = operator(a[i], n)


def convolute_coefficient_list(a, b, operator_first_order, operator_second_order):
    coefficients = [0]
    for index, element_a in enumerate(a):
        sum_coefficient_list_inplace(
            coefficients,
            shift_coefficient_list(
                multiply_coefficient_list(b, element_a, operator_second_order),
                "left", index
            ),
            operator_first_order
        )
    return coefficients


def trim_coefficient_list(a):
    end = len(a)
    for coefficient in reversed(a):
        if coefficient != 0:
            break
        end -= 1
    return a[:end].copy()


def trim_coefficient_list_in_place(a):
    for coefficient in reversed(a):
        if coefficient != 0:
            break
        a.pop()
