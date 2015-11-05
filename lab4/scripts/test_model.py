import unittest
from model import Node, Label

class TestModel(unittest.TestCase):
    def test_build_model(self):
        root = Node("Has chicken breast on menu",
                     ("true", Label("5 stars")),
                     ("false", Node("Has burritos on menu",
                                     ("true", Node("Has chicken in burritos",
                                                    ("true", Label("5 stars")),
                                                    ("false", Label("3 stars")))),
                                     ("false", Label("0 stars")))))

        self.assertEqual(root.name, "Has chicken breast on menu")
        self.assertEqual(len(root.edges.keys()), 2)
        self.assertEqual(root.edges['true'], Label("5 stars"))

        node = root.edges['false']
        self.assertEqual(node.name, "Has burritos on menu")
        self.assertEqual(len(node.edges.keys()), 2)
        self.assertEqual(node.edges['false'], Label("0 stars"))

        node = node.edges['true']
        self.assertEqual(node.name, "Has chicken in burritos")
        self.assertEqual(node.edges['true'], Label("5 stars"))
        self.assertEqual(node.edges['false'], Label("3 stars"))
