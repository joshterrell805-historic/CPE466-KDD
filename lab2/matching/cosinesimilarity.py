from matching.algorithm import Algorithm 
from vector.vector import Vector

class CosineSimilarity(Algorithm):
    def match(self, queryWords, docWords):
        words = self.sharedWords(queryWords, docWords)
        idf = [self.invDocFreq(w) for w in words]

        docVec = self.wordVector(words, docWords)
        maxFreq = docVec.largest()
        docVec = Vector([docVec[i] / maxFreq * idf[i]
                for i in range(len(words))])

        queryVec = self.wordVector(words, queryWords)
        maxFreq = queryVec.largest()
        queryVec = Vector([0 if idf[i] == 0 else \
                (0.5 + (0 if maxFreq == 0 else 0.5*queryVec[i]/maxFreq)) \
                * idf[i] for i in range(len(words))])

        return queryVec.dot(docVec) / \
                (queryVec.length() * docVec.length())
        
