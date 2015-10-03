import unittest
from io import StringIO
from document import Document
from elements.stopword import StopwordElement
from elements.porterstemmer import PorterStemmerElement
from elements.summary import SummaryElement
from elements.jsonreader import JsonReader
from elements.freqcounter import FreqCounter
class TestModelBuilder(unittest.TestCase):
    def testStopwords(self):
        doc_itr = FakeParser({'words': {'this': 3, 'that': 2, 'these': 4, 'those': 5}})
        self.assertEqual(next(sw_itr), {'this': 3, 'that': 2})
        sw_itr = iter(StopwordElement(doc_itr, ['these', 'those']))

    def testStemming(self):
        doc_itr = FakeParser({'words': {'caresses': 3, 'flies': 4, 'dies': 5, 'mules': 6, 'mule': 4, 'denied': 7}})
        stem_itr = iter(PorterStemmerElement(doc_itr))
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

    def testReader(self):
        with open('elements/test.json') as fh:
            read_itr = JsonReader(fh)
            data = [document for document in read_itr]
            expected = [{'words': {'first' : 1}},
                        {'things': {'second' : 2}},
                        {'another': {'third' : 3}}]
            self.assertEqual(expected, data)
        fh.close()

    def testFreqCount(self):
        doc_itr = FakeParser({'text': "first second first second second"})
        freq_itr = iter(FreqCounter(doc_itr, 'text'))
        data = next(freq_itr)
        expected = {'text': "first second first second second",
                    'words': {'first': 2, 'second': 3}}
        self.assertEqual(expected, data)

def document(words):
    return {'words': words}

class FakeParser:
    def __init__(self, doc):
        self.__doc = doc

    def __iter__(self):
        return iter([self.__doc])
