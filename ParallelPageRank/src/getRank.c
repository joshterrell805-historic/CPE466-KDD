#include "mkl.h"
   
void makeP(float *Avals, MKL_INT *rowind, MKL_INT *numRow, MKL_INT *colind, MKL_INT *nnz, int n, float dP){

   float *d = (float*)malloc(sizeof(float)*N);
   int i;
   for(i = 0; i<N; i++){
      d[i] = 1;
   }
   char transa = 'N';
   mkl_cspblas_scoogemv (&tansa, numRow, Avals ,rowind , colind , nnz , d, d );
   for(i = 0; i<N; i++){
     printf("d[%d] = %lf\n", i, d[i]); 
   }
   for (i = 0; i<*nnz; i++){
      Avals[i] = dP/d[i];
   }
} 

void getRank(float *Pvals, MKL_INT *rowind, MKL_INT *colind, MKL_INT *numRows, MKL_INT numCols, MKL_INT *nnz, float tol){

   float *z = (float*)malloc(sizeof(float)*N);
   float *x = (float*)malloc(sizeof(float)*N);
   int i;
   for(i = 0; i<N; i++){
      z[i] = 1;
      x[i] = 1/N;
   }
   float *y = z;
   char transa = 'N';
   float alpha = 1;
   float beta = ((1-dP)/N)*sum(x, N);
   char[6] matdescra = {'G', 'L', 'N','C'};
   float error = 10;
   while(N*error/dP >tol){
      //call mat mult
      error = x[1];
      mkl_scoomv (&transa, numRows, numRows, &alpha ,matdescra , Pvals , 
                  rowind , colind , nnz , x , &beta , y );
      x = y;
      y = z;
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
