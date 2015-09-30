import unittest
from modelbuilder import ModelBuilder
class TestModelBuilder(unittest.TestCase):
    def basicRead(self):
        fake = FakeElement(['thing', 'another'])
        ret = next(fake)
        utterances = fake.document
        self.assertEqual('thing', ret)
        self.assertEqual('thing', utterances)

        ret = next(fake)
        utterances = fake.document
        self.assertEqual('another', ret)
        self.assertEqual('another', utterances)


class FakeElement:
    def __init__(self, parent):
        self.parent = parent

    def __iter__(self):
        return self

    def __next__(self):
        self.document = next(parent)
        return self.document
