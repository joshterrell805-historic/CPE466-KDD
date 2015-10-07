import math
class SummaryElement:
    def __init__(self, parent):
        self.__parent = parent
        self.__df = {}
        self.__idf = None
        self.N = 0

    def DF(self):
        return self.__df.copy()

    def IDF(self):
        if self.__idf:
            return self.__idf.copy()
        else:
            self.__idf = {word: math.log2(self.N/dfi) for word, dfi in self.__df.items()}
            return self.__idf
    def averageLength(self):
        return self.__totalLength/self.N

    def __iter__(self):
        return self

    def __next__(self):
        document = next(self.__parent)
        self.N += 1
        self.__totalLength += len(document['text'])
        for word in document['words'].keys():
            if word in self.__df:
                self.__df[word] += 1
            else:
                self.__df[word] = 1
        return document


