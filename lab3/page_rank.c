int converged = -1;
Node *nodes = 0;
Node *nextUnusedNode = 0;
int maxNodeCount = -1;
int iterationBatchSize = -1;
Node *nextUnusedNodeForIteration = 0;
double dVal = -1.0;
double epsilonConverge = -1.0;
// the initial page rank
// also used in computePageRank for prob of random link
double initPageRank = -1.0;
int iterationCount = 0;

Node *createNode(char *name);
Node *findOrCreateNode(char *name);
// add Node to end of LLNode linked list
void createLLNode(LLNode **llNode, Node *self);
void freeNodeData(Node *node);
void freeLLNodes(LLNode *llNode);

void init(int maxNodes, int batchSize, double d, double epsilon) {
  if (nodes) {
    cleanup();
  }

  nodes = malloc(sizeof(Node) * maxNodes);
  nextUnusedNode = nodes;
  maxNodeCount = maxNodes;
  iterationBatchSize = batchSize;
  nextUnusedNodeForIteration = 0;
  dVal = d;
  epsilonConverge = epsilon;
  iterationCount = 0;
}

void cleanup(void) {
  for (Node *n = nodes; n != nextUnusedNode; ++n) {
    freeNodeData(n);
  }

  free(nodes);
  nodes = 0;
  nextUnusedNode = 0;
  maxNodeCount = -1;
  iterationBatchSize = -1;
  nextUnusedNodeForIteration = 0;
  dVal = -1.0;
  converged = -1;
  epsilonConverge = -1.0;
  initPageRank = -1.0;
  iterationCount = 0;
}

int addEdge(char *fromName, char *toName) {
  Node* from = findOrCreateNode(fromName);
  Node* to = findOrCreateNode(toName);

  if (!(from && to)) {
    return -1;
  }

  ++from->outDegree;
  createLLNode(&to->inNodes, from);

  return 0;
}

void startIteration(void) {
  converged = 1;
  nextUnusedNodeForIteration = nodes;
  initPageRank = (double)1 / (nextUnusedNode - nodes);
  ++iterationCount;
}

void getNextBatchInIteration(Node **retStart, int *count) {
  int a = iterationBatchSize;
  int b = nextUnusedNode - nextUnusedNodeForIteration;

  *count = a < b ? a : b;
  *retStart = nextUnusedNodeForIteration;
  nextUnusedNodeForIteration += *count;
}

void computePageRank(int isSourceA) {
  int length;
  Node *node;

  while (getNextBatchInIteration(&node, &length), length) {
    while (length--) {
      computePageRankN(node++, isSourceA);
    }
  }
}

void computePageRankN(Node *node, int isSourceA) {
  if (iterationCount == 1) {
    node->pageRank_b = node->pageRank_a = initPageRank;
  }

  double *dstRank = isSourceA ? &node->pageRank_b : &node->pageRank_a;
  LLNode *llNode = node->inNodes;
  *dstRank = 0.0;

  while (llNode) {
    *dstRank +=
      (isSourceA ? llNode->self->pageRank_a : llNode->self->pageRank_b) /
      llNode->self->outDegree;
    llNode = llNode->next;
  }
  *dstRank = *dstRank * dVal + (1 - dVal) * initPageRank;

  // thread-safe! :)
  if (converged &&
      fabs(node->pageRank_b - node->pageRank_a) >= epsilonConverge) {
    converged = 0;
  }
}


int hasConverged(void) {
  return converged;
}

int getIterationCount(void) {
  return iterationCount;
}

Node *findNodeByName(char *name) {
  for (Node *n = nodes; n != nextUnusedNode; ++n) {
    if (strcmp(n->name, name) == 0) {
      return n;
    }
  }

  return 0;
}


// ----------- helper functions, not exposed to cffi -----------------

Node *createNode(char *name) {
  if (nextUnusedNode - nodes == maxNodeCount) {
    return 0;
  }

  nextUnusedNode->name = malloc(sizeof(char) * strlen(name));
  strcpy(nextUnusedNode->name, name);
  nextUnusedNode->pageRank_a = 0.0;
  nextUnusedNode->pageRank_b = 0.0;
  nextUnusedNode->outDegree = 0;
  nextUnusedNode->inNodes = 0;

  return nextUnusedNode++;
}

Node *findOrCreateNode(char *name) {
  Node *n = findNodeByName(name);

  if (!n) {
    n = createNode(name);
  }

  return n;
}

void createLLNode(LLNode **llNode, Node *self) {
  while (*llNode) {
    llNode = &(*llNode)->next;
  }
  *llNode = malloc(sizeof(LLNode));
  (*llNode)->self = self;
  (*llNode)->next = 0;
}

void freeNodeData(Node *node) {
  if (node->name) {
    free(node->name);
    node->name = 0;
  }

  free(node->inNodes);
}

void freeLLNodes(LLNode *llNode) {
  // don't free llNode->self, these are freed in freeNodeData...
  LLNode *last, *next;

  if (llNode) {
    last = llNode;

    while ((next = last->next)) {
      free(last);
      last = next;
    }

    free(last);
  }
}
