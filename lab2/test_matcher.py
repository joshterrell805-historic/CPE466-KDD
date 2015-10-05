import unittest
from scripts import matcher

class TestMatcher(unittest.TestCase):
    def test_docHasMeta(self):
        doc = {'a': 'b', 'c': 'd'}
        self.assertTrue(matcher.docHasMeta(doc, {}))
        self.assertTrue(matcher.docHasMeta(doc, {'a': ['b']}))
        self.assertTrue(not matcher.docHasMeta(doc, {'a': ['a']}))
        self.assertTrue(not matcher.docHasMeta(doc, {'b': ['a']}))
        self.assertTrue(not matcher.docHasMeta(doc, {'b': ['b']}))
        self.assertTrue(matcher.docHasMeta(doc, {'a': ['c','b']}))
        self.assertTrue(not matcher.docHasMeta(doc, {'c': ['c','b']}))
        self.assertTrue(matcher.docHasMeta(doc, {'c': ['c','d']}))
