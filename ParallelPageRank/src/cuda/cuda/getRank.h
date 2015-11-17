//
//  getRank.h
//  
//
//  Created by Morgan Yost on 11/10/15.
//  Adjusted by Drew Miller on 11/15/15.
//

#ifndef getRank_h
#define getRank_h

void makeP(double *Avals, int *rowind, int numRow, int *colind, int nnz,  double dP);
void getRank(double *Pvals, double *x, int *rowind, int *colind, int numRows, int nnz, double tol, double dP);
//void makeSinks(MKL_INT *rowind, MKL_INT *colind, float *d, MKL_INT numRow);
double sum(double *x, int N);
void ones(double *a, int N);
double getError(double *v1, double *v2, int size);

#endif /* getRank_h */
