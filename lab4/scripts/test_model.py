import unittest
from model import Node, Label
import model

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

    def test_build_tree(self):
        tree_str = """
        <Tree name = "test">
          <node var ="Gender">
            <edge var ="Female" num="2">
              <node var = "Bush Approval">
                <edge var = "Approve" num="2" >
                  <decision end = "2" choice = "McCain" p = "0.9"/>
                </edge>
                <edge var = "Disapprove" num="1">
                  <decision end = "1" choice="Obama" p = "0.95"/>
                </edge>
              </node>
            </edge>
            <edge var = "Male" num="1">
              <node var = "Ideology">
                <edge var = "Liberal" num = "1">
                  <decision end = "1" choice ="Obama" p = "0.99"/>
                </edge>
                <edge var = "Moderate" num="2">
                  <decision end = "1" choice = "Obama" p = "0.7"/>
                </edge>
                <edge var = "Conservative" num ="3">
                  <decision end = "2" choice = "McCain" p = "0.95"/>
                </edge>
              </node>
            </edge>
          </node>
        </Tree>
        """

        root = model.build_tree(tree_str)
        self.assertEqual(root.name, "Gender")
        self.assertEqual(len(root.edges.keys()), 2)

        # Gender = Female
        node = root.edges['Female']
        self.assertEqual(node.name, "Bush Approval")
        self.assertEqual(len(node.edges.keys()), 2)
        self.assertEqual(node.edges['Approve'], Label("McCain"))
        self.assertEqual(node.edges['Disapprove'], Label("Obama"))

        # Gender = Male
        node = root.edges['Male']
        self.assertEqual(node.name, "Ideology")
        self.assertEqual(len(node.edges.keys()), 3)
        self.assertEqual(node.edges['Liberal'], Label("Obama"))
        self.assertEqual(node.edges['Moderate'], Label("Obama"))
        self.assertEqual(node.edges['Conservative'], Label("McCain"))
