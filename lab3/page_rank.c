int converged = 0;
Node *nodes = 0;
Node *nextUnusedNode = 0;
int maxNodeCount = -1;

Node *createNode(char *name);
Node *findOrCreateNode(char *name);
// add Node to end of LLNode linked list
void createLLNode(LLNode **llNode, Node *self);
void freeNodeData(Node *node);
void freeLLNodes(LLNode *llNode);

void init(int maxNodes) {
  if (nodes) {
    cleanup();
  }

  nodes = malloc(sizeof(Node) * maxNodes);
  nextUnusedNode = nodes;
  maxNodeCount = maxNodes;

  converged = 0;
}

void cleanup(void) {
  for (Node *n = nodes; n != nextUnusedNode; ++n) {
    freeNodeData(n);
  }

  free(nodes);
  nodes = 0;
  nextUnusedNode = 0;
  maxNodeCount = -1;
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

void computePageRank(int sourceIsA) {
  if (sourceIsA) {
    converged = sourceIsA;
  }
}


int hasConverged(void) {
  return converged;
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
