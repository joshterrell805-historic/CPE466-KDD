import unittest
import vector

class TestVectorHandling(unittest.TestCase):

    def test_length(self):
        vec = vector.Vector()
        length = vec.length([3,4])
        self.assertEqual(length, 5)
