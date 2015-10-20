import unittest
from scripts import ranker

class TestRanker(unittest.TestCase):
    def test_csv_parse(self):
        parse = ranker.parseCSVLine('"Ball State", 48, "Northeastern", 14')
        self.assertEqual(parse[0], 'Ball State')
        self.assertEqual(parse[1], 'Northeastern')

    def test_snap_parse(self):
        parse = ranker.parseSNAPLine('0	1')
        self.assertEqual(parse[0], 0)
        self.assertEqual(parse[1], 1)

    def test_parse_comment(self):
        parse = ranker.parse_file('snap', ['# Nodes: 8846 Edges: 31839'])
        self.assertEqual(list(parse), [])
