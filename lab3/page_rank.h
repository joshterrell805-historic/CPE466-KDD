//#include <string>
//#include <pthread.h>
//#include <semaphore.h>

typedef struct Node {
  // make sure to copy this on creation!
  // cffi will destroy its copy when the variable is garbage collected
  // http://cffi.readthedocs.org/en/latest/using.html
  // "the returned pointer object has ownership"
  char *name;
  unsigned int id;
  char active;
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
  int normalize;
  int maxNodeCount;
  int threadCount;

  int converged;
  int isSourceA;
  int iterationCount;
  double initPageRank;

  struct Node *nodes;
  struct Node *nextUnusedNode;
  Node *nextUnusedNodeForIteration;

  // cffi can't #include
  // These should really be pthread_t, sem_t, and pthread_mutex_t
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
    double epsilonConverge, int threadCount, int normalize);

// destroy the graph
void cleanup(Graph*);

// add an edge to the graph from the node with `fromName` to `toName`
// creates missing nodes, if any
// return 0 if successful.
int addEdge(Graph*, char *fromName, char *toName);

// Same as addEdge, but with ids instead
int addEdgeByIds(Graph* graph, unsigned int fromId, unsigned int toId);

// called by main (python) thread only
// compute one iteration
void computeIteration(Graph*);

Node *findNodeByName(Graph*, char *name);
Node *findNodeById(Graph*, int id);

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
Node *findOrCreateNodeById(Graph *graph, int id);
// add Node to end of LLNode linked list
void createLLNode(LLNode **llNode, Node *self);
void freeNodeData(Node *node);
void freeLLNodes(LLNode *llNode);
void *threadMain(Graph*);

/////////////////////// because we cant #include ///////////////////////////////

int sem_init(void *sem, int pshared, unsigned int value);
int sem_destroy(void *sem);
int sem_wait(void *sem);
int sem_post(void *sem);
int sem_getvalue(void *sem, int *sval);

int pthread_mutex_init(void *mutex, const void *mutexattr);
int pthread_mutex_lock(void *mutex);
int pthread_mutex_unlock(void *mutex);
int pthread_mutex_destroy(void *mutex);

int pthread_create(void *thread, void *attr,
    void *(*start_routine)(void *), void * arg);
int pthread_cancel(size_t thread);
int pthread_join(size_t th, void **thread_return);
