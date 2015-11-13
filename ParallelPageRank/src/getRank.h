//
//  getRank.h
//  
//
//  Created by Morgan Yost on 11/10/15.
//
//

#ifndef getRank_h
#define getRank_h

#include "mkl.h"
void makeP(double *Avals, MKL_INT *rowind, MKL_INT *numRow, MKL_INT *colind, MKL_INT *nnz,  double dP);
void getRank(double *Pvals, double *x, MKL_INT *rowind, MKL_INT *colind, MKL_INT *numRows, MKL_INT *nnz, double tol, float dP);
//void makeSinks(MKL_INT *rowind, MKL_INT *colind, float *d, MKL_INT numRow);
double sum(double *x, int N);
void ones(double *a, int N);
double getError(double *v1, double *v2, MKL_INT size);

#endif /* getRank_h */
