CCINTEL=icc

SRCFILES=ranker.c getRank.c hashtable.c
FLAGS= -mkl -O3 -openmp

default:
	$(CCINTEL) $(FLAGS) -o pageRank $(SRCFILES)

mic:
	$(CCINTEL) $(FLAGS) -mmic -o pageRank $(SRCFILES)
	
clean:
	-rm -f pageRank
