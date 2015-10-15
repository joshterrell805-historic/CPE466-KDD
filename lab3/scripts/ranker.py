from _page_rank import ffi, lib
import click
import time
import vector

@click.command()
@click.argument('datafile', type=click.File('r'))
def rank(datafile):
    nameToIndex = {}
    lines = []
    start = time.clock()
    for line in datafile:
        lines.append(line)
    setuptime = time.clock() - start
    print(setuptime)
    lib.init(len(lines), -1)
    nodes = set()
    for edge in lines:
        parts = edge.split(',')

        left = parts[0].strip('"')
        right = parts[2].strip('"')

        nodes.add(left)
        nodes.add(right)
        
        lib.addEdge(left.encode(), right.encode())
    lib.startIteration()
    lib.computePageRank(100)

    if lib.hasConverged():
        print("Converged!")
    else:
        print("Didn't converge.")

    print("Outdegree:")
    for node in nodes:
        struct = lib.findNodeByName(node.encode())
        if struct:
            print("{0!s} {1}".format(node, struct.outDegree))
