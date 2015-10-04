class SubstitutableElement:
    def __init__(self):
        self.setParent([])

    def setParent(self, parent):
        self.__parent = iter(parent)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.__parent)
