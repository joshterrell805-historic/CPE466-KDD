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
void makeP(float *Avals, MKL_INT *rowind, MKL_INT *numRow, MKL_INT *colind, MKL_INT *nnz,  float dP);
void getRank(float *Pvals, float *x, MKL_INT *rowind, MKL_INT *colind, MKL_INT *numRows, MKL_INT *nnz, float tol, float dP);
//void makeSinks(MKL_INT *rowind, MKL_INT *colind, float *d, MKL_INT numRow);
float sum(float *x, int N);
void ones(float *a, int N);
float getError(float *v1, float *v2, MKL_INT size);

#endif /* getRank_h */
