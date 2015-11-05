#include <stdio.h>
#include <stdbool.h>
#include <unistd.h>
#include <getopt.h>


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

  if (grumpy) {
    printf("Get off my lawn!\n");
  } else {
    printf("Hello World!\n");
  }
  return 0;
}
