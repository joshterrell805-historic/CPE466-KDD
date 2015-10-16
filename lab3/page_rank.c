Graph *newGraph(int maxNodeCount, int iterationBatchSize, double dVal,
    double epsilonConverge, int threadCount) {
  Graph *graph = calloc(sizeof(Graph), 1);

  graph->nodes = calloc(sizeof(Node), maxNodeCount);
  graph->nextUnusedNode = graph->nodes;
  graph->maxNodeCount = maxNodeCount;
  graph->iterationBatchSize = iterationBatchSize;
  graph->dVal = dVal;
  graph->epsilonConverge = epsilonConverge;
  graph->threadCount = threadCount;

  graph->iterationStartSem = malloc(sizeof(size_t) * 4);
  graph->iterationEndSem = malloc(sizeof(size_t) * 4);
  graph->getBatchLock = malloc(sizeof(size_t) * 5);

  sem_init(graph->iterationStartSem, 0, 0);
  sem_init(graph->iterationEndSem, 0, 0);
  pthread_mutex_init(graph->getBatchLock, 0);

  graph->pthreads = malloc(sizeof(size_t) * threadCount);

  for (int i = 0; i < threadCount; ++i) {
    int ret = pthread_create(graph->pthreads+i, 0, threadMain, graph);
    if (ret) {
      printf("ERROR: failed to create thread! (%d)\n", ret);
      exit(-1);
    }
  }

  return graph;
}

void cleanup(Graph *graph) {
  if (!graph->nodes) {
    printf("ERROR: already cleaned up!\n");
    exit(-1);
  }

  for (Node *n = graph->nodes; n != graph->nextUnusedNode; ++n) {
    freeNodeData(n);
  }

  free(graph->nodes);
  graph->nodes = 0;

  // kill the threads
  for (int i = 0; i < graph->threadCount; ++i) {
    if (graph->pthreads[i]) {
      if (pthread_cancel(graph->pthreads[i])) {
        printf("ERROR: failed to kill thread\n");
        exit(-1);
      }
      pthread_join(graph->pthreads[i], 0);
      graph->pthreads[i] = 0;
    }
  } 
  free(graph->pthreads);
  graph->pthreads = 0;

  sem_destroy(graph->iterationStartSem);
  sem_destroy(graph->iterationEndSem);
  pthread_mutex_destroy(graph->getBatchLock);

  free(graph);
}

int addEdge(Graph* graph, char *fromName, char *toName) {
  Node* from = findOrCreateNode(graph, fromName);
  Node* to = findOrCreateNode(graph, toName);

  if (!(from && to)) {
    return -1;
  }

  ++from->outDegree;
  createLLNode(&to->inNodes, from);

  return 0;
}

// called by main (python) thread only
void computeIteration(Graph *graph) {
  graph->converged = 1;
  graph->nextUnusedNodeForIteration = graph->nodes;
  graph->initPageRank = 1.0 / (graph->nextUnusedNode - graph->nodes);
  ++graph->iterationCount;
  graph->isSourceA = !graph->isSourceA;

  // unlock all the threads so they can start computing
  for (int i = 0; i < graph->threadCount; ++i) {
    sem_post(graph->iterationStartSem);
  }

  // wait for all threads to finish computing
  for (int i = 0; i < graph->threadCount; ++i) {
    sem_wait(graph->iterationEndSem);
  }
}

void getNextBatchInIteration(Graph *graph, Node **retStart, int *count) {
  pthread_mutex_lock(graph->getBatchLock); 

  int a = graph->iterationBatchSize;
  int b = graph->nextUnusedNode - graph->nextUnusedNodeForIteration;

  *count = a < b ? a : b;
  *retStart = graph->nextUnusedNodeForIteration;
  graph->nextUnusedNodeForIteration += *count;

  pthread_mutex_unlock(graph->getBatchLock);
}

void computePageRank(Graph *graph) {
  int length;
  Node *node;

  while (getNextBatchInIteration(graph, &node, &length), length) {
    while (length--) {
      computePageRankN(graph, node++);
    }
  }
}

// p(i) = (1-d) * 1 / |V| + d * SUM(1->k, 1/|Ojk| * p(jk)
// pageRank_i+1(node) = (1-d) / #nodeCount    +
//    d * SUM(1/outdegree(incommingNode) * pageRank_i(incommingNode))
void computePageRankN(Graph* graph, Node *node) {
  if (graph->iterationCount == 1) {
    node->pageRank_b = node->pageRank_a = graph->initPageRank;
  }

  double *dstRank = graph->isSourceA ? &node->pageRank_b : &node->pageRank_a;
  LLNode *llNode = node->inNodes;
  *dstRank = 0.0;

  while (llNode) {
    *dstRank +=
      (graph->isSourceA ? llNode->self->pageRank_a : llNode->self->pageRank_b) /
      llNode->self->outDegree;
    llNode = llNode->next;
  }
  *dstRank = *dstRank * graph->dVal + (1 - graph->dVal) * graph->initPageRank;

  // thread-safe! :)
  if (graph->converged &&
      fabs(node->pageRank_b - node->pageRank_a) >= graph->epsilonConverge) {
    graph->converged = 0;
  }
}

Node *findNodeByName(Graph *graph, char *name) {
  for (Node *n = graph->nodes; n != graph->nextUnusedNode; ++n) {
    if (strcmp(n->name, name) == 0) {
      return n;
    }
  }

  return 0;
}


// ----------- helper functions, not exposed to cffi -----------------

Node *createNode(Graph *graph, char *name) {
  if (graph->nextUnusedNode - graph->nodes == graph->maxNodeCount) {
    return 0;
  }

  graph->nextUnusedNode->name = calloc(sizeof(char), strlen(name) + 1);
  strcpy(graph->nextUnusedNode->name, name);

  return graph->nextUnusedNode++;
}

Node *findOrCreateNode(Graph *graph, char *name) {
  Node *n = findNodeByName(graph, name);

  if (!n) {
    n = createNode(graph, name);
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

  freeLLNodes(node->inNodes);
  node->inNodes = 0;
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

void threadMain(Graph *graph) {
  while (1) {
    sem_wait(graph->iterationStartSem);
    computePageRank(graph);
    sem_post(graph->iterationEndSem);
  }
}
