#ifndef benchmark_h
#define benchmark_h
#include <sys/time.h>

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

#endif
