import xml.etree.ElementTree as ET

class Node:
    def __init__(self, name, *edge_tuples):
        self.name = name
        self.edges = {}
        for edge in edge_tuples:
            name = 0
            label = 1
            self.edges[edge[name]] = edge[label]

class Label:
    def __init__(self, category):
        self.category = category

    def __eq__(self, other):
        return self.category == other.category

def build_tree(xml_str):
    xml_tree = ET.fromstring(xml_str)
    xml_root = xml_tree #xml_tree.getroot()
    children = list(xml_root)

    if not (xml_root.tag == "Tree" and 'name' in xml_root.keys() and \
            len(children) == 1 and children[0].tag == 'node'):
        raise Exception('Invalid Tree root node')

    return build_tree_recursive(children[0])

def build_tree_recursive(xml_root):
    if xml_root.tag == 'node':
        if 'var' not in xml_root.keys():
            raise Exception('nodes must have "var" attribute')

        xml_children = list(xml_root)
        if len(xml_children) < 2 or\
                False in [c.tag == 'edge' for c in xml_children]:
            raise Exception('nodes must have >= 2 edge children')
        return Node(xml_root.get('var'),\
                *[build_tree_recursive(c) for c in xml_children])
    elif xml_root.tag == 'edge':
        if 'var' not in xml_root.keys() or 'num' not in xml_root.keys():
            raise Exception('edges must have "var" and "num" attributes')

        xml_children = list(xml_root)
        if len(xml_children) != 1 or xml_children[0].tag == 'edge':
            raise Exception('edges must have exactly 1 non-edge child')
        return (xml_root.get('var'), build_tree_recursive(xml_children[0]))
    elif xml_root.tag == 'decision':
        if 'choice' not in xml_root.keys() or 'end' not in xml_root.keys():
            raise Exception('leafs must have "choice" and "end" attributes')
        return Label(xml_root.get('choice'))
    else:
        raise Exception('tree elements must be "node" or "edge"')
