from _page_rank import ffi, lib
import unittest

class TestPageRank(unittest.TestCase):
    def test_graphCreation(self):
        graph = lib.newGraph(4, -1, -1, -1, 1, 0)

        ret = lib.addEdgeByIds(graph, 1, 2, 1)
        self.assertEqual(ret, 0)

        ret = lib.addEdgeByIds(graph, 2, 3, 1)
        self.assertEqual(ret, 0)

        ret = lib.addEdgeByIds(graph, 1, 3, 1)
        self.assertEqual(ret, 0)

        ret = lib.addEdgeByIds(graph, 0, 3, 1)
        self.assertEqual(ret, 0)

        # can't create more than 4 nodes
        ret = lib.addEdgeByIds(graph, 3, 4, 1)
        self.assertEqual(ret, -1)
        self.assertEqual(lib.findNodeById(graph, 4), ffi.NULL)

        # nodes have correct data
        n = lib.findNodeById(graph, 1)
        self.assertEqual(n.outDegree, 2)
        self.assertLLValuesById(n.inNodes, [])

        n = lib.findNodeById(graph, 2)
        self.assertEqual(n.outDegree, 1)
        self.assertLLValuesById(n.inNodes, [1])

        n = lib.findNodeById(graph, 3)
        self.assertEqual(n.outDegree, 0)
        self.assertLLValuesById(n.inNodes, [2, 1, 0])

        n = lib.findNodeById(graph, 0)
        self.assertEqual(n.outDegree, 1)
        self.assertLLValuesById(n.inNodes, [])

        lib.cleanup(graph)

    def test_graphCreationById(self):
        graph = lib.newGraph(4, -1, -1, -1, 1, 0)

        ret = lib.addEdgeByIds(graph, 0, 1, 1)
        self.assertEqual(ret, 0)

        ret = lib.addEdgeByIds(graph, 1, 2, 1)
        self.assertEqual(ret, 0)

        ret = lib.addEdgeByIds(graph, 0, 2, 1)
        self.assertEqual(ret, 0)

        ret = lib.addEdgeByIds(graph, 3, 2, 1)
        self.assertEqual(ret, 0)

        # can't create more than 4 nodes
        ret = lib.addEdgeByIds(graph, 2, 4, 1)
        self.assertEqual(ret, -1)
        self.assertEqual(lib.findNodeById(graph, 4), ffi.NULL)

        # nodes have correct data
        n = lib.findNodeById(graph, 0)
        self.assertNodeById(n, 0)
        self.assertEqual(n.outDegree, 2)
        self.assertLLValuesById(n.inNodes, [])

        n = lib.findNodeById(graph, 1)
        self.assertNodeById(n, 1)
        self.assertEqual(n.outDegree, 1)
        self.assertLLValuesById(n.inNodes, [0])

        n = lib.findNodeById(graph, 2)
        self.assertNodeById(n, 2)
        self.assertEqual(n.outDegree, 0)
        self.assertLLValuesById(n.inNodes, [1, 0, 3])

        n = lib.findNodeById(graph, 3)
        self.assertNodeById(n, 3)
        self.assertEqual(n.outDegree, 1)
        self.assertLLValuesById(n.inNodes, [])

        lib.cleanup(graph)

    def test_computePageRank(self):
        epsilon = 0.00001
        nodeCount = 3
        graph = lib.newGraph(nodeCount+10, 1, 0.5, epsilon, 2, 0)
        lib.addEdgeByIds(graph, 1, 2, 1)
        lib.addEdgeByIds(graph, 1, 3, 1)
        lib.addEdgeByIds(graph, 2, 3, 1)
        lib.addEdgeByIds(graph, 3, 1, 1)

        lib.computeIteration(graph)

        # initial pageRank
        n = lib.findNodeById(graph, 1)
        self.assertTrue(abs(n.pageRank_a - 1.0/graph.weightedSize) < epsilon)
        n = lib.findNodeById(graph, 2)
        self.assertTrue(abs(n.pageRank_a - 1.0/graph.weightedSize) < epsilon)
        n = lib.findNodeById(graph, 3)
        self.assertTrue(abs(n.pageRank_a - 1.0/graph.weightedSize) < epsilon)

        while graph.converged == 0:
            lib.computeIteration(graph)

        # one more so both a and b have the converged page rank
        lib.computeIteration(graph)

        a = lib.findNodeById(graph, 1)
        b = lib.findNodeById(graph, 2)
        c = lib.findNodeById(graph, 3)

        # the examples are not normalized so we must divide by nodeCount
        # http://pr.efactory.de/e-pagerank-algorithm.shtml
        self.assertTrue(abs(a.pageRank_a - 1.07692308 / nodeCount) < epsilon*10)
        self.assertTrue(abs(a.pageRank_b - 1.07692308 / nodeCount) < epsilon*10)
        self.assertTrue(abs(b.pageRank_a - 0.76923077 / nodeCount) < epsilon*10)
        self.assertTrue(abs(b.pageRank_b - 0.76923077 / nodeCount) < epsilon*10)
        self.assertTrue(abs(c.pageRank_a - 1.15384615 / nodeCount) < epsilon*10)
        self.assertTrue(abs(c.pageRank_b - 1.15384615 / nodeCount) < epsilon*10)

        lib.cleanup(graph)

    def test_computePageRankById(self):
        epsilon = 0.00001
        nodeCount = 3
        graph = lib.newGraph(nodeCount+10, 1, 0.5, epsilon, 2, 0)
        lib.addEdgeByIds(graph, 0, 1, 1)
        lib.addEdgeByIds(graph, 0, 2, 1)
        lib.addEdgeByIds(graph, 1, 2, 1)
        lib.addEdgeByIds(graph, 2, 0, 1)

        lib.computeIteration(graph)

        n = lib.findNodeById(graph, 2)
        # initial pageRank
        self.assertTrue(abs(n.pageRank_a - 1.0/nodeCount) < epsilon)

        while graph.converged == 0:
            lib.computeIteration(graph)

        # one more so both a and b have the converged page rank
        lib.computeIteration(graph)

        a = lib.findNodeById(graph, 0)
        b = lib.findNodeById(graph, 1)
        c = lib.findNodeById(graph, 2)

        # the examples are not normalized so we must divide by nodeCount
        # http://pr.efactory.de/e-pagerank-algorithm.shtml
        self.assertTrue(abs(a.pageRank_a - 1.07692308 / nodeCount) < epsilon*10)
        self.assertTrue(abs(a.pageRank_b - 1.07692308 / nodeCount) < epsilon*10)
        self.assertTrue(abs(b.pageRank_a - 0.76923077 / nodeCount) < epsilon*10)
        self.assertTrue(abs(b.pageRank_b - 0.76923077 / nodeCount) < epsilon*10)
        self.assertTrue(abs(c.pageRank_a - 1.15384615 / nodeCount) < epsilon*10)
        self.assertTrue(abs(c.pageRank_b - 1.15384615 / nodeCount) < epsilon*10)

        lib.cleanup(graph)


    def assertLLValuesById(self, lln, values):
        lln = ffi.cast('LLNode*', lln)

        for i in range(len(values)):
            self.assertNodeById(lln.self, values[i])
            lln = ffi.cast('LLNode*', lln.next)

        self.assertEqual(lln, ffi.NULL)

    def assertNodeById(self, node, id):
        node = ffi.cast('Node*', node)
        self.assertEqual(node.id, id)
