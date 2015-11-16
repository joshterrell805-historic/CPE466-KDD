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
#include "mkl.h"
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
  } else {
    printf("Hello World!\n");
  }

  printf("Filename: %s\n", options->filename);

  AdjacencyList *list = create_adjacency_list(options->filename);

  //dump_adjacency_list(list->rowind, list->colind, list->values, list->nnz,
  //    "adjacency.csv");

  /*********** compute page rank ***********/

  makeP(list->values, list->rowind, &list->numRows, list->colind, &list->nnz,
      options->dP);
  double *x = (double *) malloc(sizeof(double) * list->numRows);
  //#pragma omp parallel for simd
  for(i = 0; i < list->numRows; i++){
    x[i] = (double) 1 / list->numRows;
  }
  getRank(list->values, x, list->rowind, list->colind, &list->numRows,
      &list->nnz, options->tol, options->dP);
  printf("result: it did things...\n");
  
  //for(i = 0; i < list->numRows; i++){
  //   printf("x[%d] = %lf\n", i+1, x[i]);
  //}

  /*********** sort page rank and print results ***********/

  pair *nodeStructs = (pair *) malloc(sizeof(pair) * list->numRows);
  //#pragma omp parallel for simd
  for (i = 0; i < list->numRows; i++) {
    nodeStructs[i].node = list->unmap[i];
    nodeStructs[i].score = x[i];
  }
  int (*compare) (const void *, const void*);
  compare = compar;
  qsort(nodeStructs, list->numRows, sizeof(pair), compare);

  FILE *fid = fopen("output.out", "w");
  for (i = 0; i < list->numRows; i++) {
    fprintf(fid, "Node %i ranked %f\n", nodeStructs[i].node,
        nodeStructs[i].score);
  }
  fclose(fid);

  free_adjacency_list(list);
  free_options(options);
  return 0;
}
