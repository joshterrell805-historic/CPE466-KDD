from _page_rank import ffi, lib
import unittest

class TestPageRank(unittest.TestCase):
    def test_graphCreation(self):
        graph = lib.newGraph(4, -1, -1, -1, 1)

        ret = lib.addEdge(graph, b"a", b"b")
        self.assertEqual(ret, 0)

        ret = lib.addEdge(graph, b"b", b"c")
        self.assertEqual(ret, 0)

        ret = lib.addEdge(graph, b"a", b"c")
        self.assertEqual(ret, 0)

        ret = lib.addEdge(graph, b"d", b"c")
        self.assertEqual(ret, 0)

        # can't create more than 4 nodes
        ret = lib.addEdge(graph, b"c", b"e")
        self.assertEqual(ret, -1)
        self.assertEqual(lib.findNodeByName(graph, b"e"), ffi.NULL)

        # nodes have correct data
        n = lib.findNodeByName(graph, b"a")
        self.assertNode(n, b"a")
        self.assertEqual(n.outDegree, 2)
        self.assertLLValues(n.inNodes, [])

        n = lib.findNodeByName(graph, b"b")
        self.assertNode(n, b"b")
        self.assertEqual(n.outDegree, 1)
        self.assertLLValues(n.inNodes, [b"a"])

        n = lib.findNodeByName(graph, b"c")
        self.assertNode(n, b"c")
        self.assertEqual(n.outDegree, 0)
        self.assertLLValues(n.inNodes, [b"b", b"a", b"d"])

        n = lib.findNodeByName(graph, b"d")
        self.assertNode(n, b"d")
        self.assertEqual(n.outDegree, 1)
        self.assertLLValues(n.inNodes, [])

        lib.cleanup(graph)

    def test_computePageRank(self):
        epsilon = 0.00001
        nodeCount = 3
        graph = lib.newGraph(nodeCount+10, 1, 0.5, epsilon, 2)
        lib.addEdge(graph, b"a", b"b")
        lib.addEdge(graph, b"a", b"c")
        lib.addEdge(graph, b"b", b"c")
        lib.addEdge(graph, b"c", b"a")

        lib.computeIteration(graph)

        n = lib.findNodeByName(graph, b"c")
        # initial pageRank
        self.assertTrue(abs(n.pageRank_a - 1.0/nodeCount) < epsilon)

        while graph.converged == 0:
            lib.computeIteration(graph)

        # if next is A, the converged must be B
        attrName = 'pageRank_b' if graph.iterationCount % 2 == 0 \
                else 'pageRank_b'

        a = lib.findNodeByName(graph, b"a")
        b = lib.findNodeByName(graph, b"b")
        c = lib.findNodeByName(graph, b"c")

        #print(
        #    a.pageRank_a*nodeCount, b.pageRank_a*nodeCount,
        #    c.pageRank_a*nodeCount)

        # the examples are not normalized so we must divide by nodeCount
        # http://pr.efactory.de/e-pagerank-algorithm.shtml
        self.assertTrue(abs(a.pageRank_a - 1.07692308 / nodeCount) < epsilon*10)
        self.assertTrue(abs(b.pageRank_a - 0.76923077 / nodeCount) < epsilon*10)
        self.assertTrue(abs(c.pageRank_a - 1.15384615 / nodeCount) < epsilon*10)

        lib.cleanup(graph)

    def assertLLValues(self, lln, values):
        lln = ffi.cast('LLNode*', lln)

        for i in range(len(values)):
            self.assertNode(lln.self, values[i])
            lln = ffi.cast('LLNode*', lln.next)

        self.assertEqual(lln, ffi.NULL)

    def assertNode(self, node, name):
        node = ffi.cast('Node*', node)
        self.assertEqual(lib.strcmp(node.name, name), 0)
