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
