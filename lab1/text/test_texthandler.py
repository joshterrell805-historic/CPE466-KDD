import unittest
import texthandler
from io import StringIO

class TestTextHandler(unittest.TestCase):

    def getFileHandle(self):
        return open(os.path.dirname(__file__) + "/test.txt", "r")

    def test_readWords(self):
        with self.getFileHandle() as fh:
            handler = TextHandler(fh)
            reader = handler.wordReader()
            words = list(reader)
            self.assertEqual(["It's", 'a', 'truth', 'universally', 'acknowledged'], words[0:4])
            self.assertEqual('grown-up', words[894])
        fh.close()

    def test_readSentences(self):
        with self.getFileHandle() as fh:
            handler = TextHandler(fh)
            reader = handler.sentenceReader()
            sentences = list(reader)
            data = ["""It's a truth' 'universally acknowledged, that a single man in possession
of a good fortune, must be in want of a wife.""",

"""However little known the feelings or views of such a man may be on his
first entering a neighbourhood, this truth is so well fixed in the minds
of the surrounding families, that he is considered the rightful property
of some one or other of their daughters.""",

""""My dear Mr. Bennet," said his lady to him one day."""]

            self.assertEqual(data, sentences[0:2])
        fh.close()

    def test_readParagraphs(self):
        with self.getFileHandle() as fh:
            fh = self.getFileHandle()
            handler = TextHandler(fh)
            reader = handler.paragraphReader()
            paragraphs = list(reader)
            data = ["""It's a truth' 'universally acknowledged, that a single man in possession
of a good fortune, must be in want of a wife.""",

"""However little known the feelings or views of such a man may be on his
first entering a neighbourhood, this truth is so well fixed in the minds
of the surrounding families, that he is considered the rightful property
of some one or other of their daughters.""",

""""My dear Mr. Bennet," said his lady to him one day. "have you heard that
Netherfield Park is let at last?"\
"""]

            self.assertEqual(data, paragraphs[0:2])
        fh.close()

    def test_wordList(self):
        fh = StringIO("what are words")
        handler = TextHandler(fh)
        self.assertEqual(handler.words(), ['what', 'are', 'words'])

    def test_wordFreqList(self):
        fh = StringIO("what are words what")
        handler = TextHandler(fh)
        self.assertEqual(handler.freqWords(), {'what' : 2, 'are' : 1, 'words' : 1})
