import string
from vector import Vector

class CSVHandler:
  def parseVector(self, line):
    items = line.split(',')
    items = map(string.strip, items)
    items = map(lambda str: None if str == '' else str, items)
    return Vector(map(lambda str: None if str is None else float(str), items))

  def parseLines(self, lines):
    return map(lambda line: self.parseVector(line), lines)
