import math

class Vector(list):
    def length(self):
        return math.sqrt(sum(i**2 for i in self))

    def dot(self, vec):
        return sum([i * j for (i, j) in zip(self, vec)])

    def euclidDist(self, vec):
        return math.sqrt(sum([(i-j)**2 for (i, j) in  zip(self, vec)]))
