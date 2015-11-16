#include "offload.h"
/*
int main(int argc, char *argv[]){
   MKL_INT nnz = 14;
   double tol = .0001;
   double Avals[14];
   ones(Avals, nnz);
   MKL_INT rowind[14] = {0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4};
   MKL_INT colind[14] = {1, 2, 3, 4, 1, 3, 4, 1, 2, 4, 1, 2, 3, 5};
   MKL_INT numRow = 6;
   makeP(Avals, rowind, &numRow, colind, &nnz, .95);
   //float *sinkNodes = (float*)malloc(sizeof(float)*numRow*numSinks);
   //ones(sinkNodes, numRow*numSinks);
   //MKL_INT *sinkRow = (MKL_INT*)malloc(sizeof(MKL_INT)*numRow*numSinks);
   //MKL_INT *sinkCol = (MKL_INT*)malloc(sizeof(MKL_INT)*numRow*numSinks);
   //makeSinks(sinkRow, sinkCol, d, numRow);

   double *x = (float*)malloc(sizeof(float)*numRow);
   int i;
   for(i = 0; i<numRow; i++){
      x[i] = (float)1/numRow;
   }
   getRank(Avals, x, rowind, colind, &numRow, &nnz, tol, .95);
   printf("result: \n");
   for(i = 0; i<numRow; i++){
      printf("x[%d] = %lf\n", i+1, x[i]);
   }

   free(x);
   return 0;
}
*/
void makeP(double *Avals, MKL_INT *rowind, MKL_INT *numRow, MKL_INT *colind, MKL_INT *nnz, double dP){

   double *one = (double*)malloc(sizeof(double)*(*numRow));
   double *d = (double*)malloc(sizeof(double)*(*numRow));
   ones(d, *numRow);
   int i, sinkNodes = 0;
   ones(one, *numRow);
   char transa = 'N';
   mkl_cspblas_dcoogemv (&transa, numRow, Avals ,rowind , colind , nnz , one, d );
   /*
   for(i = 0; i<*numRow; i++){
    printf("d[%d] = %lf\n", i, d[i]);
   }
   */
   for (i = 0; i<*nnz; i++){
         if (d[rowind[i]] && Avals[i]) {
            Avals[i] = dP/d[rowind[i]];
         }
         //printf("P[%d, %d] = %lf\n", rowind[i]+1, colind[i]+1, Avals[i]);
   }
   free(one);
}
/*
 makeP will need to spit out d for for this to work
void makeSinks(MKL_INT *rowind, MKL_INT *colind, float *d, MKL_INT numRow){
   int i, j, count= 0;
   for (i = 0; i<numRow; i++) {
      if (!d[i]) {
         for (j = 0; j<numRow; j++) {
            rowind[count] = i;
            colind[count] = j;
            count++;
         }
      }
   }
}
*/
void getRank(double *Pvals, double *x, MKL_INT *rowind, MKL_INT *colind, MKL_INT *numRows, MKL_INT *nnz, double tol, double dP){

   double *y = (double*)malloc(sizeof(double)*(*numRows));
   int i, j;
   ones(y, *numRows);
   char transa = 'T';
   double alpha = 1, beta;
   char matdescra[6] = {'G', 'U', 'U','C'};
   double error = 10.0;
   i = 0;
   //while (error>tol) {
   while(i++<500){
      beta = (double)((1-dP)/(*numRows));
      mkl_dcoomv(&transa, numRows, numRows, &alpha ,matdescra , Pvals ,rowind , colind , nnz , x , &beta , y );
      error = getError(x, y, *numRows);
      memcpy(x, y, *numRows*sizeof(double));
      ones(y, *numRows);
      //printf("error: %lf\n", error);
   }
   free(y);
}

double sum(double *x, int N){
   int i;
   double result = 0;
//#pragma omp parallel for simd reduction(+:result)
   for (i = 0; i<N; i++){
      result+= x[i];
   }
   return result;
}

void ones(double *a, int N){
   int i;
//#pragma omp parallel for simd
   for (i =0; i< N; i++) {
      a[i] = 1;
   }
}

double getError(double *v1, double *v2, MKL_INT size){
   int i;
 //  #pragma omp parallel for simd
   for (i = 0; i<size; i++) {
      v1[i] = v1[i]-v2[i];
   }
   return cblas_dnrm2(size, v1, 1);
}
