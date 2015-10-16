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
    lib.init(len(lines), 1, 0.85, 0.001)
    nodes = set()
#    import pdb; pdb.set_trace()
    print("Adding lines")
    num = 0
    for edge in lines:
        parts = edge.split(',')

        left = parts[0].strip().strip('"')
        right = parts[2].strip().strip('"')

        nodes.add(left)
        nodes.add(right)
        num += 1
        print("{0}->{1}^{2}".format(num, left, right))
        lib.addEdge(left.encode(encoding="ascii"), right.encode(encoding="ascii"))
        
    print("Added lines")

    isSourceA = 1
    for i in range(1000):
        lib.startIteration()
        # thread = threading.Thread(target= args=(isSourceA))
        lib.computePageRank(isSourceA)
        # thread.run()
        print("Iterating...")
        # thread.join()
        isSourceA ^= 1
        if lib.hasConverged() == 1:
            break

    # This is basically a lambda
    def getRank(node):
        struct = lib.findNodeByName(node.encode())
        return struct.pageRank_a if isSourceA == 0 else struct.pageRank_b

    ordered = sorted(nodes, key=getRank)
    if lib.hasConverged():
        print("Converged!")
    else:
        print("Didn't converge.")

    print("Outdegree:")
    for node in ordered:
        struct = lib.findNodeByName(node.encode())
        if struct:
            print("{0!s}\t{1}\t({2})".format(node, getRank(node), abs(struct.pageRank_a - struct.pageRank_b)))

    lib.cleanup()

