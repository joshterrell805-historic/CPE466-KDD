#include <stdio.h>
// Provides boolean definitions
#include <stdbool.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <ctype.h>
#include <string.h>
//#include <bsd/stdlib.h>
#include "hashtable.h"
#include "mkl.h"
#include "getRank.h"
#include "benchmark.h"
#include "read_options.h"
#include "dump_adjacency_list.h"

typedef struct {
  int node;
  double score;
} pair;
int compar(const void *left, const void *right) {
  double diff = ((pair *) right)->score - ((pair *) left)->score;
  if (diff < 0) {
    return -1;
  } else {
    return 1;
  }
}

int main(int argc, char **argv) {
  // read_options.h
  Options* options = create_options(argc, argv);
  if (options->grumpy) {
    printf("Get off my lawn!\n");
  } else {
    printf("Hello World!\n");
  }

  printf("Filename: %s\n", options->filename);

  /*********** create adjacency list ***********/

  struct stat finfo;
  int from, to , i;
  stat(options->filename, &finfo);
  int fd = open(options->filename, O_RDONLY);
  Benchmark benchMmap = startBenchmark(); 
  char *data = (char *) mmap(NULL, finfo.st_size + 1, PROT_READ | PROT_WRITE, MAP_PRIVATE, fd, 0);
  data[finfo.st_size] = '\0';
  printf("Data loaded (%.2fms)\n", msSinceBenchmark(&benchMmap));

  char *curr = data;
  for (i = 0; i < 2; i++) {
    curr = strchr(curr, '\n');
    curr++;
  }
  // Skip "# Nodes: "
  curr += 9;

  char *nodesStr = curr;

  curr = strchr(curr, ' ');
  *curr = '\0';

  // Skip "\0Edges: "
  curr += 8;
  char *edgesStr = curr;
  curr = strchr(curr, '\r');
  *curr = '\0';
  curr += 2;

  curr = strchr(curr, '\n');
  curr++;

  int nodes = atoi(nodesStr);
  int edges = atoi(edgesStr);
  printf("edges: %d, nodes %d\n", edges, nodes);

  double *values = calloc(edges, sizeof(double));
  MKL_INT *rowind = calloc(edges, sizeof(MKL_INT));
  MKL_INT *colind = calloc(edges, sizeof(MKL_INT));
  MKL_INT nnz = edges;
  MKL_INT numRows = nodes;
  int numNodes = nodes * nodes;

  map *undense = createMap(3 * nodes);
  int *unmap = calloc(nodes, sizeof(int));
  unsigned int denseId = 0;

  unsigned int sparseEdgeIndex = 0;
  // Is this faster with ints?

  char *end = data + finfo.st_size;
  Benchmark benchSparse = startBenchmark(); 
  while(curr < end) {
    /* printf("From %i to %i\n", from, to); */
    char *fromStr = curr;
    curr = strchr(curr, '\t');
    *curr = '\0';
    from = atoi(fromStr);

    curr++;

    char *toStr = curr;
    curr = strchr(curr, '\r');
    *curr = '\0';
    to = atoi(toStr);

    curr += 1;
    curr = strchr(curr, '\n');
    curr += 1;

    int denseFrom;
    if (hasItem(undense, from)) {
      denseFrom = getItem(undense, from);
    } else {
      addItem(undense, from, denseId);
      denseFrom = denseId;
      unmap[denseId] = from;
      denseId++;
    }
      
    int denseTo;
    if (hasItem(undense, to)) {
      denseTo = getItem(undense, to);
    } else {
      addItem(undense, to, denseId);
      denseTo = denseId;
      unmap[denseId] = to;
      denseId++;
    }

    // printf("From %i to %i first time\n", from, to);

    values[sparseEdgeIndex] = 1;
    rowind[sparseEdgeIndex] = denseFrom;
    colind[sparseEdgeIndex] = denseTo;
    sparseEdgeIndex++;
  }

  printf("Done creating sparse matrix (%.2fms)\n", 
      msSinceBenchmark(&benchSparse));

  //dump_adjacency_list(rowind, colind, values, nnz, "adjacency.csv");

  // for ( i = 0; i < edges; i++) {
  //     printf("From %i to %i\n", unmap[rowind[i]], unmap[colind[i]]);
  //}

  /*********** compute page rank ***********/

  makeP(values, rowind, &numRows, colind, &nnz, options->dP);
  double *x = (double *) malloc(sizeof(double) * numRows);
  //#pragma omp parallel for simd
  for(i = 0; i<numRows; i++){
    x[i] = (double) 1/numRows;
  }
  getRank(values, x, rowind, colind, &numRows, &nnz, options->tol, options->dP);
  printf("result: it did things...\n");
  
  //for(i = 0; i<numRows; i++){
  //   printf("x[%d] = %lf\n", i+1, x[i]);
  //}

  /*********** sort page rank and print results ***********/

  pair *nodeStructs = (pair *) malloc(sizeof(pair) * numRows);
  //#pragma omp parallel for simd
  for (i = 0; i < numRows; i++) {
    nodeStructs[i].node = unmap[i];
    nodeStructs[i].score = x[i];
  }
  int (*compare) (const void *, const void*);
  compare = compar;
  qsort(nodeStructs, numRows, sizeof(pair), compare);

  FILE *fid = fopen("output.out", "w");
  for (i = 0; i < numRows; i++) {
    fprintf(fid, "Node %i ranked %f\n", nodeStructs[i].node, nodeStructs[i].score);
  }
  fclose(fid);

  free_options(options);
  return 0;
}
