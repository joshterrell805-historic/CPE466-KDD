from _page_rank import ffi, lib
import click
import time
import vector

def newGraph(maxNodes, epsilon, dVal, threads):
    if maxNodes / (threads * 10) < 5:
        # too little nodes? just do |threads| batches per iteration dividing
        # the nodes up equally amongst the threads
        batchSize = (int) (maxNodes / threads) + 1
    else:
        batchSize = (int)(maxNodes / (threads * 10))

    return lib.newGraph(maxNodes, batchSize, dVal, epsilon, threads)

def addEdge(graph, line):
    parts = line.split(',')

    left = parts[0].strip().strip('"')
    right = parts[2].strip().strip('"')

    lib.addEdge(
            graph, left.encode(encoding="ascii"),
            right.encode(encoding="ascii"))

    return [left, right]

@click.command()
@click.option('--epsilon', help='If every node changes less than epsilon in an iteration, consider pagerank of the network to have converged.', default=0.00001)
@click.option('--maxiterations', default=100)
@click.option('--dval', help='Probability of following a link in pagerank algorithm.', default=0.85)
@click.option('--threads', help='number of threads computing pagerank.', default=4)
@click.option('--undirected', help='Specify flag to indicate that this source file contains undirected node data.', is_flag=True)
@click.argument('datafile', type=click.File('r'))
def rank(epsilon, maxiterations, dval, threads, datafile, undirected):

    start = time.clock()

    maxNodes = 0
    for line in datafile:
        maxNodes += 1

    maxNodes = maxNodes * 2 if undirected else maxNodes
    graph = newGraph(maxNodes, epsilon, dval, threads)
    datafile.seek(0)
    nodes = set()

    for line in datafile:
        nodes.update(addEdge(graph, line))

    loadtime = time.clock() - start
    print("Load Time:", loadtime)

    # todo undirected stuff
    for i in range(maxiterations):
        lib.computeIteration(graph)
        if graph.converged == 1:
            break

    # This is basically a lambda
    def getRank(node):
        struct = lib.findNodeByName(graph, node.encode())
        return struct.pageRank_b if graph.isSourceA == 1 else struct.pageRank_a

    ordered = sorted(nodes, key=getRank, reverse=True)
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

