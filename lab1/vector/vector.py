import math

class Vector:
    def length(self, vector):
        sumsquare = reduce(lambda memo, i: memo + i**2, vector, 0)
        return math.sqrt(sumsquare)
