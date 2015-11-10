#include "mkl.h"
#include <stdio.h>
void makeP(float *Avals, MKL_INT *rowind, MKL_INT *numRow, MKL_INT *colind, MKL_INT *nnz, int n, float dP);
void getRank(float *Pvals, MKL_INT *rowind, MKL_INT *colind, MKL_INT *numRows, MKL_INT numCols, MKL_INT *nnz, float tol, int N, float dP);
float sum(float *x, int N);
void ones(float *a, int N);

int main(int argc, char *argv[]){
   MKL_INT nnz = 14;
   int N = 36;
   float Avals[14];
   ones((float*)Avals, (int)nnz);
   MKL_INT rowind[14] = {0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4};
   MKL_INT colind[14] = {1, 2, 3, 4, 1, 3, 4, 1, 2, 4, 1, 2, 3, 5};
   MKL_INT numRow = 6;
   float dP = .95;
   makeP(Avals, rowind, &numRow, colind, &nnz, N, dP);
   return 0;
}

void makeP(float *Avals, MKL_INT *rowind, MKL_INT *numRow, MKL_INT *colind, MKL_INT *nnz, int N, float dP){

   float *d = (float*)malloc(sizeof(float)*(*numRow));
   int i;
   for(i = 0; i<*numRow; i++){
      d[i] = 1;
   }
   char transa = 'N';
   mkl_cspblas_scoogemv (&transa, numRow, Avals ,rowind , colind , nnz , d, d );
   for(i = 0; i<*numRow; i++){
     printf("d[%d] = %lf\n", i, d[i]); 
   }
   for (i = 0; i<*nnz; i++){
      Avals[i] = dP/d[i];
   }
} 

void getRank(float *Pvals, MKL_INT *rowind, MKL_INT *colind, MKL_INT *numRows, MKL_INT numCols, MKL_INT *nnz, float tol, int N, float dP){

   float *y = (float*)malloc(sizeof(float)*N);
   ones(y, N);
   float *x = (float*)malloc(sizeof(float)*N);
   int i;
   for(i = 0; i<N; i++){
      x[i] = 1/N;
   }
   char transa = 'N';
   float alpha = 1;
   float beta = ((1-dP)/N)*sum(x, N);
   char matdescra[6] = {'G', 'L', 'N','C'};
   float error = 10;
   while(N*error/dP >tol){
      //call mat mult
      error = x[1];
      mkl_scoomv(&transa, numRows, numRows, &alpha ,matdescra , Pvals ,
                  rowind , colind , nnz , x , &beta , y );
      x = y;
      ones(y, N);
      beta = ((1-dP)/N)*sum(x, N);
      error -=x[1];
   }
}

float sum(float *x, int N){
   int i;
   float result = 0;
   for (i = 0; i<N; i++){
      result+= x[i];
   }
   return result;
}

void ones(float *a, int N){
   int i;
   for (i =0; i< N; i++) {
      a[i] = 1;
   }
}
