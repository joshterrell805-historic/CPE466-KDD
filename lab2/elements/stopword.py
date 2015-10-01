class StopwordElement:
    def __init__(self, parent, stopwords):
        self.__stopwords = stopwords
        self.__parent = parent

    def __iter__(self):
        return self

    def __next__(self):
        document = next(self.__parent)
        return [x for x in document['words'] if not x in self.__stopwords]
