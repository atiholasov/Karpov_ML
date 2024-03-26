class BaseFigure:
    n_dots = None

    def __init__(self):
        self.validate()

    def area(self):
        raise NotImplementedError

    def validate(self):
        raise NotImplementedError


class Triangle(BaseFigure):
    n_dots = 3

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.p = None
        self.s = None
        super().__init__()

    def area(self):
        self.p = (self.a + self.b + self.c) * 0.5
        self.s = (self.p * (self.p - self.a) * (self.p - self.b) * (self.p - self.c)) ** 0.5
        return self.s

    def validate(self):
        if (self.a + self.b <= self.c) or (self.a + self.c <= self.b) or (self.b + self.c <= self.a):
            raise ValueError("triangle inequality does not hold")


class Rectangle(BaseFigure):
    n_dots = 4

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.s = None
        super().__init__()

    def area(self):
        self.s = self.a * self.b
        return self.s

    def validate(self):
        return self.a, self.b


class Circle(BaseFigure):
    n_dots = float('inf')

    def __init__(self, r):
        self.r = r
        self.s = None
        super().__init__()

    def area(self):
        self.s = 3.14 * (self.r ** 2)
        return self.s

    def validate(self):
        pass


class Vector:
    def __init__(self, coords: list):
        self.coords = coords

    def __str__(self):
        return str(self.coords)

    def __add__(self, other):
        out = []
        if len(self.coords) != len(other.coords):
            raise ValueError(f'left and right lengths differ: {len(self.coords)} != {len(other.coords)}')
        else:
            for i in range(len(self.coords)):
                out.append(self.coords[i] + other.coords[i])
        return Vector(out)

    def __mul__(self, other):
        out = None
        if isinstance(other, (int, float)):
            out = []
            for i in range(len(self.coords)):
                out.append(self.coords[i] * other)
            out = Vector(out)
        if isinstance(other, Vector):
            out = 0
            if len(self.coords) != len(other.coords):
                raise ValueError(f'left and right lengths differ: {len(self.coords)} != {len(other.coords)}')
            for i in range(len(self.coords)):
                out += self.coords[i] * other.coords[i]
        return out

    def __abs__(self):
        l_abs = 0
        for i in range(len(self.coords)):
            l_abs += self.coords[i] ** 2
        return l_abs ** 0.5

    def __eq__(self, other):
        return self.coords == other.coords


