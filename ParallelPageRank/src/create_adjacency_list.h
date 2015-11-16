#ifndef create_adjacency_list_h
#define create_adjacency_list_h

#include <sys/stat.h>
#include <sys/mman.h>
#include "hashtable.h"

typedef struct AdjacencyList {
  MKL_INT *rowind;
  MKL_INT *colind;
  MKL_INT nnz;
  MKL_INT numRows;
  double* values;
  int* unmap;
} AdjacencyList;

typedef struct Graph {
  AdjacencyList *adj_list;
  int nodes;
  int edges;
} Graph;


typedef struct RawDataset {
  char* data;
  off_t length;
} RawDataset;

typedef struct BuildState {
  char* curr;
  char* end;
  map* undense;
  int* unmap;
  unsigned int denseId;
  unsigned int sparseEdgeIndex;
} BuildState;

void free_adjacency_list(AdjacencyList *list) {
  free(list->unmap); list->unmap = 0;
  free(list);
}

RawDataset read_dataset(char* filename);
void read_metadata(BuildState* buildState, Graph* graph);
void read_edge(BuildState*, AdjacencyList*);

AdjacencyList* create_adjacency_list(char* filename) {
  Graph graph;
  graph.adj_list = malloc(sizeof(AdjacencyList));

  RawDataset ds = read_dataset(filename);

  BuildState buildState;
  buildState.curr = ds.data;

  read_metadata(&buildState, &graph);
  printf("Edges: %d, Nodes %d\n", graph.edges, graph.nodes);

  graph.adj_list->values = calloc(graph.edges, sizeof(double));
  graph.adj_list->rowind = calloc(graph.edges, sizeof(MKL_INT));
  graph.adj_list->colind = calloc(graph.edges, sizeof(MKL_INT));
  graph.adj_list->nnz = graph.edges;
  graph.adj_list->numRows = graph.nodes;

  buildState.undense = createMap(3 * graph.nodes);
  buildState.unmap = calloc(graph.nodes, sizeof(int));
  buildState.denseId = 0;
  buildState.sparseEdgeIndex = 0;
  buildState.end = ds.data + ds.length;

  Benchmark benchSparse = startBenchmark(); 
  while(buildState.curr < buildState.end) {
    read_edge(&buildState, graph.adj_list);
  }

  printf("Done creating sparse matrix (%.2fms)\n", 
      msSinceBenchmark(&benchSparse));

  free(buildState.undense);
  graph.adj_list->unmap = buildState.unmap;

  return graph.adj_list;
}

RawDataset read_dataset(char* filename) {
  RawDataset ds;
  struct stat finfo;
  stat(filename, &finfo);
  int fd = open(filename, O_RDONLY);

  Benchmark benchMmap = startBenchmark(); 
  ds.data = mmap(NULL, finfo.st_size + 1, PROT_READ | PROT_WRITE,
      MAP_PRIVATE, fd, 0);
  ds.data[finfo.st_size] = '\0';
  printf("Data loaded (%.2fms)\n", msSinceBenchmark(&benchMmap));

  ds.length = finfo.st_size;

  close(fd);

  return ds;
}

void read_metadata(BuildState* buildState, Graph* graph) {
  int i;
  for (i = 0; i < 2; i++) {
    buildState->curr = strchr(buildState->curr, '\n');
    buildState->curr++;
  }
  // Skip "# Nodes: "
  buildState->curr += 9;

  char *nodesStr = buildState->curr;

  buildState->curr = strchr(buildState->curr, ' ');
  *buildState->curr = '\0';

  // Skip "\0Edges: "
  buildState->curr += 8;
  char *edgesStr = buildState->curr;
  buildState->curr = strchr(buildState->curr, '\r');
  *buildState->curr = '\0';
  buildState->curr += 2;

  buildState->curr = strchr(buildState->curr, '\n');
  buildState->curr++;

  graph->nodes = atoi(nodesStr);
  graph->edges = atoi(edgesStr);
}

void read_edge(BuildState* buildState, AdjacencyList* list) {
  int from, to;

  char *fromStr = buildState->curr;
  buildState->curr = strchr(buildState->curr, '\t');
  *buildState->curr = '\0';
  from = atoi(fromStr);

  buildState->curr++;

  char *toStr = buildState->curr;
  buildState->curr = strchr(buildState->curr, '\r');
  *buildState->curr = '\0';
  to = atoi(toStr);

  buildState->curr += 1;
  buildState->curr = strchr(buildState->curr, '\n');
  buildState->curr += 1;

  int denseFrom;
  if (hasItem(buildState->undense, from)) {
    denseFrom = getItem(buildState->undense, from);
  } else {
    addItem(buildState->undense, from, buildState->denseId);
    denseFrom = buildState->denseId;
    buildState->unmap[buildState->denseId] = from;
    buildState->denseId++;
  }
    
  int denseTo;
  if (hasItem(buildState->undense, to)) {
    denseTo = getItem(buildState->undense, to);
  } else {
    addItem(buildState->undense, to, buildState->denseId);
    denseTo = buildState->denseId;
    buildState->unmap[buildState->denseId] = to;
    buildState->denseId++;
  }

  list->values[buildState->sparseEdgeIndex] = 1;
  list->rowind[buildState->sparseEdgeIndex] = denseFrom;
  list->colind[buildState->sparseEdgeIndex] = denseTo;
  buildState->sparseEdgeIndex++;
}

#endif
