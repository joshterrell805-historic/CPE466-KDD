import unittest
from elements.stopword import StopwordElement
from document import Document
from elements.porterstemmer import PorterStemmerElement
class TestModelBuilder(unittest.TestCase):
    def testStopwords(self):
        doc_itr = FakeParser({'words': ['this', 'that', 'these', 'those']})
        sw_itr = StopwordElement(doc_itr, ['these', 'those'])
        self.assertEqual(next(sw_itr), ['this', 'that'])

    def testStemming(self):
        doc_itr = FakeParser({'words': ['caresses', 'flies', 'dies', 'mules', 'denied']})
        stem_itr = PorterStemmerElement(doc_itr)
        self.assertEqual(next(stem_itr), document(['caress', 'fli', 'die', 'mule', 'deni']))

def document(words):
    return {'words': words}

class FakeParser:
    def __init__(self, doc):
        self.__doc = doc

    def __iter__(self):
        return self

    def __next__(self):
        return self.__doc
