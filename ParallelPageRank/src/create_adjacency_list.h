#ifndef create_adjacency_list_h
#define create_adjacency_list_h

#include <sys/stat.h>
#include <sys/mman.h>
#include "hashtable.h"
#include <stdlib.h>

typedef struct AdjacencyList {
  MKL_INT *rowind;
  MKL_INT *colind;
  double  *values;
  MKL_INT nnz;
  MKL_INT numRows;
  // for unmapping AdjacencyList to original node numbers
  int *unmap;
} AdjacencyList;

typedef struct Graph {
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
  free(list->values); list->values = 0;
  free(list->rowind); list->rowind = 0;
  free(list->colind); list->colind = 0;
  free(list);
}

RawDataset read_dataset(char* filename);
void read_metadata(BuildState* buildState, Graph* graph);
void read_edge(BuildState*, AdjacencyList*);

AdjacencyList* create_adjacency_list(char* filename) {
  RawDataset dataset = read_dataset(filename);

  BuildState buildState;
  buildState.curr = dataset.data;

  Graph graph;
  read_metadata(&buildState, &graph);
  printf("Edges: %d, Nodes %d\n", graph.edges, graph.nodes);

  AdjacencyList *list = malloc(sizeof(AdjacencyList));
  list->values  = calloc(graph.edges, sizeof(double));
  list->rowind  = calloc(graph.edges, sizeof(MKL_INT));
  list->colind  = calloc(graph.edges, sizeof(MKL_INT));
  list->nnz     = graph.edges;
  list->numRows = graph.nodes;

  buildState.undense = createMap(3 * graph.nodes);
  buildState.unmap = calloc(graph.nodes, sizeof(int));
  buildState.denseId = 0;
  buildState.sparseEdgeIndex = 0;
  buildState.end = dataset.data + dataset.length;

  Benchmark benchSparse = startBenchmark(); 
  while(buildState.curr < buildState.end) {
    read_edge(&buildState, list);
  }
  printf("Done creating sparse matrix (%.2fms)\n", 
      msSinceBenchmark(&benchSparse));

  destroyMap(buildState.undense);
  buildState.undense = 0;

  if (munmap(dataset.data, dataset.length)) {
    printf("failed to free mmaped data.\n");
    exit(-1);
  }

  list->unmap = buildState.unmap;

  return list;
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

void read_metadata(BuildState* bs, Graph* graph) {
  int i;
  for (i = 0; i < 2; i++) {
    bs->curr = strchr(bs->curr, '\n');
    bs->curr++;
  }
  // Skip "# Nodes: "
  bs->curr += 9;

  char *nodesStr = bs->curr;

  bs->curr = strchr(bs->curr, ' ');
  *bs->curr = '\0';

  // Skip "\0Edges: "
  bs->curr += 8;
  char *edgesStr = bs->curr;
  bs->curr = strchr(bs->curr, '\r');
  *bs->curr = '\0';
  bs->curr += 2;

  bs->curr = strchr(bs->curr, '\n');
  bs->curr++;

  graph->nodes = atoi(nodesStr);
  graph->edges = atoi(edgesStr);
}

void read_edge(BuildState* bs, AdjacencyList* list) {
  int from, to;

  char *fromStr = bs->curr;
  bs->curr = strchr(bs->curr, '\t');
  *bs->curr = '\0';
  from = atoi(fromStr);

  bs->curr++;

  char *toStr = bs->curr;
  bs->curr = strchr(bs->curr, '\r');
  *bs->curr = '\0';
  to = atoi(toStr);

  bs->curr += 1;
  bs->curr = strchr(bs->curr, '\n');
  bs->curr += 1;

  int denseFrom;
  if (hasItem(bs->undense, from)) {
    denseFrom = getItem(bs->undense, from);
  } else {
    addItem(bs->undense, from, bs->denseId);
    denseFrom = bs->denseId;
    bs->unmap[bs->denseId] = from;
    bs->denseId++;
  }
    
  int denseTo;
  if (hasItem(bs->undense, to)) {
    denseTo = getItem(bs->undense, to);
  } else {
    addItem(bs->undense, to, bs->denseId);
    denseTo = bs->denseId;
    bs->unmap[bs->denseId] = to;
    bs->denseId++;
  }

  list->values[bs->sparseEdgeIndex] = 1;
  list->rowind[bs->sparseEdgeIndex] = denseFrom;
  list->colind[bs->sparseEdgeIndex] = denseTo;
  bs->sparseEdgeIndex++;
}

#endif
