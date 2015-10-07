import math
from matching.algorithm import Algorithm
class Okapi(Algorithm):
    def match(self, queryWords, docWords, docLength):
        words = self.sharedWords(queryWords, docWords)
        n = self.metaData['docCount']

        k1 = 1.0
        b = 0.75
        k2 = 1
        total = 0
        for term in words:
            dfi = self.metaData['docFreq'].get(term, 0)
            fij = docWords.get(term, 0)
            dlj = docLength
            avdl = self.metaData['avgLength']
            fiq = queryWords.get(term, 0)
            norm_docfreq = math.log((n - dfi + 0.5)/(dfi + 0.5))
            norm_wordfreq = ((k1 + 1) * fij)/(k1 * (1 - b + b * dlj/avdl) + fij)
            norm_queryfreq = ((k2 + 1) * fiq) / (k2 + fiq)
            total += norm_docfreq * norm_wordfreq * norm_queryfreq

        return total
