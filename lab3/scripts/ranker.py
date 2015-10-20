from _page_rank import ffi, lib
import click
import time
import vector
import math

@click.command()
@click.option('--epsilon', help='If every node changes less than epsilon in an iteration, consider pagerank of the network to have converged. Should contain exactly one non-zero digit, with the value of one.', default=0.00001)
@click.option('--maxiterations', default=100)
@click.option('--limit/--no-limit', help='Limit precision of printed page rank to precision specified by epsilon option', default=False)
@click.option('--dval', help='Probability of following a link in pagerank algorithm.', default=0.85)
@click.option('--threads', help='number of threads computing pagerank.', default=4)
@click.option('--undirected', help='Specify flag to indicate that this source file contains undirected node data.', is_flag=True)
@click.argument('datafile', type=click.File('r'))
@click.option('--batchsize', help='On each iteration, each thread claims `batchsize` nodes to compute pagerank for. A batchsize of too small, and threads may constantly be sychronizing around a mutex. Too large, and a few threads may end up doing most of the work while others sit idly.', default=100)
@click.option('--format', type=click.Choice(['csv', 'snap']))
def rank(epsilon, maxiterations, dval, threads, datafile, undirected, limit,
         batchsize, format):
    ranker = Ranker()
    start = time.clock()

    maxNodes = Ranker.countNodes(datafile)

    maxNodes = maxNodes * 2 if undirected else maxNodes
    ranker.newGraph(maxNodes, epsilon, dval, threads, batchsize)
    nodes = set()
    for line in datafile:
        nodes.update(ranker.addEdge(line))

    loadtime = time.clock() - start
    print("Load Time:", loadtime)

    # todo undirected stuff
    for i in range(maxiterations):
        ranker.computeIteration()
        if ranker.graph.converged == 1:
            break

    # This is basically a lambda
    def getRank(node):
        struct = ranker.findNode(node.encode())
        return struct.pageRank_b if ranker.graph.isSourceA == 1 else struct.pageRank_a

    def getName(node):
        struct = ranker.findNode(node.encode())
        return ffi.string(struct.name)

    name_ordered = sorted(nodes, key=getName)
    ordered = sorted(name_ordered, key=getRank, reverse=True)
    if ranker.isConverged:
        print("Converged! after %s iterations" % ranker.graph.iterationCount)
    else:
        print("Didn't converge.")

    print("Outdegree:")
    if limit:
        precision = str(math.floor(-math.log10(epsilon) - 1))
        fmt = "{0!s}\t{1:." + precision + "f}\t({2:." + precision + "f})"
    else:
        fmt = "{0!s}\t{1}\t({2})"

    for node in ordered:
        struct = ranker.findNode(node.encode())
        if struct:
            print(fmt.format(node, getRank(node), abs(struct.pageRank_a - struct.pageRank_b)))

    ranker.cleanup()


class Ranker:
    def countNodes(datafile):
        maxNodes = 0
        for line in datafile:
            maxNodes += 1

        datafile.seek(0)
        return maxNodes

    def newGraph(self, maxNodes, epsilon, dVal, threads, batchsize):
        self.graph = lib.newGraph(maxNodes, batchsize, dVal, epsilon, threads)

    def addEdge(self, line):
        parts = line.split(',')

        left = parts[0].strip().strip('"')
        right = parts[2].strip().strip('"')

        lib.addEdge(
                self.graph, left.encode(encoding="ascii"),
                right.encode(encoding="ascii"))

        return [left, right]

    def findNode(self, name):
        return lib.findNodeByName(self.graph, name)

    def isConverged(self):
        return self.graph.converged

    def computeIteration(self):
        lib.computeIteration(self.graph)

    def cleanup(self):
        lib.cleanup(self.graph)

