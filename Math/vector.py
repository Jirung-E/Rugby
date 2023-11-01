import math


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, rhs):
        if rhs.__class__ == Vector:
            return self.x * rhs.x + self.y * rhs.y
        return Vector(self.x * rhs, self.y * rhs)
    
    def __truediv__(self, rhs):
        return Vector(self.x / rhs, self.y / rhs)
    
    def __div__(self, rhs):
        return Vector(self.x // rhs, self.y // rhs)
    
    def __add__(self, rhs):
        return Vector(self.x + rhs.x, self.y + rhs.y)
    
    def __sub__(self, rhs):
        return Vector(self.x - rhs.x, self.y - rhs.y)
    
    def __neg__(self):
        return Vector(-self.x, -self.y)
    
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def unit(self):
        if self.x == 0 and self.y == 0:
            return Vector(0, 0)
        return self / self.length()
    
    def normalize(self):
        if self.x == 0 and self.y == 0:
            return self
        length = self.length()
        self.x /= length
        self.y /= length
        return self
    