CCINTEL=icc

SRCFILES=ranker.c getRank.c hashtable.c
FLAGS= -mkl -O3

default:
	$(CCINTEL) $(FLAGS) -o pageRank $(SRCFILES)

clean:
	-rm -f pageRank
