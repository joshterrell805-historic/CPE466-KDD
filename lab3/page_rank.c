int converged = 0;

void computePageRank(int sourceIsA) {
  if (sourceIsA) {
    converged = sourceIsA;
  }
}

int hasConverged(void) {
  return converged;
}
