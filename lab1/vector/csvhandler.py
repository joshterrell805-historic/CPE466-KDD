from vector.vector import Vector

class CSVHandler:
  def parseVector(self, line):
    items = line.split(',')
    items = map(str.strip, items)
    items = map(lambda str: None if str == '' else str, items)
    return Vector(map(lambda str: None if str is None else float(str), items))

  def parseLines(self, lines):
    return list(map(lambda line: self.parseVector(line), lines))
