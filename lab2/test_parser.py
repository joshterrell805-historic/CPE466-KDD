import unittest
from elements.stopword import StopwordElement
from document import Document
class TestModelBuilder(unittest.TestCase):
    def testStopwords(self):
        doc_itr = FakeParser({'words': ['this', 'that', 'these', 'those']})
        sw_itr = StopwordElement(doc_itr, ['these', 'those'])
        self.assertEqual(next(sw_itr), ['this', 'that'])

    def testStemming(self):

class FakeParser:
    def __init__(self, doc):
        self.__doc = doc

    def __iter__(self):
        return self

    def __next__(self):
        return self.__doc
