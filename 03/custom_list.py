from math import isclose


class CustomList(list):
    def complement(self, num_of_comp):
        if num_of_comp <= 0:
            return self
        return CustomList(super().__add__([0] * num_of_comp))

    def __add__(self, other):
        other = CustomList(other)
        other = other.complement(len(self) - len(other))
        new = self.complement(len(other) - len(self))
        return CustomList(map(lambda x, y: x + y, new, other))

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        return CustomList(map(lambda x: -x, self))

    def __sub__(self, other):
        return self + -CustomList(other)

    def __rsub__(self, other):
        return -self + other

    def __eq__(self, other):
        return isclose(sum(self), sum(other))

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return self != other and sum(self) > sum(other)

    def __lt__(self, other):
        return self != other and sum(self) < sum(other)

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return not self > other

    def __str__(self):
        return f"sum = {sum(self)}, elements = {super().__str__()}"
