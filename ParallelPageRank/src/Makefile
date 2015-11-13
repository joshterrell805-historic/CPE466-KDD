CCINTEL=icc

SRCFILES=ranker.c getRank.c hashtable.c
FLAGS= -mkl -O3 -openmp

default:
	$(CCINTEL) $(FLAGS) -o pageRank $(SRCFILES)

mic:
	$(CCINTEL) $(FLAGS) -mmic -o pageRank $(SRCFILES)

offload:
	$(CCINTEL) $(FLAGS) -o pageRank offload-ranker.c getRank-offload.c hashtable.c
	
clean:
	-rm -f pageRank
