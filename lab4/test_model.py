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

    def test_tree_equality(self):
        root = Node("Has chicken breast on menu",
                     ("true", Label("5 stars")),
                     ("false", Node("Has burritos on menu",
                                     ("true", Node("Has chicken in burritos",
                                                    ("true", Label("5 stars")),
                                                    ("false", Label("3 stars")))),
                                     ("false", Label("0 stars")))))
        self.assertEqual(root, root)
        self.assertEqual(root.edges['true'], Label('5 stars'))
        self.assertEqual(root.edges['false'],
                Node("Has burritos on menu",
                      ("true", Node("Has chicken in burritos",
                                     ("true", Label("5 stars")),
                                     ("false", Label("3 stars")))),
                      ("false", Label("0 stars"))))

        self.assertEqual(root.edges['false'].edges['true'],
                Node("Has chicken in burritos",
                      ("true", Label("5 stars")),
                      ("false", Label("3 stars"))))

        self.assertEqual(root.edges['false'].edges['false'], Label('0 stars'))

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

        tree = Node("Gender",
                ("Female", Node("Bush Approval",
                        ("Approve", Label("McCain")),
                        ("Disapprove", Label("Obama")))),
                ("Male", Node("Ideology",
                        ("Liberal", Label("Obama")),
                        ("Moderate", Label("Obama")),
                        ("Conservative", Label("McCain")))))
        self.assertEqual(root, tree)

    def test_stringify_tree(self):
        tree = Node("Gender",
                ("Female", Node("Bush Approval",
                        ("Approve", Label("McCain")),
                        ("Disapprove", Label("Obama")))),
                ("Male", Node("Ideology",
                        ("Liberal", Label("Obama")),
                        ("Moderate", Label("Obama")),
                        ("Conservative", Label("McCain")))))
        xml_tree = model.stringify_tree(tree)
        self.assertEqual(tree, model.build_tree(xml_tree))

    def test_classify_success(self):
        tree = Node("Gender",
                ("Female", Node("Bush Approval",
                        ("Approve", Label("McCain")),
                        ("Disapprove", Label("Obama")))),
                ("Male", Node("Ideology",
                        ("Liberal", Label("Obama")),
                        ("Moderate", Label("Obama")),
                        ("Conservative", Label("McCain")))))

        c = tree.classify(['Female', 'Approve', None],
                          ['Gender', 'Bush Approval', 'Ideology'])
        self.assertEqual(c, 'McCain')
        # same but dif order of features
        c = tree.classify(['Approve', 'Female', None],
                          ['Bush Approval', 'Gender', 'Ideology'])
        self.assertEqual(c, 'McCain')
        # dif last node
        c = tree.classify(['Disapprove', 'Female', None],
                          ['Bush Approval', 'Gender', 'Ideology'])
        self.assertEqual(c, 'Obama')
        # dif first node
        c = tree.classify([None, 'Male', 'Liberal'],
                          ['Bush Approval', 'Gender', 'Ideology'])
        self.assertEqual(c, 'Obama')

    def test_classify_feature_names_do_not_match_tree(self):
        tree = Node("Gender",
                ("Female", Node("Bush Approval",
                        ("Approve", Label("McCain")),
                        ("Disapprove", Label("Obama")))),
                ("Male", Node("Ideology",
                        ("Liberal", Label("Obama")),
                        ("Moderate", Label("Obama")),
                        ("Conservative", Label("McCain")))))

        try:
            tree.classify(['Male', -1, -1], ['a', 'b', 'c'])
            self.assertTrue(False)
        except Exception as e:
            self.assertEqual(
                    str(e),
                    'Datapoint does not fit tree: "Gender" not in features')
        try:
            tree.classify(['Male', 'Liberal', -1], ['Gender', 'b', 'c'])
            self.assertTrue(False)
        except Exception as e:
            self.assertEqual(
                    str(e),
                    'Datapoint does not fit tree: "Ideology" not in features')

    def test_classify_invalid_value_for_column(self):
        tree = Node("Gender",
                ("Female", Node("Bush Approval",
                        ("Approve", Label("McCain")),
                        ("Disapprove", Label("Obama")))),
                ("Male", Node("Ideology",
                        ("Liberal", Label("Obama")),
                        ("Moderate", Label("Obama")),
                        ("Conservative", Label("McCain")))))
        try:
            tree.classify(['Male', -1, -1], ['Gender', 'Ideology', 'c'])
            self.assertTrue(False)
        except Exception as e:
            self.assertEqual(
                    str(e),
                    'Datapoint has invalid value for "Ideology"')
