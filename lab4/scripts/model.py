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
