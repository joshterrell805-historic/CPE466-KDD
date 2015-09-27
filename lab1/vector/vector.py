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

    def stdDev(self):
        # Algorithm taken from _The Art of Computer Programming_
        # vol. 2 _Seminumerical Algorithms_ 2e. p. 232
        m = self[0]
        mOld = m
        s = 0
        for x in range(1, len(self)):
            m = m + (self[x] - m) / (x + 1)
            s = s + (self[x] - mOld) * (self[x] - m)
            mOld = m

        length = len(self)
        return math.sqrt(s/length)

    def pearsonCorrelation(self, vec):
        return self.covariance(vec)/(self.stdDev() * vec.stdDev())

    def largest(self):
        mx = self[0]
        for x in self:
            if x > mx:
                mx = x
        return mx

    def smallest(self):
        mn = self[0]
        for x in self:
            if x < mn:
                mn = x
        return mn

    def median(self):
        sorted = self[:]
        sorted.sort()
        return sorted[len(self)//2]

