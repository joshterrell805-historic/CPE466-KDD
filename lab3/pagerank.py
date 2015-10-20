from _page_rank import ffi, lib
import sys

class PageRank:
    def __init__(self, maxNodes, epsilon, dVal, threads, batchsize):
        self.graph = lib.newGraph(maxNodes, batchsize, dVal, epsilon, threads)

    def __del__(self):
        lib.cleanup(self.graph)

    def addEdge(self, line):
        parts = line.split(',')

        left = parts[0].strip().strip('"')
        right = parts[2].strip().strip('"')

        lib.addEdge(
                self.graph, left.encode(encoding="ascii"),
                right.encode(encoding="ascii"))

        return [left, right]

    def computeRanking(self, maxiterations):
        # todo undirected stuff
        for i in range(maxiterations):
            self.computeIteration()
            if self.isConverged() == 1:
                break

    def findNode(self, name):
        return lib.findNodeByName(self.graph, name)

    def isConverged(self):
        return self.graph.converged

    def computeIteration(self):
        lib.computeIteration(self.graph)

    def getOrderedNodes(self, nodes):
        name_ordered = sorted(nodes)
        return sorted(name_ordered, key=self.getRank, reverse=True)

    def getRank(self, node):
        struct = self.findNode(node.encode())
        return struct.pageRank_b if self.graph.isSourceA == 1 else struct.pageRank_a
