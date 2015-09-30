import unittest
from modelbuilder import ModelBuilder
class TestModelBuilder(unittest.TestCase):
    def basicRead(self):
        data = '[{"pid":100, "first":"Hannah-Beth", "last":"Jackson", "PersonType":"Legislator", "date":"28-04-15", "house":"Senate", "Committee":"Judiciary", "text":"Excuse me. Excuse me. You\'re opposed to the bill. Thank you very much. Please, name, affiliation, and position."}]'

        builder = ModelBuilder()
        fake = FakeElement()
        builder.addModule(fake)
        builder.read(StringIO(data))
        utterances = fake.getDocument()
        expected = {"pid" : 100, "first":"Hannah-Beth", "last":"Jackson", "PersonType":"Legislator", "date":"28-04-15", "house":"Senate", "Committee":"Judiciary", "text":"Excuse me. Excuse me. You're opposed to the bill. Thank you very much. Please, name, affiliation, and position."}
        self.assertEqual(data, utterances)


class FakeElement:
    def process(self, document):
        self.document = document
        return None

    def getDocument(self):
        return self.document
