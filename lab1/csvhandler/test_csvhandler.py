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
