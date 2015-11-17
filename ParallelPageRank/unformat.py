import time
import re
import pickle

class Unformat:
    def __init__(self):
        self.lineprog = re.compile('^Node (\d+) ranked (.*)')

    def unformat(self):
        # Time loading the data into the graph
        start = time.clock()
        for line in sys.stdin:
            result = self.lineprog.match(line)
            if result:
                print("Node {} ranked {}".format(self.unmap[int(result.group(1))], result.group(2)))
            else:
                print(line, end='')
        loadtime = time.clock() - start
        print("Formatting Time:", formatter.data["loadtime"])
        print("Unformat Time:", loadtime)

# This section derived from https://docs.python.org/3/tutorial/modules.html#executing-modules-as-scripts
if (__name__ == "__main__"):
    import sys
    formatter = Unformat()
    with open(sys.argv[1], 'rb') as data:
        formatter.data = pickle.load(data)
        formatter.unmap = formatter.data["unmap"]
    formatter.unformat()
