import unittest
import csvhandler
import os
from vector import Vector

class TestReadVectors(unittest.TestCase):

  def test_parseVectorReturnsVector(self):
    handler = csvhandler.CSVHandler()
    vec = handler.parseVector("1,2,3")
    self.assertIsInstance(vec, Vector)
  
  def test_parseVector(self):
    handler = csvhandler.CSVHandler()
    vec = handler.parseVector("1,2,3")
    self.assertEqual(vec, Vector([1,2,3]))

    vec = handler.parseVector("1,,3")
    self.assertEqual(vec, Vector([1,None,3]))

    vec = handler.parseVector("1,")
    self.assertEqual(vec, Vector([1,None]))

  def test_parseLines(self):
    data = "1,2,3,4\n5,6,7".split("\n")
    handler = csvhandler.CSVHandler()
    vecList = handler.parseLines(data)
    self.assertEqual(vecList, [Vector([1,2,3,4]),Vector([5,6,7])])

  def test_parseFile(self):
    fh = open(os.path.dirname(__file__) + "/test.csv", "r")
    lines = fh.readlines()
    handler = csvhandler.CSVHandler()
    vecList = handler.parseLines(lines)
    self.assertEqual(vecList, [Vector([1,2,3,4]),
                               Vector([4,5,6,7]),
                               Vector([1.1,2.2,3.3,4.4]),
                               Vector([1,2,3,4,5,6,7,7,8,9]),
                               Vector([1]),
                               Vector([None,None,None,None,None,4]),
                               Vector([3,None,None,None,None]),
                               Vector([None,None,None,None,None,None])])
    fh.close()

if __name__ == '__main__':
  unittest.main()
