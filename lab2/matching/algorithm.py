class Algorithm:
    def __init__(self, documentCollectionMetadata):
        self.metaData = documentCollectionMetadata 

    def match(self, queryVec, documentVec):
        """match query against document and return the similarity score"""
        raise Exception("Subclasses must override Algorithm.query")
