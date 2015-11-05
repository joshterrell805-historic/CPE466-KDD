#include <stdio.h>
// Provides boolean definitions
#include <stdbool.h>
#include <stdlib.h>
#include <unistd.h>
#include <getopt.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

void skip_line(FILE *f, char terminator) {
  char c;
  char test;
  do {
    c = fgetc(f);
  } while (c != terminator);
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

  FILE *file = fopen(filename, "r");
  int from;
  int to;
  int nodes;

  skip_line(file, '\n');
  skip_line(file, '\n');
  fscanf(file, "# Nodes: %i Edges: %*i ", &nodes);
  printf("Total nodes: %i\n", nodes);
  skip_line(file, '\n');

  char *adjacency_matrix;
  // Is this faster with ints?
  adjacency_matrix = (char *) calloc(nodes * nodes, sizeof(char));

  while (EOF != fscanf(file, "%i %i ", &from, &to)) {
    /* printf("From %i to %i\n", from, to); */
    adjacency_matrix[from * nodes + to] = 1;
  }

  for (int i = 0; i < nodes; i++) {
    for (int j = 0; j < nodes; j++) {
      if (adjacency_matrix[i * nodes + j]) {
        printf("From %i to %i\n", i, j);
      }
    }
  }
  return 0;
}
