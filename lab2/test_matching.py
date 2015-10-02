import unittest
import matching
from vector.vector import Vector
class TestMatching(unittest.TestCase):
    epsilon = 0.0000001

    def assertApproxEqual(self, valA, valB):
        self.assertTrue(abs(valA - valB) < self.epsilon)

    def testCosineSimilarity(self):
        matcher = matching.CosineSimilarity({
            'docFreq': {
                'a': 4,
                'b': 2,
                'c': 1,
            },
            'docCount': 16
        })

        # ---- test one -----
        docWords = {'a': 13, 'c': 9}
        queryWords = {'a': 7, 'b': 4}

        idf = {w: matcher.invDocFreq(w) for w in ['a', 'b', 'c']}

        docVec = Vector([13/13*idf['a'], 0, 9/13*idf['c']])
        queryVec = Vector([(0.5+0.5*7/7)*idf['a'], (0.5+0.5*4/7)*idf['b'],
                0.5*idf['c']])

        scoreComputed = docVec[0]*queryVec[0] + docVec[1]*queryVec[1] + \
                docVec[2]*queryVec[2]
        scoreComputed = scoreComputed / docVec.length()
        scoreComputed = scoreComputed / queryVec.length()

        score = matcher.match(queryWords, docWords)
        self.assertApproxEqual(score, scoreComputed)

        # ---- test two -----
        docWords = {'a': 13, 'b': 9, 'c': 1}
        queryWords = {'a': 7, 'b': 4}
        docVec = Vector([13/13*idf['a'], 9/13*idf['b'], 1/13*idf['c']])
        queryVec = Vector([(0.5+0.5*7/7)*idf['a'], (0.5+0.5*4/7)*idf['b'],
                0.5*idf['c']])
        scoreComputed = docVec[0]*queryVec[0] + docVec[1]*queryVec[1] + \
                docVec[2]*queryVec[2]
        scoreComputed = scoreComputed / docVec.length()
        scoreComputed = scoreComputed / queryVec.length()

        score = matcher.match(queryWords, docWords)
        self.assertApproxEqual(score, scoreComputed)

        # ---- test three -----
        docWords = {'a': 13, 'b': 9}
        queryWords = {'a': 7, 'b': 4, 'c': 1}
        docVec = Vector([13/13*idf['a'], 9/13*idf['b'], 0])
        queryVec = Vector([(0.5+0.5*7/7)*idf['a'], (0.5+0.5*4/7)*idf['b'],
                (0.5+0.5*1/7)*idf['c']])
        scoreComputed = docVec[0]*queryVec[0] + docVec[1]*queryVec[1] + \
                docVec[2]*queryVec[2]
        scoreComputed = scoreComputed / docVec.length()
        scoreComputed = scoreComputed / queryVec.length()

        score = matcher.match(queryWords, docWords)
        self.assertApproxEqual(score, scoreComputed)

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
