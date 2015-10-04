class LowerCaser:
    def __init__(self, parent):
        self.__parent = iter(parent)

    def __iter__(self):
        return self

    def __next__(self):
        document = next(self.__parent)
        words = {}
        for word, count in document['words'].items():
            wordL = word.lower()
            words[wordL] = words.get(wordL, 0) + count
        document['words'] = words
        return document
