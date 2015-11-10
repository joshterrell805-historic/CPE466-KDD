#include "mkl.h"
#include <stdio.h>
void makeP(float *Avals, MKL_INT *rowind, MKL_INT *numRow, MKL_INT *colind, MKL_INT *nnz,  float dP);
void getRank(float *Pvals, float *x, MKL_INT *rowind, MKL_INT *colind, MKL_INT *numRows, MKL_INT *nnz, float tol, float dP);
float sum(float *x, int N);
void ones(float *a, int N);

int main(int argc, char *argv[]){
   MKL_INT nnz = 14;
   float tol = .0001;
   float Avals[14];
   ones(Avals, nnz);
   MKL_INT rowind[14] = {0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4};
   MKL_INT colind[14] = {1, 2, 3, 4, 1, 3, 4, 1, 2, 4, 1, 2, 3, 5};
   MKL_INT numRow = 6;
   makeP(Avals, rowind, &numRow, colind, &nnz, .95);
   float *x = (float*)malloc(sizeof(float)*numRow);
   int i;
   for(i = 0; i<numRow; i++){
      x[i] = (float)1/numRow;
   }
   getRank(Avals, x, rowind, colind, &numRow, &nnz, tol, .95);
   printf("result: \n");
   for(i = 0; i<numRow; i++){
      printf("x[%d] = %lf\n", i+1, x[i]);
   }
   return 0;
}

void makeP(float *Avals, MKL_INT *rowind, MKL_INT *numRow, MKL_INT *colind, MKL_INT *nnz, float dP){

   float *d = (float*)malloc(sizeof(float)*(*numRow));
   float *one = (float*)malloc(sizeof(float)*(*numRow));
   int i;
   ones(one, *numRow);
   char transa = 'N';
   mkl_cspblas_scoogemv (&transa, numRow, Avals ,rowind , colind , nnz , one, d );
  // for(i = 0; i<*numRow; i++){
 //   printf("d[%d] = %lf\n", i, d[i]);
//  }
   for (i = 0; i<*nnz; i++){
         if (d[rowind[i]] && Avals[i]) {
            Avals[i] = dP/d[rowind[i]];
         }
         //printf("P[%d, %d] = %lf\n", rowind[i]+1, colind[i]+1, Avals[i]);
   }
} 

void getRank(float *Pvals, float *x, MKL_INT *rowind, MKL_INT *colind, MKL_INT *numRows, MKL_INT *nnz, float tol, float dP){

   float *y = (float*)malloc(sizeof(float)*(*numRows));
   int i, j;
   ones(y, *numRows);
   char transa = 'N';
   float alpha = 1, beta;
   char matdescra[6] = {'G', 'U', 'U','C'};
//   float error = 10;
   i = 0;
   while(i++ <86){
//    error = x[1];
      beta = (float)((1-dP)/(*numRows))*sum(x, *numRows);
      mkl_scoomv(&transa, numRows, numRows, &alpha ,matdescra , Pvals ,rowind , colind , nnz , x , &beta , y );
      memcpy(x, y, *numRows*sizeof(float));
      ones(y, *numRows);
//    error -=x[1];
      //printf("error: %lf\n", (float)(*numRows)*error);
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
