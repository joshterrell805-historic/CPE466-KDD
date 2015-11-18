import time
import re
import pickle

class Reformat:
    def __init__(self):
        self.swap = False
        self.maxNode = 0
        self.nodes = {}
        self.unmap = []

    def get_nodeid(self, name):
        if name in self.nodes:
            return self.nodes[name]
        else:
            number = self.maxNode
            self.nodes[name] = number
            self.unmap.append(name)
            self.maxNode += 1
            return number

    def convert_nodes(self, nodelist):
        nodes = set()
        for (left, right) in nodelist:
            nodes.add(left)
            nodes.add(right)
        ordered_nodes = sorted(list(nodes))
        for node in ordered_nodes:
            self.get_nodeid(node)

        return [(self.get_nodeid(left), self.get_nodeid(right)) for (left, right) in nodelist]

    def parse_line(self, line):
        parts = line.split(',')

        left = parts[0].strip().strip('"')
        right = parts[2].strip().strip('"')

        if (self.swap):
            return (right, left)
        else:
            return (left, right)

    def parse_file(self, datafile):
        return [self.parse_line(line) for line in datafile]



    def reformat(self, datafile):
        # Time loading the data into the graph
        start = time.clock()
        lines = self.parse_file(datafile)
        normalized = self.convert_nodes(lines)

        print("#\n#\n# Nodes: {} Edges: {}\r\n# From\tTo".format(len(self.nodes), len(normalized)), end='\r\n')
        for (l, r) in normalized:
            print("{}\t{}".format(l, r), end='\r\n')
        self.loadtime = time.clock() - start

# This section derived from https://docs.python.org/3/tutorial/modules.html#executing-modules-as-scripts
if (__name__ == "__main__"):
    import sys
    formatter = Reformat()
    if sys.argv[1] == "--swap":
        formatter.swap = True
        filename = sys.argv[2]
    else:
        filename = sys.argv[1]
    with open(filename) as file:
        formatter.reformat(file)
    with open(filename + ".pickle", "wb") as data:
        pickle.dump({"unmap": formatter.unmap, "loadtime": formatter.loadtime}, data)
