import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, rhs):
        return Point(self.x + rhs.x, self.y + rhs.y)
    
    def __neg__(self):
        return Point(-self.x, -self.y)
    
    @staticmethod
    def distance(a, b):
        return math.sqrt(Point.distance2(a, b))
    
    @staticmethod
    def distance2(a, b):
        return (a.x - b.x) ** 2 + (a.y - b.y) ** 2