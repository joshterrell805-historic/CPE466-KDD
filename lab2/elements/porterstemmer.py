from nltk.stem.porter import PorterStemmer
class PorterStemmerElement:
    def __init__(self, parent):
        self.__porter = PorterStemmer()
        self.__parent = parent

    def __iter__(self):
        return self

    def __next__(self):
        document = next(self.__parent)
        document['words'] = {self.__porter.stem(word): count for word, count in document['words'].items()}
        return document

