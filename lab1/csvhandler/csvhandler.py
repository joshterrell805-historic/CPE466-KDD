import string

class CSVHandler:
  def parseVector(self, line):
    items = line.split(',')
    items = map(string.strip, items)
    return map(float, items)
