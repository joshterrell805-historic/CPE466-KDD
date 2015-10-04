import math
from vector.vector import Vector

class Algorithm:
    def __init__(self, documentCollectionMetadata):
        """
        metaData (dictionary)
            docFreq (dictionary) - docFreq[word] = num of docs word occurs in
            docCount (int)
        """
        self.metaData = documentCollectionMetadata 

    def match(self, queryWords, documentWords):
        """match query against document and return the similarity score.
        queryWords and documentWords are dictionaries of word:count."""
        raise Exception("Subclasses must override Algorithm.query")

    def sharedWords(self, queryWords, documentWords):
        """union of all words in both dictionaries"""
        qKeys = list(queryWords.keys())
        dKeys = list(documentWords.keys())
        return list(set(qKeys + dKeys))

    def wordVector(self, keys, words):
        """vector of counts with zeros filled in with same dimensions as keys"""
        return Vector([words.get(key, 0) for key in keys])

    def invDocFreq(self, word):
        # lets just assume that if the word doesn't exist in any document,
        # it has a document frequency and inverse document of 0
        # (it's irrelevant)
        if word in self.metaData['docFreq']:
            N = self.metaData['docCount']
            return math.log(N / self.metaData['docFreq'][word], 2)
        else:
            return 0
