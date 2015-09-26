import math

class Vector(list):
    def length(self):
        return math.sqrt(sum(i**2 for i in self))
