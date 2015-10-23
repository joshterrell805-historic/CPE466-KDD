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
@click.argument('datafile', type=click.File('r'))
@click.option('--batchsize', help='On each iteration, each thread claims `batchsize` nodes to compute pagerank for. A batchsize of too small, and threads may constantly be sychronizing around a mutex. Too large, and a few threads may end up doing most of the work while others sit idly.', default=100)
@click.option('--fmt', type=click.Choice(['csv', 'snap']), default='csv')
@click.option('--scale/--no-scale', help='Scales epsilon comparision and printed page ranks by size of graph.', default=True)
@click.option('--weighted', help='Specify flag to indicate graph is weighted.',
        is_flag=True)
@click.option('--showweights/--no-showweights', help='Specify flag to show weights gathered',
              default=False)
def rank(epsilon, maxiterations, dval, threads, datafile, limit,
         batchsize, fmt, scale, weighted, showweights):
    # Create Ranker

    # Time loading the data into the graph
    start = time.clock()
    maxNodes = countNodes(datafile)
    print("Nodes: {0}".format(maxNodes))
    ranker = PageRank(maxNodes, epsilon, dval, threads, batchsize, scale,
            weighted)
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
        precision = math.floor(-math.log10(epsilon) - 3)
        fmt = "{0!s}\t{1:." + str(precision) + "f}\t({2:." + str(precision) + "f})"
    else:
        fmt = "{0!s}\t{1}\t({2})"

    thesum = 0
    for node in ordered:
        struct = ranker.findNode(node)
        if struct:
            delta = abs(struct.pageRank_a - struct.pageRank_b)
            if scale:
                delta = delta * ranker.graph.weightedSize
            print(fmt.format(node, ranker.getRank(node), delta))
            thesum += ranker.getRank(node)

    # print('sum: %s\navg %s' % (thesum, thesum / len(ordered)))

    if (showweights):
        for node in ranker.getTotalWeightOrderedNodes(nodes):
            print("{0!s}\tweight: {1}".format(node, ranker.getTotalWeight(node)))

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
    wA = int(parts[1].strip())
    wB = int(parts[3].strip())
    weight = wA - wB

    return (left, right, weight)

def parseSNAPLine(line):
    parts = line.split()
    left = int(parts[0])
    right = int(parts[1])
    if (len(parts) > 2):
        # Handle Slashdot data
        weight = -int(parts[2])
    else:
        weight = float('NaN')

    return (left, right, weight)

def parse_file(fmt, datafile):
    if fmt == 'csv':
        parse = parseCSVLine
    else:
        parse = parseSNAPLine
    return (parse(line) for line in datafile if not line.startswith('#'))
