import unittest
import sampling
import random

class TestSampling(unittest.TestCase):
    def setUp(self):
        random.seed(42)

    def test_precision(self):
        # The values in the training set
        expected = ['a', 'b', 'a', 'b']
        # The results from the classifier
        actual = ['a', 'b', 'a', 'a']
        # As though we're asking the question "does record belong in class a?"
        positive = 'a'
        result = sampling.precision(expected, actual, positive)
        TP = 2
        TN = 1
        FP = 1
        self.assertEqual(result, TP/(TP+FP))

    def test_recall(self):
        # The values in the training set
        expected = ['a', 'b', 'a', 'b', 'a', 'c']
        # The results from the classifier
        actual = ['a', 'b', 'a', 'a', 'b', 'd']
        # As though we're asking the question "does record belong in class a?"
        positive = 'a'
        result = sampling.recall(expected, actual, positive)
        TP = 2
        TN = 1
        FP = 1
        FN = 1
        irrelevant = 1
        self.assertEqual(result, TP/(TP+FN))

    def test_pf(self):
        # The values in the training set
        expected = ['a', 'b', 'a', 'b', 'a']
        # The results from the classifier
        actual = ['a', 'b', 'a', 'a', 'b']
        # As though we're asking the question "does record belong in class a?"
        positive = 'a'
        result = sampling.pf(expected, actual, positive)
        TP = 2
        TN = 1
        FP = 1
        FN = 1
        self.assertEqual(result, FP/(FP + TN))
        
    def test_f_measure(self):
        # The values in the training set
        expected = ['a', 'b', 'a', 'b', 'a']
        # The results from the classifier
        actual = ['a', 'b', 'a', 'a', 'b']
        # As though we're asking the question "does record belong in class a?"
        positive = 'a'
        result = sampling.f_measure(expected, actual, positive)
        TP = 2
        TN = 1
        FP = 1
        FN = 1
        precision = TP/(TP+FP)
        recall = TP/(TP+FN)
        self.assertEqual(result, 2 * precision * recall / (precision + recall))

    def test_accuracy(self):
        # The values in the training set
        expected = ['a', 'b', 'a', 'b', 'a']
        # The results from the classifier
        actual = ['a', 'b', 'a', 'a', 'b']
        # As though we're asking the question "does record belong in class a?"
        result = sampling.accuracy(expected, actual)
        self.assertEqual(result, 3/5)

    def test_error_rate(self):
        # The values in the training set
        expected = ['a', 'b', 'a', 'b', 'a']
        # The results from the classifier
        actual = ['a', 'b', 'a', 'a', 'b']
        # As though we're asking the question "does record belong in class a?"
        result = sampling.error_rate(expected, actual)
        self.assertEqual(result, 1 - 3/5)

    def test_hunk_data(self):
        data = [(['a', 'f'], 'o'),
                (['b', 'g'], 'm'),
                (['a', 'g'], 'm'),
                (['a', 'g'], 'o')]
        hunks = sampling.hunk(data, 2)
        for hunk in hunks:
            self.assertEqual(len(hunk), 2)
            for row in hunk:
                if row in data:
                    data.remove(row)
        self.assertEqual(len(data), 0)

    def test_other_hunk_sizes(self):
        data = [(['a', 'f'], 'o'),
                (['b', 'g'], 'm'),
                (['a', 'g'], 'm'),
                (['a', 'g'], 'o')]
        hunks = sampling.hunk(data, 0)
        self.assertEqual(len(hunks), 1)
        hunks = sampling.hunk(data, -1)
        self.assertEqual(len(hunks), 4)
        
    def test_pull_each(self):
        data = list(range(10))
        itr = sampling.pull_each(data)
        for (i, rest) in itr:
            self.assertIn(i, data)
            self.assertNotIn(i, rest)
            for n in data:
                self.assertTrue((n in rest) or n == i)

    def test_other_pull_each_arrays(self):
        itr = sampling.pull_each([])
        self.assertEqual(len(list(itr)), 0)
        
        itr = list(sampling.pull_each(['a']))
        self.assertEqual(len(itr), 1)

        itr = list(sampling.pull_each([['a']]))
        self.assertEqual(len(itr), 1)
        self.assertEqual(itr[0], (['a'], []))
