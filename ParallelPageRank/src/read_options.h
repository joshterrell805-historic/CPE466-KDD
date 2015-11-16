#ifndef read_options_h
#define read_options_h
#include <getopt.h>

typedef struct Options {
  char* filename;
  bool grumpy;
  double dP;
  double tol;
} Options;

void free_options(Options* options) {
  free(options);
}

Options* create_options(int argc, char** argv) {
  Options* o = malloc(sizeof(Options));
  o->grumpy = false;
  o->dP = 0.95;
  o->tol = 0.0001;
  
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
      o->grumpy = true;
      break;
    }
  }

  if ((argc - optind) != 1) {
    printf("Missing required filename: pageRank <filename>\n");
    exit(2);
  }

  o->filename = argv[optind];

  return o;
}

#endif
