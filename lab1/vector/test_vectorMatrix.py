import unittest
from vector import Vector
from matrix import VectorMatrix

class TestVectorMatrix(unittest.TestCase):
  def columnData(self):
    data = [[1,2,3],
            [4,5,6],
            [3,2,1]]
    return VectorMatrix(map(Vector, data))

  def test_rotateMatrix(self):
    matrix = self.columnData()
    vec = matrix.rotate()
    self.assertEqual(VectorMatrix([Vector([1,4,3]),
      Vector([2,5,2]),
      Vector([3,6,1])]), vec)
    self.assertIsInstance(vec, VectorMatrix)

  def test_column_largest(self):
    vector = self.columnData()
    lrg = vector.colLargest()
    self.assertEqual([4,5,6], lrg)

  def test_column_smallest(self):
    vectors = self.columnData()
    smallest = vectors.colSmallest()
    self.assertEqual([1,2,1], smallest)

  @unittest.skip("unimplemented")
  def test_column_mean(self):
    vectors = self.columnData()
    mean = Vector.mean(vectors)
    self.assertEqual([8/3, 3, 10/3], mean)

  @unittest.skip("unimplemented")
  def test_column_median(self):
    vectors = self.columnData()
    median = Vector.median(vectors)
    self.assertEqual([3,None,3], median)

  @unittest.skip("unimplemented")
  def test_row_stddev(self):
    vectors = self.columnData()
    stddevs = Vector.rowwiseStdDev(vectors)
    self.assertEqual([math.sqrt(2/3), math.sqrt(2/3), (1/3) * math.sqrt(38)], stddevs)

  @unittest.skip("unimplemented")
  def test_column_stddev(self):
    vectors = self.columnData()
    stddevs = Vector.stdDev(vectors)
    self.assertEqual([math.sqrt(14)/3, math.sqrt(2), math.sqrt(38)/3], stddevs)
