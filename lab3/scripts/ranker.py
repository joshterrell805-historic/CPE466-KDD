from _page_rank import ffi, lib
import click
import time
import vector
import math

def newGraph(maxNodes, epsilon, dVal, threads, batchsize):
    return lib.newGraph(maxNodes, batchsize, dVal, epsilon, threads)

def addEdge(graph, line):
    parts = line.split(',')

    left = parts[0].strip().strip('"')
    right = parts[2].strip().strip('"')

    lib.addEdge(
            graph, left.encode(encoding="ascii"),
            right.encode(encoding="ascii"))

    return [left, right]

@click.command()
@click.option('--epsilon', help='If every node changes less than epsilon in an iteration, consider pagerank of the network to have converged. Should contain exactly one non-zero digit, with the value of one.', default=0.00001)
@click.option('--maxiterations', default=100)
@click.option('--limit/--no-limit', help='Limit precision of printed page rank to precision specified by epsilon option', default=False)
@click.option('--dval', help='Probability of following a link in pagerank algorithm.', default=0.85)
@click.option('--threads', help='number of threads computing pagerank.', default=4)
@click.option('--undirected', help='Specify flag to indicate that this source file contains undirected node data.', is_flag=True)
@click.argument('datafile', type=click.File('r'))
@click.option('--batchsize', help='On each iteration, each thread claims `batchsize` nodes to compute pagerank for. A batchsize of too small, and threads may constantly be sychronizing around a mutex. Too large, and a few threads may end up doing most of the work while others sit idly.', default=100)
def rank(epsilon, maxiterations, dval, threads, datafile, undirected, limit,
        batchsize):

    start = time.clock()

    maxNodes = 0
    for line in datafile:
        maxNodes += 1

    maxNodes = maxNodes * 2 if undirected else maxNodes
    graph = newGraph(maxNodes, epsilon, dval, threads, batchsize)
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
    if limit:
        precision = str(math.floor(-math.log10(epsilon) - 1))
        fmt = "{0!s}\t{1:." + precision + "f}\t({2:." + precision + "f})"
    else:
        fmt = "{0!s}\t{1}\t({2})"

    for node in ordered:
        struct = lib.findNodeByName(graph, node.encode())
        if struct:
            print(fmt.format(node, getRank(node), abs(struct.pageRank_a - struct.pageRank_b)))

    lib.cleanup(graph)

