from matching.algorithm import Algorithm 
from vector.vector import Vector

class CosineSimilarity(Algorithm):
    def match(self, queryWords, docWords):
        words = self.sharedWords(queryWords, docWords)
        invDocFreqs = [self.invDocFreq(w) for w in words]

        docVec = self.wordVector(words, docWords)
        maxFreq = docVec.largest()
        docVec = Vector([docVec[i] / maxFreq * invDocFreqs[i]
                for i in range(len(words))])

        queryVec = self.wordVector(words, queryWords)
        maxFreq = queryVec.largest()
        queryVec = Vector([(0.5 + 0.5*queryVec[i]/maxFreq)*invDocFreqs[i]
                for i in range(len(words))])

        return queryVec.dot(docVec) / \
                (queryVec.length() * docVec.length())
        
