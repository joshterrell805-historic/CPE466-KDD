import unittest
import matching
from vector.vector import Vector
class TestMatching(unittest.TestCase):
    def testCosineSimilarity(self):
        matcher = matching.CosineSimilarity(None)
        queryVec = Vector([3, 4]) # 5
        documentVec = Vector([5, 12]) # 13
        score = matcher.match(queryVec, documentVec)
        self.assertEqual(score, (3*5 + 4*12) / (5 * 13))
