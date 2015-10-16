from _page_rank import ffi, lib
import click
import time
import vector

def newGraph(maxNodes):
    threads = 4
    if maxNodes / (threads * 10) < 5:
        # too little nodes? just do |threads| batches per iteration dividing
        # the nodes up equally amongst the threads
        batchSize = (int) (maxNodes / threads) + 1
    else:
        batchSize = (int)(maxNodes / (threads * 10))

    dVal = 0.85
    epsilon = 0.00001

    return lib.newGraph(maxNodes, batchSize, dVal, epsilon, threads)

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

    graph = newGraph(len(lines))

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
        lib.addEdge(
                graph, left.encode(encoding="ascii"),
                right.encode(encoding="ascii"))
        
    print("Added lines")

    for i in range(1000):
        lib.computeIteration(graph)
        # thread = threading.Thread(target= args=(isSourceA))
        # thread.run()
        #print("Iterating...")
        # thread.join()
        if graph.converged == 1:
            break

    # This is basically a lambda
    def getRank(node):
        struct = lib.findNodeByName(graph, node.encode())
        return struct.pageRank_b if graph.isSourceA == 1 else struct.pageRank_a

    ordered = sorted(nodes, key=getRank)
    if graph.converged:
        print("Converged! after %s iterations" % graph.iterationCount)
    else:
        print("Didn't converge.")

    print("Outdegree:")
    for node in ordered:
        struct = lib.findNodeByName(graph, node.encode())
        if struct:
            print("{0!s}\t{1}\t({2})".format(node, getRank(node), abs(struct.pageRank_a - struct.pageRank_b)))

    lib.cleanup(graph)

