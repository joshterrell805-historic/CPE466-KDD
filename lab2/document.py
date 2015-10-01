class Document:
    def __init__(self, initDoc):
        self.__rawDoc = initDoc

        def __getattr__(self, attr):
            return self.__rawDoc[attr]
