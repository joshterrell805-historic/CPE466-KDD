import unittest
from vector import Vector

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
        self.assertEqual(sqrt(2/3), stdDev)

    def test_pearson_correlation(self):
        vec = Vector([1,2,3])
        pair = Vector([4,6,8])
        dist = vec.pearsonCorrelation(pair)
        self.assertEqual((4/3)/(sqrt(2/3) * sqrt(8/3)), dist)

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

    def columnData(self):
        data = [[1,2,3],
                [4,5,6],
                [3,2,1]]
        return map(Vector, data)


    def test_column_largest(self):
        vector = self.columnData()
        lrg = Vector.largest()
        self.assertEqual([4,5,6], lrg)

    def test_column_smallest(self):
        vectors = self.columnData()
        smallest = Vector.smallest(vectors)
        self.assertEqual([1,2,1], smallest)

    def test_column_mean(self):
        vectors = self.columnData()
        mean = Vector.mean(vectors)
        self.assertEqual([8/3, 3, 10/3], mean)

    def test_column_median(self):
        vectors = self.columnData()
        median = Vector.median(vectors)
        self.assertEqual([3,None,3], median)

    def test_row_stddev(self):
        vectors = self.columnData()
        stddevs = Vector.rowwiseStdDev(vectors)
        self.assertEqual([sqrt(2/3), sqrt(2/3), (1/3) * sqrt(38)], stddevs)

    def test_column_stddev(self):
        vectors = self.columnData()
        stddevs = Vector.stdDev(vectors)
        self.assertEqual([sqrt(14)/3, sqrt(2), sqrt(38)/3], stddevs)
