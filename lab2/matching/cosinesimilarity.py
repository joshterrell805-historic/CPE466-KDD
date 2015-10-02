from matching.algorithm import Algorithm 

class CosineSimilarity(Algorithm):
    def match(self, queryVec, documentVec):
        return queryVec.dot(documentVec) / \
                (queryVec.length() * documentVec.length())
        
