import unittest
import xml.etree.ElementTree as ET
from hierarchical_clusterer import Cluster
import pprint
import numpy as np

class TestCluster(unittest.TestCase):
    tree = Cluster([
        Cluster([Cluster([np.array([5,1])]), Cluster([np.array([9,1])])]),
        Cluster([np.array([7,7])])
    ])
    xml_str = \
    """
    <tree height="6.0">
       <node height="4.0">
           <leaf data="[5, 1]" />
           <leaf data="[9, 1]" />
        </node>
        <leaf data="[7, 7]" />
    </tree>
    """
    xml = ET.fromstring(xml_str)

    def test_to_xml(self):
        actual = ET.tostring(self.tree.to_xml())
        expected = ET.tostring(self.xml)
        self.assertEqual(actual.replace(b' ', b'').replace(b'\n', b''),
                         expected.replace(b' ', b'').replace(b'\n', b''))

    def test_to_xml_small(self):
        actual = ET.tostring(Cluster([np.array([7,4,8])]).to_xml())
        expected = ET.tostring(ET.fromstring(
                '<tree height="0.0"><leaf data="[7, 4, 8]"/></tree>'))
        self.assertEqual(actual.replace(b' ', b'').replace(b'\n', b''),
                         expected.replace(b' ', b'').replace(b'\n', b''))

    def test_from_xml_small(self):
        expected = Cluster([np.array([7,4,8])])
        actual = Cluster.from_xml(
            ET.fromstring('<tree height="0.0"><leaf data="[7, 4, 8]"/></tree>')
        )
        self.assertEqual(actual, expected)

    def test_to_xml_small2(self):
        actual = ET.tostring(
            Cluster([
                Cluster([np.array([3,0,4])]),
                Cluster([np.array([0,0,0])])
            ]).to_xml()
        )
        expected = ET.tostring(
            ET.fromstring('<tree height="5.0"><leaf data="[3, 0, 4]"/><leaf data="[0, 0, 0]"/></tree>')
        )
        self.assertEqual(actual, expected)

    def test_from_xml_small2(self):
        expected = Cluster([
            Cluster([np.array([3,0,4])]),
            Cluster([np.array([0,0,0])])
        ])
        actual = Cluster.from_xml(
            ET.fromstring('<tree height="5.0"><leaf data="[3, 0, 4]"/><leaf data="[0, 0, 0]"/></tree>')
        )
        self.assertEqual(actual, expected)
        
    def test_from_xml(self):
        actual = Cluster.from_xml(self.xml)
        expected = self.tree
        self.assertEqual(actual, expected)
