//#include <string>

// p(i) = (1-d) * 1 / |V| + d * SUM(1->k, 1/|Ojk| * p(jk)
// pageRank_i+1(node) = (1-d) / #nodeCount    +
//    d * SUM(1/outdegree(incommingNode) * pageRank_i(incommingNode))

typedef struct {
  // make sure to copy this on creation!
  // cffi will destroy it's copy when the variable is garbage collected
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
typedef struct {
  struct Node *self;
  struct LLNode *next;
} LLNode;

void init(int);

void cleanup(void);

/**
 * return 0 if successful.
 */
int addEdge(char *fromName, char *toName);

/**
 * Compute page rank. Returns when this iteration has completed.
 */
void computePageRank(int sourceIsA);

int hasConverged(void);

Node *findNodeByName(char *name);
