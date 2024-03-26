class Triangle:
    n_dots = 3

    def __init__(self, a, b, c):
        if (a + b <= c) or (a + c <= b) or (b + c <= a):
            raise ValueError("triangle inequality does not hold")
        self.a = a
        self.b = b
        self.c = c
        self.p = None
        self.s = None

    def area(self):
        self.p = (self.a + self.b + self.c) * 0.5
        self.s = (self.p * (self.p - self.a) * (self.p - self.b) * (self.p - self.c)) ** 0.5
        return self.s


tr_1 = Triangle(1, 2, 3)
tr_2 = Triangle(3, 4, 5)

square_1 = tr_1.area()
square_2 = tr_2.area()

