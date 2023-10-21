class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, rhs):
        return Vector(self.x * rhs, self.y * rhs)