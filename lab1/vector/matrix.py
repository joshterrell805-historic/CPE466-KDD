from vector import Vector

class VectorMatrix(list):
  def rotate(self):
    return VectorMatrix([Vector(t) for t in zip(*self)])

  def largest(self):
    return [v.largest() for v in self]

  def colLargest(self):
    return self.rotate().largest()
