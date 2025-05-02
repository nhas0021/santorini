from dataclasses import dataclass
from math import sqrt
from typing import Optional


@dataclass(frozen=True)
class Vector2:
    x: float
    y: float

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def magnitude_squared(self) -> float:
        return self.x**2 + self.y**2

    def magnitude(self) -> float:
        return sqrt(self.magnitude_squared())

    def normalise(self):
        mag = self.magnitude()
        if mag != 0:  # * Save compute on 0
            self = Vector2(self.x / mag, self.y / mag)

    def normalised(self):
        if mag := self.magnitude() == 0:
            return Vector2(0, 0)  # * Save compute on 0
        return Vector2(self.x / mag, self.y / mag)

    # ! v3 = v1 + v2
    def __add__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.x + other.x, self.y + other.y)

    # ! v3 = v1 - v2
    def __sub__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.x - other.x, self.y - other.y)

    # ! v2 = v1 * f
    def __mul__(self, scalar: float) -> "Vector2":
        return Vector2(self.x * scalar, self.y * scalar)

    # ! v2 = f * v1
    # * (Commutative property)
    def __rmul__(self, scalar: float) -> "Vector2":
        return self * scalar

    # ! v2 = v1 / f
    def __truediv__(self, scalar: float) -> "Vector2":
        return Vector2(self.x / scalar, self.y / scalar) if scalar != 0 else Vector2(0, 0)

    # ! v1 == v2
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vector2):  # * We can eval if both are vectors
            return (self.x == other.x) and (self.y == other.y)
        # * If another class is used maybe that has a "==" eval for this expression
        return NotImplemented

    def __iter__(self):
        return iter((self.x, self.y))

    def __getitem__(self, index: int):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError


@dataclass(frozen=True)
class Vector2I:
    x: int
    y: int

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    # ! v3 = v1 + v2

    def __add__(self, other: "Vector2I") -> "Vector2I":
        return Vector2I(self.x + other[0], self.y + other[1])

    # ! v3 = v1 - v2
    def __sub__(self, other: "Vector2I") -> "Vector2I":
        return Vector2I(self.x - other[0], self.y - other[1])

    def magnitude_squared(self) -> float:
        return self.x**2 + self.y**2

    def magnitude(self) -> float:
        return sqrt(self.magnitude_squared())

    def to_tuple(self):
        return (self.x, self.y)

    def is_adjacent(self, v: "Vector2I") -> bool:
        dx = abs(v.x - self.x)
        dy = abs(v.y - self.y)
        return max(dx, dy) <= 1

    def get_adjacent_positions(self, bounds: Optional["Vector2I"] = None) -> list["Vector2I"]:
        deltas = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]

        adjacent = [
            Vector2I(self.x + dx, self.y + dy)
            for dx, dy in deltas
        ]

        if bounds:
            # Clip to grid bounds
            adjacent = [pos for pos in adjacent if 0 <=
                        pos.x < bounds.x and 0 <= pos.y < bounds.y]

        return adjacent

    # ? Most likely won't need
    # # ! v2 = v1 * f
    # def __mul__(self, scalar: int) -> "Vector2I":
    #     return Vector2I(self.x * scalar, self.y * scalar)

    def __iter__(self):
        return iter((self.x, self.y))

    def __getitem__(self, index: int):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError
