class StopwordElement:
    def __init__(self, parent, stopwords):
        self.__stopwords = stopwords
        self.__parent = iter(parent)

    def __iter__(self):
        return self

    def __next__(self):
        document = next(self.__parent)
        words = document['words']
        return {x: count for x, count in words.items() if not x in self.__stopwords}
