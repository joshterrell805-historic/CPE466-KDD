#ifndef dump_adjacency_list_h
#define dump_adjacency_list_h

#include <stdio.h>

void dump_adjacency_list(int *rowind, int *colind, double *values, int nodes,
    char* filename) {

  FILE* fd = fopen(filename, "w");
   int index;
  for (index = 0; index < nodes; ++index) {
    fprintf(fd, "%d,%d,%lf\n", rowind[index], colind[index], values[index]);
  }

  fclose(fd);
}

#endif
