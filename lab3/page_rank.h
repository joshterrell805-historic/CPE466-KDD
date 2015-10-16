//#include <string>

// p(i) = (1-d) * 1 / |V| + d * SUM(1->k, 1/|Ojk| * p(jk)
// pageRank_i+1(node) = (1-d) / #nodeCount    +
//    d * SUM(1/outdegree(incommingNode) * pageRank_i(incommingNode))

typedef struct Node {
  // make sure to copy this on creation!
  // cffi will destroy its copy when the variable is garbage collected
  // http://cffi.readthedocs.org/en/latest/using.html
  // "the returned pointer object has ownership"
  char *name;
  double pageRank_a;
  double pageRank_b;
  int outDegree;
  // nodes that can reach this node directly
  struct LLNode *inNodes;
} Node;

// a wrapper around a node so we can create a linked list of nodes
typedef struct LLNode {
  struct Node *self;
  struct LLNode *next;
} LLNode;

// create an empty graph
// maxNodes: maximum number of nodes to be stored in the graph
// iterationBatchSize: batch size of how many nodes each thread gets at
//  a time when computing the page rank for a given iteration
// dVal: the "d" in the page rank equation specifying the probability of
//  going to a new page vs following a link
// epsilonConverged: init converged flag to true on every iteration
//  if any node has change in pageRank >= epsilonConverged, set converged
//  flag to false
void init(int maxNodes, int iterationBatchSize, double dVal,
    double epsilonConverge, int threadCount);

// destroy the graph
void cleanup(void);

// add an edge to the graph from the node with `fromName` to `toName`
// creates missing nodes, if any
// return 0 if successful.
int addEdge(char *fromName, char *toName);

// called by main (python) thread only
// compute one iteration
void computeIteration(void);

int hasConverged(void);

int getIterationCount(void);

Node *findNodeByName(char *name);

/////////////////////// exposed for testing only ///////////////////////////////

// in this iteration, get `iterationBatchSize` of the next unprocessed elements
// and claim them as being processed (used in computePageRank)
// return count of 0 when there are no elements remaining
void getNextBatchInIteration(Node **retStart, int *retCount);

// Compute page rank. Returns when this iteration has completed.
void computePageRank(void);

// compute page rank for a node
// using pageRank_a to compute pageRank_b if isSourceA, else visa-versa
void computePageRankN(Node* node);
