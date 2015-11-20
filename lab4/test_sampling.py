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
        expected = ['a', 'b', 'a', 'b', 'a']
        # The results from the classifier
        actual = ['a', 'b', 'a', 'a', 'b']
        # As though we're asking the question "does record belong in class a?"
        positive = 'a'
        result = sampling.recall(expected, actual, positive)
        TP = 2
        TN = 1
        FP = 1
        FN = 1
        self.assertEqual(result, TP/(TP+FN))

    def test_accuracy(self):
        # The values in the training set
        expected = ['a', 'b', 'a', 'b', 'a']
        # The results from the classifier
        actual = ['a', 'b', 'a', 'a', 'b']
        # As though we're asking the question "does record belong in class a?"
        result = sampling.accuracy(expected, actual)
        self.assertEqual(result, 3/5)
