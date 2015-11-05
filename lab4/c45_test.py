import unittest

class TestC45(unittest.TestCase):
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
                        ("North", Label("Not Visited"))
                        ("South", Node("Bedrooms"
                                       (3, Node("Basement"
                                                (true, Node("Floorplan"
                                                            ("traditional", Label("Visited"))
                                                            ("open", Label("Not Visited"))))
                                                (false, Label("Not Visited"))))
                                       (4, Label("Visited")))))
        self.assertEqual(result, expected)
