import unittest
from document import Document
from elements.stopword import StopwordElement
from elements.porterstemmer import PorterStemmerElement
from elements.summary import SummaryElement
class TestModelBuilder(unittest.TestCase):
    def testStopwords(self):
        doc_itr = FakeParser({'words': {'this': 3, 'that': 2, 'these': 4, 'those': 5}})
        sw_itr = StopwordElement(doc_itr, ['these', 'those'])
        self.assertEqual(next(sw_itr), {'this': 3, 'that': 2})

    def testStemming(self):
        doc_itr = FakeParser({'words': {'caresses': 3, 'flies': 4, 'dies': 5, 'mules': 6, 'mule': 4, 'denied': 7}})
        stem_itr = PorterStemmerElement(doc_itr)
        self.assertEqual(next(stem_itr), document({'caress': 3, 'fli': 4, 'die': 5, 'mule': 10, 'deni': 7}))

    def testAccumulator(self):
        documents = [document({'this': 3, 'that': 2, 'these': 4, 'those': 5}),
                     document({'this': 2, 'those': 2})]
        # Run all the documents through the summary filter
        summary = SummaryElement(x for x in documents)
        for doc in summary:
            pass
        self.assertEqual({'this': 2, 'that': 1, 'these': 1, 'those': 2}, summary.DF())
        self.assertEqual({'this': 0, 'that': 1, 'these': 1, 'those': 0}, summary.IDF())

def document(words):
    return {'words': words}

class FakeParser:
    def __init__(self, doc):
        self.__doc = doc

    def __iter__(self):
        return self

    def __next__(self):
        return self.__doc
