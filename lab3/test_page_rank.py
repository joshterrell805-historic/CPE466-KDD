from _page_rank import ffi, lib
import unittest

class TestPageRank(unittest.TestCase):
    def test_sample_cffi(self):
        self.assertFalse(lib.hasConverged())

        lib.computePageRank(False)
        self.assertFalse(lib.hasConverged())

        lib.computePageRank(True)
        self.assertTrue(lib.hasConverged())

        lib.computePageRank(False)
        self.assertTrue(lib.hasConverged())

    def test_graphCreation(self):
        lib.init(4, -1)

        ret = lib.addEdge(b"a", b"b")
        self.assertEqual(ret, 0)

        ret = lib.addEdge(b"b", b"c")
        self.assertEqual(ret, 0)

        ret = lib.addEdge(b"a", b"c")
        self.assertEqual(ret, 0)

        ret = lib.addEdge(b"d", b"c")
        self.assertEqual(ret, 0)

        # can't create more than 4 nodes
        ret = lib.addEdge(b"c", b"e")
        self.assertEqual(ret, -1)
        self.assertEqual(lib.findNodeByName(b"e"), ffi.NULL)

        # nodes have correct data
        n = lib.findNodeByName(b"a")
        self.assertNode(n, b"a")
        self.assertEqual(n.outDegree, 2)
        self.assertLLValues(n.inNodes, [])

        n = lib.findNodeByName(b"b")
        self.assertNode(n, b"b")
        self.assertEqual(n.outDegree, 1)
        self.assertLLValues(n.inNodes, [b"a"])

        n = lib.findNodeByName(b"c")
        self.assertNode(n, b"c")
        self.assertEqual(n.outDegree, 0)
        self.assertLLValues(n.inNodes, [b"b", b"a", b"d"])

        n = lib.findNodeByName(b"d")
        self.assertNode(n, b"d")
        self.assertEqual(n.outDegree, 1)
        self.assertLLValues(n.inNodes, [])


        lib.cleanup()

    def test_getNextNodesInIteration(self):
        lib.init(7, 2)
        lib.addEdge(b"a", b"a")
        lib.addEdge(b"b", b"a")
        lib.addEdge(b"c", b"a")
        lib.addEdge(b"d", b"a")
        lib.addEdge(b"e", b"a")
        lib.addEdge(b"f", b"a")
        lib.addEdge(b"g", b"a")

        head = ffi.cast('LLNode*', lib.findNodeByName(b"a"))
        pNode = ffi.new('Node [1]')
        pCount = ffi.new('int [1]')
        ppNode = ffi.addressof(pNode)
        ppNode = ffi.cast('Node **', ppNode)

        lib.startIteration()

        lib.getNextBatchInIteration(ppNode, pCount)
        self.assertEqual(pCount[0], 2)
        self.assertNode(ppNode[0], b"a")

        lib.getNextBatchInIteration(ppNode, pCount)
        self.assertEqual(pCount[0], 2)
        self.assertNode(ppNode[0], b"c")

        lib.getNextBatchInIteration(ppNode, pCount)
        self.assertEqual(pCount[0], 2)
        self.assertNode(ppNode[0], b"e")

        lib.getNextBatchInIteration(ppNode, pCount)
        self.assertEqual(pCount[0], 1)
        self.assertNode(ppNode[0], b"g")

        lib.getNextBatchInIteration(ppNode, pCount)
        self.assertEqual(pCount[0], 0)

        lib.startIteration()

        lib.getNextBatchInIteration(ppNode, pCount)
        self.assertEqual(pCount[0], 2)
        self.assertNode(ppNode[0], b"a")

        lib.getNextBatchInIteration(ppNode, pCount)
        self.assertEqual(pCount[0], 2)
        self.assertNode(ppNode[0], b"c")

        lib.cleanup()

    def assertLLValues(self, lln, values):
        lln = ffi.cast('LLNode*', lln)

        for i in range(len(values)):
            self.assertNode(lln.self, values[i])
            lln = ffi.cast('LLNode*', lln.next)

        self.assertEqual(lln, ffi.NULL)

    def assertNode(self, node, name):
        node = ffi.cast('Node*', node)
        self.assertEqual(lib.strcmp(node.name, name), 0)
