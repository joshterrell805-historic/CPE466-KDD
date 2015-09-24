import unittest
import vector

class TestVectorHandling(unittest.TestCase):

    def test_length(self):
        vec = vector.Vector([3,4])
        length = vec.length()
        self.assertEqual(length, 5)
