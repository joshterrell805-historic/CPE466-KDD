
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
int threadCount = -1;

// this is some superrrr shinanigans, but cffi wont let us #include.
size_t *pthreads = 0;
void *iterationStartSem;
void *iterationEndSem;
void *getBatchLock;
int isSourceA = 0;

Node *createNode(char *name);
Node *findOrCreateNode(char *name);
// add Node to end of LLNode linked list
void createLLNode(LLNode **llNode, Node *self);
void freeNodeData(Node *node);
void freeLLNodes(LLNode *llNode);
void threadMain(void);

void init(int maxNodes, int batchSize, double d, double epsilon, int threads) {
  if (nodes) {
    printf("ERROR: already inited!\n");
    exit(-1);
  }

  nodes = malloc(sizeof(Node) * maxNodes);
  nextUnusedNode = nodes;
  maxNodeCount = maxNodes;
  iterationBatchSize = batchSize;
  nextUnusedNodeForIteration = 0;
  dVal = d;
  epsilonConverge = epsilon;
  iterationCount = 0;
  threadCount = threads;
  isSourceA = 0;

  // this is some superrrr shinanigans, but cffi wont let us #include.
  iterationStartSem = malloc(sizeof(size_t) * 4);
  iterationEndSem = malloc(sizeof(size_t) * 4);
  getBatchLock = malloc(sizeof(size_t) * 5);

  sem_init(iterationStartSem, 0, 0);
  sem_init(iterationEndSem, 0, 0);
  pthread_mutex_init(getBatchLock, 0);

  pthreads = malloc(sizeof(size_t) * threadCount);
  for (size_t* pth = pthreads; pth - pthreads < threadCount; ++pth) {
    int ret = pthread_create(pth, 0, threadMain, 0);
    if (ret) {
      printf("ERROR: failed to create thread! (%d)\n", ret);
      exit(-1);
    }
  }
}

void cleanup(void) {
  if (!nodes) {
    printf("ERROR: already cleaned up!\n");
    exit(-1);
  }

  for (Node *n = nodes; n != nextUnusedNode; ++n) {
    freeNodeData(n);
  }

  free(nodes);
  nodes = 0;

  // free the threads
  for (int i = 0; i < threadCount; ++i) {
    if (pthreads[i]) {
      if (pthread_cancel(pthreads[i])) {
        printf("ERROR: failed to kill thread\n");
        exit(-1);
      }
      pthread_join(pthreads[i], 0);
      pthreads[i] = 0;
    }
  } 
  free(pthreads);
  pthreads = 0;

  sem_destroy(iterationStartSem);
  sem_destroy(iterationEndSem);
  pthread_mutex_destroy(getBatchLock);
  free(iterationStartSem);
  free(iterationEndSem);
  free(getBatchLock);
  iterationStartSem = 0;
  iterationEndSem = 0;
  getBatchLock = 0;

  nextUnusedNode = 0;
  maxNodeCount = -1;
  iterationBatchSize = -1;
  nextUnusedNodeForIteration = 0;
  dVal = -1.0;
  converged = -1;
  epsilonConverge = -1.0;
  initPageRank = -1.0;
  iterationCount = 0;
  threadCount = -1;
  isSourceA = 0;
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

// called by main (python) thread only
void computeIteration(void) {
  converged = 1;
  nextUnusedNodeForIteration = nodes;
  initPageRank = (double)1 / (nextUnusedNode - nodes);
  ++iterationCount;
  isSourceA = !isSourceA;

  // unlock all the threads
  for (int i = 0; i < threadCount; ++i) {
    sem_post(iterationStartSem);
  }

  // wait for all threads to finish
  for (int i = 0; i < threadCount; ++i) {
    sem_wait(iterationEndSem);
  }

  if (converged) {
    // free the threads
    for (int i = 0; i < threadCount; ++i) {
      if (pthreads[i]) {
        if (pthread_cancel(pthreads[i])) {
          printf("ERROR: failed to kill thread\n");
          exit(-1);
        }
        pthread_join(pthreads[i], 0);
        pthreads[i] = 0;
      }
    } 
  }
}

void getNextBatchInIteration(Node **retStart, int *count) {
  pthread_mutex_lock(getBatchLock); 

  int a = iterationBatchSize;
  int b = nextUnusedNode - nextUnusedNodeForIteration;

  *count = a < b ? a : b;
  *retStart = nextUnusedNodeForIteration;
  nextUnusedNodeForIteration += *count;

  pthread_mutex_unlock(getBatchLock);
}

void computePageRank(void) {
  int length;
  Node *node;

  while (getNextBatchInIteration(&node, &length), length) {
    while (length--) {
      computePageRankN(node++);
    }
  }
}

void computePageRankN(Node *node) {
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

  nextUnusedNode->name = malloc(sizeof(char) * (strlen(name) + 1));
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

void threadMain(void) {
  while (1) {
    sem_wait(iterationStartSem);
    computePageRank();
    sem_post(iterationEndSem);
  }
}
