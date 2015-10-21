from _page_rank import ffi, lib
import sys

class PageRank:
    def __init__(self, maxNodes, epsilon, dVal, threads, batchsize, scale,
            weighted):
        self.graph = lib.newGraph(maxNodes, batchsize, dVal, epsilon, threads,
                1 if scale else 0)
        self.mapping = {}
        self.index = 0
        self.scale = scale
        self.weighted = weighted

    def __del__(self):
        lib.cleanup(self.graph)

    def addEdge(self, line):
        (left, right, weight) = line

        # see http://stackoverflow.com/a/402704/2243495
        if isinstance(left, int):
            leftId = left
        else:
            leftId = self.getOrSetId(left)

        if isinstance(right, int):
            rightId = right
        else:
            rightId = self.getOrSetId(right)

        if not self.weighted:
            weight = 1

        if weight > 0:
            lib.addEdgeByIds(self.graph, rightId, leftId, weight)
        elif weight < 0:
            lib.addEdgeByIds(self.graph, leftId, rightId, -weight)
        else:
            # lets not figure out how to handle this until it happens
            raise Exception("zero weight")

        return [left, right]

    def getId(self, name):
        return self.mapping[name]

    def setId(self, name, id):
        self.mapping[name] = id

    def getOrSetId(self, name):
        if name in self.mapping:
            return self.getId(name)
        else:
            self.setId(name, self.index)
            self.index += 1
            return self.index - 1

    def computeRanking(self, maxiterations):
        # todo undirected stuff
        for i in range(maxiterations):
            self.computeIteration()
            if self.isConverged():
                break

    def findNode(self, name):
        if isinstance(name, int):
            id = name
        else:
            id = self.getId(name)
        return lib.findNodeById(self.graph, id)

    def isConverged(self):
        return self.graph.converged == 1

    def computeIteration(self):
        lib.computeIteration(self.graph)

    def getOrderedNodes(self, nodes):
        name_ordered = sorted(nodes)
        return sorted(name_ordered, key=self.getRank, reverse=True)

    def getRank(self, node):
        struct = self.findNode(node)
        rank = struct.pageRank_b if self.graph.isSourceA == 1 else struct.pageRank_a
        if self.scale:
            rank = rank * self.graph.weightedSize
        return rank
