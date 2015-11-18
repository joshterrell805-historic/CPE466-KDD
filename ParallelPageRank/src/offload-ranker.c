#include <stdio.h>
// Provides boolean definitions
#include <stdbool.h>
#include <stdlib.h>
#include <unistd.h>
#include <getopt.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <ctype.h>
#include <string.h>
//#include <bsd/stdlib.h>
#include "hashtable.h"
#include "mkl.h"
#include "offload.h"
#include <sys/time.h>

typedef struct {
  int node;
  double score;
} pair;
int compar(const void *left, const void *right) {
  double diff = ((pair *) right)->score - ((pair *) left)->score;
  if (diff == 0) {
    // Make diff non-zero
    diff = ((pair *) left)->node - ((pair *) right)->node;
  }

  if (diff < 0) {
    return -1;
  } else {
    return 1;
  }
}

typedef struct timeval Benchmark;

Benchmark startBenchmark() {
  struct timeval time_start;
  gettimeofday(&time_start,NULL);
  return time_start;
}

float msSinceBenchmark(Benchmark *from) {
  struct timeval to;
  gettimeofday(&to,NULL);
  return 1000 * (to.tv_sec - from->tv_sec) + (to.tv_usec - from->tv_usec) / 1000.0;
}

int main(int argc, char **argv) {
  bool grumpy = false;
  /* Derived from getopt docs: */
  int c;
  int digit_optind = 0;
   double dP = .95, tol = .0001;
  while (1) {
    int this_option_optind = optind ? optind : 1;
    int option_index = 0;
    static struct option long_options[] = {
      {"grumpy", no_argument, 0, 'g'},
      {0,        0,           0, 0}
    };

    c = getopt_long(argc, argv, "g",
                    long_options, &option_index);
    if (c == -1) {
      break;
    }

    switch (c) {
    case 'g':
      grumpy = true;
      break;
    }
  }

  if ((argc - optind) != 1) {
    printf("Missing required filename: pageRank <filename>\n");
    exit(2);
  }

  char *filename = argv[optind];

  if (grumpy) {
    printf("Get off my lawn!\n");
  } else {
  }

  printf("Filename: %s\n", filename);

  struct stat finfo;
  int from, to , i;
  stat(filename, &finfo);
  int fd = open(filename, O_RDONLY);
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

    curr += 2;

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

//  for ( i = 0; i < edges; i++) {
 //     printf("From %i to %i\n", unmap[rowind[i]], unmap[colind[i]]);
 // }
#pragma offload target(mic)\
   in(numRows, nnz)\
   inout(values [0:nnz])\
   in(rowind [0:nnz])\
   in(colind [0:nnz])
   makeP(values, rowind, &numRows, colind, &nnz, dP);
   double *x = (double *) malloc(sizeof(double) * numRows);
   //#pragma omp parallel for simd
   for(i = 0; i<numRows; i++){
      x[i] = (double) 1/numRows;
   }
  Benchmark benchRank = startBenchmark();
#pragma offload target(mic)\
   in(numRows, nnz, tol)\  
   in(values [0:nnz])\
   in(x [0:numRows])\
   out(x [0:numRows])\
   in(rowind [0:nnz])\
   in(colind [0:nnz])
   getRank(values, x, rowind, colind, &numRows, &nnz, tol, dP);
   printf("Done computing page rank in (%.2fms)\n",
       msSinceBenchmark(&benchRank));

 //  for(i = 0; i<numRows; i++){
 //     printf("x[%d] = %lf\n", i+1, x[i]);
 //  }

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
   free(x);
   free(nodeStructs);
   fclose(fid);
  return 0;
}
