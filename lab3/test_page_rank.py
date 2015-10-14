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
        lib.init(4)

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
        self.assertEqual(lib.strcmp(n.name, b"a"), 0)
        self.assertEqual(n.outDegree, 2)
        self.assertEqual(n.inNodes, ffi.NULL)

        n = lib.findNodeByName(b"b")
        self.assertEqual(lib.strcmp(n.name, b"b"), 0)
        self.assertEqual(n.outDegree, 1)
        llNode = ffi.cast('LLNode*', n.inNodes)
        n = ffi.cast('Node*', llNode.self)
        self.assertEqual(lib.strcmp(n.name, b"a"), 0)
        llNode = ffi.cast('LLNode*', llNode.next)
        self.assertEqual(llNode, ffi.NULL)

        n = lib.findNodeByName(b"c")
        self.assertEqual(lib.strcmp(n.name, b"c"), 0)
        self.assertEqual(n.outDegree, 0)
        llNode = ffi.cast('LLNode*', n.inNodes)
        n = ffi.cast('Node*', llNode.self)
        self.assertEqual(lib.strcmp(n.name, b"b"), 0)
        llNode = ffi.cast('LLNode*', llNode.next)
        n = ffi.cast('Node*', llNode.self)
        self.assertEqual(lib.strcmp(n.name, b"a"), 0)
        llNode = ffi.cast('LLNode*', llNode.next)
        n = ffi.cast('Node*', llNode.self)
        self.assertEqual(lib.strcmp(n.name, b"d"), 0)
        llNode = ffi.cast('LLNode*', llNode.next)
        self.assertEqual(llNode, ffi.NULL)

        n = lib.findNodeByName(b"d")
        self.assertEqual(lib.strcmp(n.name, b"d"), 0)
        self.assertEqual(n.outDegree, 1)
        self.assertEqual(n.inNodes, ffi.NULL)

        lib.cleanup()
