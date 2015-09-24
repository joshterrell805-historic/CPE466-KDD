import math

class Vector(list):
    def length(self):
        sumsquare = reduce(lambda memo, i: memo + i**2, self, 0)
        return math.sqrt(sumsquare)
