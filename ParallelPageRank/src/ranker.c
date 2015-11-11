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
#include "hashtable.h"
#include "mkl.h"
#include "getRank.h"

void skip_line(FILE *f, char terminator) {
  char c;
  char test;
  do {
    c = fgetc(f);
  } while (c != terminator);
}

int read_int(FILE *f) {
  char buf[150];
  int i;
  char c = '9';
  // Read non-space characters
  for (i = 0; i < 150 && isdigit(c); i++) {
    buf[i] = c = fgetc(f);
  }
  // Set the last (non-digit) character we wrote to buf to a null,
  // making buf a string.
  buf[i] = '\0';

  // Drop all following space
  while (isspace(c)) {
    c = fgetc(f);
  }
  // The last character we read won't be a space
  ungetc(c, f);
  return atoi(buf);
}
int main(int argc, char **argv) {
  bool grumpy = false;
  /* Derived from getopt docs: */
  int c;
  int digit_optind = 0;

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
    printf("Missing required filename: ranker <filename>\n");
    exit(2);
  }

  char *filename = argv[optind];

  if (grumpy) {
    printf("Get off my lawn!\n");
  } else {
    printf("Hello World!\n");
  }

  printf("Filename: %s\n", filename);

  struct stat finfo;
  int from, to , i;
  stat(filename, &finfo);
  int fd = open(filename, O_RDONLY);
  char *data = (char *) mmap(NULL, finfo.st_size + 1, PROT_READ | PROT_WRITE, MAP_PRIVATE, fd, 0);
  data[finfo.st_size] = '\0';
  printf("Data loaded.\n");

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

  float *values = calloc(edges, sizeof(float));
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

    printf("From %i to %i first time\n", from, to);
    values[sparseEdgeIndex] = 1;
    rowind[sparseEdgeIndex] = denseFrom;
    colind[sparseEdgeIndex] = denseTo;
    sparseEdgeIndex++;
  }

  printf("Done creating sparse matrix.\n");
   float tol = .0001;
  for ( i = 0; i < edges; i++) {
      printf("From %i to %i\n", unmap[rowind[i]], unmap[colind[i]]);
  }
   makeP(values, rowind, &numRows, colind, &nnz, .95);
   float *x = (float*)malloc(sizeof(float)*numRows);
   for(i = 0; i<numRows; i++){
      x[i] = (float)1/numRows;
   }
   getRank(values, x, rowind, colind, &numRows, &nnz, tol, .95);
   printf("result: \n");
   for(i = 0; i<numRows; i++){
      printf("x[%d] = %lf\n", i+1, x[i]);
   }
//void makeP(float *Avals, MKL_INT *rowind, MKL_INT *numRow, MKL_INT *colind, MKL_INT *nnz, int n, float dP);
  //makeP(values, rowind, &numRows, colind, &nnz, numNodes, float dP);
  return 0;
}
