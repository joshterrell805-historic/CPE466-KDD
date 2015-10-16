//#include <string>
//#include <pthread.h>
//#include <semaphore.h>

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

typedef struct Graph {
  int iterationBatchSize;
  double dVal;
  double epsilonConverge;
  int maxNodeCount;
  int threadCount;

  int converged;
  int isSourceA;
  int iterationCount;
  double initPageRank;

  struct Node *nodes;
  struct Node *nextUnusedNode;
  Node *nextUnusedNodeForIteration;

  size_t *pthreads;
  void *iterationStartSem;
  void *iterationEndSem;
  void *getBatchLock;
} Graph;

// create an empty graph
// maxNodes: maximum number of nodes to be stored in the graph
// iterationBatchSize: batch size of how many nodes each thread gets at
//  a time when computing the page rank for a given iteration
// dVal: the "d" in the page rank equation specifying the probability of
//  going to a new page vs following a link
// epsilonConverged: init converged flag to true on every iteration
//  if any node has change in pageRank >= epsilonConverged, set converged
//  flag to false
Graph *newGraph(int maxNodes, int iterationBatchSize, double dVal,
    double epsilonConverge, int threadCount);

// destroy the graph
void cleanup(Graph*);

// add an edge to the graph from the node with `fromName` to `toName`
// creates missing nodes, if any
// return 0 if successful.
int addEdge(Graph*, char *fromName, char *toName);

// called by main (python) thread only
// compute one iteration
void computeIteration(Graph*);

Node *findNodeByName(Graph*, char *name);

/////////////////////// exposed for testing only ///////////////////////////////

// in this iteration, get `iterationBatchSize` of the next unprocessed elements
// and claim them as being processed (used in computePageRank)
// return count of 0 when there are no elements remaining
void getNextBatchInIteration(Graph*, Node **retStart, int *retCount);

// Keep chipping away at the remaining nodes in this iteration
// until all page ranks have been computed
void computePageRank(Graph*);

// Compute page rank for a node
// using pageRank_a to compute pageRank_b if isSourceA, else visa-versa
void computePageRankN(Graph*, Node* node);

////////////////////// exposed, but really shouldn't be used ///////////////////
Node *createNode(Graph*, char *name);
Node *findOrCreateNode(Graph*, char *name);
// add Node to end of LLNode linked list
void createLLNode(LLNode **llNode, Node *self);
void freeNodeData(Node *node);
void freeLLNodes(LLNode *llNode);
void threadMain(Graph*);
