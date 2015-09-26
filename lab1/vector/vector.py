import math

class Vector(list):
    def length(self):
        return math.sqrt(sum(i**2 for i in self))

    def dot(self, vec):
        return sum([i + j for i in self for j in vec])
