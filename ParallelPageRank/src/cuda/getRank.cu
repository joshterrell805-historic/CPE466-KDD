#include <stdio.h>
#include "getRank.h"
#include "/usr/include/cuda/cuda_runtime.h"
#include <cublas.h>
#include <cusparse.h>

void makeP(double *Avals, int *rowind, int numRow, int *colind, int nnz, double dP){
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
   int i;

   dP = .95;
   //Convert rowInd vector to CSR format
   cudaMalloc(&dev_rowind, sizeof(int)*(nnz));
   cudaMalloc(&dev_csrRowInd, sizeof(int)*(numRow+1));
   cudaMemcpy(dev_rowind, rowind, sizeof(int) * (nnz), cudaMemcpyHostToDevice);

   status = cusparseXcoo2csr(handle, dev_rowind, nnz, numRow, dev_csrRowInd, idxBase);
   
   if (status != CUSPARSE_STATUS_SUCCESS) {
      perror("FAILURE to set csr row indices.");
      exit(2);
   }


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

   cusparseDcsrmv(handle, transa, numRow, numRow, nnz, &alpha, descr, 
                  dev_Avals, dev_csrRowInd, dev_colind, dev_one, &beta, dev_d);

   if (status != CUSPARSE_STATUS_SUCCESS) {
      perror("FAILURE to makeP.");
      exit(2);
   }
   
   cudaMemcpy(Avals, dev_Avals, sizeof(int) * (nnz), cudaMemcpyDeviceToHost);
   cudaMemcpy(one, dev_one, sizeof(double) * (numRow), cudaMemcpyDeviceToHost);
   cudaMemcpy(d, dev_d, sizeof(double) * (numRow), cudaMemcpyDeviceToHost);

   for (i = 0; i< nnz; i++){
         if (d[rowind[i]] && Avals[i]) {
            Avals[i] = dP/d[rowind[i]];
         }
   }
   cudaFree(dev_rowind);
   cudaFree(dev_colind);
   cudaFree(dev_Avals);
   cudaFree(dev_one);
   cudaFree(dev_d);
   free(d);
   free(one);
}

void getRank(double *Pvals, double *x, int *rowind, int *colind, int numRows, int nnz, double tol, double dP){
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
   double *alpha, *beta;
   alpha = (double*) malloc(sizeof(double));
   beta = (double*) malloc(sizeof(double));
   alpha[0] = 1;

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

   
   i = 0;
//   while (error>tol) {
   while(i++<50){
      //i++;
      beta[0] = (double)((1-dP)/(numRows));
      cusparseDcsrmv(handle, transa, numRows, numRows, nnz, alpha, descr, dev_Pvals,
                     dev_csrRowInd, dev_colind, dev_x, beta, dev_y);
     // error = cublasDnrm2(numRows, dev_y, 1);
      cudaMemcpy(dev_x, dev_y, numRows*sizeof(double), cudaMemcpyDeviceToDevice);
      cudaMemcpy(dev_y, y, sizeof(double) * numRows, cudaMemcpyHostToDevice);
   }
   cudaMemcpy(x, dev_x, sizeof(double)*numRows, cudaMemcpyDeviceToHost);
   cudaFree(dev_x);
   cudaFree(dev_y);
   cudaFree(dev_Pvals);
   cudaFree(dev_rowind);
   cudaFree(dev_colind);
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

double getError(double *v1, double *v2, int size){
   
   int i;
   double result;
 //  #pragma omp parallel for simd
   for (i = 0; i<size; i++) {
      v1[i] = v1[i]-v2[i];
   }
   result = 10; // not using this function to terminate while loop currently.
   double *dev_v1;
   cudaMalloc(&dev_v1, sizeof(double)*size);

   return result;
}
