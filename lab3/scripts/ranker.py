import click
import time
import vector
import math
import functools
from pagerank import PageRank

@click.command()
@click.option('--epsilon', help='If every node changes less than epsilon in an iteration, consider pagerank of the network to have converged. Should contain exactly one non-zero digit, with the value of one.', default=0.00001)
@click.option('--maxiterations', default=100)
@click.option('--limit/--no-limit', help='Limit precision of printed page rank to three less places than the precision specified by epsilon option. Note that this doesn\'t handle the case where epsilon >= 0.001', default=False)
@click.option('--dval', help='Probability of following a link in pagerank algorithm.', default=0.85)
@click.option('--threads', help='number of threads computing pagerank.', default=4)
@click.option('--undirected', help='Specify flag to indicate that this source file contains undirected node data.', is_flag=True)
@click.argument('datafile', type=click.File('r'))
@click.option('--batchsize', help='On each iteration, each thread claims `batchsize` nodes to compute pagerank for. A batchsize of too small, and threads may constantly be sychronizing around a mutex. Too large, and a few threads may end up doing most of the work while others sit idly.', default=100)
@click.option('--fmt', type=click.Choice(['csv', 'snap']), default='csv')
def rank(epsilon, maxiterations, dval, threads, datafile, undirected, limit,
         batchsize, fmt):
    # Create Ranker

    # Time loading the data into the graph
    start = time.clock()
    maxNodes = countNodes(datafile)
    print("Nodes: {0}".format(maxNodes))
    maxNodes = maxNodes * 2 if undirected else maxNodes
    ranker = PageRank(maxNodes, epsilon, dval, threads, batchsize)
    nodes = set()
    loaded = 0
    for line in parse_file(fmt, datafile):
        nodes.update(ranker.addEdge(line))
        loaded += 1
        if maxNodes > 1000 and (loaded % 100000) == 0:
            print("Loaded {0} nodes...".format(loaded))

    loadtime = time.clock() - start
    print("Load Time:", loadtime)

    # Run algorithm
    retries = 0
    iterations = maxiterations
    while True:
        ranker.computeRanking(iterations)

        if ranker.isConverged():
            print("Converged! after %s iterations" % ranker.graph.iterationCount)
            break
        else:
            retries += 1
            # Increase the number of iterations exponentially
            olditerations = iterations
            iterations = int(math.pow(2, retries)) * maxiterations
            if not click.confirm("We've run {0} iterations and it's not converged. Keep running for {1} iterations?".format(olditerations, iterations), default=True):
                break

    print("Outdegree:")

    ordered = ranker.getOrderedNodes(nodes)
    if limit:
        # Skip the last 3 places of the epsilon's precision. They're
        # too variable for diff-based testing
        precision = str(math.floor(-math.log10(epsilon) - 3))
        fmt = "{0!s}\t{1:." + precision + "f}\t({2:." + precision + "f})"
    else:
        fmt = "{0!s}\t{1}\t({2})"

    for node in ordered:
        struct = ranker.findNode(node)
        if struct:
            print(fmt.format(node, ranker.getRank(node), abs(struct.pageRank_a - struct.pageRank_b)))

def countNodes(datafile):
    maxNodes = 0
    for line in datafile:
        maxNodes += 1

    datafile.seek(0)
    return maxNodes

def parseCSVLine(line):
    parts = line.split(',')

    left = parts[0].strip().strip('"')
    right = parts[2].strip().strip('"')
    return (left, right)

def parseSNAPLine(line):
    parts = line.split("\t")
    left = int(parts[0].strip())
    right = int(parts[1].strip())
    return (left, right)

def parse_file(fmt, datafile):
    if fmt == 'csv':
        parse = parseCSVLine
    else:
        parse = parseSNAPLine
    return (parse(line) for line in datafile if not line.startswith('#'))
