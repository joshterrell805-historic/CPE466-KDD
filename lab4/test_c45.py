import unittest
import c45
from model import Node, Label

class TestC45(unittest.TestCase):
    def setUp(self):
        self.d = [([1, 2], 1),
                  ([2, 2], 1),
                  ([2, 1], 2)]
        self.attr = ["color", "shape"]

    @unittest.skip("Need attributes to behave")
    def test_basic(self):
        d = [([3,        "false",        "traditional",        "South"],        "Not Visited"),
             ([3,        "true",        "traditional",        "South"],        "Visited"),
             ([3,        "true",        "open",         "North"],       "Not Visited"),
             ([3,        "true",        "traditional",        "North"],        "Not Visited"),
             ([3,        "false",        "open",                "North"],       "Not Visited"),
             ([3,        "true",        "traditional",        "South"],        "Visited"),
             ([3,        "true",        "open",                "South"],       "Not Visited"),
             ([3,        "false",        "traditional",        "South"],        "Not Visited"),
             ([4,        "false",        "traditional",        "South"],        "Visited"),
             ([4,        "true",        "open",                "North"],       "Not Visited"),
             ([4,        "true",        "open",                "South"],       "Visited"),
             ([4,        "false",        "traditional",        "North"],        "Not Visited"),
             ([4,        "false",        "open",                "South"],       "Visited"),
             ([4,        "true",        "open",                "South"],       "Visited"),
             ([4,        "false",        "traditional",        "North"],        "Not Visited"),
             ([4,        "true",        "open",                "North"],       "Not Visited")]

        attributes = ["Location", "Bedrooms", "Basement", "Floorplan"]
        threshold = 0.8
        result = c45.run(d, attributes, threshold)
        expected = Node("Location",
                        ("North", Label("Not Visited")),
                        ("South", Node("Bedrooms",
                                       (3, Node("Basement",
                                                ("true", Node("Floorplan",
                                                              ("traditional", Label("Visited")),
                                                              ("open", Label("Not Visited")))),
                                                ("false", Label("Not Visited")))),
                                       (4, Label("Visited")))))
        self.assertEqual(result, expected)

    @unittest.skip("Need attributes to behave")
    def test_small_run(self):
        result = c45.run(self.d, [0,1], 0)
        self.assertEqual(result, Node("shape",
                                      (1, Label(2)),
                                      (2, Label(1))))
        print(result)

    def test_splitting_select(self):
        splitting = c45.select_splitting_attribute_idx(self.d, len(self.attr), 0.1)
        self.assertEqual(splitting, 1)

    def test_entropy(self):
        self.assertAlmostEqual(c45.entropy(self.d), 0.9182958)
        
    def test_entropy_wrt(self):
        self.assertAlmostEqual(c45.entropy_wrt(self.d, 1), 0)

    def test_has_single_class(self):
        self.assertEqual(c45.has_single_class(self.d[0:2]), Label(1))
        self.assertFalse(c45.has_single_class(self.d))

    def test_has_no_attrib(self):
        self.assertEqual(c45.has_no_attrib([([], 2),
                                            ([], 3),
                                            ([], 2)], []), Label(2))
        self.assertEqual(c45.has_no_attrib([([], 3),
                                            ([], 2)], []), Label(2))
        self.assertEqual(c45.has_no_attrib([([1], 3)], ["fish"]), None)
    def test_find_most_frequent_label(self):
        self.assertEqual(c45.find_most_frequent_label(self.d), 1)

    def test_idx_of_max(self):
        self.assertEqual(c45.idx_of_max([1,3,5,4]), 2)
