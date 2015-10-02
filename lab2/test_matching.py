import unittest
import matching
from vector.vector import Vector
class TestMatching(unittest.TestCase):
    def testCosineSimilarity(self):
        matcher = matching.CosineSimilarity({
            'docFreq': {
                'a': 4,
                'b': 2,
                'c': 1,
            },
            'docCount': 16
        })
        docWords = {'a': 13, 'c': 9}
        queryWords = {'a': 7, 'b': 4}

        idf = {w: matcher.invDocFreq(w) for w in ['a', 'b', 'c']}

        docVec = Vector([13/13*idf['a'], 0, 9/13*idf['c']])
        queryVec = Vector([(0.5+0.5*7)*idf['a'], (0.5+0.5*4)*idf['b'],
                0.5*idf['c']])

        scoreComputed = docVec[0]*queryVec[0] + docVec[1]*queryVec[1] + \
                docVec[2]*queryVec[2]
        scoreComputed = scoreComputed / docVec.length()
        scoreComputed = scoreComputed / queryVec.length()

        score = matcher.match(queryWords, docWords)
        self.assertEqual(score, scoreComputed)

    def testAlgorithm_sharedWords(self):
        algorithm = matching.algorithm.Algorithm(None)
        shared = algorithm.sharedWords({'a': None, 'c': None}, {'d': None})
        self.assertEqual(shared.sort(), ['a', 'c', 'd'].sort())

    def testAlgorithm_wordVector(self):
        algorithm = matching.algorithm.Algorithm(None)
        wordVector = algorithm.wordVector(['c', 'b', 'a'],
                {'a': 1, 'c': 3})
        self.assertEqual(wordVector, [3, 0, 1])

    def testAlgorithm_invDocFreq(self):
        algorithm = matching.algorithm.Algorithm({'docFreq': {'a': 2},
                'docCount': 16})
        invDocFreq = algorithm.invDocFreq('a')
        self.assertEqual(invDocFreq, 3)
