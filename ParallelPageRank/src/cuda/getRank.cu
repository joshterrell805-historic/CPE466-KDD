#include <stdio.h>
#include "getRank.h"
#include "cublas.h"
#include "cublas_api.h"
#include "cusparse.h"
#include "cuda.h"

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
void makeP(double *Avals, int *rowind, int numRow, int *colind, int nnz, double dP){
   FILE *f0 = fopen("csrAvals.txt", "w");
   FILE *f2 = fopen("csrCols.txt", "w");
   FILE *f3 = fopen("csrRow.txt", "w");
   FILE *f4 = fopen("newCsrRow.txt", "w");
   int *testRowind = (int*)calloc(sizeof(int), nnz);
   int s;
   for (s = 0; s < nnz; s++) {
      fprintf(f0,"%lf\n", Avals[s]);
      fprintf(f3, "%d\n", colind[s]);
   }
   printf("Entering MAKEP.\n");
   cusparseStatus_t status;
   cusparseHandle_t handle=0;
   cusparseMatDescr_t descr=0;
   cusparseOperation_t transa = CUSPARSE_OPERATION_NON_TRANSPOSE;
    
    status = cusparseCreate(&handle);
   if (status != CUSPARSE_STATUS_SUCCESS) {
      perror("Cusparse Library Initialization.");
      exit(2);
   }
   status = cusparseCreateMatDescr(&descr);
   if (status != CUSPARSE_STATUS_SUCCESS) {
      perror("Matrix descriptor initialization failed");
      exit(2);
   }
   status = cusparseSetMatType(descr, CUSPARSE_MATRIX_TYPE_GENERAL);
   if (status != CUSPARSE_STATUS_SUCCESS) {
      perror("cusparseSetMatType failed");
      exit(2);
   }
   status = cusparseSetMatIndexBase(descr, CUSPARSE_INDEX_BASE_ONE);
   if (status != CUSPARSE_STATUS_SUCCESS) {
      perror("cusparseSetMatIndexBase failed");
      exit(2);
   }
   cusparseIndexBase_t idxBase = CUSPARSE_INDEX_BASE_ONE;
   double *one = (double*)malloc(sizeof(double)*(numRow));
   double *d = (double*)calloc(numRow, sizeof(double));
   double *dev_one, *dev_d, *dev_Avals;
   int *dev_csrRowInd, *dev_colind, *dev_rowind;
   int i; 
   //int sinkNodes = 0;

   ones(one, numRow);
   //Convert rowInd vector to CSR format
   cudaMalloc(&dev_rowind, sizeof(int)*(numRow));
   cudaMalloc(&dev_csrRowInd, sizeof(int)*numRow+1);
   cudaMemcpy(dev_rowind, rowind, sizeof(int) * (numRow), cudaMemcpyHostToDevice);
   printf("Before coo2csr.\n");
   status = cusparseXcoo2csr(handle, dev_rowind, nnz, numRow, dev_csrRowInd, idxBase);
   if (status != CUSPARSE_STATUS_SUCCESS) {
      perror("FAILURE to set csr row indices.");
      exit(2);
   }
   printf("after coo2csr.\n");
   cudaMemcpy(testRowind, dev_rowind, sizeof(int)*(numRow), cudaMemcpyDeviceToHost);
   for(i = 0; i < numRow; i++) {
      fprintf(f2,"%d\n", testRowind[s]);
   }

   cudaMemcpy(rowind, dev_csrRowInd, sizeof(int)*(numRow), cudaMemcpyDeviceToHost);
   for(i = 0; i < numRow; i++) {
      fprintf(f4,"%d\n", rowind[s]);
   }


   // csr format only way suportted in CUDA
   cudaMalloc(&dev_one, sizeof(double)*(numRow));
   cudaMalloc(&dev_d, sizeof(double)*(numRow));
   cudaMalloc(&dev_Avals, sizeof(double)*(numRow));
   cudaMalloc(&dev_colind, sizeof(int)*(numRow));

   
   cudaMemcpy(dev_one, one, sizeof(double) * (numRow), cudaMemcpyHostToDevice);
   cudaMemcpy(dev_d, d, sizeof(double) * (numRow), cudaMemcpyHostToDevice);
   cudaMemcpy(dev_Avals, Avals, sizeof(double) * (numRow), cudaMemcpyHostToDevice);
   cudaMemcpy(dev_colind, colind, sizeof(int) * (numRow),  cudaMemcpyHostToDevice);
   //csr multiplication call
   double alpha = 1, beta = 0;

   printf("Before csrmv.\n");
   cusparseDcsrmv(handle, transa, numRow, numRow, nnz, &alpha, descr, 
                  dev_Avals, dev_csrRowInd, dev_colind, one, &beta, dev_d);
   printf("After csrmv.\n");
   printf("Before uncompressing row indices.\n");
   cusparseXcsr2coo(handle, dev_csrRowInd, nnz, numRow, dev_rowind, idxBase);
   printf("After uncompressing row indices.\n");

   cudaMemcpy(rowind, dev_rowind, sizeof(int) * (numRow), cudaMemcpyDeviceToHost);
   cudaMemcpy(colind, dev_colind, sizeof(int) * (numRow), cudaMemcpyDeviceToHost);
   cudaMemcpy(d, dev_d, sizeof(double) * (numRow), cudaMemcpyDeviceToHost);

//   mkl_cspblas_dcoogemv (&transa, numRow, Avals ,rowind , colind , nnz , one, d );
   /*
   for(i = 0; i<*numRow; i++){
    printf("d[%d] = %lf\n", i, d[i]);
   }
   */
   FILE *f1 = fopen("csrAvalsAfter.txt", "w");

   for (i = 0; i< nnz; i++){
         if (d[rowind[i]] && Avals[i]) {
            Avals[i] = dP/d[rowind[i]];
         }
         fprintf(f1, "P[%d, %d] = %lf\n", rowind[i]+1, colind[i]+1, Avals[i]);
   }
   cudaFree(dev_rowind);
   cudaFree(dev_colind);
   cudaFree(dev_Avals);
   cudaFree(dev_one);
   cudaFree(dev_d);
   free(d);
   free(one);
   printf("Leaving MAKEP.\n");
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
void getRank(double *Pvals, double *x, int *rowind, int *colind, int numRows, int nnz, double tol, double dP){
   printf("Entering getRank.\n");
      //cusparseDcsrmv(cusparseHandle_t handle, cusparseOperation_t transA, int m, int n, int nnz, const double *alpha, const cusparseMatDescr_t descrA, const double *csrValA, const int *csrRowPtrA, const int *csrColIndA, const double *x, const double *beta, double *y)
   cusparseStatus_t status;
   cusparseHandle_t handle=0;
   cusparseMatDescr_t descr=0;
//   cusparseOperation_t transa = CUSPARSE_OPERATION_NON_TRANSPOSE;
    
    status = cusparseCreate(&handle);
    if (status != CUSPARSE_STATUS_SUCCESS) {
            perror("CUSPARSE Library initialization failed");
           exit(2);
    }
    status = cusparseCreateMatDescr(&descr);
    if (status != CUSPARSE_STATUS_SUCCESS) {
           perror("Matrix descriptor initialization failed");
           exit(2);
    }
    status = cusparseSetMatType(descr, CUSPARSE_MATRIX_TYPE_GENERAL);
    if (status != CUSPARSE_STATUS_SUCCESS) {
           perror("cusparseSetMatType failed");
           exit(2);
    }
    status = cusparseSetMatIndexBase(descr, CUSPARSE_INDEX_BASE_ZERO);
    if (status != CUSPARSE_STATUS_SUCCESS) {
           perror("cusparseSetMatIndexBase failed");
           exit(2);
    }
   double *dev_y;
   double *dev_x;
   double *dev_Pvals;
   int *dev_rowind;
   int *dev_colind;

   cudaMalloc(&dev_y, (sizeof(double)*numRows));
   cudaMalloc(&dev_x, sizeof(double)*(numRows));
   cudaMalloc(&dev_Pvals, sizeof(double)*(numRows));
   cudaMalloc(&dev_rowind, sizeof(double)*(numRows));
   cudaMalloc(&dev_colind, sizeof(double)*(numRows));
   int i;
   double *y = (double*)malloc(sizeof(double)*numRows);
   ones(y, numRows);
   double alpha = 1, beta = 1;
   double *dev_alpha, *dev_beta;
   cudaMalloc(&dev_alpha, sizeof(double)*1);
   cudaMalloc(&dev_beta, sizeof(double)*1);
   cudaMemcpy(dev_alpha, &alpha, sizeof(double)*1, cudaMemcpyHostToDevice);
   cudaMemcpy(dev_beta, &beta, sizeof(double)*1, cudaMemcpyHostToDevice);

   //double error = 10.0;
   //while (error>tol) {
   printf("Before While loop.\n");
   FILE *file;
   file = fopen("cudaCSR.txt", "w");
   for (i = 0; i < nnz; i++) {
      fprintf(file, "Pvals[%d] = %lf.\n", i, Pvals[i]);
   } 
   i = 0;
   while(i++<500){
      printf("i = %d.\n", i);
      beta = (double)((1-dP)/(numRows));
      //launch kernel
      //cusparseDcsrmv(handle, transa, numRows, numRows, nnz, dev_alpha, descr, dev_Pvals, dev_rowind, dev_colind, dev_x, dev_beta, dev_y);
      printf("After cusparseDCsrmv.\n");
      /*cudaMemcpy(x, dev_x, sizeof(double)*(numRows));
      cudaMemcpy(y, dev_y, sizeof(double)*(numRows));
      error = getError(x, y, numRows);*/
      cudaMemcpy(dev_x, dev_y, numRows*sizeof(double), cudaMemcpyDeviceToDevice);
      ones(y, numRows);
      //printf("error: %lf\n", error);
   }
   printf("After while loop.\n");
   cudaMemcpy(x, dev_x, sizeof(double)*numRows, cudaMemcpyDeviceToHost);
   cudaFree(dev_x);
   cudaFree(dev_y);
   cudaFree(dev_Pvals);
   cudaFree(dev_rowind);
   cudaFree(dev_colind);
   free(y);
   printf("Leaving getRank.\n");
}

double sum(double *x, int N){
   printf("Entering sum.\n");
   int i;
   double result = 0;
//#pragma omp parallel for simd reduction(+:result)
   for (i = 0; i<N; i++){
      result+= x[i];
   }
   printf("Leaving sum.\n");
   return result;
}

void ones(double *a, int N){
   printf("Entering ones.\n");
   int i;
//#pragma omp parallel for simd
   for (i =0; i< N; i++) {
      a[i] = 1;
   }
   printf("Leaving ones.\n");
}

double getError(double *v1, double *v2, int size){
   
   int i;
   double result;
 //  #pragma omp parallel for simd
   for (i = 0; i<size; i++) {
      v1[i] = v1[i]-v2[i];
   }
   result = 10; // not using this function to terminate while loop currently.
   return result;
}
