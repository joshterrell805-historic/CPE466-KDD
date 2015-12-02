import unittest
import xml.etree.ElementTree as ET
from hierarchical_clusterer import Cluster
import pprint

class TestCluster(unittest.TestCase):
    def test_to_xml(self):
        tree = Cluster()
        tree.height = 5
        node = Cluster()
        node.height = 2
        left = Cluster()
        left.clusters = [(1,0)]
        right = Cluster()
        right.clusters = [(3,0)]
        node.clusters = [left, right]
        leaf = Cluster()
        leaf.clusters = [(6,0)]
        tree.clusters = [node, leaf]
        xml = tree.to_xml()
        expected = ET.fromstring("""<tree height = "5" ><node height = "2"><leaf data ="(1, 0)"/><leaf   data ="(3, 0)"/></node><leaf  data = "(6, 0)"/></tree>""")
        self.assertEqual(ET.tostring(xml.getroot()), ET.tostring(expected))
    
    def test_xml(self):
        tree = Cluster()
        left = Cluster()
        right = Cluster()
        left.clusters = ["(1,2)"]
        right.clusters = ["(3,4)"]
        tree.clusters = [left, right]
        xml = tree.to_xml()
        reinflated = Cluster.from_xml(xml.getroot())
        self.assertEqual(tree, reinflated)
