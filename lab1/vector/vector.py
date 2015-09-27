import math

class Vector(list):
    def length(self):
        return math.sqrt(sum(i**2 for i in self))

    def dot(self, vec):
        return sum([i * j for (i, j) in zip(self, vec)])

    def euclidDist(self, vec):
        return math.sqrt(sum([(i-j)**2 for (i, j) in zip(self, vec)]))

    def manhattanDist(self, vec):
        return sum([abs(i - j) for (i, j) in zip(self, vec)])

    def mean(self):
        return sum(self)/len(self)

    def covariance(self, vec):
        self_mean = self.mean()
        vec_mean = vec.mean()
        return Vector([(x - self_mean) * (y - vec_mean) for (x,y) in zip(self, vec)]).mean()
