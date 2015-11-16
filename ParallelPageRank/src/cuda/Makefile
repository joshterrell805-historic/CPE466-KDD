NVFLAGS=-O3 -g -ccbin g++ -m64 -gencode arch=compute_20,code=sm_20 -gencode arch=compute_30,code=sm_30 -gencode arch=compute_35,code=sm_35 -gencode arch=compute_37,code=sm_37 -gencode arch=compute_50,code=sm_50 -gencode arch=compute_52,code=sm_52 -gencode arch=compute_52,code=compute_52 -lcublas -lcusparse -lcudart -lcuda
# list .c and .cu source files here
SRCFILES=ranker.cu getRank.cu hashtable.cu

all:	cuda	

cuda: $(SRCFILES) 
	nvcc $(NVFLAGS) -o pageRank $^ 

clean: 
	rm -f *.o 

