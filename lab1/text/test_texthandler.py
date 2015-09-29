import unittest
from text import texthandler
import os
from io import StringIO

class TestTextHandler(unittest.TestCase):

    def getFileHandle(self):
        return open(os.path.dirname(__file__) + "/test.txt", "r")

    def test_readWords(self):
        with self.getFileHandle() as fh:
            reader = texthandler.WordReader(fh)
            words = list(reader)
            self.assertEqual(["It's", 'a', 'truth', 'universally', 'acknowledged'], words[0:5])
            self.assertEqual('grown-up', words[170])
        fh.close()

    def test_readSentences(self):
        with self.getFileHandle() as fh:
            reader = texthandler.SentenceReader(fh)
            sentences = list(reader)
            data = ["""It's a truth' 'universally acknowledged, that a single man in possession
of a good fortune, must be in want of a wife.""",

"""However little known the feelings or views of such a man may be on his
first entering a neighbourhood, this truth is so well fixed in the minds
of the surrounding families, that he is considered the rightful property
of some one or other of their daughters.""",

""""My dear Mr Bennet," said his lady to him one day."""]

            self.assertEqual(data, sentences[0:3])
        fh.close()

    def test_readParagraphs(self):
        with self.getFileHandle() as fh:
            reader = texthandler.ParagraphReader(fh)
            paragraphs = list(reader)
            data = ["""It's a truth' 'universally acknowledged, that a single man in possession
of a good fortune, must be in want of a wife.""",

"""However little known the feelings or views of such a man may be on his
first entering a neighbourhood, this truth is so well fixed in the minds
of the surrounding families, that he is considered the rightful property
of some one or other of their daughters.""",

""""My dear Mr Bennet," said his lady to him one day. "have you heard that
Netherfield Park is let at last?"\
"""]
            self.assertEqual(data, paragraphs[0:3])

    def test_wordList(self):
        fh = StringIO("what are words")
        reader = texthandler.WordReader(fh)
        self.assertEqual(list(reader), ['what', 'are', 'words'])

    def test_wordFreqMap(self):
        fh = StringIO("what are words what")
        reader = texthandler.WordReader(fh)
        reader.readAll()
        self.assertEqual(reader.freqWordsMap(),
                {'what' : 2, 'are' : 1, 'words' : 1})

    def test_readAll(self):
        fh = StringIO("what are words what")
        reader = texthandler.WordReader(fh)
        self.assertEqual(reader.__next__(), 'what')
        self.assertEqual(reader.readAll(), ['are', 'words', 'what'])
        self.assertEqual(reader.readAll(), [])

        fh = StringIO("what. are? words! what")
        reader = texthandler.SentenceReader(fh)
        self.assertEqual(reader.readAll(), ['what.', 'are?', 'words!', 'what'])
        self.assertEqual(reader.readAll(), [])

    def test_uniqWords(self):
        fh = StringIO("what are words what")
        reader = texthandler.WordReader(fh)
        reader.readAll()
        self.assertEqual(reader.uniqWords().sort(),
                ['what', 'are', 'words'].sort())

    def test_countWords(self):
        fh = StringIO("what are words what")
        reader = texthandler.WordReader(fh)
        reader.readAll()
        self.assertEqual(reader.countWords(), 4)

    def test_countUniqWords(self):
        fh = StringIO("what are words what")
        reader = texthandler.WordReader(fh)
        reader.readAll()
        self.assertEqual(reader.countUniqWords(), 3)

    def test_mostFreqWords(self):
        fh = StringIO("what are words what")
        reader = texthandler.WordReader(fh)
        next(reader)
        next(reader)
        self.assertEqual(reader.mostFreqWords().sort(), ['what', 'are'].sort())
        next(reader)
        self.assertEqual(reader.mostFreqWords().sort(),
                ['what', 'are', 'words'].sort())
        reader.readAll()
        self.assertEqual(reader.mostFreqWords(), ['what'])
        
    def test_wordsWithFreq(self):
        fh = StringIO("what are words what")
        reader = texthandler.WordReader(fh)
        reader.readAll()
        self.assertEqual(reader.wordsWithFreq(1).sort(),
                ['are', 'words'].sort())
        self.assertEqual(reader.wordsWithFreq(2), ['what'])
        self.assertEqual(reader.wordsWithFreq(3), [])

    def test_wordsWithFreq(self):
        fh = StringIO("what are words what")
        reader = texthandler.WordReader(fh)
        next(reader)
        next(reader)
        self.assertEqual(reader.wordsWithGreaterFreq(0).sort(),
                ['what', 'are'].sort())
        reader.readAll()
        self.assertEqual(reader.wordsWithGreaterFreq(1), ['what'])
        self.assertEqual(reader.wordsWithGreaterFreq(2), [])
