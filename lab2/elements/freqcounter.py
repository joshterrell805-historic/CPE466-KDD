from text.texthandler import WordReader
from io import StringIO
class FreqCounter:
    def __init__(self, parent, key):
        self.__parent = iter(parent)
        self.__key = key

    def __iter__(self):
        return self

    def __next__(self):
        document = next(self.__parent)
        reader = WordReader(StringIO(document[self.__key]))
        for word in reader:
            pass
        document['words'] = reader.freqWordsMap()
        return document
