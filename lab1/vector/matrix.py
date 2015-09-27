from vector import Vector

class VectorMatrix(list):
  def rotate(self):
    return VectorMatrix([Vector(t) for t in zip(*self)])

  def largest(self):
    return [v.largest() for v in self]

  def colLargest(self):
    return self.rotate().largest()

  def smallest(self):
    return [v.smallest() for v in self]

  def colSmallest(self):
    return self.rotate().smallest()

  def mean(self):
    return [v.mean() for v in self]

  def colMean(self):
    return self.rotate().mean()
