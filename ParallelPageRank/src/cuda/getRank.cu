#include <stdio.h>
#include "getRank.h"
#include "/usr/include/cuda/cuda_runtime.h"
#include <cublas.h>
#include <cublas_api.h>
#include <cusparse.h>

void makeP(double *Avals, int *rowind, int numRow, int *colind, int nnz, double dP){
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
   status = cusparseSetMatIndexBase(descr, CUSPARSE_INDEX_BASE_ZERO);
   if (status != CUSPARSE_STATUS_SUCCESS) {
      perror("cusparseSetMatIndexBase failed");
      exit(2);
   }
   cusparseIndexBase_t idxBase = CUSPARSE_INDEX_BASE_ZERO;
   double *one = (double*)malloc(sizeof(double)*(numRow));
   double *d = (double*)malloc(numRow*sizeof(double));
   double *dev_one, *dev_d, *dev_Avals;
   int *dev_csrRowInd, *dev_colind, *dev_rowind;
 //  int *csrRowInd;
   int i;

//   csrRowInd = (int*)malloc(sizeof(int)*(numRow+1));

   //Convert rowInd vector to CSR format
   cudaMalloc(&dev_rowind, sizeof(int)*(nnz));
   cudaMalloc(&dev_csrRowInd, sizeof(int)*(numRow+1));
   cudaMemcpy(dev_rowind, rowind, sizeof(int) * (nnz), cudaMemcpyHostToDevice);

   printf("Before coo2csr.\n");
   status = cusparseXcoo2csr(handle, dev_rowind, nnz, numRow, dev_csrRowInd, idxBase);
   
   if (status != CUSPARSE_STATUS_SUCCESS) {
      perror("FAILURE to set csr row indices.");
      exit(2);
   }
   printf("after coo2csr.\n");
//   FILE *fileCSR = fopen("newCSRarray.txt", "w");
//   cudaMemcpy(csrRowInd, dev_csrRowInd, sizeof(int)*(numRow+1), cudaMemcpyDeviceToHost);
//   for(i = 0; i < numRow + 1; i++) {
//      fprintf(fileCSR,"%d\n", csrRowInd[i]);
//   }


   ones(one, numRow);
   ones(d, numRow);
   // csr format only way suportted in CUDA
   cudaMalloc(&dev_one, sizeof(double)*(numRow));
   cudaMalloc(&dev_d, sizeof(double)*(numRow));
   cudaMalloc(&dev_Avals, sizeof(double)*(nnz));
   cudaMalloc(&dev_colind, sizeof(int)*(nnz));

   cudaMemcpy(dev_d, d, sizeof(double) * (numRow), cudaMemcpyHostToDevice);
   cudaMemcpy(dev_one, one, sizeof(double) * (numRow), cudaMemcpyHostToDevice);
   cudaMemcpy(dev_Avals, Avals, sizeof(double) * (nnz), cudaMemcpyHostToDevice);
   cudaMemcpy(dev_colind, colind, sizeof(int) * (nnz),  cudaMemcpyHostToDevice);
   //csr multiplication call
   double alpha = 1, beta = 0;

   printf("Before csrmv.\n");
   cusparseDcsrmv(handle, transa, numRow, numRow, nnz, &alpha, descr, 
                  dev_Avals, dev_csrRowInd, dev_colind, dev_one, &beta, dev_d);

   if (status != CUSPARSE_STATUS_SUCCESS) {
      perror("FAILURE to makeP.");
      exit(2);
   }
   printf("After csrmv.\n");
   
   cudaMemcpy(Avals, dev_Avals, sizeof(int) * (nnz), cudaMemcpyDeviceToHost);
   cudaMemcpy(one, dev_one, sizeof(double) * (numRow), cudaMemcpyDeviceToHost);
   cudaMemcpy(d, dev_d, sizeof(double) * (numRow), cudaMemcpyDeviceToHost);

   for (i = 0; i< nnz; i++){
         if (d[rowind[i]] && Avals[i]) {
            Avals[i] = dP/d[rowind[i]];
         }
//         fprintf(f1, "P[%d, %d] = %lf\n", rowind[i]+1, colind[i]+1, Avals[i]);
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

void getRank(double *Pvals, double *x, int *rowind, int *colind, int numRows, int nnz, double tol, double dP){
   printf("Entering getRank.\n");
   cusparseStatus_t status;
   cusparseHandle_t handle=0;
   cusparseMatDescr_t descr=0;
   cusparseOperation_t transa = CUSPARSE_OPERATION_TRANSPOSE;
    
   status = cusparseCreate(&handle);
   if (status != CUSPARSE_STATUS_SUCCESS) {
      perror("Failed to create handle.");
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
   cusparseIndexBase_t idxBase = CUSPARSE_INDEX_BASE_ZERO;
   double *dev_y;
   double *dev_x;
   double *dev_Pvals;
   int *dev_rowind, *dev_csrRowInd, *dev_colind;
   int i;
   double *y = (double*)malloc(sizeof(double)*numRows);
   double alpha = 1, beta;
   //double error = 10.0;

   ones(y, numRows);

   cudaMalloc(&dev_y, (sizeof(double)*numRows));
   cudaMalloc(&dev_x, sizeof(double)*(numRows));
   cudaMalloc(&dev_Pvals, sizeof(double)*(nnz));
   cudaMalloc(&dev_rowind, sizeof(double)*(nnz));
   cudaMalloc(&dev_csrRowInd, sizeof(double)*(numRows+1));
   cudaMalloc(&dev_colind, sizeof(double)*(nnz));

   cudaMemcpy(dev_y, y, sizeof(double)*(numRows), cudaMemcpyHostToDevice);
   cudaMemcpy(dev_x, x, sizeof(double)*(numRows), cudaMemcpyHostToDevice);
   cudaMemcpy(dev_rowind, rowind, sizeof(double)*(nnz), cudaMemcpyHostToDevice);
   cudaMemcpy(dev_colind, colind, sizeof(double)*(nnz), cudaMemcpyHostToDevice);
   cudaMemcpy(dev_Pvals, Pvals, sizeof(double)*(nnz), cudaMemcpyHostToDevice);

   status = cusparseXcoo2csr(handle, dev_rowind, nnz, numRows, dev_csrRowInd, idxBase);
   
   if (status != CUSPARSE_STATUS_SUCCESS) {
      perror("FAILURE to set csr row indices.");
      exit(2);
   }

   int *csrRowInd = (int*) malloc(sizeof(int)*(numRows+1));
   cudaMemcpy(csrRowInd, dev_csrRowInd, sizeof(int) *(numRows + 1), cudaMemcpyDeviceToHost);
   //while (error>tol) {
   printf("Before While loop.\n");
//   FILE *file;
//   file = fopen("cudaCSR.txt", "w");
//   for (i = 0; i < numRows; i++) {
//      printf("csrRowInd[%d] = %d\t", i, csrRowInd[i]);
//      printf("x = %lf, y = %lf\n", x[i], y[i]);
//   }
//   for (i = 0; i < nnz; i++) {
//      fprintf(file, "Pvals[%d] = %lf.\n", i, Pvals[i]);
//   } 
   i = 0;
//   int j;
   while(i++<20){
      printf("i = %d.\n", i);
      beta = (double)((1-dP)/(numRows));
      printf("Before cusparseDcsrmv.\n");
      cusparseDcsrmv(handle, transa, numRows, numRows, nnz, &alpha, descr, dev_Pvals,
                     dev_csrRowInd, dev_colind, dev_x, &beta, dev_y);
      printf("After cusparseDCsrmv.\n\n\n\n");
      cudaMemcpy(x, dev_x, sizeof(double)*(numRows), cudaMemcpyDeviceToHost);
      cudaMemcpy(y, dev_y, sizeof(double)*(numRows), cudaMemcpyDeviceToHost);
//   for (j = 0; j < numRows; j++) {
//      printf("csrRowInd[%d] = %d\t", j, csrRowInd[j]);
//      printf("x = %lf, y = %lf\n", x[j], y[j]);
//   }
      //error = getError(x, y, numRows);
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
