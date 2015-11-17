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

typedef struct AdjacencyCell {
  int row;
  int col;
  // all values have 1.0 to start with
  // double value;
} AdjacencyCell;

typedef struct RawDataset {
  char* data;
  off_t length;
} RawDataset;

typedef struct BuildState {
  AdjacencyCell *unsortedAdjList;
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
void read_edge(BuildState*);
AdjacencyList* actually_create_adj_list(BuildState*, Graph*);
void sort_adjacency_list(AdjacencyCell* list, int edges);

AdjacencyList* create_adjacency_list(char* filename) {
  RawDataset dataset = read_dataset(filename);

  BuildState buildState;
  buildState.curr = dataset.data;

  Graph graph;
  read_metadata(&buildState, &graph);
  printf("Edges: %d, Nodes %d\n", graph.edges, graph.nodes);

  buildState.undense = createMap(3 * graph.nodes);
  buildState.unmap = (int*)calloc(graph.nodes, sizeof(int));
  buildState.denseId = 0;
  buildState.sparseEdgeIndex = 0;
  buildState.end = dataset.data + dataset.length;
  buildState.unsortedAdjList = (AdjacencyCell*)malloc(graph.edges * sizeof(AdjacencyCell));

  Benchmark benchSparse = startBenchmark(); 
  while(buildState.curr < buildState.end) {
    read_edge(&buildState);
  }
  printf("Done creating sparse matrix (%.2fms)\n", 
      msSinceBenchmark(&benchSparse));

  AdjacencyList *list = actually_create_adj_list(&buildState, &graph);

  destroyMap(buildState.undense); buildState.undense = 0;
  free(buildState.unsortedAdjList); buildState.unsortedAdjList = 0;
  // don't free buildState.unmap, adj list owns it now.

  if (munmap(dataset.data, dataset.length)) {
    printf("Failed to free mmaped data.\n");
    exit(-1);
  }

  return list;
}

AdjacencyList* actually_create_adj_list(BuildState* bs, Graph* g) {
  sort_adjacency_list(bs->unsortedAdjList, g->edges);

  AdjacencyList *list = (AdjacencyList*)malloc(sizeof(AdjacencyList));
  list->values  = (double*)calloc(g->edges, sizeof(double));
  list->rowind  = (int*)calloc(g->edges, sizeof(MKL_INT));
  list->colind  = (int*)calloc(g->edges, sizeof(MKL_INT));
  list->nnz     = g->edges;
  list->numRows = g->nodes;

  if (bs->sparseEdgeIndex != g->edges) {
    printf("sparseEdgeCount(%d) != graph.edges(%d)\n", bs->sparseEdgeIndex + 1,
        g->edges);
    exit(-1);
  }
   int i;
  for (i = 0; i < g->edges; ++i) {
    list->values[i] = 1.0;
    list->rowind[i] = bs->unsortedAdjList[i].row;
    list->colind[i] = bs->unsortedAdjList[i].col;
  }

  return list;
}

RawDataset read_dataset(char* filename) {
  RawDataset ds;
  struct stat finfo;
  stat(filename, &finfo);
  int fd = open(filename, O_RDONLY);

  Benchmark benchMmap = startBenchmark(); 
  ds.data = (char*)mmap(NULL, finfo.st_size + 1, PROT_READ | PROT_WRITE,
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

void read_edge(BuildState* bs) {
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

  bs->unsortedAdjList[bs->sparseEdgeIndex].row = denseFrom;
  bs->unsortedAdjList[bs->sparseEdgeIndex].col = denseTo;
  //printf("%d,", bs->unsortedAdjList[bs->sparseEdgeIndex].col);
  ++bs->sparseEdgeIndex;
}

int compare_AdjacencyCell(AdjacencyCell *left, AdjacencyCell *right) {
  if (right->row < left->row) {
    return 1;
  } else if (right->row > left->row) {
    return -1;
  } else {
    if (right->col < left->col) {
      return 1;
    } else if (right->col > left->col) {
      return -1;
    } else {
      return 0;
    }
  }
}

void sort_adjacency_list(AdjacencyCell* list, int edges) {
  qsort(list, edges, sizeof(AdjacencyCell),
      (int (*) (const void*, const void*))compare_AdjacencyCell);
}

#endif
