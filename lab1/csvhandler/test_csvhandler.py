import unittest
import csvhandler

class TestReadVectors(unittest.TestCase):
  
  def test_parseVector(self):
    handler = csvhandler.CSVHandler()
    vec = handler.parseVector("1,2,3")
    self.assertEqual(vec, [1,2,3])

    vec = handler.parseVector("1,,3")
    self.assertEqual(vec, [1,None,3])

    vec = handler.parseVector("1,")
    self.assertEqual(vec, [1,None])

  def test_parseLines(self):
    data = "1,2,3,4\n5,6,7".split("\n")
    handler = csvhandler.CSVHandler()
    vecList = handler.parseLines(data)
    self.assertEqual(vecList, [[1,2,3,4],[5,6,7]])

  def test_parseFile(self):
    fh = open("test.csv", "r")
    lines = fh.readlines()
    handler = csvhandler.CSVHandler()
    vecList = handler.parseLines(lines)
    self.assertEqual(vecList, [[1,2,3,4],
                               [4,5,6,7],
                               [1.1,2.2,3.3,4.4],
                               [1,2,3,4,5,6,7,7,8,9],
                               [1],
                               [None,None,None,None,None,4],
                               [3,None,None,None,None],
                               [None,None,None,None,None,None]])
