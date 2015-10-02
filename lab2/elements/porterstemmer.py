from nltk.stem.porter import PorterStemmer
class PorterStemmerElement:
    def __init__(self, parent):
        self.__porter = PorterStemmer()
        self.__parent = parent

    def __iter__(self):
        return self

    def __next__(self):
        document = next(self.__parent)
        words = {}
        for word, count in document['words'].items():
            stem = self.__porter.stem(word)
            if stem in words:
                words[stem] += count
            else:
                words[stem] = count
        document['words'] = words
        return document

