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


class ParsesCookies:

    def cookies(self):
        return self.request['cookies']

    def is_authed(self):
        is_key = "auth_key" in self.cookies()
        return is_key


class ParsesBody:

    def body(self):
        return self.request.get('body', None)


class ParsesHeaders:
    def headers(self):
        return self.request['headers']

    def need_json(self):
        is_cont = ("application/json" == self.headers().get('content-type'))
        return is_cont


import json


class JsonHandler(ParsesBody, ParsesHeaders):

    def __init__(self, request):
        self.request = request

    def process(self):
        if self.need_json() == False:
            return None
        else:
            try:
                num_key = len(json.loads(self.body()).keys())
                return num_key
            except:
                return None


class SecureTextHandler(ParsesBody, ParsesCookies):
    def __init__(self, request):
        self.request = request

    def process(self):
        if self.is_authed() == False:
            return None
        else:
            l_body = len(self.body())
            return l_body

# Примеры
r = {'cookies': {'auth_key': '123'},
     'body': 'hello'
    }
print(SecureTextHandler(r).process())
# 5

r = {'cookies': {},
     'body': 'hello'
    }
print(SecureTextHandler(r).process())
# None