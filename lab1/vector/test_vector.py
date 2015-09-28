import unittest
import math
from vector.vector import Vector

class TestVectorHandling(unittest.TestCase):

  def test_length(self):
    vec = Vector([3,4])
    length = vec.length()
    self.assertEqual(length, 5)

  def test_dot_product(self):
    vec = Vector([1,2])
    by = Vector([3,4])
    dot = vec.dot(by)
    self.assertEqual(11, dot)

  def test_euclidian(self):
    vec = Vector([-1,2])
    pair = Vector([3,5])
    dist = vec.euclidDist(pair)
    self.assertEqual(5, dist)

  def test_manhattan(self):
    vec = Vector([1,2])
    pair = Vector([3,4])
    dist = vec.manhattanDist(pair)
    self.assertEqual(4, dist)

  def test_mean(self):
    vec = Vector([1,2,3])
    mean = vec.mean()
    self.assertEqual(2, mean)

  def test_covariance(self):
    vec = Vector([1,2,3])
    pair = Vector([4,6,8])
    cov = vec.covariance(pair)
    self.assertEqual(4/3, cov)

  def test_std_dev(self):
    vec = Vector([1,2,3])
    stdDev = vec.stdDev()
    self.assertEqual(math.sqrt(2/3), stdDev)

  def test_pearson_correlation(self):
    vec = Vector([1,2,3])
    pair = Vector([4,6,8])
    dist = vec.pearsonCorrelation(pair)
    self.assertEqual((4/3)/(math.sqrt(2/3) * math.sqrt(8/3)), dist)

  def test_largest(self):
    vec = Vector([1,2,3])
    lrg = vec.largest()
    self.assertEqual(3, lrg)

  def test_smallest(self):
    vec = Vector([1,2,3])
    smallest = vec.smallest()
    self.assertEqual(1, smallest)

  def test_median(self):
    vec = Vector([1,2,3])
    median = vec.median()
    self.assertEqual(2, median)

