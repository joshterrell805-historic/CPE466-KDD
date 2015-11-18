#include <stdio.h>
// Provides boolean definitions
#include <stdbool.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <fcntl.h>
#include <ctype.h>
#include <string.h>
//#include <bsd/stdlib.h>
#include "hashtable.h"
#include "getRank.h"
#include "benchmark.h"
#include "read_options.h"
#include "dump_adjacency_list.h"
#include "create_adjacency_list.h"

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
  int i;

  // read_options.h
  Options* options = create_options(argc, argv);
  if (options->grumpy) {
    printf("Get off my lawn!\n");
  }

  printf("Filename: %s\n", options->filename);

  AdjacencyList *list = create_adjacency_list(options->filename);

  //dump_adjacency_list(list->rowind, list->colind, list->values, list->nnz,
  //    "adjacency.csv");

  /*********** compute page rank ***********/

  makeP(list->values, list->rowind, list->numRows, list->colind, list->nnz,
      options->dP);
  Benchmark benchRank = startBenchmark();
  double *x = (double *) malloc(sizeof(double) * list->numRows);
  //#pragma omp parallel for simd
  for(i = 0; i < list->numRows; i++){
    x[i] = (double) 1 / list->numRows;
  }
  getRank(list->values, x, list->rowind, list->colind, list->numRows,
         list->nnz, options->tol, options->dP);

  printf("Done computing page rank (%.2fms)\n", msSinceBenchmark(&benchRank));
  free_options(options);

  /*********** sort page rank and print results ***********/

  pair *nodeStructs = (pair *) malloc(sizeof(pair) * list->numRows);
  //#pragma omp parallel for simd
  for (i = 0; i < list->numRows; i++) {
    nodeStructs[i].node = list->unmap[i];
    nodeStructs[i].score = x[i];
  }
  int (*compare) (const void *, const void*);
  compare = compar;
  Benchmark benchSort = startBenchmark();
  qsort(nodeStructs, list->numRows, sizeof(pair), compare);
  printf("Done Sorting Output(%.2fms)\n", msSinceBenchmark(&benchSort));

  FILE *fid = fopen("output.out", "w");
  for (i = 0; i < list->numRows; i++) {
    fprintf(fid, "Node %i ranked %f\n", nodeStructs[i].node,
        nodeStructs[i].score);
  }
  fclose(fid);
   free(nodeStructs);
  free_adjacency_list(list);
  free(x);
  return 0;
}
